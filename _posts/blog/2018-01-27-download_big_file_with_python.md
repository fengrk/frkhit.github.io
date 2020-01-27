---
layout: post
title: python下载大文件的方法
category: 技术
tags: 
    - python
keywords: 
description: 
---

# python下载大文件的方法

## 1. wget

```
def download_big_file_with_wget(url, target_file_name):
    """
        使用wget下载大文件
        Note: 需要系统安装wget
    """
    import os
    import subprocess
    
    download_process = subprocess.Popen(["wget", "-c", "-O", target_file_name, "'{}'".format(url)])
    
    download_process.wait()
    
    if not os.path.exists(target_file_name):
        raise Exception("fail to download file from {}".format(url))

```

## 2. python自带库

```
def download_big_file(url, target_file_name):
    """
        使用python核心库下载大文件
        ref: https://stackoverflow.com/questions/1517616/stream-large-binary-files-with-urllib2-to-file
    """
    import sys
    if sys.version_info > (2, 7):
        # Python 3
        from urllib.request import urlopen
    else:
        # Python 2
        from urllib2 import urlopen
    
    response = urlopen(url)
    chunk = 16 * 1024
    with open(target_file_name, 'wb') as f:
        while True:
            chunk = response.read(chunk)
            if not chunk:
                break
            f.write(chunk)

```
