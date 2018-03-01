# frkhit.github.io

技术博客.

## 技术支持

这是一个flask项目, 原始博客通过md书写,放置在project/pages目录下.

利用flask工具,将md文件生成静态html文件. md2html, 技术上采用调用github api的方法实现.

html样式暂时没处理.

## flask生成html

1.安装依赖
```
pip install -r requirements.txt
```

2.书写日志

在 project/pages 下添加 .md 文件

3.md2html

```
python freeze.py
```
4.部署

```
git push origin master
```









