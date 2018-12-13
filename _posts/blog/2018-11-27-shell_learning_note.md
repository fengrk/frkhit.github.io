---
layout: post
title: shell 学习笔记
category: 技术
tags: ubuntu,shell
keywords: 
description: 
---

# shell学习笔记

```
# 一个命令的结果填充到另一个命令中
ssh foo@$(cat /data/ip.result)

# sudo执行echo命令
sudo sh -c "echo '{
  \"registry-mirrors\": [\"https://registry.docker-cn.com\"]
}' >> /etc/docker/daemon.json"

# 清空文件
echo -n > ~/xx.conf

```
