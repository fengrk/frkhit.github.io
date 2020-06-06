---
layout: post
title:  python 元编程
category: 技术
tags:  
    - python
    - 元编程
keywords: 
description: 
---

# python 元编程

## 1. `type` 可用于创建类

```python

import unittest


class TestMetaClass(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def testType(self):
        """ type 含义 """

        class A(dict):
            some_info = "info"

            def echo(self, name):
                return "name is: {}".format(name)

        def create_A_class():
            return type(
                "A",
                (dict,),
                dict(some_info="info", echo=lambda self, name: "name is: {}".format(name))
            )

        # A class by hand
        self.assertTrue(type(A), type)
        print(A)
        info_class_1 = A.some_info
        a_1 = A()
        info_instance_1 = a_1.some_info
        name_1 = a_1.echo(name="A")

        # A class by type
        NewA = create_A_class()
        print(NewA)
        info_class_2 = NewA.some_info
        a_2 = NewA()
        info_instance_2 = a_2.some_info
        name_2 = a_2.echo(name="A")

        # 两个类相等
        self.assertEqual(info_class_1, info_class_2)
        self.assertEqual(info_instance_1, info_instance_2)
        self.assertEqual(name_1, name_2)

```

`type` 基本用法:

```python

class type(object):
    """
    type(object_or_name, bases, dict)
    type(object) -> the object's type
    type(name, bases, dict) -> a new type
    """
    ...
```

## 2. `metaclass` 基本原理

[python官网文档](https://docs.python.org/zh-cn/3/reference/datamodel.html#customizing-class-creation), 描述了 类的创建过程.

默认情况下，类是使用 `type()` 来构建的。

类体会在一个新的命名空间内执行，类名会被局部绑定到 `type(name, bases, namespace)` 的结果。

类创建过程可通过在定义行传入 `metaclass` 关键字参数，或是通过继承一个包含此参数的现有类来进行定制。

在以下示例中，`MyClass` 和 `MySubclass` 都是 `Meta` 的实例:

```python

class Meta(type):
    pass

class MyClass(metaclass=Meta):
    pass

class MySubclass(MyClass):
    pass

```

*注意: `metaclass` 是 `type` 的子类*

在类定义内指定的任何其他关键字参数都会在下面所描述的所有元类操作中进行传递。

当一个类定义被执行时，将发生以下步骤:

- 解析 MRO 条目
- 确定适当的元类
- 准备类命名空间
- 执行类主体
- 创建类对象

## 3. `metaclass` 的 `__call__` 方法


以 python cookbook 中例子为例:

```python

class NoInstances(type):
    def __call__(self, *args, **kwargs):
        raise TypeError("Can't instantiate directly")


class Spam(metaclass=NoInstances):
    @staticmethod
    def grok(x):
        print('Spam.grok')  

print(Spam.grok(42))  # Spam.grok

Spam()  # raise TypeError

```

`NoInstances` 是一个禁止 类执行 `__init__` 的元类.

简单解析其原理:

首先, 类定义的方法 `__call__` 是 其实例 `instance` 执行 `instance()` 时调用的. 

在本例中, `Spam` 是 `NoInstances`  的实例, 因为
 
`Spam = NoInstances("Spam", (), dict(grok=...))`.

当 `Spam()` 时, 会调用 `NoInstances` 的 `__call__` 方法.


## 4. `metaclass` 实现单例模式

```python

class Singleton(type):
    def __init__(self, *args, **kwargs):
        self.__instance = None
        super().__init__(*args, **kwargs)
    
    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance

# Example
class Spam(metaclass=Singleton):
    def __init__(self):
        print('Creating Spam')  


assert Spam() is Spam()

```


## 5. `metaclass` 缓存实例

```python

import weakref


class Cached(type):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__cache = weakref.WeakValueDictionary()

    def __call__(self, *args):
        if args in self.__cache:
            return self.__cache[args]
        else:
            obj = super().__call__(*args)
            self.__cache[args] = obj
        return obj

# Example
class Spam(metaclass=Cached):
    def __init__(self, name):
        print('Creating Spam({!r})'.format(name))
        self.name = name
```





