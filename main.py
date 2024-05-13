import json

import pandas as pd

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    for i in range(10):
        # 读取原始文本文件
        with open('dataset/part-0000' + str(i) + '-905505be-27fc-4ec6-9fb3-3c3a9eee30c4-c000.json', 'r') as file:
            data = file.readlines()

        # 处理每一行数据
        json_data = []
        for line in data:
            # 将每行数据转换为JSON对象
            json_obj = json.loads(line)

            # 将position字段从字符串转换为字典
            json_obj['position'] = json.loads(json_obj['position'])

            # 将shape字段从字符串转换为字典
            json_obj['shape'] = json.loads(json_obj['shape'])

            # 将处理后的JSON对象添加到列表中
            json_data.append(json_obj)

        # 将处理后的数据以JSON格式输出到文件
        with open('output.json', 'w') as file:
            json.dump(json_data, file, indent=4)
        data = pd.read_json('output.json')
        # print(data.head(5))
        data = data[(data['is_moving'] != 0) & (data['type'] != 0)]
        # print(data.head(5))
        data['id_diff'] = data['id'].diff().fillna(1)

        # 标记差异为1
        data['id_diff'] = data['id_diff'].apply(lambda x: 1 if x != 0 else 0)

        # 使用cumsum函数重新编号
        data['new_id'] = data['id_diff'].cumsum()

        # print(data.info)
        # 输出重新编号后的结果
        # print(data.head(5))
        # 将 'time_meas' 字段转换为 datetime 类型
        data['time_meas'] = pd.to_datetime(data['time_meas'], unit='us')

        # 根据 'time_meas' 和 'id' 字段进行排序
        data = data.sort_values(by=['time_meas', 'new_id'])
        # print(data.info)
        # 输出排序后的结果
        # print(data.head(5))

        data.to_csv("output" + str(i) + ".csv")
        print("output" + str(i) + ".csv" + " is done!")