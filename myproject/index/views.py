import os

from django.http import FileResponse, HttpResponseNotFound
from django.shortcuts import render


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

