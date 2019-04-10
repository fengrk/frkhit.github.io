---
layout: post
title: shell 学习笔记
category: 技术
tags: ubuntu, shell
keywords: 
description: 
---

# shell学习笔记

## 1. 一个命令的结果填充到另一个命令中
```ssh foo@$(cat /data/ip.result)```

## 2. sudo执行echo命令
```
sudo sh -c "echo '{
  \"registry-mirrors\": [\"https://registry.docker-cn.com\"]
}' >> /etc/docker/daemon.json"
```
## 3. 清空文件
```echo -n > ~/xx.conf```

## 4. 常用命令
```
# 查看磁盘使用
df -lh

# 查看当前目录所占空间
du -sh ./

```

## 5. ssh命令
```
# 上传文件
scp ./local.file ubuntu@host:/remote/remote.file

# 下载文件
scp ubuntu@host:/remote/remote.file ./local.file
```
