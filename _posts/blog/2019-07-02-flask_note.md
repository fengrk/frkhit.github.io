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

### 1.3 图片处理

```
from io import BytesIO

import numpy as np
import requests
from PIL import Image
from flask import Flask, request, make_response

@app.route("/", methods=["POST", 'GET'])
def search_image():
    url = request.args.get("url") or request.form.get("url")
    if not url:
        response = make_response("OK", 200)
    else:
        try:
            # load image
            raw_image_response = requests.get(url=url, timeout=10)

            # do something
            image = Image.open(BytesIO(raw_image_response.content))
            new_image_obj = image

            # response
            new_image_bytes = BytesIO()
            new_image_obj.save(new_image_bytes, 'JPEG')
            response = make_response(new_image_bytes.getvalue())
            response.headers['Content-Type'] = "image/jpeg"
        except Exception as e:
            print(e)
            response = make_response("error {}".format(e), 200)

    return response

```