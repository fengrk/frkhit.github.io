---
layout: post
title:  python 代码提示
category: 技术
tags:  
    - python
keywords: 
description: 
---

# python 代码提示

## 1. 为无源码对象提供类型提示

在跨语言开发时, 返回的对象, 由于没有 python 源码, 无法提供代码提示.

这时, 可以定义一个假的对象, 声明其方法, 并标注类型, 帮助进行代码提示. 

```python
import unittest


class DemoObj:

    # noinspection PyPep8Naming
    def getName(self) -> str: ...

    # noinspection PyPep8Naming
    def doSomething(self, input_value: int) -> int: ...


class TestTypeHint(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def _get_unknown_obj(self):
        """ 模拟返回一个来自根据 so 构造的对象 """

        class X:
            def __init__(self):
                self.name = "X"

            def getName(self):
                return self.name

            def doSomething(self, input_value):
                return input_value * input_value

        return X()

    def testTypeHint(self):
        """ """
        obj: DemoObj = self._get_unknown_obj()
        print(obj.getName())
        print(obj.doSomething(input_value=10))

```

## 2. 获取 annotations

```python

def add(a: int, b: int) -> int:
    return a + b


print(add.__annotations__)
# {'a': <class 'int'>, 'b': <class 'int'>, 'return': <class 'int'>}
```