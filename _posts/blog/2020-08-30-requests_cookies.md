---
layout: post
title:  requests cookie 配置
category: 技术
tags:  
    - python
keywords: 
description: 
---

# requests cookie 配置


```python

import logging

import requests
from requests.cookies import cookiejar_from_dict


class RequestsSessionDemo(object):
    """ requests session 示例 """

    def __init__(self, ):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._session = None

    def request(self) -> requests.Session:
        """ """
        if self._session is None:
            # 创建 session
            session = requests.Session()

            # cookie 赋值
            header_str = '''
            accept: application/json, text/plain, */*
            accept-encoding: gzip, deflate, br
            accept-language: zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7,ja;q=0.6
            '''
            headers = {}
            for line in header_str.split("\n"):
                line = line.strip()
                if not line:
                    continue
                headers[line.split(":")[0]] = ":".join(line.split(":")[1:]).strip()

            session.headers.update(headers)

            cookie_str = "a=1597978255; sessionid=abcdfefefg"  # 初始 cookie
            cookie_dict = {}
            for line in cookie_str.split("; "):
                name, value = line.strip().split("=", 1)
                cookie_dict[name] = value
            session.cookies = cookiejar_from_dict(cookie_dict)
            self._session = session

        return self._session

    def query_page(self, url: str):
        """ """
        response = self.request().get(url=url)
        self.logger.info("res:\n{}\n\n".format(response.text))
   

```
