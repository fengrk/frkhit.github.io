---
layout: post
title: 在ubuntu16.04中安装wine3.0+winetricks
category: 技术
tags: 
    - ubuntu
    - wine
keywords: 
description: 
---

# 在ubuntu16.04中安装wine3.0+winetricks

## 1.新建install_wine.sh脚本

```
# install wine 3.0
cd ~
sudo dpkg --add-architecture i386 
wget -nc https://dl.winehq.org/wine-builds/Release.key
sudo apt-key add Release.key
sudo apt-add-repository https://dl.winehq.org/wine-builds/ubuntu/
sudo apt-add-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ xenial main'
sudo apt-get update
sudo apt-get install --install-recommends winehq-stable

# install winetricks
wget https://raw.githubusercontent.com/Winetricks/winetricks/master/src/winetricks
chmod +x winetricks
sudo mv winetricks /usr/local/bin
```

## 2.执行代码

```
sudo chmod +x install_wine.sh

```
