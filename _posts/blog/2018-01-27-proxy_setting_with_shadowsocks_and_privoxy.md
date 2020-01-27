---
layout: post
title: shadowsocks+privoxy设置本地代理
category: 技术
tags: 
    - shadowsocks
keywords: 
description: 
---

# shadowsocks+privoxy设置本地代理

- 1.sslocal启动, 本地监听1080端口
- 2.安装privoxy, `sudo apt install -y privoxy`
- 3.配置privoxy

```
sudo vim /etc/privoxy/config

# 添加一行
forward-socks5 / 127.0.0.1:1080 .

```

- 4.重启privoxy， `/etc/init.d/privoxy restart`
- 5.python中使用proxy

```
def set_proxy():
    import os
    os.environ["https_proxy"] = "http://127.0.0.1:8118"
    os.environ["HTTPS_PROXY"] = "http://127.0.0.1:8118"
    os.environ["http_proxy"] = "http://127.0.0.1:8118"
    os.environ["HTTP_PROXY"] = "http://127.0.0.1:8118"

if __name__ == '__main__':
    import requests
    
    try:
        print(requests.get("https://www.google.com").status_code)  # raise Exception
    except Exception as e:
        print(e)
    
    set_proxy()
    
    print(requests.get("https://www.google.com").status_code)  # 200

```
