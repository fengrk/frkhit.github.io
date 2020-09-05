---
layout: post
title:  python 动态加载所有子类
category: 技术
tags:  
    - python
keywords: 
description: 
---

# python 动态加载所有子类

python 类提供 `__subclass__` 方法, 可用于获取所有子类列表. 同时, 提供 `issubclass`, 判断一个类是否是另一个类的子类.

## 1. `__subclass__` 使用示例 

使用方法见示例:

```python

import unittest


class TestSubClass(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def testSubClass(self):
        """ """

        class A(object):
            pass

        class B(A):
            pass

        class C(A):
            pass

        for sub_class in A.__subclasses__():
            print(sub_class)
            self.assertTrue(issubclass(sub_class, A))

        # <class 'x.TestSubClass.testSubClass.<locals>.B'>
        # <class 'x.TestSubClass.testSubClass.<locals>.C'>

    def testSubClassV2(self):
        """ """

        class A(object):
            pass

        class B(A):
            pass

        class C(B):
            pass

        self.assertEqual(len(A.__subclasses__()), 1)
        self.assertEqual(len(B.__subclasses__()), 1)

        self.assertTrue(issubclass(B, A))
        self.assertTrue(issubclass(C, B))
        self.assertTrue(issubclass(C, A))

```

## 2. 使用 `__subclass__` 及 `importlib` 动态加载基类的所有实现类

示例:

```python

import glob
import importlib.util
import os
import shutil
import sys
import unittest
from collections import OrderedDict


class TestDynamicImport(unittest.TestCase):
    def setUp(self) -> None:
        self.script_dir: str = os.path.abspath("./script")

        self.prepare_scripts()

    def prepare_scripts(self):
        """ """

        def _create_script(_class_name: str, _script_file: str):
            content = """
from collections import OrderedDict

class {class_name}(OrderedDict):
    pass
            """.format(class_name=_class_name)
            with open(_script_file, "w") as f:
                f.write(content)

        if os.path.exists(self.script_dir):
            shutil.rmtree(self.script_dir)

        os.makedirs(self.script_dir, exist_ok=True)

        # create SB
        _create_script(_class_name="SB", _script_file=os.path.join(self.script_dir, "sb.py"))

        # create SC
        _create_script(_class_name="SC", _script_file=os.path.join(self.script_dir, "sc.py"))

    def testDynamicImport(self):
        """ """
        # 加载所有脚本
        py_file_list = [py_file for py_file in glob.glob("{}/*.py".format(os.path.abspath(self.script_dir).rstrip("/")))]
        print("{} script found!".format(len(py_file_list)))

        for py_file in py_file_list:
            script_module_name = "scripts.{}".format(os.path.basename(py_file)[:-len(".py")])
            spec = importlib.util.spec_from_file_location(script_module_name, py_file)
            script_module = importlib.util.module_from_spec(spec)
            sys.modules[script_module_name] = script_module
            spec.loader.exec_module(script_module)

        # 获取所有脚本类
        for sub_class in OrderedDict.__subclasses__():
            print(sub_class)
            self.assertTrue(issubclass(sub_class, OrderedDict))

        # <class 'scripts.sb.SB'>
        # <class 'scripts.sc.SC'>           
```