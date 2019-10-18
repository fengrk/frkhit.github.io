---
layout: post
title:  spark 集群试用
category: 技术
tags:  spark, docker, python
keywords: 
description: 
---

# spark 集群使用

利用 `docker` 可以方便地搭建 `spark` 集群。 网上相关资源较少， 本文将分享作者的经验。

## 1. docker 搭建 spark集群

github 项目[mvillarrealb/docker-spark-cluster](https://github.com/mvillarrealb/docker-spark-cluster)， 提供了一个基于 docker 的 spark 集群搭建方案。

但有两个问题：

- 仅提供 Dockerfile 文件，国内环境创建 docker 时，速度非常慢
- 没有提供新手友好的入门实例，尤其是基于 python 的实例

本人在该项目基础上，完善入门实例，并将 docker 镜像发布到 docker hub 上。国内用户适用 docker 加速器，便可以很方便地将该项目运行起来。项目源码见[github: frkhit/docker-spark-cluster](https://github.com/frkhit/docker-spark-cluster)。


环境搭建教程：

- 克隆项目: `git clone git@github.com:frkhit/docker-spark-cluster.git`
- 进入项目目录，使用前, 请设置 docker 加速器， 具体可以参考[Docker Hub 镜像加速器](https://juejin.im/post/5cd2cf01f265da0374189441)
- 启动集群: `docker-compose down && docker-compose up -d`, 如果 docker-compose 没安装，可参考[docker-compose 安装方法](https://blog.arkfeng.xyz/2019/10/14/docker_compose_install.html)

访问 `http://localhost:8080/` 即可访问 spark 集群。 更详细的教程可以参考 `README.md` 文件。


## 2. 向 docker 集群提交 python 代码任务

项目中提供一个 python 任务样例 `data/spark-apps/test.py`， 具体代码如下：

```
# coding:utf-8

__author__ = 'rk.feng'

from pyspark import SparkContext, SparkConf

conf = SparkConf().set("spark.worker.cleanup.enabled", False)
sc = SparkContext(
    master="spark://spark-master:7077",
    appName="WordCount",
    environment={"PYSPARK_PYTHON": "python3"},
    conf=conf
)
lines = sc.textFile("/spark/README.md")
print("count of text is {}".format(lines.count()))
result = lines.flatMap(lambda x: x.split(" ")).countByValue()
for key, value in result.items():
    print("%s %i" % (key, value))

```

该任务用于统计spark 自带的`/spark/README.md` 文件的各个单词出现的次数。

任务提交的方法为， 在项目根目录下， 执行 `./crimes-app.sh`。

访问 `http://localhost:8080/` 可以看到执行情况。
