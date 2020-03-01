---
layout: post
title:  docker-compose 笔记
category: 技术
tags:  
    - docker
    - docker-compose
keywords: 
description: 
---

# docker-compose 笔记


## 1. 数据卷

通过 `volumes` 或 宿主文件/目录， 挂载数据。

```
version: '3.7'
services:
    nginx:
        image: nginx
        volumes:
            - static-html:/usr/share/nginx/html
            - ./nginx.conf:/etc/nginx/conf.d/default.conf
        ports:
            - 80:80

volumes:
    static-html:

```

`volumes` 常用操作

```
docker volume list

docker volume rm vo-1

```

## 2. 网络


### 2.1 HOST

`nginx` 可以通过 `127.0.0.1:6000` 访问宿主机的 `127.0.0.1:6000` 服务

```
services:
    nginx:
        image: nginx
        volumes:
            - ./nginx.conf:/etc/nginx/conf.d/default.conf
        ports:
            - 80:80
        network_mode: host

```

### 2.2 Bridge

```
services:
    nginx:
        image: nginx
        volumes:
            - ./nginx.conf:/etc/nginx/conf.d/default.conf
        depends_on:
            - tornado
        ports:
            - 80:80
        networks:
            - xxx-network

    tornado:
        image: tornado
        networks:
            - xxx-network

networks:
    xxx-network:
        driver: bridge

```

### 2.3 bridge + ip 分配


```
services:
    nginx:
        image: nginx
        volumes:
            - ./nginx.conf:/etc/nginx/conf.d/default.conf
        depends_on:
            - tornado
        ports:
            - 80:80
        networks:
            xxx-network:
                ipv4_address: 10.5.0.2

    tornado:
        image: tornado
        networks:
            xxx-network:
                ipv4_address: 10.5.0.3

networks:
    xxx-network:
        driver: bridge
        ipam:
            driver: default
            config:
                - subnet: 10.5.0.0/16
```

## 3. 常用命令

- 多实例： `docker-compose up --scale kafka=3 -d`
