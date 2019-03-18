---
layout: post
title: mongo学习笔记
category: 技术
tags: mongo
keywords: 
description: 
---

# mongo学习笔记

## 1.聚合操作

### 1.1 获取列表元素集合

keywords: group, unwind, aggregate

举例,有如下数据:
```
{"_id": "1", "tags": ["a", "b"]}
{"_id": "2", "tags": ["a", "b", "c"]}
{"_id": "3", "tags": []}
{"_id": "4", "tags": ["c", "d"]}
```
求tags元素集合?

方法:

```
db.test.aggregate([
    {"$unwind": "$tags"},
    {"$group": {"_id": "$tags"}},
])
```




