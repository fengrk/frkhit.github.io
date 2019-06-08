---
layout: post
title: 定时备份linux系统的history记录
category: 技术
tags: python, linux
keywords: 
description: 
---

# 定时备份linux系统的history记录

# 1. `~`下新建`backup_history.py`文件
代码为

```
# -*- coding:utf-8 -*-

import os
import shutil
import time
from subprocess import Popen, PIPE, STDOUT


def backup_linux_history(target_file_path):
    def list_history_lines():
        cmd = Popen("bash -i -c  'history -r;history' ", shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        return [_line.decode("utf-8") for _line in cmd.stdout.readlines()]

    def can_connect(first_list, second_list):
        if not first_list or len(second_list) < len(first_list):
            return False

        for _index, _value in enumerate(first_list):
            if second_list[_index] != _value:
                return False

        return True

    def get_start_connect_line_index(history_line_list, ):
        # total count
        _total_count = 0
        with open(target_file_path, "r", encoding="utf-8") as f:
            for _ in f:
                _total_count += 1

        # start checking line index
        _history_line_count = len(history_line_list)
        if _total_count <= _history_line_count:
            _start_checking_line_index = 0
        else:
            _start_checking_line_index = _total_count - _history_line_count

        # calc
        _line_index = 0
        with open(target_file_path, "r", encoding="utf-8") as f:
            # skip not checking lines
            if _start_checking_line_index > 0:
                for _ in f:
                    _line_index += 1
                    if _line_index >= _start_checking_line_index:
                        break

            _target_checking_lines = [" ".join(_line.lstrip(" ").rstrip("\n").split(" ")[1:]) for _line in f]

        _history_checking_lines = [" ".join(_line.lstrip(" ").rstrip("\n").split(" ")[1:]) for _line in
                                   history_line_list]

        _current_total_index = _line_index
        for _index, _line in enumerate(_target_checking_lines):
            _current_total_index = _index + _line_index
            if can_connect(_target_checking_lines[_index:], _history_checking_lines):
                return _current_total_index

        return _current_total_index

    history_lines = list_history_lines()
    start_connect_line_index = get_start_connect_line_index(history_lines)
    tmp_target_file_path = target_file_path + ".{}.tmp".format(int(time.time()))

    with open(tmp_target_file_path, "w", encoding="utf-8") as fw:
        with open(target_file_path, "r", encoding="utf-8") as fr:
            for line_index, line in enumerate(fr):
                if line_index >= start_connect_line_index:
                    break
                fw.write(line)

        for line in history_lines:
            fw.write(line)

    shutil.move(tmp_target_file_path, target_file_path)


if __name__ == '__main__':
    backup_linux_history(os.path.join(os.path.expanduser("~"), "history.all.log"))

```
# 2. 设置定时任务
通过`crontab -e`添加任务：

```
*/15 * * * * python ~/backup_history.py
```

