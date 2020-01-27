---
layout: post
title: docker引起的空间不足
category: 技术
tags: 
    - docker
keywords: 
description: 
---

# docker引起的空间不足

使用docker-compose编译docker时，提示空间不足。

docker文件在/var/lib/docker/下。

/tmp/下生成tmp* 文件，可删除。
