---
layout: post
title:  python 类型标注
category: 技术
tags:  
    - python
keywords: 
description: 
---

# python 类型标注

## 1. 基本用法

```
from typing import List, Dict, Callable, Tuple


def list_word() -> List[str]:
    return ["a", "b"]


def fix_max(cache: Dict[str, Tuple[float, float]], weight_func: Callable[[Tuple[float, float]], float]) -> str:
    """ """
    if not cache:
        return

    before_list = [(key, value) for key, value in cache.items()]
    sorted_list = sorted(before_list, key=lambda x: weight_func(x[1]), reverse=True)
    return sorted_list[0][0]


assert fix_max(cache={"A": (1, 2), "B": (1, 5), "C": (2, 2)}, weight_func=lambda x: 10 * x[0] + x[1]) == "C"

```

## 2. 别名

类型别名可用于简化复杂类型签名, 例如:

``` 
from typing import Dict, Tuple, Sequence

ConnectionOptions = Dict[str, str]
Address = Tuple[str, int]
Server = Tuple[Address, ConnectionOptions]

def broadcast_message(message: str, servers: Sequence[Server]) -> None:
    ...

# The static type checker will treat the previous type signature as
# being exactly equivalent to this one.
def broadcast_message(
        message: str,
        servers: Sequence[Tuple[Tuple[str, int], Dict[str, str]]]) -> None:
    ...
```


## 3. NewType

使用 NewType() 辅助函数创建不同的类型:

``` 
from typing import NewType

UserId = NewType('UserId', int)
some_id = UserId(524313)
```

## 4. Callable

期望特定签名的回调函数的框架可以将类型标注为 Callable[[Arg1Type, Arg2Type], ReturnType]。

``` 

def feeder(get_next_item: Callable[[], str]) -> None:
    # Body

def async_query(on_success: Callable[[int], None],
                on_error: Callable[[int, Exception], None]) -> None:
    # Body
```

通过用文字省略号替换类型提示中的参数列表： Callable[...，ReturnType]，可以声明可调用的返回类型，而无需指定调用签名。


## 5. 标注类和实例

``` 
from typing import Type


class A(object):
    pass


class B(A):
    pass


class C(A):
    pass


def get_a(a_cls: Type[A]) -> A:
    return a_cls()


```

## 参考

- [typing --- 类型标注支持](https://docs.python.org/zh-cn/3/library/typing.html)