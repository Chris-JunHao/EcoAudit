import time
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import pandas as pd
import numpy as np
from tqdm import tqdm
from sklearn.model_selection import train_test_split


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


# 修改后的数据集类，生成单分类标注，判断整体是否异常
class WaterQualityAnomalyDatasetV6(Dataset):
    def __init__(self, features, device):
        self.features = features
        self.device = device

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        x = self.features[idx].copy()  # 获取当前样本的特征
        y = 0.0  # 初始化标签为0（无异常）

        # 根据设定的概率决定是否修改数据并生成异常
        anomaly_type = np.random.choice([0, 1], p=[0.75, 0.25])  # 0=不修改，1=生成异常

        if anomaly_type == 1:  # 生成异常
            anomaly_idx = np.random.choice(len(x), size=1, replace=False)  # 随机选择一个特征进行修改
            if np.random.rand() > 0.5:
                x[anomaly_idx] = x[anomaly_idx] * np.random.uniform(1.5, 5.0)  # 随机放大
            else:
                x[anomaly_idx] = x[anomaly_idx] * np.random.uniform(0.05, 0.5)  # 随机缩小
            y = 1.0  # 标记为异常

        return torch.tensor(x, dtype=torch.float32).to(self.device), torch.tensor([y], dtype=torch.float32).to(self.device)


# 定义下游异常检测模型，单分类输出
class DownstreamAnomalyDetectionModelV4(nn.Module):
    def __init__(self, pretrained_encoder, hidden_dim=64, dropout_rate=0.3):
        super(DownstreamAnomalyDetectionModelV4, self).__init__()
        self.encoder = pretrained_encoder

        # Anomaly detection head，输出单一的分类结果
        self.anomaly_detection_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),  # 加入BN层
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(hidden_dim, 1)  # 单一输出，表示样本是否异常
        )

    def forward(self, src):
        encoded = self.encoder(src)
        anomaly_prediction = self.anomaly_detection_head(encoded)
        return anomaly_prediction


# 定义损失函数
def anomaly_detection_loss_v4(predictions, targets):
    criterion = nn.BCEWithLogitsLoss()  # 单分类二分类交叉熵损失
    return criterion(predictions, targets)


# 数据加载与缩放处理，进行归一化和标准化
def load_data_with_adaptive_scaling(file_path):
    data = pd.read_csv(file_path)

    # 假设数据中包含需要缩放的特征列
    features = data[['水温', 'pH', '溶解氧', '电导率', '浊度', '高锰酸盐指数', '氨氮', '总磷', '总氮']].astype(float)

    # 归一化（缩放到 [0, 1]）
    min_vals = features.min()
    max_vals = features.max()
    features_normalized = (features - min_vals) / (max_vals - min_vals)

    # 标准化（Z-score标准化）
    means = features_normalized.mean()
    stds = features_normalized.std()
    features_standardized = (features_normalized - means) / stds

    # 返回归一化和标准化后的数据，以及所需的最小值、最大值、均值和标准差
    return features_standardized.values, min_vals, max_vals, means, stds


# 训练函数
def train_model_v4(downstream_model, train_dataloader, val_dataloader, optimizer, scheduler, num_epochs=100):
    best_val_loss = float('inf')

    for epoch in range(num_epochs):
        downstream_model.train()
        train_loss = 0
        with tqdm(train_dataloader, unit="batch") as tepoch:
            for inputs, targets in tepoch:
                tepoch.set_description(f"Epoch {epoch + 1}")
                optimizer.zero_grad()
                predictions = downstream_model(inputs)
                loss = anomaly_detection_loss_v4(predictions, targets)
                loss.backward()

                torch.nn.utils.clip_grad_norm_(downstream_model.parameters(), max_norm=1.0)
                optimizer.step()
                train_loss += loss.item()

        downstream_model.eval()
        val_loss = 0
        with torch.no_grad():
            with tqdm(val_dataloader, unit="batch") as vepoch:
                for inputs, targets in vepoch:
                    predictions = downstream_model(inputs)
                    loss = anomaly_detection_loss_v4(predictions, targets)
                    val_loss += loss.item()

        avg_train_loss = train_loss / len(train_dataloader)
        avg_val_loss = val_loss / len(val_dataloader)

        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            torch.save(downstream_model.state_dict(), 'anomaly_detection_model_v4.pth')

        print(f'Epoch {epoch + 1}, Train Loss: {avg_train_loss:.4f}, Val Loss: {avg_val_loss:.4f}')
        scheduler.step(avg_val_loss)


# 设置设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 加载数据并进行归一化和标准化
file_path = 'combined_output2.csv'
features, min_vals, max_vals, means, stds = load_data_with_adaptive_scaling(file_path)

# 数据集拆分
train_features, val_features = train_test_split(features, test_size=0.1, random_state=42)

# 数据集和数据加载器
anomaly_train_dataset_v6 = WaterQualityAnomalyDatasetV6(train_features, device)
anomaly_val_dataset_v6 = WaterQualityAnomalyDatasetV6(val_features, device)

# 调整 batch_size
anomaly_train_dataloader_v6 = DataLoader(anomaly_train_dataset_v6, batch_size=512, shuffle=True)
anomaly_val_dataloader_v6 = DataLoader(anomaly_val_dataset_v6, batch_size=512, shuffle=False)

# 加载预训练的 encoder 部分
pretrained_model = WaterQualityMLPMAE(num_features=9, hidden_dim=512, num_layers=3, dropout_rate=0.1)
pretrained_state_dict = torch.load('water_quality_mlp_mae.pth')

# 过滤掉 decoder 相关的权重，并去掉 'encoder.' 前缀
encoder_state_dict = {k.replace('encoder.', ''): v for k, v in pretrained_state_dict.items() if 'encoder' in k}

# 加载 encoder 部分的权重
pretrained_model.encoder.load_state_dict(encoder_state_dict)

# 创建下游任务模型
downstream_model_v4 = DownstreamAnomalyDetectionModelV4(pretrained_model.encoder, hidden_dim=512, dropout_rate=0.1).to(device)

# 优化器和学习率调度器
optimizer = optim.AdamW(downstream_model_v4.parameters(), lr=1e-3)
scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', patience=10)

# 开始训练
train_model_v4(downstream_model_v4, anomaly_train_dataloader_v6, anomaly_val_dataloader_v6, optimizer, scheduler, num_epochs=400)
