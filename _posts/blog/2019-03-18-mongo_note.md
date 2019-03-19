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


## 2.update操作

### 2.1 修改列表元素的值
keywords: update_many

举例,有如下数据:
```
{"_id": "1", "tags": ["a", "b"]}
{"_id": "2", "tags": ["a", "b", "c"]}
{"_id": "3", "tags": []}
{"_id": "4", "tags": ["c", "d"]}
```
将`tags`中"a"修改为"A"? 

方法:

```
self.db["test"].update_many(
    filter={"tags": "a"},
    update={"$set": {'tags.$': "A"}},
    upsert=False,
    )
    
# 一次操作只能修改一个值
# 如果tags中存在多个"a", 需要多次执行以上代码
```

### 2.2 删除列表元素的值
keywords: update_many

举例,有如下数据:
```
{"_id": "1", "tags": ["a", "b"]}
{"_id": "2", "tags": ["a", "b", "c"]}
{"_id": "3", "tags": []}
{"_id": "4", "tags": ["c", "d"]}
{"_id": "5", "tags": ["c", "d", "a", "a"]}
```
将`tags`中所有"a"删除?

方法:

```
tag_list = ["a"]
self.db["test"].update_many(
    filter={"tags": {"$in": tag_list}},
    update={"$pull": {'tags': {"$in": tag_list}}},
    upsert=False,
)
# 执行后, _id = "5"的记录, tags中两个"a"均被删除
```
