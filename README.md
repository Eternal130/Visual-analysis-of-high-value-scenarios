# Visual-analysis-of-high-value-scenarios
部署方式:
1. 选择一个目录打开cmd或powershell，在cmd中执行`git clone https://github.com/Eternal130/Visual-analysis-of-high-value-scenarios.git`
2. 在项目中新建一个dataset文件夹,完成后的目录结构如下:
```
Visual-analysis-of-high-value-scenarios/dataset
Visual-analysis-of-high-value-scenarios/README.md
Visual-analysis-of-high-value-scenarios/map
Visual-analysis-of-high-value-scenarios/myproject
```
3. 将十个数据集放入dataset文件夹中,数据集在群文件里,完成后目录结构如下：
```
Visual-analysis-of-high-value-scenarios/dataset/part-00000-905505be-27fc-4ec6-9fb3-3c3a9eee30c4-c000.json
Visual-analysis-of-high-value-scenarios/dataset/part-00001-905505be-27fc-4ec6-9fb3-3c3a9eee30c4-c000.json
......
Visual-analysis-of-high-value-scenarios/dataset/part-00009-905505be-27fc-4ec6-9fb3-3c3a9eee30c4-c000.json
```
4. 运行main.py,等待运行完成
5. 在项目文件夹中打开cmd， 运行`python manage.py runserver`
6. 几秒后会显示`Starting development server at http://127.0.0.1:8000/` ,打开链接
