import torch
import torch.nn as nn
import numpy as np


# 定义基于MLP的MAE模型
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

    def forward(self, src):
        encoded = self.encoder(src)
        return encoded


# 定义下游异常检测模型（单分类）
class DownstreamAnomalyDetectionModelV4(nn.Module):
    def __init__(self, pretrained_encoder, hidden_dim=64, dropout_rate=0.3):
        super(DownstreamAnomalyDetectionModelV4, self).__init__()
        self.encoder = pretrained_encoder

        # Anomaly detection head，输出单一分类结果
        self.anomaly_detection_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(hidden_dim, 1)  # 输出一个单一的结果
        )

    def forward(self, src):
        encoded = self.encoder(src)
        anomaly_prediction = self.anomaly_detection_head(encoded)
        return anomaly_prediction


# 数据的预处理（归一化、标准化）
def preprocess_input(input_data, min_vals, max_vals, means, stds):
    # 归一化
    input_normalized = (input_data - min_vals) / (max_vals - min_vals)

    # 标准化
    input_standardized = (input_normalized - means) / stds

    return input_standardized


# 从文件读取参数
def load_params(file_path):
    params = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split(':')
            params[key] = np.array([float(v) for v in value.split(',')])
    return params['min_vals'], params['max_vals'], params['norm_means'], params['norm_stds']


# 加载模型
def load_model(model_path, device, num_features=9):
    # 加载预训练的 encoder 部分
    pretrained_model = WaterQualityMLPMAE(num_features=num_features, hidden_dim=512, num_layers=3, dropout_rate=0.1)
    pretrained_state_dict = torch.load(model_path, map_location=device)

    # 过滤掉 decoder 相关的权重，并去掉 'encoder.' 前缀
    encoder_state_dict = {k.replace('encoder.', ''): v for k, v in pretrained_state_dict.items() if 'encoder' in k}

    # 加载 encoder 部分的权重
    pretrained_model.encoder.load_state_dict(encoder_state_dict)

    # 加载下游任务模型
    downstream_model_v4 = DownstreamAnomalyDetectionModelV4(pretrained_model.encoder, hidden_dim=512, dropout_rate=0.1).to(device)
    downstream_model_v4.load_state_dict(torch.load('anomaly_detection_model_v4.pth', map_location=device))
    downstream_model_v4.eval()

    return downstream_model_v4


# 推理函数
def infer_single_data(input_data, model, device, min_vals, max_vals, means, stds):
    # 对输入数据进行预处理
    input_data = preprocess_input(input_data, min_vals, max_vals, means, stds)

    # 转换为张量
    input_tensor = torch.tensor(input_data, dtype=torch.float32).unsqueeze(0).to(device)

    # 进行推理
    with torch.no_grad():
        prediction = model(input_tensor)
        prediction = torch.sigmoid(prediction).cpu().item()  # 获取预测值（0~1之间的概率）

    # 判断是否为异常
    if prediction > 0.5:
        print(f"Sample is classified as anomalous (Probability: {prediction:.4f})")
    else:
        print(f"Sample is classified as normal (Probability: {prediction:.4f})")

    return prediction


if __name__ == "__main__":
    # 设置设备
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # 模型路径
    model_path = 'water_quality_mlp_mae.pth'

    # 从文件加载数据缩放所需的参数
    params_file = 'params.txt'
    min_vals, max_vals, means, stds = load_params(params_file)

    # 加载模型
    model = load_model(model_path, device)

    # 输入单条数据（待推理的数据，假设用户输入）
    input_data = np.array([25.1, 8.46, 9.89, 819.8, 13.7, 3.28, 0.09, 0.067, 1.79])

    # 进行推理并输出结果
    prediction = infer_single_data(input_data, model, device, min_vals, max_vals, means, stds)
