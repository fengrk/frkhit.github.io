---
layout: post
title: privoxy实现PAC代理上网
category: 技术
tags: privoxy, socks5, proxy, PAC
keywords: 
description: 
---

# privoxy实现PAC代理上网

本文主要参考: [Linux 使用 ShadowSocks + Privoxy 实现 PAC 代理](https://huangweitong.com/229.html)

## 1. Privoxy实现http代理上网

安装privoxy:

```
sudo apt install privoxy
```

配置:
```
vim /etc/privoxy/config

# 修改监听地址
listen-address 127.0.0.1:8118

# 代理转发: 若不打算实现PAC模式, 确保去除下一行的注释
# forward-socks5 / 127.0.0.1:1080 .
```

重启服务:

```
sudo service privoxy start
```

## 2. PAC

[生成pac.action:](https://github.com/zfl9/gfwlist2privoxy)

```
cd /tmp && curl -4sSkLO https://raw.github.com/zfl9/gfwlist2privoxy/master/gfwlist2privoxy && bash gfwlist2privoxy 127.0.0.1:1080
mv -f pac.action /etc/privoxy/ && echo 'actionsfile pac.action' >>/etc/privoxy/config && sudo service privoxy start
```

## 3. 测试

```
# 使用代理
curl www.google.com

# 本地地址
curl "http://pv.sohu.com/cityjson?ie=utf-8"
```
