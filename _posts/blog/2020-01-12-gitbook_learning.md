---
layout: post
title:  gitbook 笔记
category: 技术
tags:  gitbook, docker
keywords: 
description: 
---

# gitbook 笔记

## 1. 导出 pdf 文件

源码: [gitbook-pdf](https://github.com/frkhit/docker-practice/tree/master/hubs/gitbook-pdf)

``` 
# install dependencies
docker run --rm -v $(pwd)/sample:/book frkhit/docker-practice:gitbook-pdf gitbook install

# build pdf
docker run --rm -v $(pwd)/sample:/book frkhit/docker-practice:gitbook-pdf gitbook pdf

# build epub
docker run --rm -v $(pwd)/sample:/book frkhit/docker-practice:gitbook-pdf gitbook epub

# serve web page
docker run --rm -v $(pwd)/sample:/book -p 4000:4000 frkhit/docker-practice:gitbook-pdf gitbook serve

```

备注: 导出的 pdf 字体可能有问题, 可以参考[给Docker镜像(Debian)添加中文支持和中文字体](https://blog.llcat.tech/2018/12/03/add-zh-CN-locales-and-fonts-in-docker-images/)在 docker 中 安装必要的字体.
