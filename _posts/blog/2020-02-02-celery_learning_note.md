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


## 2. task 加 装饰符

有些python调度器, 如 `apscheduler`, 在任务函数上增加装饰符, 会导致方法找不到的错误. 

实践证明, celery 的 task 函数可以增加装饰符. 示例源码见[celery-learning](https://github.com/frkhit/celery-learning/tree/task_decorator).


装饰符方法示例

``` 
import functools
import time

def simple_log(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        time_start = time.time()
        try:
            result = func(*args, **kw)
            print('call {}, time_cost {:.2f}, success True'.format(func.__name__, time.time() - time_start))
            return result
        except:
            print('call {}, time_cost {:.2f}, success False'.format(func.__name__, time.time() - time_start))
            raise

    return wrapper
``` 

tasks 上使用装饰符:

```
import time

from celery_proj.app import celery_app
from libs.demo_utils import demo_add, simple_log


@celery_app.task
@simple_log
def demo_sum(a: float, b: float, c: float) -> float:
    time.sleep(5)
    _result = demo_add(demo_add(a, b), c)
    print("demo_sum: a {}, b {}, c {} => {}".format(a, b, c, _result))
    return _result


@celery_app.task
@simple_log
def demo_func(a: float, b: float) -> float:
    time.sleep(1)
    _result = a * 2 + b * b
    print("demo_func: a {}, b {} => {}".format(a, b, _result))
    return _result

```

运行示例:

``` 
docker-compose up -d
```

结果示例如下, 证实装饰符的使用不会影响 celery task 的执行.

![celery task 装饰符测试结果](../../../../public/img/celery_learning_note/task-decorator.png)
