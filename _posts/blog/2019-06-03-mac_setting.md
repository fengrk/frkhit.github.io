---
layout: post
title: mac 配置
category: 技术
tags: mac, osx
keywords: 
description: 
---

# mac 配置

## 1. 系统配置

### 1.1 禁用 git-credential-osxkeychain

```
git config --local credential.helper && git config --local --unset credential.helper
git config --global credential.helper && git config --global --unset credential.helper
git config --system credential.helper && git config --system --unset credential.helper
```

### 1.2 brew 加速

参考[Homebrew国内加速](https://www.noonme.com/post/2017/03/homebrew-speed-up/)

替换Homebrew默认源

```
# 替换brew.git:
cd "$(brew --repo)" && git remote set-url origin https://mirrors.ustc.edu.cn/brew.git

# 替换homebrew-core.git:
cd "$(brew --repo)/Library/Taps/homebrew/homebrew-core" && git remote set-url origin https://mirrors.ustc.edu.cn/homebrew-core.git

brew update

```

替换Homebrew Bottles源

```
echo 'export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles' >> ~/.bash_profile
source ~/.bash_profile
```


## 2. python 环境安装

### 2.1 安装 `mysqlclient`

执行 `pip3 install mysqlclient` 报错：
```
    ERROR: /bin/sh: mysql_config: command not found
```

解决方法参考[stackoverflow](https://stackoverflow.com/questions/25459386/mac-os-x-environmenterror-mysql-config-not-found):

- `brew install mysql`
- `export PATH=$PATH:/usr/local/mysql/bin`
- `pip3 install mysqlclient`

### 2.2 安装 `cheat`

``` brew install cheat ```

测试
```
cheat xargs
cheat less
```
