---
layout: post
title: python if 判断
category: 技术
tags:  
    - python
keywords: 
description: 
---

# python if 判断


## 1. 背景

最近, 在使用 `if` 进行条件判断时, 遇到一个坑. 从而引发我对 `if` 使用的一些思考.

看一段demo代码:

```
import logging
import os
import pickle

from pybloom import BloomFilter


def load_bloom_filter(logger: logging.Logger, bloom_filter_file: str) -> BloomFilter:
    """  """
    logger.info("load_bloom_filter: {}".format(bloom_filter_file))
    if not bloom_filter_file:
        return

    # load bloom filter obj
    if os.path.exists(bloom_filter_file):
        try:
            with open(bloom_filter_file, "rb") as f:
                bloom_obj = pickle.load(f)

            if bloom_obj:
                return bloom_obj

        except Exception as e:
            logger.error(e, exc_info=True)
    else:
        logger.warning("bloom filter file not found: {}".format(bloom_filter_file))

    bloom_obj = BloomFilter(capacity=10000 * 10000, error_rate=0.001)
    dump_bloom_filter(logger=logger, bloom_filter=bloom_obj, bloom_filter_file=bloom_filter_file)
    return bloom_obj


def dump_bloom_filter(logger: logging.Logger, bloom_filter: BloomFilter, bloom_filter_file: str):
    """ """
    logger.info("dump_bloom_filter: {}".format(bloom_filter_file))
    if not bloom_filter_file:
        return

    with open(bloom_filter_file, "wb") as f:
        pickle.dump(bloom_filter, f)

    logger.info("success to dump bloom filter to file: {}".format(bloom_filter_file))


def demo():
    bloom_filter_file = "./abc.pkl"
    if os.path.exists(bloom_filter_file):
        os.remove(bloom_filter_file)

    for _ in range(5):
        load_bloom_filter(logger=logging, bloom_filter_file=bloom_filter_file)


if __name__ == '__main__':
    demo()

```

在这段代码中, 我使用 [python-bloomfilter](https://github.com/jaybaird/python-bloomfilter) 对数据进行去重处理.

在执行`demo()` 时, 日志中出现 5 次  `success to dump bloom filter to file: ./abc.pkl`, 即新建 5 次 bloom_filter 对象.

按照逻辑, 理论上只会在第 1 次新建对象, 后面 4 次应该是直接从文件中加载 `bloom_obj`. 

## 2. 解决问题

demo 处的代码非常简单, 问题就出在代码块:

```
    if bloom_obj:
        return bloom_obj
```

`bloom_obj` 作为一个类的实例, 为什么条件 `if bloom_obj` 不成立?  `if <class_instance>` , 调用了类的哪个方法?

通过打断点调试, 发现 `if bloom_obj`, 进入到 `BloomFilter` 类的 `__len__(self):` 方法中. 

```
class BloomFilter(object):

    def __len__(self):
        """Return the number of keys stored by this bloom filter."""
        return self.count

```

由于空的 `bloom_obj`, `self.count` 为 0, 所以`if bloom_obj` 不成立.

## 3. 思考

`if <class_instance>` 单纯根据 `__len__` 判断吗? 

如果类没有`__len__` 方法, 会有什么结果?

在文章 [Python 中一些特殊方法的自定义及作用](https://toutiao.io/posts/mpbxjd/preview) 找到了答案:

```
像if v/if not v等，python会调用bool(v)方法，而bool(v)背后的调用时尝试调用 v.__bool__(),如果没有__bool__方法，就会尝试调用__len__方法，若这是返回0则 是False否则为True,这两个方法都没有的话只能按照默认处理了
```
