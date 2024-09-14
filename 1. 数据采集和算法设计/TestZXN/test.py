import torch
import pandas as pd
import numpy as np
from torch import nn
from torch.utils.data import DataLoader
import os

# 设置输出格式，避免使用科学计数法
np.set_printoptions(suppress=True, precision=4)  # precision 控制小数点后精度，suppress=True 避免科学计数法

# 定义模型结构
class WaterQualityMLPMAE(nn.Module):
    def __init__(self, num_features, hidden_dim=64, num_layers=3, dropout_rate=0.3):
        super(WaterQualityMLPMAE, self).__init__()
        layers = []
        input_dim = num_features

        # Encoder部分，加入BatchNorm
        for _ in range(num_layers):
            layers.append(nn.Linear(input_dim, hidden_dim))
            layers.append(nn.BatchNorm1d(hidden_dim))  # 加入BN层
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout_rate))
            input_dim = hidden_dim

        self.encoder = nn.Sequential(*layers)

        # Decoder部分，添加BatchNorm
        layers = []
        input_dim = hidden_dim
        for _ in range(num_layers):
            layers.append(nn.Linear(input_dim, hidden_dim))
            layers.append(nn.BatchNorm1d(hidden_dim))  # 加入BN层
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout_rate))
            input_dim = hidden_dim
        layers.append(nn.Linear(hidden_dim, num_features))  # 最后一层输出原始特征维度
        self.decoder = nn.Sequential(*layers)

    def forward(self, src):
        encoded = self.encoder(src)
        reconstructed = self.decoder(encoded)
        return reconstructed

# 归一化函数
def normalize(feature, min_val, max_val):
    return (feature - min_val) / (max_val - min_val + 1e-8)  # 加 1e-8 防止除以零

# 标准化函数
def standardize(feature, mean_val, std_val):
    return (feature - mean_val) / (std_val + 1e-8)  # 加 1e-8 防止除以零

# 保存归一化和标准化参数到txt文件
def save_params_to_txt(min_vals, max_vals, norm_means, norm_stds, file_path='params.txt'):
    with open(file_path, 'w') as f:
        f.write("min_vals: " + ','.join(map(str, min_vals)) + '\n')
        f.write("max_vals: " + ','.join(map(str, max_vals)) + '\n')
        f.write("norm_means: " + ','.join(map(str, norm_means)) + '\n')
        f.write("norm_stds: " + ','.join(map(str, norm_stds)) + '\n')

# 从txt文件读取归一化和标准化参数
def load_params_from_txt(file_path='params.txt'):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        min_vals = np.array([float(x) for x in lines[0].split(': ')[1].split(',')])
        max_vals = np.array([float(x) for x in lines[1].split(': ')[1].split(',')])
        norm_means = np.array([float(x) for x in lines[2].split(': ')[1].split(',')])
        norm_stds = np.array([float(x) for x in lines[3].split(': ')[1].split(',')])
    return min_vals, max_vals, norm_means, norm_stds

# 加载数据并进行归一化和标准化
def load_data(file_path, params_file='params.txt'):
    # 检查是否已经存在参数文件
    if os.path.exists(params_file):
        # 如果存在参数文件，直接读取
        print("读取已保存的归一化和标准化参数...")
        return load_params_from_txt(params_file)

    # 否则计算归一化和标准化值，并保存到文件中
    print("计算归一化和标准化参数并保存...")
    data = pd.read_csv(file_path)

    # 假设数据中包含需要缩放的特征列
    features = data[['水温', 'pH', '溶解氧', '电导率', '浊度', '高锰酸盐指数', '氨氮', '总磷', '总氮']].astype(float)

    # 计算每个特征的最小值和最大值用于归一化
    min_vals = features.min().to_numpy()
    max_vals = features.max().to_numpy()

    # 对每个特征应用归一化
    normalized_features = features.copy()
    for col in features.columns:
        normalized_features[col] = normalize(features[col], min_vals[features.columns.get_loc(col)], max_vals[features.columns.get_loc(col)])

    # 计算归一化后的均值和标准差用于标准化
    norm_means = normalized_features.mean().to_numpy()
    norm_stds = normalized_features.std().to_numpy()

    # 保存归一化和标准化参数到文件
    save_params_to_txt(min_vals, max_vals, norm_means, norm_stds, params_file)

    return min_vals, max_vals, norm_means, norm_stds

# 推理函数与反归一化和反标准化
def infer_single_data(model, input_data, min_vals, max_vals, norm_means, norm_stds, device):
    model.eval()

    # 先归一化再标准化输入数据
    input_data_normalized = (input_data - min_vals) / (max_vals - min_vals + 1e-8)  # 先归一化
    input_data_standardized = (input_data_normalized - norm_means) / (norm_stds + 1e-8)  # 再标准化
    input_tensor = torch.tensor(input_data_standardized, dtype=torch.float32).to(device).unsqueeze(0)

    with torch.no_grad():
        reconstructed = model(input_tensor)
        reconstructed = reconstructed.cpu().numpy()

        # 反标准化
        reconstructed = reconstructed * norm_stds + norm_means
        # 反归一化
        reconstructed = reconstructed * (max_vals - min_vals) + min_vals

    return reconstructed.squeeze()

# 计算百分比差异并找出最大差异项
def calculate_percentage_difference(input_data, prediction, feature_names):
    # 防止除以零，避免数据中有零值
    input_data_safe = np.where(input_data == 0, 1e-8, input_data)

    # 计算每个元素的百分比差异
    percentage_differences = (np.abs((prediction - input_data_safe) / input_data_safe) * 100)

    # 找出最大的百分比差异及其对应的项
    max_diff_index = np.argmax(percentage_differences)
    max_diff_value = percentage_differences[max_diff_index]
    max_diff_feature = feature_names[max_diff_index]

    return percentage_differences, max_diff_value, max_diff_feature

# 主推理函数
def run_single_inference(input_data, file_path, params_file='params.txt'):
    # 加载模型
    model = WaterQualityMLPMAE(num_features=9, hidden_dim=512, num_layers=3, dropout_rate=0.1)
    model.load_state_dict(torch.load('water_quality_mlp_mae.pth'))
    model.to(device)

    # 加载归一化和标准化参数
    min_vals, max_vals, norm_means, norm_stds = load_data(file_path, params_file)

    # 对单条数据进行推理
    prediction = infer_single_data(model, input_data, min_vals, max_vals, norm_means, norm_stds, device)

    # 特征名称
    feature_names = ['水温', 'pH', '溶解氧', '电导率', '浊度', '高锰酸盐指数', '氨氮', '总磷', '总氮']

    # 计算百分比差异
    percentage_differences, max_diff_value, max_diff_feature = calculate_percentage_difference(input_data, prediction, feature_names)

    # 输出推理结果和最大差异项
    print("Prediction (Real Scale):", prediction)
    print("Input Data (Real Scale):", input_data)
    print("Percentage Differences (%):", percentage_differences)
    print(f"Max Percentage Difference: {max_diff_value:.2f}% in {max_diff_feature}")

    # 返回推理结果
    return prediction

# 设备配置
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

if __name__ == "__main__":
    # 输入单条数据进行推理
    input_data = np.array([25.1, 8.46, 9.89, 819.8, 13.7, 3.28, 0.09, 0.067, 1.79])  # 示例输入数据
    file_path = 'combined_output2.csv'
    prediction = run_single_inference(input_data, file_path)
