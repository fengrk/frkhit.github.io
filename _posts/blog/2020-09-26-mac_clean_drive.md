---
layout: post
title: 释放 mac 磁盘空间
category: 技术
tags: 
    - mac
keywords: 
description: 
---

# 释放 mac 磁盘空间

## 1. 彻底删除软件

[参考: 如何彻底卸载在 Mac 上安装的一个软件？ - 新垣結衣的回答 - 知乎](https://www.zhihu.com/question/19551885/answer/229372713)

```
通过 关于本机 - 储存空间 - 管理 - 检查文件 - 左边栏中的应用程序按钮来进行删除.
```

同时, 删除应用目录:

``` 
rm ~/Library/Application\ Support/<应用目录>

```

## 磁盘释放流程

先借助 `关于本机 - 储存空间 - 管理 - 检查文件` , 处理大文件.

如果大文件处理完, 还需要释放磁盘, 可以执行:

``` 
# 判断 当前用户下, 目录大小
>> cd ~
>> du -sh * | grep G

2.9G    Downloads
 40G    Library
2.1G    OneDrive
 17G    Pictures
6.8G    data


# 进入占用磁盘大的目录, 如 Library, 重复执行上述动作
>> cd Library
>> du -sh * | grep G

15G    Android
8.1G    Application Support
4.5G    Caches
8.1G    Containers
3.9G    Developer
  0B    GameKit
4.8M    Google
 95M    Group Containers

```

