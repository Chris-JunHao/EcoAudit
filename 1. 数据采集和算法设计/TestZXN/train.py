import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import pandas as pd
import numpy as np
from tqdm import tqdm
from sklearn.model_selection import train_test_split
import time


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


# 修改后的数据集类，加入掩码机制
class WaterQualityDatasetMAE(Dataset):
    def __init__(self, features, labels, device, mask_ratio=0.5):
        self.features = features
        self.labels = labels
        self.device = device

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        x = self.features[idx].copy()  # 获取当前样本的特征
        y = self.labels[idx]  # 获取当前样本的标签

        # 根据设定的概率决定掩盖策略
        mask_type = np.random.choice([0, 1, 2], p=[0.1, 0.7, 0.2])  # 0=不掩盖，1=掩盖一个特征，2=掩盖两个特征

        mask = np.zeros_like(x, dtype=bool)  # 初始化全false的掩盖mask

        if mask_type == 1:  # 掩盖一个特征
            mask_idx = np.random.choice(len(x), size=1, replace=False)  # 随机选择一个特征进行掩盖
            mask[mask_idx] = True
        elif mask_type == 2:  # 掩盖两个特征
            mask_idx = np.random.choice(len(x), size=2, replace=False)  # 随机选择两个特征进行掩盖
            mask[mask_idx] = True

        # 对选中的特征进行掩盖，用 [0, 1] 区间内的随机值替换
        x[mask] = np.random.uniform(0, 1, size=np.sum(mask))  # 替换为 [0, 1] 标准分布随机值

        return torch.tensor(x, dtype=torch.float32).to(self.device), \
               torch.tensor(y, dtype=torch.float32).to(self.device), \
               torch.tensor(mask, dtype=torch.bool)


# MAE损失函数，计算掩盖部分的误差
def mae_loss(reconstructed, original, mask, mask_weight=0.7):
    mask = mask.to(reconstructed.device)  # 确保 mask 在与 reconstructed 同样的设备上

    # 掩码部分的误差
    masked_reconstructed = reconstructed * mask
    masked_original = original * mask
    mask_loss = nn.MSELoss()(masked_reconstructed, masked_original)

    # 非掩码部分的误差
    non_masked_reconstructed = reconstructed * ~mask  # 使用按位非来取反掩码
    non_masked_original = original * ~mask
    non_mask_loss = nn.MSELoss()(non_masked_reconstructed, non_masked_original)

    # 综合误差，使用权重来平衡掩码和非掩码部分
    total_loss = mask_weight * mask_loss + (1 - mask_weight) * non_mask_loss
    return total_loss


# 自适应缩放和归一化函数
def adaptive_scaling_and_normalization(feature):
    # 归一化到[0, 1]区间
    min_val = feature.min()
    max_val = feature.max()
    normalized_feature = (feature - min_val) / (max_val - min_val + 1e-8)  # 防止除以0

    # 标准化 (Z-Score)
    scaled_feature = (normalized_feature - normalized_feature.mean()) / normalized_feature.std()

    return scaled_feature, min_val, max_val, normalized_feature.mean(), normalized_feature.std()


# 数据加载与缩放处理
def load_data_with_adaptive_scaling(file_path):
    data = pd.read_csv(file_path)

    # 假设数据中包含需要缩放的特征列
    features = data[['水温', 'pH', '溶解氧', '电导率', '浊度', '高锰酸盐指数', '氨氮', '总磷', '总氮']].astype(float)

    norm_means = {}
    norm_stds = {}
    min_vals = {}
    max_vals = {}

    # 对每个特征应用自适应缩放和归一化
    for col in features.columns:
        features[col], min_vals[col], max_vals[col], norm_means[col], norm_stds[
            col] = adaptive_scaling_and_normalization(features[col])

    # 将缩放后的数据作为标签进行重建
    labels = features.copy()

    return features.values, labels.values, min_vals, max_vals, norm_means, norm_stds


