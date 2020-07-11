---
layout: post
title:  基于lua 脚本实现 redis 锁
category: 技术
tags:  
    - python
    - redis
    - lua
keywords: 
description: 
---

# 基于lua 脚本实现 redis 锁

本文演示如何实现一个基于 lua 脚本, 并支持超时的 redis 锁. 源码见[redis-lock](https://github.com/frkhit/docker-practice/tree/master/python/redis-lock).

锁的代码如下

```python
import logging
import os
import random
import time
import uuid

import redis


def redis_from_url(url: str, **kwargs) -> redis.Redis:
    if "decode_responses" not in kwargs:
        kwargs["decode_responses"] = True
    return redis.from_url(url=url, **kwargs)


class RedisLockV2(object):

    def __init__(self, name, redis_db: redis.Redis, key: str, expire: int):
        """
        :param redis_db:
        :param key:
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self._name = name
        self._redis = redis_db
        self._key = key
        self._expire = expire

        #
        self._identifier: str = None  # 获取到锁的标识

        # cache
        self._ttl_lua_instance = None

    @property
    def have_lock(self) -> bool:
        """ """
        return bool(self._identifier is not None)

    def set_lock_ttl(self, ttl: int) -> bool:
        """" """

        self.logger.debug("[name {}][extend_lock][lock {}][ttl {}]extending lock...".format(self._name, self._key, ttl))
        if self.have_lock:
            if self._ttl_lua_instance is None:
                ttl_script = """
                               if redis.call("get",KEYS[1]) == ARGV[1] then
                                   return redis.call("EXPIRE", KEYS[1], ARGV[2])
                               else
                                   return 0
                               end
                               """
                self._ttl_lua_instance = self._redis.register_script(ttl_script)
            result = self._ttl_lua_instance(keys=[self._key], args=[self._identifier, ttl])
            if result:
                return True

        return False

    def acquire_lock(self, ) -> bool:
        """
        基于 Redis 实现的分布式锁
        """
        self.logger.debug("[name {}][acquire_lock][lock {}]getting lock...".format(self._name, self._key))
        identifier = str(uuid.uuid4())
        lock_timeout = int(self._expire)

        if self._redis.set(self._key, identifier, ex=lock_timeout, nx=True):
            self._identifier = identifier
            self.logger.debug("[name {}][acquire_lock][lock {}][identifier {}]success to get lock!".format(self._name, self._key, identifier))
            return True

        self._identifier = None
        return False

    def release_lock(self) -> bool:
        """
        释放锁
        :return:
        """
        self.logger.debug("[name {}][release_lock][lock {}]releasing lock...".format(self._name, self._key))
        if not self._identifier:
            return False

        unlock_script = """
        if redis.call("get",KEYS[1]) == ARGV[1] then
            return redis.call("del",KEYS[1])
        else
            return 0
        end
        """
        unlock = self._redis.register_script(unlock_script)
        result = unlock(keys=[self._key], args=[self._identifier])

        if result:
            self.logger.debug(
                "[name {}][release_lock][lock {}][identifier {}]success to release lock!".format(self._name, self._key, self._identifier))

            # clean
            self._identifier = None

            return True
        else:
            self._identifier = None

            return False


```

演示代码:

```python


class LockDemo(object):
    def __init__(self):
        self._ttl = 2
        self.host_name = os.environ.get("HOSTNAME")
        self.redis_lock = RedisLockV2(name=self.host_name, redis_db=redis_from_url("redis://redis-stream:6379/0"), key="lock", expire=self._ttl)
        self._lock_file = None

    def acquire_lock(self):
        print("[name {}][acquire_lock]acquiring lock...".format(self.host_name))
        _time_start = time.time()
        while True:
            if self.redis_lock.acquire_lock():
                break
            time.sleep(0.1)
        print("[name {}][acquire_lock][identifier {}] waited {:.3f} seconds".format(self.host_name, self.redis_lock._identifier,  time.time() - _time_start))
        print("<lock status> <{}> got".format(self.host_name))

    def release_lock(self):
        success = self.redis_lock.release_lock()
        print("[name {}][release_lock] {} to release lock".format(self.host_name, "success" if success else "fail"))
        print("<lock status> <{}> release".format(self.host_name))

    def run(self):
        """ """
        while True:
            loss_lock = bool(random.random() > 0.8)
            self.acquire_lock()
            if loss_lock:
                time.sleep(self._ttl)
                print("[name {}]lock timeout!".format(self.host_name))
                time.sleep(self._ttl * 2)
            else:
                print("[name {}]doing sth...".format(self.host_name))
                for _ in range(int(self._ttl / 0.2)):
                    time.sleep(0.2)
                    success = self.redis_lock.set_lock_ttl(ttl=self._ttl)
                    if not success:
                        print("[name {}]fail to update ttl for lock!".format(self.host_name))
                print("[name {}]release lock!".format(self.host_name))
            self.release_lock()

            time.sleep(random.randint(max(1, self._ttl - 2), max(4, self._ttl + 2)))


if __name__ == '__main__':
    LockDemo().run()

```

使用 docker-compose 同时启动十个进程, 执行上述代码.

`docker-compose.yaml` 配置为:

``` 
version: '3.5'

networks:
    network-lock:
        driver: bridge

volumes:
    data-redis:

services:
    redis-stream:
        image: redis:5.0.7-buster
        container_name: redis-stream
        hostname: redis-stream
        restart: always
        ports:
            - "127.0.0.1:6379:6379"
        command: ["redis-server", "--appendonly", "yes"]
        volumes:
            - data-redis:/data
        networks:
            - network-lock
            
    py-server:
        build: .
        image: python:3.7.6-alpine-redis
        hostname: server-${SERVER_INDEX}
        command: ["python", "-u", "python_worker.py"]
        working_dir: /app
        depends_on:
          - redis-stream
        restart: always
        volumes:
            - ./:/app
        environment:
            TZ: Asia/Shanghai
        networks:
            - network-lock

```

docker 镜像 `python:3.7.6-alpine-redis`的 Dockerfile:

```
FROM python:3.7.6-alpine

RUN pip3 install redis

```

执行指令:

```
for i in $(seq 1 4); do
  SERVER_INDEX=$i docker-compose up -d --scale py-server=$i --no-recreate;
  # if not work, use command below
  # echo "SERVER_INDEX=${i}" > .env && SERVER_INDEX=$i docker-compose up -d --scale py-server=$i --no-recreate
done

```


通过 `docker-compose logs -f ` 可看到如下日志：

```
py-server_4     | [name server-4][acquire_lock]acquiring lock...
py-server_3     | [name server-3][acquire_lock]acquiring lock...
py-server_1     | [name server-1]release lock!
py-server_1     | [name server-1][release_lock] success to release lock
py-server_1     | <lock status> <server-1> release
py-server_3     | [name server-3][acquire_lock][identifier a8cf90a3-9ddc-4725-b029-a894ebb9e48c] waited 0.105 seconds
py-server_3     | <lock status> <server-3> got
py-server_3     | [name server-3]doing sth...
py-server_3     | [name server-3]release lock!
py-server_3     | [name server-3][release_lock] success to release lock
py-server_3     | <lock status> <server-3> release
py-server_2     | [name server-2][acquire_lock][identifier 038499c5-c7b7-4fc7-85d4-4f579acba352] waited 8.389 seconds
py-server_2     | <lock status> <server-2> got
py-server_2     | [name server-2]doing sth...
py-server_1     | [name server-1][acquire_lock]acquiring lock...
py-server_2     | [name server-2]release lock!
py-server_2     | [name server-2][release_lock] success to release lock
py-server_2     | <lock status> <server-2> release
py-server_1     | [name server-1][acquire_lock][identifier 8eb612e5-d8dc-4e15-8749-0c3df86dcafb] waited 0.207 seconds
py-server_1     | <lock status> <server-1> got
py-server_3     | [name server-3][acquire_lock]acquiring lock...
py-server_1     | [name server-1]lock timeout!
py-server_3     | [name server-3][acquire_lock][identifier 9d60daf1-55fe-4ffb-a19b-0b6e3df599fe] waited 1.145 seconds
py-server_3     | <lock status> <server-3> got
py-server_2     | [name server-2][acquire_lock]acquiring lock...
py-server_3     | [name server-3]lock timeout!
py-server_4     | [name server-4][acquire_lock][identifier b3c5b3df-6341-4d4c-aee5-21fcecc7ece5] waited 8.348 seconds
py-server_4     | <lock status> <server-4> got
py-server_4     | [name server-4]doing sth...
py-server_1     | [name server-1][release_lock] fail to release lock
py-server_1     | <lock status> <server-1> release
py-server_4     | [name server-4]release lock!
py-server_4     | [name server-4][release_lock] success to release lock
py-server_4     | <lock status> <server-4> release
py-server_2     | [name server-2][acquire_lock][identifier 1c5b0cc1-45fb-4aad-ac92-475cada80a6b] waited 2.183 seconds
py-server_2     | <lock status> <server-2> got
py-server_2     | [name server-2]doing sth...
py-server_1     | [name server-1][acquire_lock]acquiring lock...
py-server_3     | [name server-3][release_lock] fail to release lock
py-server_3     | <lock status> <server-3> release
py-server_2     | [name server-2]release lock!
py-server_2     | [name server-2][release_lock] success to release lock
py-server_2     | <lock status> <server-2> release
py-server_1     | [name server-1][acquire_lock][identifier 40e442bc-b50c-4ee4-bef2-dc2db0c6f993] waited 0.315 seconds
py-server_1     | <lock status> <server-1> got
py-server_1     | [name server-1]doing sth...
py-server_3     | [name server-3][acquire_lock]acquiring lock...
py-server_2     | [name server-2][acquire_lock]acquiring lock...
py-server_4     | [name server-4][acquire_lock]acquiring lock...
py-server_1     | [name server-1]release lock!
py-server_1     | [name server-1][release_lock] success to release lock
py-server_1     | <lock status> <server-1> release
py-server_3     | [name server-3][acquire_lock][identifier 7db7e437-e469-4a0c-aaa7-176082be8a09] waited 1.357 seconds
py-server_3     | <lock status> <server-3> got
py-server_3     | [name server-3]doing sth...
py-server_1     | [name server-1][acquire_lock]acquiring lock...
py-server_3     | [name server-3]release lock!
py-server_3     | [name server-3][release_lock] success to release lock
py-server_3     | <lock status> <server-3> release
py-server_2     | [name server-2][acquire_lock][identifier d9763bdb-8fdf-47b0-81b5-fadb7ba9eafa] waited 3.203 seconds
py-server_2     | <lock status> <server-2> got
py-server_1     | [name server-1][acquire_lock][identifier af676488-84ee-43c9-8e49-37db0ad6fa17] waited 2.059 seconds
py-server_1     | <lock status> <server-1> got
py-server_2     | [name server-2]lock timeout!
py-server_3     | [name server-3][acquire_lock]acquiring lock...
py-server_1     | [name server-1]lock timeout!
py-server_3     | [name server-3][acquire_lock][identifier 18fd6dc4-8226-420a-8fd0-3419f046fdff] waited 1.141 seconds
py-server_3     | <lock status> <server-3> got
py-server_3     | [name server-3]doing sth...
py-server_2     | [name server-2][release_lock] fail to release lock
py-server_2     | <lock status> <server-2> release
py-server_3     | [name server-3]release lock!
py-server_3     | [name server-3][release_lock] success to release lock
py-server_3     | <lock status> <server-3> release
py-server_4     | [name server-4][acquire_lock][identifier cceb2740-9b81-41f7-ac71-37b70237ee8c] waited 8.537 seconds
py-server_4     | <lock status> <server-4> got
py-server_4     | [name server-4]doing sth...
py-server_2     | [name server-2][acquire_lock]acquiring lock...
py-server_1     | [name server-1][release_lock] fail to release lock
py-server_1     | <lock status> <server-1> release
py-server_4     | [name server-4]release lock!
py-server_4     | [name server-4][release_lock] success to release lock
py-server_4     | <lock status> <server-4> release
py-server_2     | [name server-2][acquire_lock][identifier 9860e5fb-288f-44a5-9343-f6b8eed914cd] waited 0.310 seconds
py-server_2     | <lock status> <server-2> got
py-server_3     | [name server-3][acquire_lock]acquiring lock...
py-server_4     | [name server-4][acquire_lock]acquiring lock...
py-server_2     | [name server-2]lock timeout!
py-server_3     | [name server-3][acquire_lock][identifier 00bfbfda-9807-4e49-8dae-cd5f5cd69319] waited 1.152 seconds
py-server_3     | <lock status> <server-3> got
py-server_3     | [name server-3]doing sth...
py-server_1     | [name server-1][acquire_lock]acquiring lock...
py-server_3     | [name server-3]release lock!
py-server_3     | [name server-3][release_lock] success to release lock
py-server_3     | <lock status> <server-3> release
py-server_4     | [name server-4][acquire_lock][identifier a017ed5d-cd13-44de-9ae2-6f47fdb0e68c] waited 2.172 seconds
py-server_4     | <lock status> <server-4> got
py-server_4     | [name server-4]doing sth...
py-server_2     | [name server-2][release_lock] fail to release lock
py-server_2     | <lock status> <server-2> release
py-server_4     | [name server-4]release lock!
py-server_4     | [name server-4][release_lock] success to release lock
py-server_4     | <lock status> <server-4> release
py-server_1     | [name server-1][acquire_lock][identifier 59ff0d1b-d381-4d1d-89e8-5a30e0132acc] waited 2.471 seconds
py-server_1     | <lock status> <server-1> got
py-server_1     | [name server-1]doing sth...
py-server_3     | [name server-3][acquire_lock]acquiring lock...
py-server_1     | [name server-1]release lock!
py-server_1     | [name server-1][release_lock] success to release lock
py-server_1     | <lock status> <server-1> release
py-server_3     | [name server-3][acquire_lock][identifier 88ee4487-5978-4610-af60-c40ae1072ed1] waited 1.139 seconds
py-server_3     | <lock status> <server-3> got
py-server_3     | [name server-3]doing sth...
py-server_4     | [name server-4][acquire_lock]acquiring lock...
py-server_2     | [name server-2][acquire_lock]acquiring lock...
py-server_3     | [name server-3]release lock!
py-server_3     | [name server-3][release_lock] success to release lock
py-server_3     | <lock status> <server-3> release
py-server_4     | [name server-4][acquire_lock][identifier 800a2a8b-70ad-4abb-b8bb-c59e787bdc22] waited 1.127 seconds
py-server_4     | <lock status> <server-4> got
py-server_4     | [name server-4]doing sth...
py-server_1     | [name server-1][acquire_lock]acquiring lock...
py-server_3     | [name server-3][acquire_lock]acquiring lock...
py-server_4     | [name server-4]release lock!
py-server_4     | [name server-4][release_lock] success to release lock
py-server_4     | <lock status> <server-4> release
py-server_1     | [name server-1][acquire_lock][identifier 776fd937-6a31-44ed-9acc-b85e3bd3d5a4] waited 1.142 seconds
py-server_1     | <lock status> <server-1> got
py-server_1     | [name server-1]doing sth...
py-server_4     | [name server-4][acquire_lock]acquiring lock...
py-server_1     | [name server-1]release lock!
py-server_1     | [name server-1][release_lock] success to release lock
py-server_1     | <lock status> <server-1> release

```

日志中, 可能出现 `A成功获取锁, B成功获取锁, A成功释放锁` 的情形, 这是因为输入日志时的时间误差引起的.
