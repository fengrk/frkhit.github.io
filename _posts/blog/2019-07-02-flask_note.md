---
layout: post
title: flask 笔记
category: 技术
tags: python,  flask
keywords: 
description: 
---

# flask学习笔记

## 1. 响应

### 1.1 展示文本

```
from flask import make_response

@app.route('/')
def hello():
    response = make_response("文本内容!")
    response.headers["Content-Type"] = "text/plain;charset=UTF-8"
    return response
```

### 1.2  下载 txt

```
from flask import make_response

@app.route('/')
def hello():
    response = make_response("文本内容!")
    # response.headers['Content-Type'] = "text/plain"
    response.headers['Content-Disposition'] = "attachment; filename=download.txt"
    return response
```
