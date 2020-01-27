---
layout: post
title: ubuntu16.04中安装wine-qq
category: 技术
tags: 
    - ubuntu
    - wine
keywords: 
description: 
---

# ubuntu16.04中安装wine-qq

## 1.安装wine3.0+winetricks

按照[方法](https://github.com/frkhit/frkhit.github.io/blob/master/project/pages/2018/01/31/install_wine3.0_and_winetricks.md)安装环境。


## 2.安装wine-qq

根据[Wine-QQ-TIM](https://github.com/askme765cs/Wine-QQ-TIM)项目，安装wine-qq.

```
git clone https://github.com/askme765cs/Wine-QQ-TIM

cd Wine-QQ-TIM/Wine-QQ8.9.3 && sudo ./Install.sh

```

在系统的程序菜单中找到QQ，打开即可。

## 3.体验
环境： ubuntu16.04 + fcitx + 搜狗拼音 + wine3.0 + TIM8.9.3

安装成功：

- 安装一步到位，中间没有报错。
- 输入法正常，能正常收发图片，文件。
