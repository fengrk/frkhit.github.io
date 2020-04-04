---
layout: post
title: mongo学习笔记
category: 技术
tags: 
    - mongo
keywords: 
description: 
---

# mongo学习笔记

## 1. mongo document学习笔记
### 1.1 BSON 类型
- ObjectId: 快速, 有序, 时间相关
- String
- Timestamps
- Date


### 1.2 Document类型
- 字段(field)有长度限制: 如field name不超过128, 等
- Dot Notation: `<array>.<index>`, `<embedded document>.<field>`
- 单文档有大小限制:16MB

### 1.3 聚合
```MongoDB provides three ways to perform aggregation: the aggregation pipeline, the map-reduce function, and single purpose aggregation methods.```

聚合字段:
- `$match`: 匹配, `{ $match: { name: "Joe Schmoe" } }`
- `unwind`: 打散,针对array, `{ $unwind: "$resultingArray"}`
- `$project`: 投射, `{"$project":{"author":1,"_id":0} #只提前author`
- `$redact`: 校验, `{ $redact: { $cond: { if: { $eq: [ "$level", 5 ] }, then: "$$PRUNE", else: "$$DESCEND" } } }`
- `$skip`: 跳过, `{ $skip: 5 }`
- `$lookup`: 跨表检索, ```{
  $lookup: {
    from: "otherCollection",
    as: "resultingArray",
    localField: "x",
    foreignField: "y"
  }
}```

