---
layout: post
title: docker学习笔记
category: 技术
tags: 
    - docker
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

## 4. 镜像重命名
```docker tag <image_id> image_name:latest```

## 5. 使用外部文件

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

## 6. docker常用命令示例

- 获取container日志: `docker logs <container_id>`
- 实时获取container日志: `docker logs -f <container_id>`
- 停止container: `docker stop <container_id>`
- 删除镜像标签: `docker rmi -f <image_name>:<tag>`
- 指定工作目录: `docker run -d -v /home/frkhit/rkfeng/server:/app  -w /app frkhit/docker-python:3.6-chrome python main.py`
- 使用宿主时区：`docker run -d  -v /etc/localtime:/etc/localtime:ro ...`
- 运行时指定时区：`docker run -d --env TZ=Asia/Shanghai ...`
- 执行多条命令: `docker run -d -w /app frkhit/docker-python:3.6-chrome sh -c "python jd_main.py; python main.py"`
- 查看容器变化: `docker diff <container>`

## 7. Dockerfile常用命令示例

- 复制多个文件: `COPY file_1 file_2 file_3 ./`
- 添加作者信息: `MAINTAINER frkhit "frkhit@gmail.com"`

## 8. 端口绑定

```
# 端口绑定
docker run -d -p 8080:80 ...

# ip + 端口 绑定
docker run -d -p 127.0.0.1:9999:80 ...

# ip + 所有端口 绑定
docker run -d -p 127.0.0.1::80 ...

# 查看容器端口绑定
docker port <container_id>
```

## 9. docker充当命令行工具

`docker compose`命令行工具

详见 `https://github.com/docker/compose/releases` 中的 `run.sh`工具。

运行 4.0版本的 mongoimport命令
  
```
mkdir -p dodo && chmod 777 dodo/ -R && cd dodo/

docker pull mongo:4.0

docker run --rm -v $(pwd):/workdir/ -w /workdir/ mongo:4.0 mongoexport --uri "<url>" --collection my_collection --out ./my_collection.bak
```

## 10. 宿主与容器传数据

```
# cp
docker cp container:/app/data ./
docker cp ./data container:/app/

# 管道
cat input.txt | docker exec -i tor-1 /bin/bash -c 'cat > /app/data.txt'

```

## 11. 中文乱码

`Dockerfile`增加 `ENV LANG C.UTF-8`

如果需要增加中文字体支持， 可以参考: [给Docker镜像(Debian)添加中文支持和中文字体](https://blog.llcat.tech/2018/12/03/add-zh-CN-locales-and-fonts-in-docker-images/)


## 12. 支持 `crontab`

容器中安装 `crontab`, `Dockerfile` 配置:

``` 
# add crontab
RUN apt-get -y install cron && \
    echo '*/10 * * * * date >> /date.log ' >> /etc/cron.d/hello-cron && \
    crontab /etc/cron.d/hello-cron && \
    rm -rf /var/lib/apt/lists/*

```

启动命令增加 `cron && ...`
