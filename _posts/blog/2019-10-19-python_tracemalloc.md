---
layout: post
title:  使用 tracemalloc 分析 python 内存使用情况
category: 技术
tags:  OOM, python
keywords: 
description: 
---

# 使用 tracemalloc 分析 python 内存使用情况

工作中，遇到 tornado 启动的服务器，启动成功后单进程内存过大的问题。

尝试使用内存分析工具，分析代码中那部分占用的内存过多。

在 python3环境下， python自带的工具`tracemalloc`，可以分析内存的使用情况。

## 实例

建立如下的 tornado 服务，期望`tracemalloc`找到内存占用最大的代码块：

```
import tracemalloc

logs = []
tracemalloc.start(25)

import tornado.ioloop
import tornado.web


class BadHandler(tornado.web.RequestHandler):
    memory_list = [i for i in range(1000000)]

    def get(self):
        global logs
        self.write("<br><br><br><br>".join(logs))


app = tornado.web.Application([
    (r'/bad', BadHandler),
])

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('traceback')

logs.append("[ Top Biggest 10 block ]")
for stat in top_stats[:10]:
    _msg = ["%s memory blocks: %.1f KiB" % (stat.count, stat.size / 1024)]
    for line in stat.traceback.format():
        _msg.append(line.strip())

    logs.append("<br>".join(_msg))

print("\n\n\n\n".join(logs).replace("<br>", "\n"))

if __name__ == '__main__':
    app.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

```




启动服务后， 结果可以通过查看控制台或访问 `http://localhost:8080/bad`得到。

输出结果如下：

