---
layout: post
title:  python内存泄漏测试示例
category: 技术
tags:  
    - python
keywords: 
description: 
---

# python内存泄漏测试示例


## 1. 测试代码

测试代码：

```

import gc
import os
import time
import weakref

import psutil


class A(object):
    def __init__(self, b):
        self._cache = [i + time.time() for i in range(10000)]
        self.b = b


class B(object):
    def __init__(self, name):
        self.name = name
        self._a = A(b=self)


class BWeakRef(object):
    def __init__(self, name):
        self.name = name
        self._a = A(b=weakref.proxy(self))


class MemoryCheckTool(object):
    def __init__(self):
        self._pid: int = None
        self._global_cache = []

    @property
    def pid(self) -> int:
        if self._pid is None:
            self._pid = int(os.getpid())
        return self._pid

    def get_current_memory(self) -> str:
        """ """
        process = psutil.Process(self.pid)
        return '%8.2fMB' % (process.memory_info().rss / 1024 / 1024)

    def check(self, func: callable, ) -> dict:
        """ """
        result = {}
        for trigger_gc in [False, True]:
            info = "With{} GC".format("" if trigger_gc else "out")
            result[info] = []
            self._global_cache.clear()
            for _ in range(10):
                _cur_memory = self.get_current_memory()
                result[info].append(_cur_memory)
                func()
                time.sleep(0.1)
                if trigger_gc:
                    gc.collect()

        return result

    def test_reference(self):
        b_list = []
        for index in range(100):
            b_list.append(B(name="A-{}-{}".format(index, time.time())))

    def test_weakref(self):
        b_list = []
        for index in range(100):
            b_list.append(BWeakRef(name="A-{}-{}".format(index, time.time())))

    def test_global_cache(self):
        b_list = []
        for index in range(100):
            b_list.append(B(name="A-{}-{}".format(index, time.time())))
        self._global_cache.extend(b_list)

    def run(self):
        """ 批量测试 """
        for func, desc in [(self.test_reference, "循环引用"), (self.test_weakref, "循环引用:弱引用"), (self.test_global_cache, "全局引用")]:
            self._global_cache.clear()
            gc.collect()
            result = self.check(func=func)

            log_list = ["{}\n".format(desc)]
            key_list = list(result.keys())
            key_list.sort()
            log_list.append("{}\t\t{}".format(key_list[0], key_list[1]))
            for _result_1, _result_2 in zip(result[key_list[0]], result[key_list[1]]):
                log_list.append("{}\t\t{}".format(_result_1, _result_2))

            print("\n\n" + "\n".join(log_list))


if __name__ == '__main__':
    tool = MemoryCheckTool()
    tool.run()

```

## 2. 结果分析

交叉引用：内存释放变慢

```

交叉引用

With GC		Without GC
  135.96MB		   25.62MB
   28.09MB		   64.55MB
   28.09MB		   64.09MB
   28.09MB		  103.04MB
   28.09MB		   76.63MB
   27.84MB		   78.20MB
   27.84MB		  117.04MB
   27.84MB		  107.74MB
   27.84MB		  146.58MB
   27.84MB		  126.39MB

```

使用弱引用可以加速内存释放：

```

交叉引用:弱引用

With GC		Without GC
   29.32MB		   27.60MB
   27.85MB		   29.07MB
   27.85MB		   29.32MB
   27.85MB		   29.32MB
   27.85MB		   29.32MB
   27.85MB		   29.32MB
   27.85MB		   29.32MB
   27.85MB		   29.32MB
   27.85MB		   29.32MB
   27.85MB		   29.32MB

```

对象被引用，内存无法释放：

```
全局引用

With GC		Without GC
  414.26MB		   27.10MB
   69.50MB		   64.29MB
  103.28MB		  103.16MB
  142.13MB		  142.03MB
  180.99MB		  180.90MB
  219.85MB		  219.76MB
  258.72MB		  258.63MB
  297.58MB		  297.56MB
  336.45MB		  336.52MB
  375.32MB		  375.39MB

```