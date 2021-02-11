---
layout: post
title: 协程开发下处理 tornado websocket 关闭事件
category: 技术
tags: 
    - python
    - tornado
keywords: 
description: 
---

# 协程开发下处理 tornado websocket 关闭事件

验证代码如下: 

```python
import asyncio
import logging  # noqa
import os  # noqa
import typing  # noqa
import unittest
from threading import Thread

import arrow
import tornado.httpserver
import tornado.ioloop
import tornado.web
import websockets
from tornado.websocket import WebSocketHandler


class _Ws(WebSocketHandler):

    def check_origin(self, origin):
        """校验权限"""
        return True

    async def open(self):
        """开启连接"""
        print("on open")

    async def on_message(self, message):
        """连接通信"""
        print(f"on_message: {message}")


class WsHandler(_Ws):

    def on_close(self):
        """关闭连接"""
        print("on_closed")


def server(ws_handler_cls):
    asyncio.set_event_loop(asyncio.new_event_loop())

    app = tornado.web.Application(
        handlers=[
            (r'/ws', ws_handler_cls),
        ],
    )
    app.listen(8004)
    tornado.ioloop.IOLoop.instance().start()


class TestWs(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def _req(self):
        """ """

        async def main():
            # 这些命令, 有问题
            version = arrow.now().to("local").format("YYYY-MM-DD HH:mm:ss")
            async with websockets.connect("ws://localhost:8004/ws") as ws:
                await ws.send(f"[{version}]start")
                await asyncio.sleep(2)
                await ws.send(f"[{version}]stop")

        for _ in range(5):
            asyncio.run(main())

    def testBasic(self):
        """ 非协程环境下, websocket 能接收到 关闭 事件 """
        Thread(target=server, args=(WsHandler,), daemon=True).start()

        self._req()

    def testAsyncioBad(self):
        """ 协程环境下, 使用 async def on_close 无法接收到 关闭 事件 """

        class Ws(_Ws):
            async def on_close(self):
                """关闭连接"""
                print("on_closed")
                await asyncio.sleep(1)
                print("print_close")

        Thread(target=server, args=(Ws,), daemon=True).start()

        self._req()

    def testAsyncioGood(self):
        """ 协程环境下, 使用 asyncio.ensure_future 能接收到 关闭 事件 """

        class Ws(_Ws):
            async def _close(self):
                """ """
                await asyncio.sleep(1)
                print("print_close")

            def on_close(self):
                """关闭连接"""
                print("on_closed")

                asyncio.ensure_future(self._close())

        Thread(target=server, args=(Ws,), daemon=True).start()

        self._req()

````

结论:

1) 协程环境下, 可以使用 async def get/on_message 等方法, 将接口方法变为  awaitable 方法. 但 on_close 不能使用这个样的方式处理

2) 协程方式执行on_close方法, 需要在方法内部, 使用 `asyncio.ensure_future`
