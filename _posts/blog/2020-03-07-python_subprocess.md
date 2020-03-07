---
layout: post
title:  python调用子进程
category: 技术
tags:  
    - python
keywords: 
description: 
---

# python调用子进程

python可以使用 `subprocess` 模块, 启动命令. 

如果需要控制子进程的执行时间, 可以使用 `check_output` 方法.

提供一个相对复杂的例子, 展示子进程调用的使用方法:


```
import json
import os
import subprocess
import sys
import time
import unittest

result_file = "./result.log"
sleep_time = 3


def do_some_job():
    with open(result_file, "a") as f:
        f.write("{}\n".format(json.dumps({"time": time.time(), "step": "start"})))

    time.sleep(sleep_time)

    with open(result_file, "a") as f:
        f.write("{}\n".format(json.dumps({"time": time.time(), "step": "end"})))


class TestSubprocess(unittest.TestCase):

    @staticmethod
    def _call_subprocess(timeout: float = None):
        """ """
        cur_package = os.path.basename(__file__).split(".py")[0]
        cmd = '''{python} -c "from {package} import do_some_job; do_some_job() "'''.format(python=sys.executable, package=cur_package)
        subprocess_kwargs = dict(
            shell=True,
            env=dict(PYTHONIOENCODING="utf-8", LANG="en_US.UTF-8"),
            timeout=timeout,
        )
        subprocess.check_output(cmd, **subprocess_kwargs)

    def testSubprocess(self):
        """  """
        for _ in range(3):
            if os.path.exists(result_file):
                os.remove(result_file)

            self._call_subprocess()

            # read result
            self.assertTrue(os.path.exists(result_file))
            with open(result_file, "r") as f:
                line_list = f.readlines()
            self.assertEqual(len(line_list), 2)
            self.assertEqual(json.loads(line_list[0].strip())["step"], "start")
            self.assertEqual(json.loads(line_list[1].strip())["step"], "end")
            self.assertTrue(abs(json.loads(line_list[1].strip())["time"] - json.loads(line_list[0].strip())["time"] - sleep_time) < 0.1)

    def testSubprocessWithTimeout(self):
        """  """
        for _ in range(3):
            if os.path.exists(result_file):
                os.remove(result_file)

            with self.assertRaises(subprocess.TimeoutExpired):
                self._call_subprocess(timeout=1)

            # read result
            self.assertTrue(os.path.exists(result_file))
            with open(result_file, "r") as f:
                line_list = f.readlines()
            self.assertEqual(len(line_list), 1)
            self.assertEqual(json.loads(line_list[0].strip())["step"], "start")
```

要点:
- 可以使用 `python -c "from xxx import do_some_job; do_some_job()` 的方法, 执行 python 内方法
- `subprocess.check_output` 使用 `timeout` 参数控制子进程的执行时间, 查看源码可以发现, 内部其实使用 `subprocess.run`来执行代码
