import pandas as pd

data = pd.read_csv('output.csv')
# 定义一个列表，包含你想保留的type值
types_to_keep = [1, 2, 3, 4, 5, 6]

# 使用isin函数创建一个布尔序列，表示每一行的type值是否在types_to_keep中
condition = data['type'].isin(types_to_keep)

# 使用这个条件过滤DataFrame
data = data[condition]
data.to_csv("outclean.csv", index=False)
