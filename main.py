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
        # data = data[(data['is_moving'] != 0) & (data['type'] != 0)]
        # print(data.head(5))
        # data['id_diff'] = data['id'].diff().fillna(1)
        #
        # # 标记差异为1
        # data['id_diff'] = data['id_diff'].apply(lambda x: 1 if x != 0 else 0)
        #
        # # 使用cumsum函数重新编号
        # data['new_id'] = data['id_diff'].cumsum()

        # print(data.info)
        # 输出重新编号后的结果
        # print(data.head(5))
        # 将 'time_meas' 字段转换为 datetime 类型
        data['time_meas'] = pd.to_datetime(data['time_meas'], unit='us')

        # 根据 'time_meas' 和 'id' 字段进行排序
        data = data.sort_values(by=['time_meas', 'id'])
        # print(data.info)
        # 输出排序后的结果
        # print(data.head(5))
        # del data['id']
        # del data['seq']
        # del data[data.columns[0]]
        # del data['is_moving']
        del data['shape']
        del data['orientation']
        del data['heading']
        data['x'] = data['position'].apply(lambda x: x['x'])
        data['y'] = data['position'].apply(lambda x: x['y'])
        del data['position']

        data.to_csv("output" + str(i) + ".csv", index=False)
        print("output" + str(i) + ".csv" + " is done!")
    import pandas as pd

    # 创建一个空的DataFrame用于存储合并后的数据
    merged_data = pd.DataFrame()

    # 遍历每个输出文件
    for i in range(10):
        # 读取输出文件
        file_path = "output" + str(i) + ".csv"
        data = pd.read_csv(file_path)

        # 将数据添加到合并后的DataFrame中
        merged_data = pd.concat([merged_data, data])

    # 创建一个布尔序列，表示每一行的seq值是否大于或等于0
    condition = merged_data['seq'] >= 0

    # 使用这个条件过滤DataFrame
    merged_data = merged_data[condition]
    # 按照时间戳和ID进行排序
    merged_data = merged_data.sort_values(by=['time_meas', 'id'])

    # 将合并后的数据保存为output.csv文件
    merged_data.to_csv("output.csv", index=False)

    print("合并并排序完成！")


def loading_data():
    data = pd.read_csv('outclean.csv')
    data.drop(0, inplace=True)
    return data
# if __name__ == '__main__':
#     print(loading_data().iloc[10])
