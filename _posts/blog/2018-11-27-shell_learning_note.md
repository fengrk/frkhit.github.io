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
ssh例子:
```
# 获取远程服务器的 ip, 并 ssh连接到该服务器上
ssh foo@$(cat /data/ip.result)
```

docker例子:
```
# 删除所有仓库名为 redis 的镜像：
docker image rm $(docker image ls -q redis)
```
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

## 6. 获取本机ip
获取本机ip:

```
 ifconfig|sed -n '/inet addr/s/^[^:]*:\([0-9.]\{7,15\}\) .*/\1/p'
```

获取当前虚拟机ip:
```
 ifconfig|sed -n '/inet addr/s/^[^:]*:\([0-9.]\{7,15\}\) .*/\1/p' | grep 192.168
```

## 7. 设置屏幕亮度为0
```
[[ "$(cat /sys/class/backlight/intel_backlight/brightness)" -ne "0" ]] && (echo 0 | sudo tee /sys/class/backlight/intel_backlight/brightness)
```

