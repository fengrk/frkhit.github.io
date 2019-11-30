---
layout: post
title:  sqlite 使用总结
category: 技术
tags:  python, sqlite
keywords: 
description: 
---

# sqlite 使用总结

[SQLite官方文档 Appropriate Uses For SQLite](https://www.sqlite.org/whentouse.html) 指出:

```
SQLite does not compete with client/server databases. SQLite competes with fopen().
```

SQLite的竞争对手是`fopen`(相当于 python 中的 `open`)。 


## 1. 存储文本数据集

存在一个大规模的文本数据集， 以 （index/int, hash/str, content/str）的形式存储，使用方式仅是通过搜索 index 或 hash， 获取文本信息。此外， 该数据集的读取，都在一个进程中执行。

在这种特殊的应用场景中， 如果将数据集存储到诸如 mysql， mongo 等数据库中， 会造成资源的浪费。这时候， sqlite 便可以派上用场。

```
import logging
import os
import sqlite3

from collections import namedtuple

TextModel = namedtuple("TextModel", field_names=["index", "hash_id", "content"])

_cur_dir = os.path.dirname(__file__)


class SqliteTextDao(object):
    def __init__(self, db_file: str, logger: logging.Logger = None):
        self.db_file = db_file
        self.logger = logger or logging.getLogger(self.__class__.__name__)

    def search(self, index_list: [int]) -> [(int, str, str)]:
        """ 搜索 """
        conn = self._get_connect()

        try:
            args = list(set(index_list))
            sql = "SELECT INDEX, HASHID, CONTENT from TEXTDB where ID IN ({})".format(",".join(["?" for _ in range(len(args))]))
            cursor = conn.cursor().execute(sql, args)
            return [(row[0], row[1], row[2]) for row in cursor]
        except Exception as e:
            self.logger.error(e)

    def insert(self, hash_id: str, content: str, index: int):
        """ 插入数据 """
        conn = self._get_connect()
        try:
            sql = "INSERT INTO TEXTDB(INDEX, HASHID, CONTENT) VALUES (?, ?, ?)"
            conn.cursor().execute(sql, (index, hash_id, content))
            conn.commit()
        except Exception as e:
            self.logger.error(e)
            return None
        finally:
            conn.close()

    def _get_connect(self):
        """ 创建模型 """
        if not os.path.exists(self.db_file):
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            c.execute('''CREATE TABLE TEXTDB
                   (INDEX INTEGER PRIMARY KEY,
                   HASHID CHAR(32) NOT NULL,
                   CONTENT TEXT);''')
            conn.commit()
            conn.close()

        return sqlite3.connect(self.db_file)

    def list_instance_by_index(self, index_list: [int]) -> [TextModel]:
        """
        根据 index 返回 数据模型 列表
        :param index_list:
        :return:
        :rtype: list of TextModel
        """
        index_list = [int(_index) for _index in list(set(index_list))] # numpy 来源的 index 可能类型不一样

        instance_dict = {}
        for index, hash_id, content in self.search(index_list=index_list):
            instance_dict[int(index)] = TextModel(index=int(index), hash_id=hash_id, content=content)

        result_list = []
        for index in index_list:
            result_list.append(instance_dict.get(index))

        return result_list

```
