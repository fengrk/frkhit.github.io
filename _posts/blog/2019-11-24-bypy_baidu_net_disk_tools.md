---
layout: post
title:  百度网盘命令行工具 bypy
category: 技术
tags:  python
keywords: 
description: 
---

# 百度网盘命令行工具 bypy

最近收集一些公开的数据集。遇到需要将大文件直接在服务器上传百度云盘的需求（主要是赌百度网盘已经有这个文件，直接利用文件指纹秒传）。

[houtianze/bypy](https://github.com/houtianze/bypy)刚好能实现我的需求。

## 1. 安装

```
# 下载项目
git clone  https://github.com/houtianze/bypy

# 安装
cd bypy && python -m pip install .

# 测试
bypy help
```

## 2. 百度网盘授权

### 首次授权

执行 `bypy list`

拷贝 输出中的授权链接， 在浏览器打开，进行百度网盘授权；接着 将百度网盘提供的授权码，复制到 当前命令行中。

### 使用其他机器的授权信息

假设机器A已经获取授权，机器B希望直接使用机器A的授权，可以这样做：

- 将机器A中的 `~/.bypy/`目录下的所有文件，复制到机器B中的`~/.bypy/`下
- 在机器B中执行`bypy list`即可知道是否成功

## 3. 使用

上传文件：如果文件已经存在百度网盘中，即可实现秒传

```
bypy upload xxx.tar.gz
```

其他所有命令， 可以通过 `bypy help` 获取。
