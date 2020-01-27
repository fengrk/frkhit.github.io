---
layout: post
title:  Systemd 教程
category: 技术
tags:  
    - Systemd
    - ubuntu
keywords: 
description: 
---

# Systemd 教程

## 1. systemd 管理 `autossh`

创建 `autossh.service` 文件， 配置服务：

```
[Unit]
Description=Auto SSH Tunnel
After=network-online.target
[Service]
User=root
Type=simple
ExecStart=/usr/bin/autossh -p 22 -M 23 -NR 'localhost:23:localhost:22' root@remote.com
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=always
[Install]
WantedBy=multi-user.target
WantedBy=graphical.target

```

执行命令， 运行 `autossh` :

```
apt update && apt install autossh -y

chmod 644 autossh.service
cp autossh.service /lib/systemd/system/

systemctl enable systemd-networkd-wait-online
systemctl enable autossh
systemctl start autossh

```