# 设置设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 加载数据
file_path = 'combined_output2.csv'
features, labels, min_vals, max_vals, norm_means, norm_stds = load_data_with_adaptive_scaling(file_path)

# 数据集拆分
train_features, val_features, train_labels, val_labels = train_test_split(features, labels, test_size=0.1,
                                                                          random_state=42)

# 数据集和数据加载器
train_dataset = WaterQualityDatasetMAE(train_features, train_labels, device, mask_ratio=0.3)
val_dataset = WaterQualityDatasetMAE(val_features, val_labels, device, mask_ratio=0.3)

train_dataloader = DataLoader(train_dataset, batch_size=8192, shuffle=True)
val_dataloader = DataLoader(val_dataset, batch_size=512, shuffle=False)

# 模型、优化器和学习率调度器
model = WaterQualityMLPMAE(num_features=9, hidden_dim=512, num_layers=3, dropout_rate=0.1).to(device)
optimizer = optim.AdamW(model.parameters(), lr=1e-4)
scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', patience=10)

best_val_loss = 100
# 训练循环
for epoch in range(500):
    model.train()
    train_loss = 0
    for inputs, targets, masks in tqdm(train_dataloader):
        optimizer.zero_grad()
        reconstructed = model(inputs)
        loss = mae_loss(reconstructed, targets, masks, mask_weight=0.7)  # 设置掩码的权重
        loss.backward()

        # 添加梯度裁剪
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        train_loss += loss.item()

    model.eval()
    val_loss = 0
    with torch.no_grad():
        for inputs, targets, masks in val_dataloader:
            reconstructed = model(inputs)
            loss = mae_loss(reconstructed, targets, masks, mask_weight=0.7)  # 设置掩码的权重
            val_loss += loss.item()

    avg_train_loss = train_loss / len(train_dataloader)
    avg_val_loss = val_loss / len(val_dataloader)
    if avg_val_loss < best_val_loss:
        best_val_loss = avg_val_loss
        # 保存模型
        torch.save(model.state_dict(), 'water_quality_mlp_mae.pth')

    print(f'Epoch {epoch + 1}, Train Loss: {avg_train_loss:.4f}, Val Loss: {avg_val_loss:.4f}')
    time.sleep(0.01)

    # 使用学习率调度器
    scheduler.step(avg_val_loss)


# 推理函数与反归一化和反标准化
def infer_and_denormalize_mae(model, dataloader, min_vals, max_vals, norm_means, norm_stds, device):
    model.eval()
    predictions = []
    actuals = []

    with torch.no_grad():
        for inputs, targets, _ in dataloader:
            reconstructed = model(inputs)
            reconstructed = reconstructed.cpu().numpy()

            # 逐列进行反标准化和反归一化
            for i, col in enumerate(min_vals.keys()):
                reconstructed[:, i] = (reconstructed[:, i] * norm_stds[col]) + norm_means[col]  # 反标准化
                reconstructed[:, i] = reconstructed[:, i] * (max_vals[col] - min_vals[col]) + min_vals[col]  # 反归一化

            # 保证所有输出为正数
            reconstructed = np.maximum(reconstructed, 1e-8)

            # 同样对目标值进行反标准化和反归一化
            targets = targets.cpu().numpy()
            for i, col in enumerate(min_vals.keys()):
                targets[:, i] = (targets[:, i] * norm_stds[col]) + norm_means[col]  # 反标准化
                targets[:, i] = targets[:, i] * (max_vals[col] - min_vals[col]) + min_vals[col]  # 反归一化

            predictions.extend(reconstructed)
            actuals.extend(targets)

    return np.array(predictions), np.array(actuals)


# 进行推理
predictions, actuals = infer_and_denormalize_mae(model, val_dataloader, min_vals, max_vals, norm_means, norm_stds,
                                                 device)

# 输出结果
print("Predictions (Real Scale):\n", predictions[:5])
print("Actuals (Real Scale):\n", actuals[:5])
