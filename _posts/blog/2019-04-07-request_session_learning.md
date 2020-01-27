---
layout: post
title: session请求示例
category: 技术
tags: 
    - python
    - session
    - tornado
    - requests
    - scrapy
keywords: 
description: 
---

# session请求示例

## 1. requests session
`requests`自带`session`管理, 示例:
```
import json
import requests

with requests.Session() as session:
    session.get('https://httpbin.org/cookies/set/sessioncookie/123456789')
    r = session.get('https://httpbin.org/cookies')
    assert r.status_code == 200
    assert json.loads(r.text)["cookies"]["sessioncookie"] == "123456789"
```

## 2. scrapy session
`scrapy`使用`cookiejar`管理`session`. [参考](https://doc.scrapy.org/en/latest/topics/downloader-middleware.html?highlight=cookiejar#multiple-cookie-sessions-per-spider).

```
def start_first_page(self, ):
   yield scrapy.Request("https://httpbin.org/cookies/set/sessioncookie/123456789", meta={'cookiejar': 0},
        callback=self.parse_second_page)
        
def parse_second_page(self, response):
    return scrapy.Request("https://httpbin.org/cookies",
        meta={'cookiejar': response.meta['cookiejar']},
        callback=self.parse_other_page)
```

## 3. tornado client + session

`tornado`本身不带`session`模块, 客户端可使用`cookies`维护session.


获取新`cookies`:

```
cookies = response.headers.get_list('Set-Cookie')
```

使用新`cookies`:

```
import tornado.httpclient

http_client = tornado.httpclient.HTTPClient()
# cookies = {"Cookie" : 'my_cookie=abc'}
http_client.fetch("http://abc.com/test", headers=cookies)
```
