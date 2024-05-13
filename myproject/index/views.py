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
