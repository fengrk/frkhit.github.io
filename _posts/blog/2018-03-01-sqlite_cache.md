---
layout: post
title: 基于sqlite3实现数据缓存
category: 技术
tags: python
keywords: 
description: 
---

# 基于sqlite3实现数据缓存

```
# -*- coding:utf-8 -*-
import os
import pickle
import sqlite3
import time


class SimpleCache(object):
    def __init__(self):
        self.cache_file = os.path.join("./tmp.dat")

    def get(self, key):
        """

        :rtype: object
        :type key: str
        """
        conn = self._get_connect()

        try:
            value, exp_time = self._get_uid_value(conn, key)
            if exp_time > self._get_current_time():
                return value

        except Exception as e:
            print(e)
        finally:
            conn.close()

        return None

    @staticmethod
    def _get_uid_value(conn, key):
        try:
            sql = "SELECT VALUE, EXPTIME from CACHE where UID = ?"
            cursor = conn.cursor().execute(sql, (key,))
            for row in cursor:
                return pickle.loads(row[0]), row[1]
        except Exception as e:
            print(e)

        return None, None

    def set(self, key, value, ttl=1e10):
        """

        :param ttl: int, living time in second
        :param value: object can pickle
        :param key: str
        """
        conn = self._get_connect()

        try:
            old_value, exp_time = self._get_uid_value(conn, key)
            if old_value is None and exp_time is None:
                sql = "INSERT INTO CACHE(ID, VALUE, EXPTIME, UID) VALUES (NULL, ?, ?, ?)"
            else:
                sql = "UPDATE CACHE SET VALUE = ?, EXPTIME = ? where UID = ?"

            conn.cursor().execute(sql, (pickle.dumps(value), self._get_current_time() + ttl, key))
            conn.commit()
        except Exception as e:
            print(e)
            return None
        finally:
            conn.close()

    def _get_connect(self):
        if not os.path.exists(self.cache_file):
            conn = sqlite3.connect(self.cache_file)
            c = conn.cursor()
            c.execute('''CREATE TABLE CACHE
                   (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                   UID CHAR(32) UNIQUE NOT NULL,
                   EXPTIME INT NOT NULL ,
                   VALUE TEXT);''')
            conn.commit()
            conn.close()

        return sqlite3.connect(self.cache_file)

    @staticmethod
    def _get_current_time():
        """

        :rtype: int
        """
        return time.time()

```

使用方法

```
cache = SimpleCache()

key_id = "key"

print(cache.get(key_id))
cache.set(key_id, "a", 10)
print(cache.get(key_id))

print(cache.get(key_id))
cache.set(key_id, [1, 3, 4], 1)
print(cache.get(key_id))
time.sleep(2)
print(cache.get(key_id))

```
