---
layout: post
title:  mac 下安装 adb 
category: 技术
tags: mac, adb, android, airtest
keywords: 
description: 
---

# mac 下安装 adb

原理， 使用 python 包 `airtest`自带的 `adb`, 实现 adb **安装**。

步骤如下：

- 安装[Airtest](https://github.com/AirtestProject/Airtest), 具体为 `pip install -U airtest`
- 为 adb 增加执行权限, `chmod +x  {your_python_path}/site-packages/airtest/core/android/static/adb/mac/adb`, 如， `{your_python_path}`为 `/opt/py35/lib/python3.5`
- 设置全局配置: 在`~/.bash_profile` 中， 添加 `export PATH=$PATH:/opt/py35/lib/python3.5/site-packages/airtest/core/android/static/adb/mac`
- adb 使用： `source ~/.bash_profile && adb devices`

注意，刚方法适用于 linux， 区别在于， linux 下的 adb 位于 `{your_python_path}/site-packages/airtest/core/android/static/adb/linux`目录下