```
[ Top Biggest 10 block ]



999744 memory blocks: 35830.3 KiB
File "/Users/rkfeng/code/streamit_demo/demo_memory/server.py", line 11
memory_list = [i for i in range(1000000)]
File "/Users/rkfeng/code/streamit_demo/demo_memory/server.py", line 11
memory_list = [i for i in range(1000000)]
File "/Users/rkfeng/code/streamit_demo/demo_memory/server.py", line 10
class BadHandler(tornado.web.RequestHandler):



2147 memory blocks: 784.9 KiB
File "", line 487
File "", line 779
File "", line 674
File "", line 665
File "", line 955
File "", line 971
File "/Users/rkfeng/code/streamit_demo/demo_memory/server.py", line 7
import tornado.web



3986 memory blocks: 243.9 KiB
File "", line 487
File "", line 779
File "", line 674
File "", line 665
File "", line 955
File "", line 971
File "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/html/__init__.py", line 6
from html.entities import html5 as _html5
File "", line 219
File "", line 678
File "", line 665
File "", line 955
File "", line 971
File "", line 219
File "", line 941
File "", line 971
File "/opt/streamit_demo/lib/python3.6/site-packages/tornado/escape.py", line 31
import html.entities as htmlentitydefs
File "", line 219
File "", line 678
File "", line 665
File "", line 955
File "", line 971
File "/opt/streamit_demo/lib/python3.6/site-packages/tornado/log.py", line 36
from tornado.escape import _unicode
File "", line 219
File "", line 678
File "", line 665



1758 memory blocks: 232.1 KiB
File "", line 219
File "", line 734
File "", line 571
File "", line 658
File "", line 955
File "", line 971
File "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/ast.py", line 27
from _ast import *
File "", line 219
File "", line 678
File "", line 665
File "", line 955
File "", line 971
File "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/inspect.py", line 35
import ast
File "", line 219
File "", line 678
File "", line 665
File "", line 955
File "", line 971
File "/opt/streamit_demo/lib/python3.6/site-packages/tornado/util.py", line 30
from inspect import getfullargspec as getargspec
File "", line 219
File "", line 678
File "", line 665
File "", line 955
File "", line 971
File "/opt/streamit_demo/lib/python3.6/site-packages/tornado/escape.py", line 27
from tornado.util import PY3, unicode_type, basestring_type



1568 memory blocks: 153.5 KiB
File "", line 487
File "", line 779
File "", line 674
File "", line 665
File "", line 955
File "", line 971
File "/opt/streamit_demo/lib/python3.6/site-packages/tornado/util.py", line 30
from inspect import getfullargspec as getargspec
File "", line 219
File "", line 678
File "", line 665
File "", line 955
File "", line 971
File "/opt/streamit_demo/lib/python3.6/site-packages/tornado/escape.py", line 27
from tornado.util import PY3, unicode_type, basestring_type
File "", line 219
File "", line 678
File "", line 665
File "", line 955
File "", line 971
File "/opt/streamit_demo/lib/python3.6/site-packages/tornado/log.py", line 36
from tornado.escape import _unicode
File "", line 219
File "", line 678
File "", line 665
File "", line 955
File "", line 971
File "/opt/streamit_demo/lib/python3.6/site-packages/tornado/concurrent.py", line 38
from tornado.log import app_log



1670 memory blocks: 142.8 KiB
File "", line 487
File "", line 779
File "", line 674
File "", line 665
File "", line 955
File "", line 971
File "/opt/streamit_demo/lib/python3.6/site-packages/tornado/util.py", line 48
import typing # noqa
File "", line 219
File "", line 678
File "", line 665
File "", line 955
File "", line 971
File "/opt/streamit_demo/lib/python3.6/site-packages/tornado/escape.py", line 27
from tornado.util import PY3, unicode_type, basestring_type
File "", line 219
File "", line 678
File "", line 665
File "", line 955
File "", line 971
File "/opt/streamit_demo/lib/python3.6/site-packages/tornado/log.py", line 36
from tornado.escape import _unicode
File "", line 219
File "", line 678
File "", line 665
File "", line 955
File "", line 971
File "/opt/streamit_demo/lib/python3.6/site-packages/tornado/concurrent.py", line 38
from tornado.log import app_log



1255 memory blocks: 132.2 KiB
File "", line 219
File "", line 922
File "", line 571
File "", line 658
File "", line 955
File "", line 971
File "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/ssl.py", line 101
import _ssl # if we can't import it, let the error propagate
File "", line 219
File "", line 678
File "", line 665
File "", line 955
File "", line 971
File "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/asyncio/selector_events.py", line 16
import ssl
File "", line 219
File "", line 678
File "", line 665
File "", line 955
File "", line 971
File "", line 219
File "", line 1023
File "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/asyncio/unix_events.py", line 21
from . import selector_events
File "", line 219
File "", line 678
File "", line 665
File "", line 955



1303 memory blocks: 122.3 KiB
File "", line 487
File "", line 779
File "", line 674
File "", line 665
File "", line 955
File "", line 971
File "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/ssl.py", line 93
import ipaddress
File "", line 219
File "", line 678
File "", line 665
File "", line 955
File "", line 971
File "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/asyncio/selector_events.py", line 16
import ssl
File "", line 219
File "", line 678
File "", line 665
File "", line 955
File "", line 971
File "", line 219
File "", line 1023
File "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/asyncio/unix_events.py", line 21
from . import selector_events
File "", line 219
File "", line 678
File "", line 665
File "", line 955



1179 memory blocks: 112.9 KiB
File "", line 487
File "", line 779
File "", line 674
File "", line 665
File "", line 955
File "", line 971
File "/opt/streamit_demo/lib/python3.6/site-packages/tornado/ioloop.py", line 41
import logging
File "", line 219
File "", line 678
File "", line 665
File "", line 955
File "", line 971
File "/Users/rkfeng/code/streamit_demo/demo_memory/server.py", line 6
import tornado.ioloop



1675 memory blocks: 100.1 KiB
File "", line 487
File "", line 779
File "", line 674
File "", line 665
File "", line 955
File "", line 971
File "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/calendar.py", line 10
import locale as _locale
File "", line 219
File "", line 678
File "", line 665
File "", line 955
File "", line 971
File "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/email/_parseaddr.py", line 16
import time, calendar
File "", line 219
File "", line 678
File "", line 665
File "", line 955
File "", line 971
File "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/email/utils.py", line 33
from email._parseaddr import quote
File "", line 219
File "", line 678
File "", line 665
File "", line 955
File "", line 971
File "/opt/streamit_demo/lib/python3.6/site-packages/tornado/web.py", line 65
import email.utils
```

通过输出结果可以找到内存占用最大的代码段为：

```
class BadHandler(tornado.web.RequestHandler):
    memory_list = [i for i in range(1000000)]
```

## 进阶

参考[官方文档](https://docs.python.org/3/library/tracemalloc.html), 

常见的应用：

- 展示分配内存最多的前 n 个 py 文件(Display the 10 files allocating the most memory)
- 比较两次快照之间的内存差别(Compute differences: Take two snapshots and display the differences)
- 显示最大内存块回溯的代码(Get the traceback of a memory block)
