---
layout: post
title:  pymongo按时间聚合
category: 技术
tags:  
    - python
    - mongo
keywords: 
description: 
---

# pymongo按时间聚合

## 时间戳字段按小时聚合

对于 `mongo` 表中数据, 其中字段 `update_time` 为时间戳(`float`), 现在需要使用 `pymongo` 对该字段按小时进行聚合.

能找到最好的参考资料是这个: [https://stackoverflow.com/questions/33078773/mongodb-aggregation-by-day-based-on-unix-timestamp](https://stackoverflow.com/questions/33078773/mongodb-aggregation-by-day-based-on-unix-timestamp)

不同的 `mongo` server 版本, 能执行的语句会有差异. 碰到过两种情况, 现将使用到的代码例子记录如下. 

版本 1, 使用 `$substr` 命令:

```
aggregate_list = [
    {"$project": {
        "hour": {"$substr": [{"$add": ["$update_time", 28800000]}, 0, 14]},
    }},
    {"$group": {"hour": "$hour", "count": {"$sum": 1}}},
    {"$sort": {"hour": 1}},
]

for doc in collection.aggregate(aggregate_list):
    print("{}:\t{}".format(doc["hour"], doc["count"]))
```

版本 2, 使用 `$dateToString` 命令

``` 
import arrow
aggregate_list = [
    {"$project": {
        "hour": {
                "$dateToString": {
                    "format": "%Y%m%d%H",
                    "date": {
                        "$add": [arrow.get(0).datetime, {"$multiply": [1000, "$update_time"]}, 8 * 3600 * 1000]
                    }
                }
            }
    }},
    {"$group": {"hour": "$hour", "count": {"$sum": 1}}},
    {"$sort": {"hour": 1}},
]
for doc in collection.aggregate(aggregate_list):
    print("{}:\t{}".format(doc["hour"], doc["count"]))

```
