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
cat path_to_package >> xx/lib/python2.7/site-packages/pk1.pth
```
