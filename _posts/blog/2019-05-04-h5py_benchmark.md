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
        pass

    @staticmethod
    def get_file_size(file_path):
        file_size = os.path.getsize(file_path) / float(1024 * 1024)
        return "{}MB".format(round(file_size, 2))

    @staticmethod
    def get_size(obj):
        return sys.getsizeof(obj)

    def testFileSize(self, ):
        """ 文件大小 """
        data = np.random.random(size=(100000, 128))

        # pickle
        pickle_file = "./data.pkl"
        with open(pickle_file, "wb") as fw:
            pickle.dump(data, fw)
        print("pickle file size is {}".format(self.get_file_size(pickle_file)))

        # h5py
        h5_file = "./data.h5"
        with h5py.File(h5_file, 'w') as hf:
            hf.create_dataset('data', data=data)
        print("h5 file size is {}".format(self.get_file_size(h5_file)))

        # remove file
        os.remove(pickle_file)
        os.remove(h5_file)

    def testFileLoad(self):
        """ 文件加载 """
        data = np.random.random(size=(100000, 1024))
        print("size of data is {}".format(self.get_size(data)))
        target_index = [1, 5, 10, 50, 100, 500, 1000, 5000, 9000, 9001, 9003]
        target_result = data[target_index]
        print("size of target_result is {}".format(self.get_size(target_result)))

        # pickle
        pickle_file = "./data.pkl"
        with open(pickle_file, "wb") as fw:
            pickle.dump(data, fw)
        print("pickle file size is {}".format(self.get_file_size(pickle_file)))

        # load 100 time
        time_list = []
        for i in range(100):
            time_start = time.time()
            with open(pickle_file, "rb") as fr:
                all_data = None
                all_data = pickle.load(fr)
                self.assertTrue((target_result == all_data[target_index]).all())
            time_list.append(time.time() - time_start)

        print("size of pickle all_data is {}".format(self.get_size(all_data)))
        print("pickle load 100 times: {}s per step, max time is {}s, min time is {}s!".format(
            sum(time_list) / len(time_list), max(time_list), min(time_list)))

        # h5py
        h5_file = "./data.h5"
        with h5py.File(h5_file, 'w') as hf:
            hf.create_dataset('data', data=data)
        print("h5 file size is {}".format(self.get_file_size(h5_file)))

        # load 100 time
        time_list = []
        for i in range(100):
            time_start = time.time()
            with h5py.File(h5_file, 'r') as hf:
                all_data = None
                all_data = hf["data"]
                self.assertTrue((target_result == all_data[target_index]).all())
            time_list.append(time.time() - time_start)

        print("size of h5 all_data is {}".format(self.get_size(all_data)))
        print("h5 load 100 times: {}s per step, max time is {}s, min time is {}s!".format(
            sum(time_list) / len(time_list), max(time_list), min(time_list)))

        # remove file
        os.remove(pickle_file)
        os.remove(h5_file)
```

## 测试结果

文件加载测试结果如下:
```
hdf5_benchmark.TestH5.testFileLoad
Launching unittests with arguments python -m unittest hdf5_benchmark.TestH5.testFileLoad in /mnt/e/frkhit/wsl/tmp/pycharm_benchmark
size of data is 819200112
size of target_result is 90224
pickle file size is 781.25MB
size of pickle all_data is 112
pickle load 100 times: 2.3805650806427003s per step, max time is 2.9585835933685303s, min time is 2.2419371604919434s!
h5 file size is 781.25MB
size of h5 all_data is 56
h5 load 100 times: 0.003202075958251953s per step, max time is 0.13279366493225098s, min time is 0.0013022422790527344s!
```

结论:
- h5py不一定能节省空间, 在本测试中, h5py的文件大小与pickle一样
- h5py在加载数据时, 更省时间
