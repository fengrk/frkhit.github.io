---
layout: post
title:  gitbook 笔记
category: 技术
tags:  
    - gitbook
    - docker
keywords: 
description: 
---

# gitbook 笔记

## 1. 导出 pdf 文件

### 1.1 docker 导出 pdf
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


### 1.2 mac 下 使用 gitbook 命令导出 pdf

使用 `gitbook pdf ./ ./myBook.pdf --log=debug` 导出 pdf。

如果安装 `4.x` 版本的 `calibre-ebook`， 会出现报错：

`
Invalid file descriptor to ICU data received.
`

解决方案是安装 `3.x` 版本的 `calibre-ebook`, 下载地址在[这里](https://download.calibre-ebook.com/3.html)。 

参考： [解決 Gitbook 匯出 PDF 檔案時沒有產出的問題](https://blog.chunkai.me/2019/12/16/solving-the-problem-that-gitbook-exporting-pdf-without-results/)

## 2. 细节定制

参考: [Gitbook 细节定制](https://zhuanlan.zhihu.com/p/27171995)

### 2.1 去除 published by gitbook

`book.json`中加入 css 文件:

``` 
"styles":{
    "website": "./res/remove_publisher.css"
}
```

`remove_publisher.css`文件:

``` 
.gitbook-link {
    display: none !important;
}
```

### 2.2 去除分享按钮

`book.json`:

``` 
"plugins": [ "-sharing"],
"links": {
        "sharing": {
            "all": null,
            "facebook": null,
            "google": null,
            "twitter": null,
            "weibo": null
        }
}
```
