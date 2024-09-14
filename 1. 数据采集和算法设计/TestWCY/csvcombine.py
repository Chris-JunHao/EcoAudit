import os
import pandas as pd

# 设置CSV文件所在的目录
directory = r'E:\code\tensorflowTest\csv2'  # 你的GB2312编码的CSV文件目录
output_file = r'E:\code\tensorflowTest\combined_output.csv'  # 合并后的输出文件路径

# 获取该目录下所有CSV文件
csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

# 初始化一个空的DataFrame用于合并
combined_csv = pd.DataFrame()

# 遍历所有CSV文件，按行合并
for file in csv_files:
    file_path = os.path.join(directory, file)
    # 读取CSV文件时指定GB2312编码
    df = pd.read_csv(file_path, encoding='GB2312')
    # 将其添加到合并的DataFrame中
    combined_csv = pd.concat([combined_csv, df], ignore_index=True)

# 将合并后的数据保存为一个新的CSV文件，仍使用GB2312编码
combined_csv.to_csv(output_file, index=False, encoding='GB2312')

print(f'所有GB2312编码的CSV文件已成功合并并保存为 {output_file}')
