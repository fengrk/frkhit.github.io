---
layout: post
title:  docker-compose scale 场景下向容器传递容器序号
category: 技术
tags:  
    - docker-compose
keywords: 
description: 
---

# docker-compose scale 场景下向容器传递容器序号


本示例， 展示在 `docker-compose up --scale` 场景下， 如何向容器传递当前容器序号。源码见[scale-demo](https://github.com/frkhit/docker-practice/tree/master/docker-compose/scale-demo)


`docker-compose`文件配置:

```
version: '3.5'
services:
    py-server:
        image: python:3.7.6-alpine
        hostname: server-${SERVER_INDEX}
        command: ["python", "demo_server.py"]
        working_dir: /app
        restart: always
        volumes:
            - ./:/app
```

`demo_server.py` 打印当前容器的 `$HOSTNAME`:

``` 
import os
import time


host_name = os.environ.get("HOSTNAME")

with open("/app/demo.log", "a") as f:
    f.write("{}\n".format(host_name))


while True:
    time.sleep(60)

```

`scale.sh` 将序号传递给容器:

``` 
#!/bin/bash

for i in $(seq 1 10); do
  echo 'SERVER_INDEX=${i}' > .env &&  SERVER_INDEX=$i docker-compose up -d --scale py-server=$i --no-recreate;
done
```

执行示例：

```
docker-compose down
chmod +x ./scale.sh 
./scale.sh
```

结果文件 `demo.log` 中出现：

```
server-1
server-2
server-3
server-4
server-5
server-6
server-7
server-8
server-9
server-10
```

结果表明：

- 每个容器只会执行一次
- 每个容器可根据 `$HOSTNAME` 获知容器的序号
