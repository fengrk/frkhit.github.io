---
layout: post
title:  python shell 命令总结
category: 技术
tags:  
    - python
    - shell
keywords: 
description: 
---

# python shell 命令总结

## fileinput 实现管道输入

`parse_time.py` 实现一个清洗时间的命令:

```
# !/usr/bin/env python3
import datetime
import fileinput
import sys


def parse_time(date_str):
    _time = datetime.datetime.strptime(date_str.strip(), "%d %b %y")
    return _time.strftime("%Y-%m-%d")


with fileinput.input() as f_input:
    for line in f_input:
        try:
            new_line = parse_time(line)
        except Exception as e:
            sys.exit(1)
        print(new_line)

sys.exit(0)

```

使用方法:

``` 
# 清洗
( echo -e "30 Nov 00\n29 May 20" | python3 parse_time.py ) && echo "success"

输出结果:
2000-11-30
2020-05-29
success

# 解析错误
( echo -e "30 abc 00\n29 May 20" | python3 parse_time.py ) || echo "failed" 

输出结果:
failed

```
