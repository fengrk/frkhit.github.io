---
layout: post
title:  docker-compose 安装方法
category: 技术
tags:  
    - docker-compose
    - mac
    - linux
keywords: 
description: 
---

# docker-compose 安装方法

本文提供一种简单的`docker-compose`安装方法。

[compose](https://github.com/docker/compose)项目提供了一种通过封装 docker 中 compose 容器的方式，执行 compose 命令的方案。

具体步骤是：

- 下载 compose 项目中releases提供的`run.sh`文件， 链接为`https://github.com/docker/compose/releases/download/1.25.0-rc2/run.sh`
- 赋予执行权限 `sudo chmod +x run.sh`
- 移动到系统目录下并改名为 docker-compose: `sudo mv run.sh /usr/local/bin/docker-compose`
- 执行 docker-compose命令： `docker-compose ps`
