# frkhit.github.io

技术博客.

## 技术支持

这是一个`flask(python3.6)`项目, 原始博客通过md书写,保存在`blog`目录下.

利用flask工具,将md文件生成静态html文件. md2html, 技术上采用调用github api的方法实现.

html样式暂时没处理.

## flask生成html

1.安装依赖
```
pip install -r requirements.txt
```

2.书写日志

在 `blog` 下添加 .md 文件, 文件名格式`2000-01-01-your.file.name.md`(`日期-文件名.md`)

3.md2html

```
python freeze.py
```
4.部署

```
git push origin master
```

## 感谢
该项目主要参考了[pierrebarroca.github.io](https://github.com/pierrebarroca/pierrebarroca.github.io).感谢作者[@pierrebarroca](https://github.com/pierrebarroca)的分享!









