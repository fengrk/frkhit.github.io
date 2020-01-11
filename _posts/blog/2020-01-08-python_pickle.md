---
layout: post
title:  python pickle 实践
category: 技术
tags:   python, pickle
keywords: 
description: 
---

# python pickle 实践

## 魔术方法

pickle 提供了 `__getstate__` 和 `__setstate__` 两个魔术方法， 用于定制 pickle 过程。

利用这两个方法， 可以解决 不能 pickle 对象的 pickle 问题。

```
import threading


class UnPickleObj(object):
    def __init__(self,):
        # unpickle obj
        self.lock = threading.Lock()

        # pickle obj
        self.name = self.__class__.__name__

    def __getstate__(self):
        """ 持久化: """
        state = self.__dict__.copy()

        # 处理不能 pickle 的对象
        state["lock"] = None

        return state

    def __setstate__(self, state: dict):
        """ 反持久化 """
        # 还原不能 pickle 的对象
        state["lock"] = threading.Lock()

        # 还原 obj
        self.__dict__.update(state)

```

## 持久化到数据库中

可以使用通用方法， 现将 `pickle` 对象持久化后得到的 `bytes`, 转为 字符串， 再入库。

例如利用 `base64`库， 实现转换方法

```
import base64
import pickle

def ojb2str(obj: object) -> str:
    return base64.b64encode(pickle.dumps(obj)).decode("utf-8")

def str2obj(text:str) -> object:
    return pickle.loads(base64.b64decode(text.encode("utf-8")))

```

对于 `mongo`等数据库，可以存储为二进制类型。如：

```
import pickle
from bson.binary import Binary


def ojb2bin(obj: object) -> Binary:
    return Binary(pickle.dumps(obj))

def str2obj(bin: Binary) -> object:
    return pickle.loads(bin)

```

## 参考

- [pickle — Python object serialization](https://docs.python.org/3/library/pickle.html)