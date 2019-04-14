---
layout: post
title: python小技巧
category: 技术
tags: python
keywords: 
description: 
---

# python小技巧

## 1. 使用指定 pypi源安装包
```
pip install jieba gensim numpy tornado -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
```

## 2. 将指定包安装到lib目录下
```
echo path_to_package >> xx/lib/python2.7/site-packages/pk1.pth
```

## 3. cheat: 命令示例
```
python -m pip install cheat

# tar命令使用示例
cheat tar

# To extract an uncompressed archive:
tar -xvf /path/to/foo.tar

# To create an uncompressed archive:
tar -cvf /path/to/foo.tar /path/to/foo/
....
```

## 4. pip 工具

逐行安装, 忽略错误:
```
cat requirements.txt | xargs -n 1 python -m pip install
```

## 5. python 文件服务器
```
# python3 or python2
python -m http.server || python -m SimpleHTTPServer
```

