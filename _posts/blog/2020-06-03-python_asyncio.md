---
layout: post
title:  python asyncio 使用总结
category: 技术
tags:  
    - python
keywords: 
description: 
---

# python asyncio 使用总结

## 1. 多次创建 `event_loop`

```python 

import asyncio

async def main():
    while True:
        await asyncio.sleep(10)

def run():
    event_loop = asyncio.new_event_loop()
    event_loop.run_until_complete(main())
    del event_loop


for _ in range(100):
    run()

```

## 2. `This event loop is already running`

```python

import asyncio
import unittest

import aiohttp


class TestAsync(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    async def _async_as_http_client(self, count=10):
        """ """

        async def call_web(url):
            async with aiohttp.request("GET", url=url) as r:
                content = (await r.json())["args"]["a"]
                print("[url {}]content is {}".format(url, content))

        url_list = []
        for i in range(count):
            url_list.append("http://httpbin.org/get?a={}".format("X{}".format(i)))

        await asyncio.gather(
            *[call_web(url) for url in url_list]
        )
        return url_list

    def testEventLoopWithAiohttp(self):
        """ """

        async def http_client():
            await self._async_as_http_client(count=5)

        async def main():
            for _ in range(3):
                await asyncio.sleep(3)
                await self._async_as_http_client(count=3)

        def run(task):
            event_loop = asyncio.new_event_loop()
            event_loop.run_until_complete(task())
            del event_loop

        run(task=http_client)
        run(task=main)

    def testAiohttpClient(self):
        """ """

        loop = asyncio.get_event_loop()
        result_list = loop.run_until_complete(self._async_as_http_client(count=10))

        print("result is {}".format(result_list))

```

## 3. 非协程方法内调用协程方法

```python
import asyncio
import logging  # noqa
import os  # noqa
import time
import typing  # noqa
import unittest


async def async_fun():
    await asyncio.sleep(1)
    print("async_fun done!")


def fun():
    asyncio.ensure_future(async_fun())
    print("fun")


class TestAsyncFunc(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def testWithoutAsyncLoop(self):
        """ """
        fun()
        time.sleep(5)

        # output:
        # fun

    def testWitAsyncLoop(self):
        """ """

        async def main():
            await asyncio.sleep(1)
            fun()
            await asyncio.sleep(5)

        asyncio.run(main())

        # output:
        # fun
        # async_fun done!


```
