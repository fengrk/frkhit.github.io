---
layout: post
title:  charles over proxy
category: 技术
tags:  
    - charles
    - proxy
    - android
keywords: 
description: 
---

# charles over proxy

使用 charles 对安卓应用进行抓包时，会遇到部分应用必须使用代理才能上网的问题。

解决思路是， charles外接代理。原理如下所示：

```
Android App  -->  charles --> other proxy --> internet 
```

具体操作如下：

- 安卓中设置 charles 提供的代理，以便抓包
- charles 中设置外部代理，设置方法为依次展开`Proxy --> External Proxy Settings...`, 填写外部代理即可。
