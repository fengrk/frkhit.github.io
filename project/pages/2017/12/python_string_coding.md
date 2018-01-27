# 解决python中遇到的乱码问题

## 1. 解决中文乱码的一种可行方法

`
# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import chardet


def smart_decoder(raw_content, default_encoding_list=("utf-8", "gb18030")):
    """
    将字符串解码成unicode
    :type default_encoding_list: list of str
    :rtype: unicode
    :type raw_content: str|unicode
    """
    if isinstance(raw_content, unicode):
        return raw_content

    encoding = chardet.detect(raw_content).get("encoding", "utf-8")

    try:
        return raw_content.decode(encoding)
    except UnicodeEncodeError as e:
        for encoding in default_encoding_list:
            try:
                return raw_content.decode(encoding)
            except UnicodeEncodeError as e:
                pass
        raise e


if __name__ == '__main__':
    import requests

    a = requests.get("https://www.baidu.com").content
    print(smart_decoder(a))

`

## 2. requests响应结果乱码

### 问题

使用requests请求网址，获取响应response， 通过response.text得到的网页内容，有时候会出现乱码的情况。

### 原因
分析源代码发现，调用respose.text 其实就是对 response.content执行解码操作。编码通过chardet判断。

乱码的关键是，chardet获取的编码可能不正确，但在执行response.content.decode时，程序会直接忽略编码异常，从而导致使用错误的编码解码。

### 解决思路

人工解码，处理编码错误。

### 程序demo

```
def parse_response(response):
    """
    手工对requests的响应内容解码
    :rtype: unicode
    """
    return smart_decoder(response.content)

```

