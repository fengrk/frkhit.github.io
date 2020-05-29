---
layout: post
title:  python 文件锁
category: 技术
tags:  
    - python
keywords: 
description: 
---

# python 文件锁

# python 文件锁

python 中实现进程级别的全局锁, 一般可以借助 redis 实现. 

其实, python 在 linux 系统下, 提供了一种基于 `fcntl`库实现的文件锁. 

演示代码如下:

```python
import fcntl
import os
import time


class LockDemo(object):
    def __init__(self):
        self.host_name = os.environ.get("HOSTNAME")
        self._lock_file = None

    def acquire_lock(self):
        print("[name {}][acquire_lock]acquiring lock...".format(self.host_name))
        if self._lock_file is None:
            self._lock_file = open("/app/lock.file.log", "a+")
        _time_start = time.time()
        fcntl.flock(self._lock_file.fileno(), fcntl.LOCK_EX)
        print("[name {}][acquire_lock] waited {:.3f} seconds".format(self.host_name, time.time() - _time_start))

    def release_lock(self):
        try:
            if self._lock_file:
                self._lock_file.close()
                self._lock_file = None
        except Exception as e:
            print("[name {}][release_lock]error is {}".format(self.host_name, e))

        print("[name {}][release_lock] success to release lock".format(self.host_name))

    def run(self):
        """ """
        while True:
            self.acquire_lock()
            time.sleep(1)
            print("[name {}]doing sth...".format(self.host_name))
            self.release_lock()


if __name__ == '__main__':
    LockDemo().run()

```

使用 docker-compose 同时启动十个进程, 执行上述代码.

`docker-compose.yaml` 配置为:

``` 
version: '3.5'
services:
    py-server:
        image: python:3.7.6-alpine
        hostname: server-${SERVER_INDEX}
        command: ["python", "-u", "python_worker.py"]
        working_dir: /app
        restart: always
        volumes:
            - ./:/app
        environment:
            TZ: Asia/Shanghai

```

执行指令:

```
echo -n ./lock.file.log

for i in $(seq 1 10); do
  SERVER_INDEX=$i docker-compose up -d --scale py-server=$i --no-recreate;
  # if not work, use command below
  # echo "SERVER_INDEX=${i}" > .env && SERVER_INDEX=$i docker-compose up -d --scale py-server=$i --no-recreate
done

```


通过 `docker-compose logs -f ` 可看到如下日志：

```
py-server_2  | [name server-2][release_lock] success to release lock
py-server_2  | [name server-2][acquire_lock]acquiring lock...
py-server_8  | [name server-8]doing sth...
py-server_8  | [name server-8][release_lock] success to release lock
py-server_8  | [name server-8][acquire_lock]acquiring lock...
py-server_4  | [name server-4][acquire_lock] waited 2.005 seconds
py-server_4  | [name server-4]doing sth...
py-server_4  | [name server-4][release_lock] success to release lock
py-server_4  | [name server-4][acquire_lock]acquiring lock...
py-server_9  | [name server-9][acquire_lock] waited 10.051 seconds
py-server_9  | [name server-9]doing sth...
py-server_9  | [name server-9][release_lock] success to release lock
py-server_9  | [name server-9][acquire_lock]acquiring lock...
py-server_8  | [name server-8][acquire_lock] waited 2.002 seconds
py-server_8  | [name server-8]doing sth...
py-server_8  | [name server-8][release_lock] success to release lock
py-server_8  | [name server-8][acquire_lock]acquiring lock...
py-server_4  | [name server-4][acquire_lock] waited 2.012 seconds
py-server_6  | [name server-6][acquire_lock] waited 9.052 seconds
py-server_4  | [name server-4]doing sth...
py-server_4  | [name server-4][release_lock] success to release lock
py-server_4  | [name server-4][acquire_lock]acquiring lock...
py-server_6  | [name server-6]doing sth...
py-server_2  | [name server-2][acquire_lock] waited 6.031 seconds
py-server_6  | [name server-6][release_lock] success to release lock
py-server_6  | [name server-6][acquire_lock]acquiring lock...
py-server_4  | [name server-4][acquire_lock] waited 2.007 seconds
py-server_2  | [name server-2]doing sth...

```

可清楚看到, 多个进程间, 争抢互斥锁. 没争到锁的进程, 一直在阻塞.

