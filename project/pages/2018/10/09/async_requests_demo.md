# asyncio异步请求示例

# 1. 不返回结果
参考:[Python并发编程](https://www.jianshu.com/p/675d2cdf7965)
测试代码：

```
from __future__ import absolute_import

"""
ref: https://www.jianshu.com/p/675d2cdf7965
"""
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

import aiohttp
import requests

NUMBERS = range(50)
MAX_THREAD_OR_SEMA = 10
URL = 'http://httpbin.org/get?a={}'


def bare_requests():
    def fetch(a):
        r = requests.get(URL.format(a))
        return r.json()['args']['a']

    start = time.time()
    for num in NUMBERS:
        print('fetch({}) = {}'.format(num, fetch(num)))

    print('Use requests cost: {}'.format(time.time() - start))


def threadpool_requests():
    def fetch(a):
        r = requests.get(URL.format(a))
        return r.json()['args']['a']

    start = time.time()
    with ThreadPoolExecutor(max_workers=MAX_THREAD_OR_SEMA) as executor:
        for num, result in zip(NUMBERS, executor.map(fetch, NUMBERS)):
            print('fetch({}) = {}'.format(num, result))

    print('Use requests+ThreadPoolExecutor cost: {}'.format(time.time() - start))


def aiohttp_asyncio():
    async def fetch_async(a):
        async with aiohttp.request('GET', URL.format(a)) as r:
            data = await r.json()
        return data['args']['a']

    start = time.time()
    event_loop = asyncio.get_event_loop()
    tasks = [fetch_async(num) for num in NUMBERS]
    results = event_loop.run_until_complete(asyncio.gather(*tasks))
    for num, result in zip(NUMBERS, results):
        print('fetch({}) = {}'.format(num, result))

    print('Use aiohttp+asyncio cost: {}'.format(time.time() - start))


def aiohttp_asyncio_sema():
    async def fetch_async(a):
        async with aiohttp.request('GET', URL.format(a)) as r:
            data = await r.json()
        return data['args']['a']

    sema = asyncio.Semaphore(MAX_THREAD_OR_SEMA)

    async def print_result(a):
        with (await sema):
            r = await fetch_async(a)
            print('fetch({}) = {}'.format(a, r))

    start = time.time()
    loop = asyncio.get_event_loop()
    f = asyncio.wait([print_result(num) for num in NUMBERS])
    loop.run_until_complete(f)
    print('Use aiohttp+asyncio+semaphore cost: {}'.format(time.time() - start))


if __name__ == '__main__':
    bare_requests()  # 25.6s
    threadpool_requests()  # 2.9s
    aiohttp_asyncio()  # 0.7s
    aiohttp_asyncio_sema()  # 2.5

```

# 2.返回结果
参考:[Python并发编程](https://www.jianshu.com/p/675d2cdf7965)
代码:

```
from __future__ import absolute_import

"""
ref: https://www.jianshu.com/p/675d2cdf7965
"""
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

import aiohttp
import requests

NUMBERS = range(50)
MAX_THREAD_OR_SEMA = 10
URL = 'http://httpbin.org/get?a={}'


def bare_requests():
    def fetch(a):
        r = requests.get(URL.format(a))
        return r.json()['args']['a']

    start = time.time()
    result_list = []
    for num in NUMBERS:
        result_list.append('fetch({}) = {}'.format(num, fetch(num)))

    print("len of result is {}, result list is {}".format(len(result_list), result_list))
    print('Use requests cost: {}'.format(time.time() - start))


def threadpool_requests():
    def fetch(a):
        r = requests.get(URL.format(a))
        return r.json()['args']['a']

    start = time.time()
    result_list = []
    with ThreadPoolExecutor(max_workers=MAX_THREAD_OR_SEMA) as executor:
        for num, result in zip(NUMBERS, executor.map(fetch, NUMBERS)):
            result_list.append('fetch({}) = {}'.format(num, result))

    print("len of result is {}, result list is {}".format(len(result_list), result_list))
    print('Use requests+ThreadPoolExecutor cost: {}'.format(time.time() - start))


def aiohttp_asyncio():
    async def fetch_async(a):
        async with aiohttp.request('GET', URL.format(a)) as r:
            data = await r.json()
        return data['args']['a']

    start = time.time()
    result_list = []
    event_loop = asyncio.get_event_loop()
    tasks = [fetch_async(num) for num in NUMBERS]
    results = event_loop.run_until_complete(asyncio.gather(*tasks))
    for num, result in zip(NUMBERS, results):
        result_list.append('fetch({}) = {}'.format(num, result))

    print("len of result is {}, result list is {}".format(len(result_list), result_list))
    print('Use aiohttp+asyncio cost: {}'.format(time.time() - start))


def aiohttp_asyncio_sema():
    async def fetch_async(a):
        async with aiohttp.request('GET', URL.format(a)) as r:
            data = await r.json()
        return data['args']['a']

    sema = asyncio.Semaphore(MAX_THREAD_OR_SEMA)

    start = time.time()
    result_list = []

    async def print_result(a):
        with (await sema):
            r = await fetch_async(a)
            result_list.append('fetch({}) = {}'.format(a, r))

    loop = asyncio.get_event_loop()
    f = asyncio.wait([print_result(num) for num in NUMBERS])
    loop.run_until_complete(f)

    print("len of result is {}, result list is {}".format(len(result_list), result_list))
    print('Use aiohttp+asyncio+semaphore cost: {}'.format(time.time() - start))


if __name__ == '__main__':
    bare_requests()  # 27.8s
    threadpool_requests()  # 2.5s
    aiohttp_asyncio()  # 0.7s
    aiohttp_asyncio_sema()  # 4.5s

```

