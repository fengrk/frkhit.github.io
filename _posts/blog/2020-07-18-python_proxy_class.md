---
layout: post
title:  python __getattribute__ 和 __setattr__ 使用研究
category: 技术
tags:  
    - python
keywords: 
description: 
---

# python __getattribute__ 和 __setattr__ 使用研究

文章 [python 中__setattr__, __getattr__,__getattribute__, __call__使用方法](https://www.cnblogs.com/huchong/p/8287799.html) 详细讲解了 `__getattribute__` 和 `__setattr__`的使用方法.

本文通过一个实例, 加深对该魔术方法的理解.

虚拟场景: 

假设有一个 python RealObj类, 提供丰富的功能接口. 

唯一的缺陷是, 该类初始化时, 非常耗资源. 

使用的时候发现, 大多数情况下, 只使用该类的 `do_job` 方法; 另外比较特殊的是, 仅使用 `do_job` 方法时, 可以使用另一更省资源方式实现.

问题: 如何在提供一个新的 `ProxyRealObj` 类, 既完全实现 `RealObj` 所有方法, 又能尽量节省运算资源 ? 

*注意: 这是一个有偏向性的问题*

本示例, 使用文章开头提到的两个魔术方法, 提供一种简陋的实现.

```python
import time
import unittest


class RealObj(object):
    def __init__(self, name: str):
        """ 初始化时, 耗资源 """
        self._name = name
        self.info = None

        self._init_info()

    def _init_info(self):
        """ init """
        time.sleep(2)  # slowly
        self.info = "info: class {}, name {}".format(type(self), self._name)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self._init_info()

    def do_job(self):
        """ """
        time.sleep(1)  # slowly
        print("job done!")


class ProxyRealObj(object):
    """ 实现 RealObj 的所有方法和属性;
        但可以在一些方法上, 使用其他方法, 加速运行
    """

    def __init__(self, name):
        self._real_obj: RealObj = None
        self._name = name

    def __setattr__(self, key, value):
        if key not in ("_real_obj", "_name") and not self.__dict__["_real_obj"]:
            setattr(self.__dict__["_real_obj"], key, value)
            return

        self.__dict__[key] = value
        if key == "name":
            self.__dict__["_name"] = value
            self.__dict__["_real_obj"] = None

    def __getattribute__(self, key):
        if key not in ("_real_obj", "_name", "__dict__", "do_job"):
            if not self.__dict__["_real_obj"]:
                self.__dict__["_real_obj"] = RealObj(name=self.__dict__["_name"])

            return getattr(self.__dict__["_real_obj"], key)

        return super(ProxyRealObj, self).__getattribute__(key)

    def do_job(self):
        """ """
        if self._real_obj is None:
            time.sleep(0.1)  # quickly
            print("job done!")
            return

        return self._real_obj.do_job()


class TestRealObj(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def testEqual(self):
        """ """
        name = "name_1"
        real_obj = RealObj(name=name)
        proxy_real_obj = ProxyRealObj(name=name)

        # proxy_real_obj not init real_obj
        time_start = time.time()
        proxy_real_obj.do_job()
        proxy_time_cost = time.time() - time_start
        print(proxy_time_cost)
        self.assertTrue(abs(proxy_time_cost - 0.1) < 1e-2)

        time_start = time.time()
        real_obj.do_job()
        time_cost = time.time() - time_start
        print(time_cost)
        self.assertTrue(abs(time_cost - 1) < 1e-2)

        # var
        self.assertEqual(real_obj.name, proxy_real_obj.name)
        self.assertEqual(real_obj.info, proxy_real_obj.info)
        real_obj.name = proxy_real_obj.name = "name_2"
        self.assertEqual(real_obj.name, proxy_real_obj.name)
        self.assertEqual(real_obj.info, proxy_real_obj.info)

        # time_cost
        time_start = time.time()
        proxy_real_obj.do_job()
        proxy_time_cost = time.time() - time_start
        self.assertTrue(abs(proxy_time_cost - 1) < 1e-2)

```

要点:
- `self.` 点操作, 一定触发 `__getattribute__` 方法. `__getattribute__` 尽量避免使用点操作, 容器引起死循环.
- 赋值操作触发 `__setattr__`
