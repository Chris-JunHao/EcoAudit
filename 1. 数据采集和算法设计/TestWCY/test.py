import pandas as pd
import numpy as np
import tensorflow as tf
import shap
import sklearn

from multiprocessing.spawn import import_main_path
from sklearn.preprocessing import MinMaxScaler
shap.initjs()
from keras.models import Model
from keras.layers import Input, Dense
from keras import regularizers
from keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.image as mpimg
mpl.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 23
plt.rcParams['figure.dpi'] = 3000
# 加载数据
data = pd.read_csv(r'combined_output3.csv', encoding="utf-8").dropna()
# data['Timestamp'] = pd.to_datetime(data['监测时间'], format = '%Y-%m-%d %H:%M')
# data.drop(['监测时间'],axis = 1,inplace= True)
data = data.reset_index(drop=True)

from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import make_pipeline

from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split

data_norm = (data - data.mean()) / data.std()
# data_norm = data_norm.iloc[:, 1:]
data_norm = data_norm.astype('float32')
start_sclice=2540
# 构建自编码器模型
data_norm_train = pd.concat([data_norm[:start_sclice],data_norm[start_sclice+2000:]],ignore_index=True)
data_norm_test = data_norm[start_sclice:start_sclice+2000]
# data_norm_train,data_norm_test = train_test_split(data_norm,test_size=0.2)

input_dim = data_norm.shape[1]
encoding_dim = 5
input_layer = tf.keras.layers.Input(shape=(input_dim,))
encoder = Dense(8, activation="relu",
                activity_regularizer=regularizers.l1(10e-7))(input_layer)

encoder = Dense(5, activation="relu",
                kernel_regularizer=regularizers.l2(10e-7))(encoder)

encoder = Dense(3, activation='relu',
                kernel_regularizer=regularizers.l2(10e-7))(encoder)
decoder = Dense(5, activation='relu',
                kernel_regularizer=regularizers.l2(10e-7))(encoder)
decoder = Dense(8, activation='relu',
                kernel_regularizer=regularizers.l2(10e-7))(decoder)

decoder = Dense(input_dim, activation='sigmoid',
                kernel_regularizer=regularizers.l2(10e-7))(decoder)

autoencoder = tf.keras.Model(inputs=input_layer, outputs=decoder)

# 设置自定义优化器和学习率
learning_rate = 0.001  # 设置学习率为0.001
adam_optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)

autoencoder.compile(
    optimizer=adam_optimizer, loss='mean_squared_error', metrics=['mse'])
# 训练自编码器模型
earlystopper = EarlyStopping(monitor='val_loss', patience=20, verbose=1)
history = autoencoder.fit(data_norm_train,data_norm_train, epochs=500, batch_size=1000, shuffle=True, validation_data=(data_norm_train, data_norm_train), callbacks=[earlystopper])
# 使用自编码器模型对数据进行预测
reconstructed_data = autoencoder.predict(data_norm_test)

# 计算重构误差
mse = np.mean(np.power(data_norm_test - reconstructed_data, 2), axis=1)
# 使用SHAP库计算SHAP值
background_set = shap.sample(data_norm,100)
explainer = shap.KernelExplainer(autoencoder,background_set,n_jobs = -1)
threshold = np.percentile(mse, 97)
anomalies = np.where(mse > threshold)[0]
need2explained = data_norm.iloc[[start_sclice + i for i in anomalies]]
shap_values = explainer.shap_values(need2explained)
# 可视化SHAP值
shap.summary_plot(shap_values, need2explained)
nshap_values = np.array(shap_values)
# 结合SHAP值和重构误差来检测异常值
print(anomalies)

data.iloc[[start_sclice + i for i in anomalies]]

shap.summary_plot(nshap_values[:,0,:],need2explained,plot_type='bar')

ad_result =data.iloc[[start_sclice + i for i in anomalies]]
ad_result.to_excel('test1.xlsx',sheet_name='Sheet1',index=False)

for i in range(8):
    plt.title(f"{i+1}")
    shap.summary_plot(nshap_values[:,i,:],need2explained,plot_type='bar',show = False,title="SHAP_value",auto_size_plot=None)
    plt.savefig(f'image_{i}.svg',bbox_inches='tight')

images = []
for i in range(8):
    img = plt.imread(f"image_{i}.svg")
    images.append(img)
# 定义画布和子图
fig, axs = plt.subplots(nrows=5,ncols=2,figsize=(1,2))
plt.subplots_adjust(wspace=0.001,hspace=0.001)
# 在子图中画出每张图片
for i, ax in enumerate(axs.flat):
    if i < len(images):
        ax.imshow(images[i])
        # ax.text(0.5, -0.1, f"{i+1}", transform=ax.transAxes,
        #         fontsize=12, ha='center')
    ax.axis('off')
plt.tight_layout
plt.savefig("most_8.svg",format="svg")

fig, ax = plt.subplots(figsize=(8, 8))
ax.plot(history.history['loss'], 'b', label='训练曲线', linewidth=3)
ax.plot(history.history['val_loss'], 'r', label='测试曲线', linewidth=3)
# ax.set_title('Model loss', fontsize=16)
ax.set_ylabel('损失率',fontsize=14)
ax.set_xlabel('迭代次数',fontsize=14)
ax.legend(loc='upper right',fontsize=12)
plt.savefig(r'\loss.png')
plt.show()

plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()
