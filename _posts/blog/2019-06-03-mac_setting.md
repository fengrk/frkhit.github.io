---
layout: post
title: mac 配置
category: 技术
tags: 
    - mac
    - osx
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

### 1.3 terminal 颜色配置

使用 `Solarized` 为 mac OS 配色.

到 `Solarized` 官网下载软件, 解压后, 在 `solarized/osx-terminal.app-colors-solarized` 文件夹下双击`Solarized Dark ansi.terminal`  和 `Solarized Light ansi.terminal` 就会自动将Solarized的两种主题导入到Terminal.app中.

在 terminal 中选择 `Solarized Dark` 为默认配置即可.

`vscode` 中也可以选择 `Solarized Dark` 作为主题色.

[参考](http://blog.seventhsense.cn/2017/04/05/%E5%9C%A8Mac-OS%E7%BB%88%E7%AB%AF%E4%B8%AD%E4%BD%BF%E7%94%A8Solarized%E9%85%8D%E8%89%B2%E6%96%B9%E6%A1%88/)


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

## 3. 安装常用软件

### 3.1 安装 redis-cli

```
brew tap ringohub/redis-cli

brew update && brew doctor

brew install redis-cli
```

### 3.2 系统命令

```
# tac
alias tac='tail -r '


```

[参考](https://stackoverflow.com/a/55733092/5588431)


