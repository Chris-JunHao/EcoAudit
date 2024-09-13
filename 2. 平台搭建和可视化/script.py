# coding=utf-8
import requests
import csv
import time
from WaterData import WaterData  # 假设 WaterData 类定义在另一个文件中

# 解析地理位置数据
def parse_name(state_name):
    name_dict = {"0": "0000"}
    name_str = state_name.split('"')[5]
    name_list = name_str.split("!!")
    for name in name_list:
        if name == "":
            break
        id, value = name.split("$")[0], name.split("$")[1]
        name_dict[id] = value
    print("解析地理位置完成")
    return name_dict

# 解析水质数据
def parse_data(state_info, name_dict):
    data_str = state_info.split('"')[5]
    data_list = data_str.split("!!")
    water_data_list = []

    for data in data_list:
        if data == "":
            break
        data_list = data.split("$")

        single_data = WaterData()
        single_data.Id = data_list[0]
        single_data.State_name = name_dict.get(single_data.Id, "0000")
        single_data.Time = data_list[1]
        single_data.PH_value = data_list[2]
        single_data.PH_Level = data_list[3]
        single_data.Dissolved_OX = data_list[4]
        single_data.Dissolved_OX_Level = data_list[5]
        single_data.KMnO = data_list[6]
        single_data.KMnO_Level = data_list[7]
        single_data.NH3N = data_list[10]
        single_data.NH3N_Level = data_list[11]
        single_data.Date = data_list[12]

        water_data_list.append(single_data)

    return water_data_list

# 获取HTML数据
def get_data(home):
    response = requests.get(home)
    html = response.text
    stainfo, staname, stationinfo = "", "", ""

    lines = html.split("\r\n")
    for line in lines:
        if 'name="stainfo"' in line:
            stainfo = line
        if 'name="staname"' in line:
            staname = line
        if 'name="stationinfo"' in line:
            stationinfo = line

    print(stainfo)
    print(staname)

    name_dict = parse_name(staname)
    water_data_list = parse_data(stainfo, name_dict)

    print("解析水质数据完成")
    return water_data_list

# 保存数据到 CSV
def save_to_csv(water_data_list, file_name):
    with open(file_name, "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "地址", "日期", "时间", "PH值", "PH级别", "溶解氧", "级别", "高锰酸盐指数", "级别", "氨氮", "级别"])

        for water_data in water_data_list:
            writer.writerow([
                water_data.Id, water_data.State_name, water_data.Date,
                water_data.Time, water_data.PH_value, water_data.PH_Level,
                water_data.Dissolved_OX, water_data.Dissolved_OX_Level,
                water_data.KMnO, water_data.KMnO_Level, water_data.NH3N,
                water_data.NH3N_Level
            ])

# 主程序
if __name__ == '__main__':
    home = 'http://online.watertest.com.cn/'  # 起始位置

    # 时间间隔（秒）
    time_i = 60

    while True:
        time_str = time.strftime('%Y-%m-%d_%H-%M', time.localtime(time.time())) + ".csv"
        print(f"创建文件: {time_str}")

        water_data_list = get_data(home)
        save_to_csv(water_data_list, time_str)

        print(f"{time_str} 文件保存成功，总共 {len(water_data_list)} 条数据")
        time.sleep(time_i)
