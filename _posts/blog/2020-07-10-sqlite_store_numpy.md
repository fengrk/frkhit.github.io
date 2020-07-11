---
layout: post
title:  sqlite存储向量(numpy)数据方案评估
category: 技术
tags:  
    - sqlite
    - numpy
keywords: 
description: 
---

# sqlite存储向量(numpy)数据方案评估


sqlite 可以使用 `Blob` 和 `real` 两种方式存储向量. 本文重点对比两种方案下所需磁盘大小.

引入`numpy`自带持久化作为参考.


评估代码如下:

```python

import io
import os
import sqlite3
import typing

import numpy as np


class _Sqlite(object):
    TABLE = "TABLE_VEC"

    def __init__(self, sqlite_file: str, dim: int, dtype):
        self.sqlite_file = sqlite_file
        self.dim = dim
        self.dtype = dtype

    def count(self) -> int:
        conn = self.get_connection()
        try:
            sql = "SELECT COUNT(*) FROM {}".format(self.TABLE)

            cursor = conn.cursor().execute(sql)
            for row in cursor:
                return int(row[0])
        except Exception as e:
            pass
        finally:
            conn.close()

    def create_index(self):
        conn = self.get_connection()
        try:
            conn.cursor().execute('CREATE INDEX c_id ON {} (ID);'.format(self.TABLE))
            conn.commit()
        finally:
            conn.close()


class SqliteFloat(_Sqlite):

    def search_index(self, index_list: [int]) -> [(int, np.ndarray)]:
        """ 搜索 """
        conn = self.get_connection()

        try:
            args = [int(index) for index in set(index_list)]
            sql = "SELECT ID, {} from {} where ID IN ({})".format(
                ", ".join(["V{}".format(i + 1) for i in range(self.dim)]),
                self.TABLE,
                ",".join(["?" for _ in range(len(args))])
            )
            cursor = conn.cursor().execute(sql, args)
            result_list = []
            for row in cursor:
                index = row[0]
                vec = np.asarray([float(row[1 + i]) for i in range(self.dim)], dtype=self.dtype)
                result_list.append((index, vec))
            return result_list
        except Exception as e:
            return []
        finally:
            conn.close()

    def insert_data(self, doc_list: [np.ndarray]):
        """ 插入数据 """
        if not doc_list:
            return

        data_list = []
        for index, vec in enumerate(doc_list):
            data_list.append([index] + [float(vec[i]) for i in range(self.dim)])

        conn = self.get_connection()
        try:
            sql = "INSERT INTO {}(ID, {}) VALUES (?, {})".format(
                self.TABLE,
                ", ".join(["V{}".format(i + 1).format(i) for i in range(self.dim)]),
                ", ".join(["?"] * self.dim),
            )
            conn.cursor().executemany(sql, data_list)
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def get_connection(self):
        """ 创建模型 """

        if not os.path.exists(self.sqlite_file):
            conn = sqlite3.connect(self.sqlite_file)
            c = conn.cursor()
            c.execute('''CREATE TABLE {}
                   (ID INTEGER,
                   {}
                   );'''.format(self.TABLE, ", ".join(["V{}".format(i + 1) for i in range(self.dim)])))
            conn.commit()
            conn.close()

        return sqlite3.connect(self.sqlite_file)


class SqliteBlob(_Sqlite):

    def search_index(self, index_list: [int]) -> [(int, np.ndarray)]:
        """ 搜索 """
        conn = self.get_connection()

        try:
            args = [int(index) for index in set(index_list)]
            sql = "SELECT ID, VEC from {} where ID IN ({})".format(
                self.TABLE,
                ",".join(["?" for _ in range(len(args))])
            )
            cursor = conn.cursor().execute(sql, args)
            return [(row[0], self.convert_array(row[1])) for row in cursor]

        except Exception as e:
            return []
        finally:
            conn.close()

    def insert_data(self, doc_list: [np.ndarray]):
        """ 插入数据 """
        if not doc_list:
            return

        data_list = [(index, self.adapt_array(vec)) for index, vec in enumerate(doc_list)]
        conn = self.get_connection()
        try:
            sql = "INSERT INTO {}(ID, VEC) VALUES (?, ?)".format(
                self.TABLE,
            )
            conn.cursor().executemany(sql, data_list)
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def get_connection(self):
        """ 创建模型 """

        if not os.path.exists(self.sqlite_file):
            conn = sqlite3.connect(self.sqlite_file)
            c = conn.cursor()
            c.execute('''CREATE TABLE {}
                   (ID INTEGER,
                   VEC BLOB NOT NULL 
                   );'''.format(self.TABLE, ))
            conn.commit()
            conn.close()

        return sqlite3.connect(self.sqlite_file)

    @staticmethod
    def adapt_array(arr: np.ndarray) -> sqlite3.Binary:
        """
        http://stackoverflow.com/a/31312102/190597 (SoulNibbler)
        """
        out = io.BytesIO()
        np.save(out, arr)
        out.seek(0)
        return sqlite3.Binary(out.read())

    @staticmethod
    def convert_array(text: sqlite3.Binary) -> np.ndarray:
        out = io.BytesIO(text)
        out.seek(0)
        return np.load(out)


class Benchmark(object):
    def __init__(self, dim: int = 128, count: int = 1024, dtype=np.float32):
        self.dim = dim
        self.dtype = dtype
        self.data_list = self._create_random_data(count=count)

    def _create_random_data(self, count: int) -> typing.List[np.ndarray]:
        """ """
        data_list = []
        for index in range(count):
            data_list.append(np.asarray([1.0 + _i * _i + index / 10 for _i in range(self.dim)], dtype=self.dtype))

        return data_list

    @staticmethod
    def is_equal(array_1: np.ndarray, array_2: np.ndarray) -> bool:
        """ """
        if array_1 is None:
            return False
        if array_2 is None:
            return False
        if array_1.shape != array_2.shape or array_1.dtype != array_2.dtype:
            return False

        return (abs(array_1 - array_2) < 1e-10).all()

    def numpy_file(self) -> int:
        """ """
        sqlite_file = "./abc.npy"
        if os.path.exists(sqlite_file):
            os.remove(sqlite_file)

        try:
            array = np.vstack(self.data_list).reshape((len(self.data_list), self.dim))
            np.save(sqlite_file, array)
            return int(os.path.getsize(sqlite_file))
        finally:
            if os.path.exists(sqlite_file):
                os.remove(sqlite_file)

    def sqlite_blob(self) -> int:
        """ """
        return self._sqlite(cls=SqliteBlob)

    def sqlite_float(self) -> int:
        """ """
        return self._sqlite(cls=SqliteFloat)

    def _sqlite(self, cls) -> int:
        """ """
        sqlite_file = "./abc.dat"
        if os.path.exists(sqlite_file):
            os.remove(sqlite_file)

        try:
            dao = cls(sqlite_file=sqlite_file, dim=self.dim, dtype=self.dtype)
            dao.insert_data(self.data_list)
            dao.create_index()
            assert dao.count() == len(self.data_list)
            result_list = dao.search_index(index_list=[i for i in range(len(self.data_list))])
            result_dict = {index: vec for index, vec in result_list}
            assert len(result_list) == len(self.data_list)
            for i in range(len(self.data_list)):
                assert self.is_equal(array_1=result_dict[i], array_2=self.data_list[i])

            return int(os.path.getsize(sqlite_file))
        finally:
            if os.path.exists(sqlite_file):
                os.remove(sqlite_file)

    def compare(self, ):
        """ """
        for func_name in ["numpy_file", "sqlite_float", "sqlite_blob", ]:
            print("{}\t\t{}\t\t{:.2f}MB".format(func_name.rjust(15), self.dtype, getattr(self, func_name)() / 1024 / 1024))


if __name__ == '__main__':
    Benchmark(dtype=np.float32).compare()
    Benchmark(dtype=np.float64).compare()

```

评估结果如下:

```
     numpy_file		<class 'numpy.float32'>		0.50MB
   sqlite_float		<class 'numpy.float32'>		1.36MB
    sqlite_blob		<class 'numpy.float32'>		0.69MB

     numpy_file		<class 'numpy.float64'>		1.00MB
   sqlite_float		<class 'numpy.float64'>		1.36MB
    sqlite_blob		<class 'numpy.float64'>		1.36MB
```

sqlite 对 `REAL` 等数据结构的说明, 可以参见:[datatype3](https://sqlite.org/datatype3.html)

```
Each value stored in an SQLite database (or manipulated by the database engine) has one of the following storage classes:

NULL. The value is a NULL value.

INTEGER. The value is a signed integer, stored in 1, 2, 3, 4, 6, or 8 bytes depending on the magnitude of the value.

REAL. The value is a floating point value, stored as an 8-byte IEEE floating point number.

TEXT. The value is a text string, stored using the database encoding (UTF-8, UTF-16BE or UTF-16LE).

BLOB. The value is a blob of data, stored exactly as it was input.
``` 

