---
layout: post
title:  docker-compose v3 版本中限制容器资源
category: 技术
tags:  
    - docker-compose
keywords: 
description: 
---

# docker-compose v3 版本中限制容器资源

本示例， 展示在docker-compose v3 版本下, 如何限制容器资源。[源码](https://github.com/frkhit/docker-practice/tree/master/docker-compose/resoure_limit)


`docker-compose`文件配置:

```
version: '3'
services:
    py-demo:
        image: python:3.7.6-alpine
        command: ["python", "-u", "demo_server.py"]
        restart: always
        working_dir: /app
        volumes:
            - ./:/app
        environment:
            TZ: Asia/Shanghai
        
        deploy:
            resources:
                limits:
                    cpus: '1'
                    memory: 100M
                reservations:
                    cpus: '0.5'
                    memory: 10M
```

`demo_server.py` 模拟内存分配:

``` 
import time

memory_list = []

if __name__ == '__main__':
    print("start container")

    while True:
        key = str(int(time.time()))
        new_list = ["{}_{}".format(key, i) for i in range(100 * 10000)]
        memory_list.extend(new_list)
        print("memory len: {}".format(len(memory_list)))
        time.sleep(1)

```

使用兼容模式启动 docker-compose:

``` 
#!/bin/bash

docker-compose --compatibility  up -d
sleep 1
docker-compose logs -f
```

执行示例：

```
docker-compose down
chmod +x ./start.sh 
./start.sh
```

结果：

```
py-demo_1  | start container
py-demo_1  | memory len: 1000000
py-demo_1  | memory len: 2000000
py-demo_1  | start container
py-demo_1  | memory len: 1000000
py-demo_1  | memory len: 2000000
py-demo_1  | start container
py-demo_1  | memory len: 1000000
py-demo_1  | memory len: 2000000
py-demo_1  | start container
py-demo_1  | memory len: 1000000
py-demo_1  | memory len: 2000000

```

`docker stats` 结果:

![docker stats](../../../../public/img/docker-compose/resource_limit_docker_stats.png)


结果表明：docker-compose v3 下, 配合 `docker-compose --compatibility  up` 可以限制容器使用资源.

