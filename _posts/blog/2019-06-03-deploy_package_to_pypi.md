---
layout: post
title: 发布自己的 python 包
category: 技术
tags: 
    - python
    - pypi
    - travis
keywords: 
description: 
---

# 发布自己的 python 包

## 1. 新建 python 包

具体可参考: [pyxtools](https://github.com/frkhit/pyxtools)

假设已经成功新建一个名为 `my-py-package` 的 python 包。


## 2. 发布

- pypi 中注册账号，假设用户名 为 `py-user`
- 安装 twine: `python -m pip install twine`
- 打包: `python setup.py sdist bdist_wheel`
- 上传: `twine upload dist/*`
- 到 pypi 中确认包是否存在

## 3. travis + github 自动发布

在项目下新建 `.travis.yml` 文件：

```
language: python
python:
  - '3.6'
  - '2.7'
  - '3.4'
  - '3.5'
install:
- pip install .
script:
- python -c "import os;"
deploy:
  provider: pypi
  user: py-user
  skip_cleanup: true
  skip_existing: true
  twine_version: 1.13.0
  distributions: "sdist bdist_wheel"
  on:
    tags: true
    python: 3.6
    branch: master
```
注意:
- `distributions: "sdist bdist_wheel"` 的目的是同时生成 whl 文件
- `tags: true`表示新建标签时触发代码发布


加密 pypi 密码: 

```
pip install travis-encrypt

travis-encrypt --deploy py-user my-py-package .travis.yml
```

master 分支 新建标签后，会自动触发包上传。

如果包上传失败，可以到 travis 网站中查看错误日志。

## 参考

- [上传并发布你自己发明的轮子 - Python PyPI 实践](https://betacat.online/posts/2017-03-09/upload-your-pypi-package/)
- [使用github+travis将Python包部署到Pypi](https://juejin.im/post/5b587d375188251b186bca6a)
