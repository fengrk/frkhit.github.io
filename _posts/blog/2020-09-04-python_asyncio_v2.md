---
layout: post
title:  python asyncio 使用总结(2)
category: 技术
tags:  
    - python
keywords: 
description: 
---

# python asyncio 使用总结(2)

## 1. 使用线程池异步执行阻塞过程

由于所有协程过程是在同一个线程中执行的, 阻塞步骤会阻塞所有协程的执行.

官方文档[Executing code in thread or process pools](https://docs.python.org/3/library/asyncio-eventloop.html#executing-code-in-thread-or-process-pools), 推荐使用线程池执行阻塞步骤:

```python
import asyncio
import concurrent.futures

def blocking_io():
    # File operations (such as logging) can block the
    # event loop: run them in a thread pool.
    with open('/dev/urandom', 'rb') as f:
        return f.read(100)

def cpu_bound():
    # CPU-bound operations will block the event loop:
    # in general it is preferable to run them in a
    # process pool.
    return sum(i * i for i in range(10 ** 7))

async def main():
    loop = asyncio.get_running_loop()

    ## Options:

    # 1. Run in the default loop's executor:
    result = await loop.run_in_executor(
        None, blocking_io)
    print('default thread pool', result)

    # 2. Run in a custom thread pool:
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(
            pool, blocking_io)
        print('custom thread pool', result)

    # 3. Run in a custom process pool:
    with concurrent.futures.ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(
            pool, cpu_bound)
        print('custom process pool', result)

asyncio.run(main())
```
