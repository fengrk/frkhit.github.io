---
layout: post
title: python多线程编程记录
category: 技术
tags: 
    - python
keywords: 
description: 
---

# python多线程编程记录

## 1. 线程锁额外耗时简单量化

多线程之间, 可借助线程锁共享变量. 线程锁的使用, 会给程序带来多大的性能损耗? 

测试示例如下:

```python

from enum import Enum
from threading import Thread, Lock
import time


class BusyMode(Enum):
    IO_BUSY = 0
    CPU_BUSY = 1


class AtomicInteger(object):
    __slots__ = ("_value", "_lock")

    def __init__(self, value: int = 0):
        self._value: int = value
        self._lock = Lock()

    def inc(self) -> int:
        with self._lock:
            self._value += 1
            return self._value

    def dec(self) -> int:
        with self._lock:
            self._value -= 1
            return self._value

    def set(self, value: int) -> int:
        with self._lock:
            self._value = value
            return self._value

    @property
    def value(self) -> int:
        with self._lock:
            return self._value


class Worker(Thread):
    def __init__(self, count: AtomicInteger, busy_mode: BusyMode, times: int, *args, **kwargs):
        super(Worker, self).__init__(*args, **kwargs)
        self.count = count
        self._busy_mode = busy_mode
        self.times = times

    def run(self) -> None:
        def io_busy():
            time.sleep(1)

        def cpu_busy():
            for count in range(1000000):
                x = count * count

        func = io_busy if self._busy_mode == BusyMode.IO_BUSY else cpu_busy

        for _ in range(self.times):
            if self.count is not None:
                cur_count = self.count.inc()
                # print("current atomic_count: {}".format(cur_count))
            func()


result_list = []
for _busy_mode in [BusyMode.IO_BUSY, BusyMode.CPU_BUSY]:
    for _use_lock in [False, True]:
        if _use_lock:
            _atomic_count = AtomicInteger(0)
        else:
            _atomic_count = None
        print("busy mode {}, use lock {} >>>".format(_busy_mode, _use_lock))
        time_start = time.time()
        threads = []
        for _ in range(20):
            threads.append(Worker(count=_atomic_count, busy_mode=_busy_mode, times=20))

        for worker in threads:
            worker.start()

        for worker in threads:
            worker.join()

        time_stop = time.time()
        log_line = "busy mode {}, use lock {}, time cost {:.3f}s".format(_busy_mode, _use_lock, time_stop - time_start)
        print("{}\n".format(log_line))
        result_list.append(log_line)

print("\n\nresult:\n{}".format("\n".join(result_list)))

```

执行结果:

``` 
busy mode BusyMode.IO_BUSY, use lock False, time cost 20.066s
busy mode BusyMode.IO_BUSY, use lock True, time cost 20.056s
busy mode BusyMode.CPU_BUSY, use lock False, time cost 32.659s
busy mode BusyMode.CPU_BUSY, use lock True, time cost 30.786s
```

# 2. 基于多线程, 实现 master-worker 模式

示例:

````python
import os
import subprocess
import sys
import time
import typing
import unittest
import weakref  # noqa
from threading import Thread


def busy_working_by_subprocess(sleep_time: int):
    subprocess_cmd = """sleep {}""".format(int(sleep_time))

    # 环境变量
    base_env = dict(os.environ)
    path_dir = os.path.dirname(__file__)
    python_path = os.path.join(path_dir, "../")
    base_env.update(dict(PYTHONIOENCODING="utf-8", LANG="en_US.UTF-8", PYTHONPATH="{}".format(os.path.abspath(python_path))))
    subprocess_kwargs = dict(shell=True, env=base_env, )
    subprocess.check_output(subprocess_cmd, **subprocess_kwargs)


class TestThread(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def testMasterWorker(self):
        """ """
        workers: typing.Dict[str, Thread] = {}

        for i in range(10):
            sleep_time = 3
            count = 10
            for j in range(count):
                thread_name = "Thread-{}-{}".format(i, j)
                worker = Thread(target=busy_working_by_subprocess, args=(sleep_time,), name=thread_name)
                worker.daemon = True
                worker.start()
                # workers[thread_name] = weakref.proxy(worker)
                #   if thread.is_alive():
                #   ReferenceError: weakly-referenced object no longer exists
                workers[thread_name] = worker
            print("{} thread start".format(count))

            while True:
                all_done = True
                done_count = 0
                for thread_name, thread in workers.items():
                    if thread.is_alive():
                        all_done = False
                    else:
                        done_count += 1

                print(f"{done_count}, {all_done}")
                if all_done:
                    print("all thread done")
                    workers.clear()
                    break
                time.sleep(1)

    def testMasterWorkerMasterExit(self):
        """ """
        workers: typing.Dict[str, Thread] = {}

        for i in range(10):
            sleep_time = 60
            count = 10
            for j in range(count):
                thread_name = "Thread-{}-{}".format(i, j)
                worker = Thread(target=busy_working_by_subprocess, args=(sleep_time,), name=thread_name)
                worker.daemon = True
                worker.start()
                # workers[thread_name] = weakref.proxy(worker)
                #   if thread.is_alive():
                #   ReferenceError: weakly-referenced object no longer exists
                workers[thread_name] = worker
            print("{} thread start".format(count))

            while True:
                all_done = True
                done_count = 0
                for thread_name, thread in workers.items():
                    if thread.is_alive():
                        all_done = False
                    else:
                        done_count += 1

                print(f"{done_count}, {all_done}")
                if all_done:
                    print("all thread done")
                    workers.clear()
                    break
                time.sleep(1)

                # 强制退出: 模拟 master die
                print("force exit: sys.exit(1)")
                sys.exit(1)
                # 强制退出后, master 退出, worker 继续执行

````
