---
layout: post
title: virtualenv中安装anaconda模块
category: 技术
tags: python
keywords: 
description: 
---

# virtualenv中安装anaconda模块

faiss是Facebook AI实验室开源的一个高性能的相似性搜索库,该项目提供了python接口.faiss提供了源码编译和anaconda的两种安装方法. 但要在现有的virtualenv中安装faiss,却不容易.

anaconda安装faiss的方法:

```
# CPU version only
conda install faiss-cpu -c pytorch

# GPU version requires CUDA to be installed, otherwise it falls back to CPU version
conda install faiss-gpu -c pytorch

```

## 解决方案

下载anaconda中编译包,解压后,复制到虚拟环境中.

代码:

```
wget  https://anaconda.org/pytorch/faiss-cpu/1.2.1/download/linux-64/faiss-cpu-1.2.1-py36_cuda9.0.176_1.tar.bz2
tar xvjf faiss-cpu-1.2.1-py36_cuda9.0.176_1.tar.bz2
cp -r lib/python3.6/site-packages/* env/lib/python3.6/site-packages/
rm lib/ -R && rm faiss-cpu-1.2.1-py36_cuda9.0.176_1.tar.bz2
pip install mkl

```

## 参考
- [Installing faiss on Google Colaboratory](https://stackoverflow.com/questions/47967252/installing-faiss-on-google-colaboratory/49359649#49359649)


