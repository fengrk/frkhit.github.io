---
layout: post
title: supervisor 使用总结
category: 技术
tags: supervisor, linux
keywords: 
description: 
---

# supervisor 使用总结

## 1. 安全添加/更新 任务
新建或者更新任务配置文件后，supervisor可以在不影响其他任务的前提下 加载或重新 加载任务。
```
supervisorctl reread && supervisorctl update
```
## 2. 任务配置示例

- 多个子进程按顺序使用不同的端口
```
[program:demo]
command=docker run --name=demo_%(process_num)05d -p %(process_num)05d:80 diy/server:latest
directory=/tmp
process_name=%(program_name)s_%(process_num)05d
numprocs=5
numprocs_start=8001
startsecs = 5
startretries = 3
redirect_stderr = true
stdout_logfile = /var/log/supervisor/xx.log
autostart=true
autorestart=unexpected
stopsignal=TERM
```

上述配置，会依次启动 demo_8001, demo_8002, ..., demo_8005 共 5 个 容器， 分别监听 8001, 8002, ..., 8005端口。

