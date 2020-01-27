---
layout: post
title:  docker运行 pyppeteer
category: 技术
tags:  
    - docker
    - puppeteer
    - pyppeteer
keywords: 
description: 
---

# docker运行 puppeteer/pyppeteer

## 1. docker 镜像

`Dockerfile`如下：

```
FROM python:3.7-buster

RUN apt-get update && apt-get upgrade -y && apt-get install -y wget && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' && \
    apt-get update && \
    apt-get install -y google-chrome-unstable fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst fonts-freefont-ttf --no-install-recommends && \
    pip install requests urllib3 fake-useragent beautifulsoup4 arrow furl parsel websockets html2text tld pytz xlwt aiohttp pymongo pyee appdirs tqdm && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /root/.cache/pip/*

```

可以自己执行构建

`docker build -t pyppeteer .`

也可以直接拉取镜像

`docker pull frkhit/docker-practice:pyppeteer`


## 2. root用户无法启动 chrome

使用 docker 的 root 用户启动 `pyppeteer` 报错：

`Running as root without --no-sandbox is not supported`.

原因详见：[Issue 638180: Exit instead of crashing when running as root without --no-sandbox.](https://bugs.chromium.org/p/chromium/issues/detail?id=638180).

解决方法是， 在启动命令中增加 `--no-sandbox` 参数.

对于 `pyppeteer`， 可以在代码中增加如下逻辑：

```
if os.geteuid() == 0:
    if args:
        args.append('--no-sandbox')
    else:
        kwargs["args"] = ['--no-sandbox']

```