---
layout: post
title: ssh over socks5
category: 技术
tags: ssh
keywords: 
description: 
---

# ssh over socks5

```
ssh -o ProxyCommand='nc -x 127.0.0.1:1080 %h %p' remote_user@remote_ssh_server

```

[参考](https://ieevee.com/tech/2017/10/19/ssh-over-socks5.html)

