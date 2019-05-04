---
layout: post
title: h5py性能测评
category: 技术
tags: python
keywords: 
description: 
---

# h5py性能测评

## 代码

```
import pickle
import sys
import time
import unittest

import h5py
import numpy as np
import os


class TestH5(unittest.TestCase):
    def setUp(self):
        self.pickle_file = "./data.pkl"
        self.h5_file = "./data.h5"

    def tearDown(self):
        os.remove(self.pickle_file)
        os.remove(self.h5_file)

    @staticmethod
    def get_file_size(file_path):
        file_size = os.path.getsize(file_path) / float(1024 * 1024)
        return "{}MB".format(round(file_size, 2))

    @staticmethod
    def get_size(obj):
        return sys.getsizeof(obj)

    def create_file(self):
        """ 创建文件 """
        data = np.random.random(size=(100000, 1024))
        print("size of data is {}".format(self.get_size(data)))
        target_index = [1, 5, 10, 50, 100, 500, 1000, 5000, 9000, 9001, 9003]
        target_result = data[target_index]
        print("size of target_result is {}".format(self.get_size(target_result)))

        # pickle
        with open(self.pickle_file, "wb") as fw:
            pickle.dump(data, fw)
        print("pickle file size is {}".format(self.get_file_size(self.pickle_file)))

        # h5py
        with h5py.File(self.h5_file, 'w') as hf:
            hf.create_dataset('data', data=data)
        print("h5 file size is {}".format(self.get_file_size(self.h5_file)))

        return target_index, target_result

    def pickle_load(self, target_index, target_result):
        time_start = time.time()
        with open(self.pickle_file, "rb") as fr:
            all_data = pickle.load(fr)
            self.assertTrue((target_result == all_data[target_index]).all())
        return time.time() - time_start

    def h5py_load(self, target_index, target_result):
        time_start = time.time()
        with h5py.File(self.h5_file, 'r') as hf:
            all_data = hf["data"]
            self.assertTrue((target_result == all_data[target_index]).all())
        return time.time() - time_start

    def testFileLoad(self):
        """ 文件加载 """

        target_index, target_result = self.create_file()

        # pickle: load 100 time
        time_list = []
        for i in range(10):
            time_list.append(self.pickle_load(target_index=target_index, target_result=target_result))
        print("pickle load 10 times: {}s per step, max time is {}s, min time is {}s!".format(
            sum(time_list) / len(time_list), max(time_list), min(time_list)))

        # h5py: load 10 time
        time_list = []
        for i in range(10):
            time_list.append(self.h5py_load(target_index=target_index, target_result=target_result))
        print("h5 load 10 times: {}s per step, max time is {}s, min time is {}s!".format(
            sum(time_list) / len(time_list), max(time_list), min(time_list)))

```

## 测试结果

文件加载测试结果如下:
```
Launching unittests with arguments python -m unittest hdf5_benchmark.TestH5 in /mnt/e/frkhit/wsl/tmp/pycharm_benchmark
size of data is 819200112
size of target_result is 90224
pickle file size is 781.25MB
h5 file size is 781.25MB
pickle load 10 times: 2.1771466970443725s per step, max time is 2.5986461639404297s, min time is 2.0592007637023926s!
h5 load 10 times: 0.002041530609130859s per step, max time is 0.004301786422729492s, min time is 0.0013699531555175781s!
```

结论:
- h5py不一定能节省空间, 在本测试中, h5py的文件大小与pickle一样
- h5py在加载数据时, 更省时间(只从硬盘中加载需要的数据)
