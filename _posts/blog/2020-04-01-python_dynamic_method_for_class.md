---
layout: post
title:  python 类和实例动态增加方法
category: 技术
tags:  
    - python
keywords: 
description: 
---

# python 类和实例动态增加方法

## 1. 类动态增加方法

```
class B(object):
    def __init__(self):
        self.b = self.__class__.__name__

    def print_b(self, ):
        print("self.b is {}".format(self.b))


if __name__ == '__main__':
    def f(self, ):
        new_b = 100
        print("I'm in f! Change self.b from {} to {}".format(self.b, new_b))
        self.b = new_b


    B.f = f

    print(B.f)
    print(B.print_b)

    b = B()
    b.f()
    b.print_b()

```

结果:

```
<function f at 0x10d918710>
<function B.print_b at 0x10d8d8680>
I'm in f! Change self.b from B to 100
self.b is 100

```

## 2. 类实例动态增加方法

```
import types


class A(object):
    def __init__(self, **kwargs):
        self.a = self.__class__.__name__
        self.f = kwargs.get("f")

    def do_f(self):
        if hasattr(self, "f"):
            if isinstance(self.f, str):
                print("self.f {}: type is str".format(self.f))
            elif callable(self.f):
                self.f()
            else:
                print("self.f {}: type is {}".format(self.f, type(self.f)))
        else:
            print("self.f not found!")

    def print_a(self, ):
        print("self.a is {}".format(self.a))


if __name__ == '__main__':
    print("before: ")
    a = A()
    a.do_f()
    a.print_a()

    # define
    def f(self, ):
        new_a = 100
        print("I'm in f! Change self.a from {} to {}".format(self.a, new_a))
        self.a = new_a


    a.f = types.MethodType(f, a)

    print("\n\nafter: ")
    a.do_f()
    a.print_a()


```

运行结果:

```
before: 
self.f None: type is <class 'NoneType'>
self.a is A


after: 
I'm in f! Change self.a from A to 100
self.a is 100
```