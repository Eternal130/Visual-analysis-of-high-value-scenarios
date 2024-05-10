from django.shortcuts import render
import os
from django.http import FileResponse
from django.http import FileResponse, HttpResponseNotFound
ab_Path=r"D:\web\myproject"+'\\'
def index(request):
    return render(request,ab_Path+r'templates\T.html')

def get_geojson(request, filename):
    # 构建完整的文件路径
    filepath = os.path.join(r'D:\web\myproject\map', filename)
    # 检查文件是否存在
    
    if os.path.exists(filepath):
        # 如果文件存在，返回该文件作为响应
        return FileResponse(open(filepath, 'rb'), content_type='application/json')
    else:
        # 如果文件不存在，返回 404 错误
        return HttpResponseNotFound()