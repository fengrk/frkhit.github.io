---
layout: post
title: python异步服务器测试
category: 技术
tags: python
keywords: 
description: 
---

# python异步服务器测试

## 1. 安装AB进行压力测试
### 1.1 准备环境
mac 安装AB, [参考](https://gist.github.com/safecat/f450ce5ed5a51b3b6f32):
``` 
curl -OL http://ftpmirror.gnu.org/libtool/libtool-2.4.2.tar.gz
tar -xzf libtool-2.4.2.tar.gz
cd libtool-2.4.2
./configure && make && sudo make install

# brew install 'https://raw.github.com/simonair/homebrew-dupes/e5177ef4fc82ae5246842e5a544124722c9e975b/ab.rb'
# brew test ab

curl -O https://archive.apache.org/dist/httpd/httpd-2.4.2.tar.bz2
tar zxvf httpd-2.4.2.tar.bz2
cd httpd-2.4.2.tar.bz2
./configure && make && make install
```

### 1.2 客户端测试代码
``` 

ab -n 10 -c 1 http://localhost:8000/
ab -n 10 -c 2 http://localhost:8000/
ab -n 10 -c 5 http://localhost:8000/
ab -n 10 -c 10 http://localhost:8000/


ab -n 100 -c 10 http://localhost:8000/
ab -n 100 -c 20 http://localhost:8000/
ab -n 100 -c 50 http://localhost:8000/
ab -n 100 -c 100 http://localhost:8000/

```

## 2. tornado测试
### 2.1 tornado服务端代码
```
from concurrent.futures import ThreadPoolExecutor
import tornado
from tornado.concurrent import run_on_executor
from tornado.web import RequestHandler
import time


class SimpleAsyncServer(RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(SimpleAsyncServer, self).__init__(application, request, **kwargs)
        self.executor = ThreadPoolExecutor(10)

    @tornado.gen.coroutine
    def get(self, ):
        print("on get...")
        result = yield self._do_something()

        self.write(result)

    @run_on_executor
    def _do_something(self, ):
        """
            模拟耗时操作
        :return:
        """
        time.sleep(5)
        return {"msg": "OK"}


def make_app():
    return tornado.web.Application([
        (r"/", SimpleAsyncServer),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()

```

### 2.2 测试结果

请求总数 | 并发数 |   ab总耗时(s) 
-----|-----|-----| 
10 | 1 | 50.0 
10 | 2 | 30.0
10 | 5 | 15.0
10 | 10 | 10.0
100 | 10 | 55.1
100 | 20 | 30.0
100 | 50 | 15.1
100 | 100 | 10.1

