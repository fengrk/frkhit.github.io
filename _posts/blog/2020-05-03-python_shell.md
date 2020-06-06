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

## 1. fileinput 实现管道输入

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

## 2. python 包命令

本示例演示两种命令行执行 python 包指令的方法. 源码见[python_command](https://github.com/frkhit/docker-practice/tree/master/python/python_command)

### 2.1 目标

在自建 python 包`py_package` 中, 提供两种命令执行方式:

一种是

```
python -m py_package
python -m py_package.a
```

另一种是

``` 
py_pacakge_print 
py_pacakge_print_a
```

### 2.2 实现

#### 指令一

对于第一种指令, 

命令 `python -m py_package` 实际上是运行 `py_package/__main__.py`.

命令 `python -m py_package.a` 实际上是运行 `py_package/a/__main__.py`.

所以, 提供相应的`__main__.py` 即可:

`./__main__.py`:

```python

from .cmd import cmd_demo

if __name__ == '__main__':
    cmd_demo(name="py_package")

```

`./a/__main__.py`: 

```python
from ..cmd import cmd_demo

if __name__ == '__main__':
    cmd_demo(name="py_package/a")

```

#### 指令二

对于第二种指令, 其实是在 `setup.py` 中的 `entry_points` 提供命令映射.

本例中, 可以这样设置:

```
    entry_points={
        'console_scripts': [
            'py_package_print = py_package.info:print_package',
            'py_package_print_a = py_package:print_a'
        ]
    }
```

### 2.3 结果

使用 `docker-compose` 运行实例:

``` docker-compose up ```

日志中可看到执行结果:

```
py-cmd    | exec:       python -m py_package xxxx
py-cmd    | [py_package] read input: /usr/local/lib/python3.7/site-packages/py_package/__main__.py xxxx
py-cmd    | 
py-cmd    | 
py-cmd    | exec:       python -m py_package.a yyyy
py-cmd    | [py_package/a] read input: /usr/local/lib/python3.7/site-packages/py_package/a/__main__.py yyyy
py-cmd    | 
py-cmd    | 
py-cmd    | exec:       py_package_print
py-cmd    | file in py_package/:
py-cmd    |     __main__.py
py-cmd    |     __pycache__
py-cmd    |     __init__.py
py-cmd    |     cmd
py-cmd    |     a
py-cmd    |     info.py
py-cmd    | 
py-cmd    | 
py-cmd    | 
py-cmd    | exec:       py_package_print_a
py-cmd    | file in py_package/a/:
py-cmd    |     __main__.py
py-cmd    |     __pycache__
py-cmd    |     __init__.py
py-cmd    | 

```

## 3. shell 执行 python 脚本

### 3.1 使用 `python -c` 执行 python 代码

```shell script
#!/bin/bash

python -c 'import os; print(os.environ)'

```

### 3.2 拷贝 python 源码到 shell 脚本

```shell script
#!/bin/bash

tmp_py="tmp.py"

# 代码行
cat > ${tmp_py} <<EOF
import os
print(os.environ)
EOF

# 执行
python -u ${tmp_py}

# 删除 临时 python 文件
rm ${tmp_py}

```
