---
layout: post
title: docker学习笔记
category: 技术
tags: docker
keywords: 
description: 
---

# docker学习笔记

## 1. 打包 flask server实例

[参考](http://containertutorials.com/docker-compose/flask-simple-app.html)

Dockerfile

``` 
FROM ubuntu:latest
MAINTAINER Rajdeep Dua "dua_rajdeep@yahoo.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
```

build: `docker build -t flask-sample-one:latest . `

run: `docker run -d -p 5000:5000 flask-sample-one`

## 2. 将 container 保存为 image
``` docker commit <CONTAIN-ID> <IMAGE-NAME>```

## 3. 导出镜像
[参考](https://blog.csdn.net/a906998248/article/details/46236687)

使用 `docker export <container_name>` 导出镜像:
```
# 导出
docker export furious_bell > /home/myubuntu-export-1204.tar

# 导入
docker import - /home/myubuntu-export-1204.tar
```

使用 `docker save <image_name>` 导出镜像:
```
# 导出
docker save 9610cfc68e8d > /home/myubuntu-save-1204.tar

# 导入
docker load < /home/myubuntu-save-1204.tar

# 重命名
docker images
docker tag <image_id> image_name:latest
```

# 4. 镜像重命名
```docker tag <image_id> image_name:latest```

# 5. 使用外部文件
```
# create Dockerfile
echo 'FROM python:3.6
WORKDIR /app
pip install tornado -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
ENTRYPOINT ["python"]
CMD ["app.py"]
' >> Dockerfile

# build container
docker build -t diy/server:latest . 

# start container
docker run -d -v /home/ubuntu/app:/app -p 5000:5000 diy/server

```

