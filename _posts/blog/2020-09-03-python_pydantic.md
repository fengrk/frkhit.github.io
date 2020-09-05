---
layout: post
title:  pydantic 使用初探
category: 技术
tags:  
    - python
keywords: 
description: 
---

# pydantic 使用初探

借助 `pydantic` 库, 定义好接口参数模型后, 可以自动进行参数校验, 自动生成接口文档. 

`pydantic` 官方简介:

```
Data validation and settings management using Python type hinting.

Fast and extensible, pydantic plays nicely with your linters/IDE/brain. Define how data should be in pure, canonical Python 3.6+; validate it with pydantic.
```

## 1. 基本使用方法

```python

import unittest
from pydantic import Field, BaseModel


class BA(BaseModel):
    a: int = Field(description="int...")


class BB(BA):
    b: str = Field(description="string...")


class TestPyDantic(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def testSchemaJson(self):
        """ """
        print(BA.schema_json())
        print(BB.schema_json())

    def testDynamicTypeHint(self, ):
        """ 测试动态代码提示 """

        class JA(object):
            BASE = BA

            def __init__(self, **kwargs):
                """ """
                self._params = self.BASE(**kwargs)

            @property
            def params(self) -> BA:
                return self._params

            def aaa(self):
                """ """
                print(type(self.params.a), self.params.a)

        class JB(JA):
            BASE = BB

            @property
            def params(self) -> BB:
                return self._params

            def bbb(self):
                """ """
                print(type(self.params.a), self.params.a)
                print(type(self.params.b), self.params.b)

        # 输入配置

        # 动态
        JA(a="10").aaa()
        JB(a=10, b="b").bbb()

```
