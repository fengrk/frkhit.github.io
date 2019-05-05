---
layout: post
title: git使用笔记
category: 技术
tags: git
keywords: 
description: 
---

# git使用笔记

# 1.old mode 100755 new mode 100644
```
git config core.filemode false
```

# 2.换行符问题
[参考](https://juejin.im/post/5ad21df05188257cc20db9de)

原因: git为了统一入库文件统一使用'\n'为换行符. 检出时根据配置转换换行符; 入库时自动转为'\n'. 但在中文环境中,该机制出问题.

解决: 配置参数,强制保持换行符统一.

git 中有三个参数于换行符有关：
`eol`: 设置工作目录中文件的换行符，有三个值 lf, crlf 和 native（默认，同操作系统）
`autocrlf`:
- `true` 表示检出是转换CRLF, 提交时转换为 LF
- `input` 表示检出是不转换，提交时转换为 LF
- `false` 表示不做转换

`safecrlf`:
- `true` 表示不允许提交时包含不同换行符
- `warn` 则只在有不同换行符时警告
- `false` 则允许提交时有不同换行符存在

编辑 `/.git/config` 文件
```
[core]
    fileMode = false
    autocrlf = true
    safecrlf = true
```

create .gitattributes file with content:
```
# Set the default behavior, in case people don't have core.autocrlf set.
* text eol=lf
core.autocrlf=true
core.fileMode=false
```

fore change crlf if found error before `git commit`
```
 python -c "from pytools import git_crlf_helper as g;g()" -d . -t lf -i *.py -e *.pyc
```

# 3.删除历史记录
- [参考](http://www.cnblogs.com/shines77/p/3460274.html)
- 删除历史记录中的 path-to-your-remove-file

```
git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch path-to-your-remove-file' --prune-empty --tag-name-filter cat -- --all
```
- 推送至服务器
```
git push origin master --force --all
```

# 4.子模块
- 添加子模块
```
git submodule add https://github.com/tensorflow/tensorflow sub/tensorflow
```
- 更新所有子模块
```
git submodule foreach git pull
```

# 5.merge commits
- merge all commits into one on a branch
```
git merge --squash feature-branch && git commit -m "all commits"
```

# 6.github without password
- set ssh key
- `cd ./pyxtools/ && git remote set-url origin git@github.com:frkhit/pyxtools.git`

# 7.proxy
- set proxy
```
git config --global https.proxy socks5://127.0.0.1:1080
git config --global http.proxy socks5://127.0.0.1:1080
```
- clear proxy
```
git config --global --unset http.proxy
git config --global --unset https.proxy
```
- or, edit `~/.gitconfig`

# 8.multi user
实现不同项目使用不同用户, 关键是设置gitconfig文件

全局配置:
```
vim ~/.gitconfig
```

项目配置
```
vim .git/config
```

# 9.拉取所有分支
```
ref: https://stackoverflow.com/questions/10312521/how-to-fetch-all-git-branches
author: Wookie88

(git --no-pager branch -r | grep -v '\->' | while read remote; do git --no-pager branch --track "${remote#origin/}" "$remote"; done) && git fetch --all && git pull --all
```

# 10.删除所有本地分支
参考:[GIT本地删除除master以外所有分支](https://blog.csdn.net/huuinn/article/details/78167873)

```
git checkout master && (git --no-pager branch | grep -v "master" | xargs git branch -D)
```
**Note:**
- 要求无修改
- 本地分支仅保留 master

更新所有分支:
```
git checkout master && (git --no-pager branch | grep -v "master" | xargs git branch -D) && (git --no-pager branch -r | grep -v '\->' | while read remote; do git --no-pager branch --track "${remote#origin/}" "$remote"; done) && git fetch --all && git pull --all
```

# 11.标签操作
- 新建标签: `git tag <tag_name>`
- 删除标签: `git tag -d <tag_name>`
- 查看所有标签: `git tag --list`
- 将标签推送到远程服务器: `git push --tags`
- 删除远程标签: `git push origin --delete tag <tag-name>`



