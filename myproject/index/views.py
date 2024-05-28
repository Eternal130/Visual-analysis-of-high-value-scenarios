import csv
import json
import os
from datetime import datetime

import pandas as pd
from pandas import to_datetime

from main import loading_data

from django.http import FileResponse, HttpResponseNotFound, HttpResponse, JsonResponse
from django.shortcuts import render

global_data = None
indexx = 0


def load_data():
    global global_data
    global_data = loading_data()


load_data()


# ab_Path=r"D:\web\myproject"+'\\'
def index(request):
    return render(request, r'T.html')


def get_geojson(request, filename):
    # 构建完整的文件路径
    filepath = os.path.join(r'map', filename)
    # 检查文件是否存在

    if os.path.exists(filepath):
        # 如果文件存在，返回该文件作为响应
        return FileResponse(open(filepath, 'rb'), content_type='application/json')
    else:
        # 如果文件不存在，返回 404 错误
        return HttpResponseNotFound()


def get_dataset(request, filename):
    # 构建完整的文件路径
    filepath = os.path.join(filename)
    # 检查文件是否存在

    if os.path.exists(filepath):
        # 如果文件存在，返回该文件作为响应
        return FileResponse(open(filepath, 'rb'), content_type='text/csv')
    else:
        # 如果文件不存在，返回 404 错误
        return HttpResponseNotFound()


def get_dataset_by_time(request, time):
    global global_data
    global indexx
    # print('awa')
    # print(global_data.iloc[indexx])
    time = to_datetime(time.replace('T', ' '))
    datas = {'0': [], '1': [], '2': [], '3': [], '4': [], '5': [], '6': [], '7': [], '8': [], '9': []}
    for j in [200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]:
        if to_datetime(global_data.iloc[indexx]['time_meas']) > time + pd.Timedelta('200ms'):
            for i in range(0, indexx, -1):
                # print('ab')
                if to_datetime(global_data.iloc[i]['time_meas']) <= time:
                    indexx = i
                    # print('a')
                    break
            indexx = 0

        if to_datetime(global_data.iloc[indexx]['time_meas']) < time:
            # print('ad')
            for i in range(indexx, len(global_data)):
                # print('ac')
                if time <= to_datetime(global_data.iloc[i]['time_meas']):
                    indexx = i
                    # print('aa')
                    break
        # print(time > to_datetime(global_data.iloc[indexx]['time_meas']))
        for i in range(indexx, len(global_data)):
            if time <= to_datetime(global_data.iloc[i]['time_meas']) <= time + pd.Timedelta('200ms'):
                datas[str(int(j / 200 - 1))].append(global_data.iloc[i].to_dict())
                # data.append(global_data.iloc[i])
                indexx += 1
                # print('aaa')
                # print(data)
            else:
                time += pd.Timedelta('200ms')
                # print('aaaa')
                # print(time > to_datetime(global_data.iloc[i]['time_meas']))
                break

    # 将数据转换为JSON格式
    # data_json = json.dumps(data)
    # print('awawa')
    # print(time)
    # print(data)
    json_data = json.dumps(datas)
    # if global_data is not None:
    #     # print(global_data)
    #     print(indexx)
    response = HttpResponse(json_data, content_type='application/json')
    # 创建一个CSV writer
    # writer = csv.writer(response)
    # # 将data写入CSV
    # print(json_data)
    # writer.writerows(json_data)
    # 返回JSON数据到前端
    return response
def calculate_timedata(request):
    # Fetch raw data from the database or other data source
    df = pd.read_csv('output0.csv')
    raw_data = df.to_dict('records')
    # Set the initial timestamp
    startdate = datetime(2023, 4, 12, 15, 59, 56, 699682)

    # Initialize the hourly data array
    hourly_data = [dict() for _ in range(24)]

    # Keep track of unique vehicle IDs
    vehicle_ids = set()

    for item in raw_data:
        timestamp_str = item['time_meas']
        vehicle_type = item['type']
        vehicle_id = item['id']

        # Only process unique vehicle IDs
        if vehicle_id not in vehicle_ids:
            vehicle_ids.add(vehicle_id)

            # Convert the timestamp string to a datetime object
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")

            # Calculate the hour difference from the initial timestamp
            time_diff = (timestamp - startdate).total_seconds() / 3600
            hour = int(time_diff)

            # Only process data within the 0-23 hour range
            if 0 <= hour < 24:
                if vehicle_type not in hourly_data[hour]:
                    hourly_data[hour][vehicle_type] = 0
                hourly_data[hour][vehicle_type] += 1

    # Convert the dictionaries to lists before returning the data
    hourly_data = [list(hourly_data[i].values()) for i in range(24)]
    with open('hourly_data.json', 'w') as file:
        json.dump(hourly_data, file)
    return JsonResponse(hourly_data, safe=False)
    
def get_timedata(request):
    # Read JSON data from file
    with open('hourly_data.json', 'r') as file:
        hourly_data = json.load(file)

    return JsonResponse(hourly_data, safe=False)

