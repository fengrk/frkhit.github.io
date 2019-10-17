---
layout: post
title:  mac下 python 报错 CERTIFICATE_VERIFY_FAILED
category: 技术
tags:  python, mac, ssl
keywords: 
description: 
---

#  mac下 python 报错 CERTIFICATE_VERIFY_FAILED


python 下载时， 报错如下：

```
ERROR: Unable to download webpage: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:581)> (caused by URLError(SSLError(1, u'[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:581)'),))

```

多方搜索，得到错误原因[urllib and “SSL: CERTIFICATE_VERIFY_FAILED” Error](https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error/42334357#42334357)

根据 [Craig Glennie](https://stackoverflow.com/users/471811/craig-glennie)分析如下：

```
This isn't a solution to your specific problem, but I'm putting it here because this thread is the top Google result for "SSL: CERTIFICATE_VERIFY_FAILED", and it lead me on a wild goose chase.

If you have installed Python 3.6 on OSX and are getting the "SSL: CERTIFICATE_VERIFY_FAILED" error when trying to connect to an https:// site, it's probably because Python 3.6 on OSX has no certificates at all, and can't validate any SSL connections. This is a change for 3.6 on OSX, and requires a post-install step, which installs the certifi package of certificates. This is documented in the ReadMe, which you should find at /Applications/Python\ 3.6/ReadMe.rtf

The ReadMe will have you run this post-install script, which just installs certifi: /Applications/Python\ 3.6/Install\ Certificates.command

Release notes have some more info: https://www.python.org/downloads/release/python-360/

```

解决方法：

步骤 1： 重新安装 `certifi`: `pip3 install certifi`

步骤 2： 执行 `/Applications/Python\ 3.6/Install\ Certificates.command`
