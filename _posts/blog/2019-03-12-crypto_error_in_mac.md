---
layout: post
title: No module named 'Crypto' on Mac
category: 技术
tags: mac
keywords:
description: 
---

# No module named 'Crypto' on Mac

# 问题 
在mac中，为新项目配置python环境，运行时报错:

```
...
from Crypto.Cipher import AES
ImportError: No module named Crypto.Cipher
```
# 原因及解决方法
原来，mac中提供Crypto模块的包，有`Crypto`，`pycrypto`,`pycryptodome`等。这些包同时安装，会产生冲突。解决方法是只保留一个包，这里建议保留`pycryptodome`。

列出所有crypto包，确认原因:

```
python -m pip list | grep rypto

```

只保留一个包:

```
python -m pip uninstall crypto
python -m pip uninstall pycrypto
python -m pip uninstall pycryptodome

python -m pip install pycryptodome
```





