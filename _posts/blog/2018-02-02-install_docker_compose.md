---
layout: post
title: 安装docker-compose
category: 技术
tags: 
    - docker
keywords: 
description: 
---

# 安装docker-compose

## 1.pip install docker-compose

存在问题：依赖包docker,docker-py分不清，出现各种问题。


## 2.github release安装包安装

```
wget 'https://github-production-release-asset-2e65be.s3.amazonaws.com/15045751/fa6c5b98-028b-11e8-9248-eb939dd05ee6?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20180201%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20180201T170222Z&X-Amz-Expires=300&X-Amz-Signature=d9809e85147280ffca3db30cd589fce63bea6c63ec3d42c1fac474ca7db1599a&X-Amz-SignedHeaders=host&actor_id=15940906&response-content-disposition=attachment%3B%20filename%3Ddocker-compose-Linux-x86_64&response-content-type=application%2Foctet-stream' -O docker-compose

sudo mv docker-compose /user/local/bin/ && sudo chmod +x /user/local/bin/docker-compose

docker-compose --version

```

