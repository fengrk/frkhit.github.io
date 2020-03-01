---
layout: post
title:  celery笔记
category: 技术
tags:  
    - python
    - docker
    - celery
keywords: 
description: 
---

# celery笔记

完整代码见[celery-learning](https://github.com/frkhit/celery-learning)

## 1. redis 优先级实现

该示例，主要参考[Tendrid/celery-redis-priority-test](https://github.com/Tendrid/celery-redis-priority-test).

celery app 配置示例：

```
from time import sleep

from celery import Celery
from kombu import Queue

app_name = "redis-priority"
app = Celery(app_name)

app.conf.result_backend = app.conf.broker_url = "redis://redis-stream:6379/1"

app.conf.task_default_queue = "b-medium"

app.conf.task_create_missing_queues = True

# app.conf.task_default_priority = 3

app.conf.broker_transport_options = {"queue_order_strategy": "sorted"}

app.conf.worker_prefetch_multiplier = 1

app.conf.task_inherit_parent_priority = True

# app.conf.broker_transport_options = {
#    'priority_steps': list(range(10)),
# }

app.conf.task_queues = (
    Queue("a-high"),
    Queue("b-medium"),
    Queue("c-low"),
)

app.conf.task_routes = {
    'celery_proj.other_apps.redis_priority.low_priority_wait': {
        'queue': 'c-low',
        'routing_key': 'c-low.priority',
    },
    'celery_proj.other_apps.redis_priority.high_priority_wait': {
        'queue': 'a-high',
        'routing_key': 'a-high.priority',
    },
}

sleep_seconds = 0.1


def _wait(*args, **kwargs):
    if not kwargs:
        for a in args:
            if type(a) is dict:
                kwargs = a
    print(kwargs.get("fixture_name"))
    sleep(sleep_seconds)
    return kwargs.get("fixture_name", "UNKNOWN")


@app.task
def wait(*args, **kwargs):
    return _wait(*args, **kwargs)


@app.task
def low_priority_wait(*args, **kwargs):
    return _wait(*args, **kwargs)


@app.task
def high_priority_wait(*args, **kwargs):
    return _wait(*args, **kwargs)

```

worker 启动：

```
celery -A celery_proj.other_apps.redis_priority \
    -n celery-worker -Q a-high,b-medium,c-low \
    -Ofair -c1 --prefetch-multiplier=1
```

调用优先级任务示例：

```
task = {"priority": 0, "fixture_name": "A", "queue": "a-high"}
signiture = wait.s(**task)
result = signiture.apply_async(priority=task["priority"], queue=task["queue"])
print("result is {}".format(result.get()))
```

运行例子：

```
docker-compose -f docker-compose-redis-priority.yml up
```

测试结果：

![celery redis 优先级测试结果](../../../../public/img/celery_learning_note/screenshot.png)
