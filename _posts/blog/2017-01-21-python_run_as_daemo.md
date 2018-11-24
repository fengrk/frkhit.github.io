---
layout: post
title: python 后台程序实现
category: 技术
tags: python
keywords: 
description: 
---

work.py

```
def work():
    print "running"
    import time
    time.sleep(100)


if __name__ == '__main__':
    work()

```

## 方法1 nohup

```
nohup python work.py > nohup.out &
```

## 方法2 python-daemon
安装python-daemon包  
`pip install python-daemon`

编写入口程序  
use_daemon.py

```
import daemon
from work import work
with daemon.DaemonContext():
    work()

```
运行  
`python use_daemon.py`