**Note:**
- 各字段配合的优化, 参考[文档](https://docs.mongodb.com/manual/core/aggregation-pipeline-optimization/)

聚合限制:
- `Result Size Restrictions`: 单doc <= 16MB
- `Memory Restrictions`: `Pipeline stages have a limit of 100 megabytes of RAM`; `The $graphLookup stage must stay within the 100 megabyte memory limit.`

todo: [聚合操作zip code data set(经纬度)](https://docs.mongodb.com/manual/tutorial/aggregation-zip-code-data-set/)

[Aggregation with User Preference Data](https://docs.mongodb.com/manual/tutorial/aggregation-with-user-preference-data/), 利用用户信息表举例:
- 获取所有员工名称
- 根据加入时间返回员工名称
- 获取每个月新加入的人数
- 获取前五个最受欢迎的爱好

### 1.4 检索

条件检索
- `$or`: `cursor = db.inventory.find({"$or": [{"status": "A"}, {"qty": {"$lt": 30}}]})`
- `$and`

检索列表:
- `Match an Array`: `db.inventory.find({"tags": ["red", "blank"]}) # tags == ["red", "blank"]`; `db.inventory.find({"tags": {"$all": ["red", "blank"]}}) # tags 同时存在"red","blank"两个元素`
- `Query an Array with Compound Filter Conditions on the Array Elements`: `db.inventory.find({"dim_cm": {"$gt": 15, "$lt": 20}}) # 15<x<20; x>15, y<20`
- `Query for an Array Element that Meets Multiple Criteria`: `db.inventory.find({"dim_cm": {"$elemMatch": {"$gt": 22, "$lt": 30}}}) # 其中有一个元素22<x<30`
- `Query for an Element by the Array Index Position`: `db.inventory.find({"dim_cm.1": {"$gt": 25}})`
- `Query an Array by Array Length`: `db.inventory.find({"tags": {"$size": 3}})`

Project：
- `db.inventory.find({"status": "A"}, {"item": 1, "status": 1})` means `SELECT _id, item, status from inventory WHERE status = "A"`
- `db.inventory.find({"status": "A"}, {"item": 1, "status": 1, "_id": 0})` means `SELECT item, status from inventory WHERE status = "A"`
- `db.inventory.find({"status": "A"}, {"status": 0, "instock": 0})` means `return All except for status and instock`


其他
- `db.inventory.find({"item": None})`: `None 或 不存在`
- `db.inventory.find({"item": {"$type": 10}})`: 类型检查, 查询值为None的记录
- `db.inventory.find({"item": {"$exists": False}})`: 不存在

### 1.5 固定集合(Capped Collection)

- 判断当前集合是否是固定集合: `db.collection.isCapped()`
- 转化为固定集合(原数据可能会丢失): `db.runCommand({"convertToCapped":"my_coll",size:2000000000, max:500000})`. max 为文档数量, size 为内容大小


## 2.聚合操作

### 2.1 获取列表元素集合

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

### 2.2 获取某个字段的所有取值
```
db.getCollection('<collection>').aggregate(
   [
     { "$group" : { _id : null, "city": { "$addToSet": "$city" } } }
   ]
)
```

## 3.update操作

### 3.1 修改列表元素的值
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

### 3.2 删除列表元素的值
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


### 3.3 列表修改高级版 
假设有数据如下

```
collection.insert_many([
{"name": "a1", "tags": [{"weight": 10}, {"weight": 20}]},
{"name": "a2", "tags": [{"weight": 11}, {"weight": 21}]},
{"name": "a3", "tags": [{"weight": 10}, {"weight": 25}]},
])
```

#### 3.3.1 将`weight=10`的标签的权重更改为20

```
# 执行一次，只会更新该条记录中满足条件的第一个元素

collection.update_many(
{"tags.weight": 10},
{"$set": {"tags.$.weight": 20}},
upsert=False,
)
```

修改所有匹配值的方法:

```
while True:
    result = collection.update_many(
                {"tags.weight": 10},
                {"$set": {"tags.$.weight": 20}},
                upsert=False,)
    if result.matched_count == 0:
        break
```

#### 3.3.2 将`weight!=10`的标签的权重更改为10

```
# 执行一次，只会更新该条记录中满足条件的第一个元素

collection.update_many(
{"tags": {"$elemMatch": {"weight": {"$ne": 10}}},
{"$set": {"tags.$.weight": 20}},
upsert=False,
)
```

#### 3.3.3 将`weight!=10 or weight!=20`的标签的权重更改为10

```
# 执行一次，只会更新该条记录中满足条件的第一个元素

collection.update_many(
{"tags": {"$elemMatch": {"$or": [{"weight": {"$ne": 10}, {"weight": {"$ne": 20}]}}},
{"$set": {"tags.$.weight": 20}},
upsert=False,
)
```

### 3.4 set only not exists

mongo 提供 `$setOnInsert` 操作符， 来实现当文档不存在才设置的功能。

```
db.collection.update(
   <query>,
   { $setOnInsert: { <field1>: <value1>, ... } },
   { upsert: true }
)
```

## 4. 工具

### 4.1 导出 collection

```
mongoexport --uri "mongodb://<username>:<password>@<host1>:<port1>,<host2>:<port2>/<database>?replicaSet=mgset-123456&authSource=admin" --collection <collection> --fields <field1>,<field2> --out <outfile>
```
**要点:**
- `uri`后加引号, `admin`放到`authSource`

或者:

```
mongoexport -h <host> -d <databse> --collection <collection> --fields <field1>,<field2> --out <outfile>
```

### 4.2 导入 collection

```
mongoimport --uri "mongodb://<username>:<password>@<host1>:<port1>,<host2>:<port2>/<database>?replicaSet=mgset-123456&authSource=admin" --collection <collection> --fields <field1>,<field2> <datafile>
```
或者

```
mongoimport -h <host> -d <databse> --collection <collection> --fields <field1>,<field2> <datafile>
```

### 4.3 索引操作
新建索引:

```
db.getCollection('<collection>').createIndex( { "age": 1}, {background: true, name:"_age_"} )

```

### 4.4 mongo 版本不兼容

mongo 升级到 4.0 版本后，其工具如`mongodump`, `mongoimport`, `mongoexport`也需要升级到 4.0版本。

为避免安装这些工具导致主机软件环境混乱，可以使用 docker 执行所需的工具。

```
# download images
docker pull mongo:4.0

# mkdir working dir
mkdir -p dodo && chmod 777 dodo/ -R && cd dodo/

# run mongo tools
docker run --rm -v $(pwd):/workdir/ -w /workdir/ mongo:4.0 mongoimport --uri "mongodb://<username>:<password>@<host1>:<port1>,<host2>:<port2>/<database>?replicaSet=mgset-123456&authSource=admin" --collection <collection> --fields <field1>,<field2> <datafile>
```
