---
layout: post
title: tornado使用总结
category: 技术
tags: tornado
keywords: 
description: 
---

# tornado使用总结

## 1. 请求参数解析
- 获取请求消息体: `self.request.body`
- 获取请求参数(query, form-data, ...): `self.get_argument("name", None) # 必须指定默认值, 不然找不到key时会触发异常`
- 获取请求参数列表(query, form-data, ...): `self.get_arguments("name[]") # 找不到key, 返回空列表; 不能设置默认值`

## 2. 异步/并发
使用线程池+`yield`实现异步:

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
```

## 3. 先响应再执行后续操作
处理一个请求时, 可以显式调用`self.finish()`, 向客户端返回响应, 接着在服务端继续处理剩下的记录日志等业务.

如:

``` 
def post(self, ):
    # 写入响应内容
    self.write({"code": 200, "msg": "OK"})
    
    # 返回响应: 客户端能拿到结果
    self.finish()
    
    # 处理剩下的业务
    self.logger.info("logging request...")
    time.sleep(60)
    self.logger.info("done!")
```

## 4. 返回响应

### 返回json
返回json结果, 最简单的方法是直接把`dict`传给`self.write(dict_obj)`, `self.write`会在内部将响应内容转为`str`, 并设置`header`.

实际使用的过程中, 遇到过客户端解析结果, 因为单/双引号问题, 导致json解析错误. 为降低风险, 直接这样调用:

``` 
self.set_header("Content-Type", "application/json; charset=UTF-8")
self.write(json.dumps(result))
```

### 返回二进制数据
有时候为了方便测试, 会在响应中直接返回二进制内容.

如服务端直接返回`pickle`序列化后的数据:
```         
self.write(pickle.dumps(data))
```

客户端可以这样解析:
```
import pickle
import requests
response = requests.post(xxx)
data = pickle.loads(response.content) # object
```