from django.shortcuts import render



ab_Path=r"D:\web\myproject\myproject"+'\\'
def index(request):
    return render(request,ab_Path+r'templates\time.html')