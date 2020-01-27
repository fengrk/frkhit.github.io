---
layout: post
title:  scrapy项目作为工具库使用
category: 技术
tags:  
    - scrapy
    - python
keywords: 
description: 
---

# scrapy项目作为工具库使用

## 1. 目录树

```
pysrc
    - main.py
    - items.py
    - ScrapyDemo
        - scrapy.cfg
        - ScrapyDemo
            - spiders
                - __init__.py
                - DemoCrawler.py
            - __init__.py
            - items.py
            - pipelines.py
            - settings.py
            - utils.py
            - demo_api.py
```


## 2. scrapy项目提供对外接口

在 `ScrapyDemo` 中 新建文件 `demo_api.py`, 提供对外访问接口

```
# coding:utf-8
import json
import os
import sys

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from scrapy.crawler import CrawlerProcess
from ScrapyDemo.spiders.DemoCrawler import DemoSpider, logger
from ScrapyDemo.utils import get_settings, reset_settings


def run_demo_spider(query: str, proxy: dict, output_file: str, lang='', max_page: int = None):
    """

    :param proxy:
    :param output_file:
    :param query:
    :param lang:
    :param max_page:
    :return:
    """
    # 记录旧的环境变量
    old_environ_dict = {}

    # proxy
    for key, value in proxy.items():
        old_environ_dict[key] = os.environ.get(key)
        os.environ[key] = value
    if proxy and ("https_proxy" not in proxy and "HTTPS_PROXY" not in proxy):
        logger.warning("https_proxy not found in proxy!")

    try:
        settings = get_settings()

        # 修改 settings
        settings.set("XXX", output_file, priority="project")

        process = CrawlerProcess(settings=settings)

        process.crawl(DemoSpider, query=query, lang=lang, max_page=max_page)
        process.start()
    finally:
        # 恢复环境变量
        for key, value in old_environ_dict.items():
            if value is None:
                if key in os.environ:
                    del os.environ[key]
            else:
                os.environ[key] = value

        reset_settings()


def run_scrapy(cmd_json: str):
    """ 执行命令 """

    # parse args
    cmd_kwargs = json.loads(cmd_json)

    # run spider
    run_demo_spider(**cmd_kwargs)


if __name__ == '__main__':
    run_scrapy(sys.argv[1])

```

## 3. 主项目通过`subprocess`调用 scrapy

在主项目`main.py`中， 通过`subprocess`调用 scrapy 项目

```
# coding:utf-8

import json
import logging
import os
import subprocess
import sys

import arrow
import shortuuid

from items import DemoItem

_cur_dir = os.path.dirname(__file__)


def _run_scrapy(**kwargs):
    """ 执行 scrapy 任务"""
    cur_dir = os.getcwd()
    try:
        os.chdir(os.path.join(_cur_dir, "ScrapyDemo"))
        subprocess.run([sys.executable, "ScrapyDemo/demo_api.py", json.dumps(kwargs)])
    finally:
        os.chdir(cur_dir)


def search(query: str, proxy: dict, lang='', max_page: int = None, logger: logging.Logger = None) -> [DemoItem]:
    """

    :param proxy:
    :param query:
    :param lang:
    :param max_page:
    :param logger:
    :return:
    """
    logger = logger or logging.getLogger("xxx")

    # 数据文件
    data_dir = "/tmp/data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    uid = arrow.get().format("YYYYMMDD") + "_" + shortuuid.ShortUUID().random(length=8)
    output_file = os.path.join(data_dir, "{}.json".format(uid))

    # 启动任务
    if proxy and ("https_proxy" not in proxy and "HTTPS_PROXY" not in proxy):
        logger.warning("https_proxy not found in proxy!")

    _run_scrapy(**dict(
        query=query, proxy=proxy, lang=lang, max_page=max_page, output_file=output_file,
    ))

    # 解析结果
    result_list = []
    if not os.path.exists(output_file):
        logger.error("{} not found!".format(output_file))
        return result_list

    result_dict = {}
    with open(output_file, "r", encoding="utf-8") as f:
        for line in f:
            if len(line) > 2:
                try:
                    raw_item_dict = json.loads(line.strip())
                    _index = raw_item_dict.pop("index")

                    if _index in result_dict:
                        logger.warning("item index {} exists before!".format(_index))

                    demo_item = DemoItem()
                    demo_item["id"] = raw_item_dict.get("ID")
                    result_dict[_index] = demo_item
                except Exception as e:
                    logger.error(e)

    # 按照 index 排序
    logger.info("index list {}".format([_index for _index in sorted(result_dict.keys())]))
    for _index in sorted(result_dict.keys()):
        result_list.append(result_dict[_index])

    # 删除临时文件

    return result_list

```