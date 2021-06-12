---
layout: post
title: 再读《MongoDB权威指南》
category: 技术
tags: 
    - mongo
keywords: 
description: 
---

# 再读《MongoDB权威指南》

刚接触mongo时,所看过最好的入门资料,就是《MongoDB权威指南》. 阅读后, 对mongo有一个直观的了解, 配合mongo官方文档, 使用mongo就没什么困难了.

最近新项目, 需要深度使用mongo, 如使用复杂的聚合操作生成报表数据. 项目中还遇到聚合操作形成数据库全局锁, 导致其他操作被阻塞的问题.

空闲之下, 决定再读《MongoDB权威指南》, 加深理解.

## 1. Mongo简介
- 聚合操作, 数据库能自动优化
- 支持存在时间有限的集合, 适合session管理等场景
- 支持固定大小的集合,适合保存日志等场景
- 支持一种协议,用于存储大文件和文件元数据(?)

## 2. MongoDB基础知识
- objectId能提取时间戳

## 3. 创建 更新和删除文档
- 删除集合最快的方法: drop + 重建索引
- 更新操作不可分割: 原子性
- array vs set. `$push` 对array添加元素; `$addToSet`将array当做set并添加元素; 前两者配合`$each`实现添加多个元素
- 删除元素: `$pop` vs `$pull`, 具体参考官方文档.
- `$`基于位置的数组修改器定位符. `db.blog.update({"comments.author" : "John"},{"$set" : {"comments.$.author" : "Jim"}})`, 定位符只更新第一个匹配的元素
- 修改器速度: mongo为文档大小预留空间; 当文档修改后大小不够,会执行文档移动操作.
- 批量更新文档,获取更新信息: ` db.runCommand({getLastError : 1}) # “返回最后一次操作的相关信息`.
- 写入安全（Write Concern）, 有两种模式, 应答式(确认成功)和非应答式(不返回响应). 非应答式用于不重要数据存储场合.

## 4. 查询
- 返回制定键, 默认返回_id. ` db.users.find({}, {"username" : 1, "email" : 1}) # 返回三个键`, ` db.users.find({}, {"fatal_weakness" : 0}) # 不返回指定键`
- 高级查询, 参数及示例.
- `$where`, 借用js. 但速度慢, 如无必要, 不要使用.
- 服务端脚本, 容易受到攻击.
- 避免使用skip略过大量结果, skip大量结果, 很占资源. 可行的方法是, 利用上一次查询的条件, 略过已查询的结果.
- 高级查询选项: `$min`, `$max`能强制使用索引, 具体参考书本. `$maxscan`, 扫描文档上限.
- 游标, 获取一致性结果. `cursor = db.foo.find();while (cursor.hasNext()) {...}`, 相同的结果可能返回多次, 原因是文档修改后空间不足可能被移动到后面. 解决方法是使用快照` db.foo.find().snapshot()`, 但占资源, 尽量不用.
- 服务端游标的生命周期. 一般客户端会通知销毁游标; 服务端有超时记录, 超时后会自动销毁, 如果客户端需要长时间使用游标, 需要告知服务端不要超时销毁.

## 5. 索引
- `explain`查看具体执行操作, 调试索引的好工具. 如` db.users.find({username: "user101"}).explain()`
- `db.currentOp()` 如果新建索引不能短时间内返回结果, 可以另开shell执行`db.currentOp()`查看
- 索引的代价: 每次操作, 需要更新索引, 耗时更长. mongo限制索引上限为64; 每个集合最好不超过两个索引.
- `hit()`: 强制 MongoDB 使用特定的索引
- 稀疏索引: `sparse`. ` db.ensureIndex({"email" : 1}, {"unique" : true, "sparse" : true})`, email存在, 则唯一.

## 6. 特殊的索引和集合
- 固定集合: 固定大小, 循环队列.
- TTL索引, 这种索引允许为每一个文档设置一个超时时间. 一个文档到达预设置的老化程度之后就会被删除. 这种类型的索引对于缓存问题（比如会话的保存）非常有用.` db.foo.ensureIndex({"lastUpdated" : 1}, {"expireAfterSecs" : 60*60*24}) # 24h`
- 全文本索引, 用于全文检索, 耗资源.
- 地理空间检索, 最常用的是 2dsphere 索引(用于地球表面类型的地图)和 2d索引(用于平面地图和时间连续的数据). 支持交集, 包含和接近查询.
- GridFS存储文件.

## 7. 聚合
TODO: 待补充


## 17. 了解应用的动态
- ` db.currentOp()`: 查看正在进行的操作
- `db.killOp()`: 终止操作. 注意, 只有交出了锁的进程才能被终止
- system profiler: 可获得慢查询日志, 该操作默认不打开
- `stats`: 获取集合, 数据库状态信息
- `mongotop` 类似top, 获取当前操作信息. `mongotop-locks`, 获得每个数据库的锁状态

# 18. 数据管理
- 权限控制: 颗粒度
- 建立索引: ` db.foo.ensureIndex({"somefield" : 1}, {"background" : true})`. 前台建索引, 锁定数据库; 后台建索引, 定期释放写锁
- 压缩数据: 数据碎片; 使用` db.runCommand({"compact" : "collName"})`压缩数据

