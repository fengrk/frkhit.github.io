---
layout: post
title:  使用 cProfile 和 gprof2dot 优化代码
category: 技术
tags:  
    - python
keywords: 
description: 
---

# 使用 cProfile 和 gprof2dot 优化代码


## 1. 环境准备

```shell script

# mac
brew install graphviz  # 提供 dot 命令
python3 -m pip install gprof2dot

```

## 2. 耗时程序优化

耗时程序 `slow.py` : 

```python
import time

def do_job(count):
    for index in range(count):
        time.sleep(0.1)
        print(index)


def main():
    print("starting...")
    do_job(count=10)
    print("finished!")


if __name__ == '__main__':
    main()

```

耗时程序 `quick.py` : 

```python
import time

def do_job(count):
    for index in range(count):
        time.sleep(0.01)
        print(index)


def main():
    print("starting...")
    do_job(count=10)
    print("finished!")


if __name__ == '__main__':
    main()

```

分析慢程序:

```shell script
python -m cProfile -o slow.pstats slow.py
python -m gprof2dot -f pstats slow.pstats | dot -Tpng -o slow.png
```

慢程序的结果如下, 耗时瓶颈在 `do_job` 中的 `time.sleep`

![慢程序cpu 耗时分析](../../../../public/img/cprofile_gprof2dot/slow.png)


分析快程序:

```shell script
python -m cProfile -o quick.pstats slow.py
python -m gprof2dot -f pstats quick.pstats | dot -Tpng -o quick.png
```

快程序的结果如下, 耗时瓶颈在 `do_job` 中的 `time.sleep`, 但 `time.sleep` 的耗时占比已经下降.

![快程序cpu 耗时分析](../../../../public/img/cprofile_gprof2dot/quick.png)



