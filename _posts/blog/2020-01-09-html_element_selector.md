---
layout: post
title:  页面元素选择
category: 技术
tags:   
    - xpath
    - css
    - scrapy
    - pyppeteer
keywords: 
description: 
---

# 页面元素选择

## 1. Scrapy

不使用 `Scrapy` 框架， 也可以使用 `Scrapy` 的元素选择语法：

```
from parsel import Selector

body = '<html><body><span>good</span></body></html>'

response = Selector(text=body)

entries = response.css('.post-list > li')

```

详细的[官方教程](https://scrapy-chs.readthedocs.io/zh_CN/latest/topics/selectors.html)


### 1.1 css 语法

选择元素

- 选择class: `response.css('.plan')` 或 `response.css('.plan > li')`
- 多个 class: `title.css('.class1 .class2')`
- 多个条件: `response.css('#id1 .class1')`

提取属性

- 提取 href: `post.css(".post-title >a ::attr(href)").extract_first()`
- 提取 标题: `post.css(".post-title >a ::attr(title)").extract_first()`
- 提取其他属性： `data.css('div::attr(data2)').extract_first()`


提取内容

- 提取 text: `"".join(post.css(".post-title >a ::text").extract())`

### 1.2 xpath

- 获取 class 名称: `entry.xpath("@class").extract_first() == "class1"`
- 获取属性: `entry.css("img").xpath("@src").extract_first()`
- 获取 href: `entry.css(".abc").xpath("@href").extract_first()`
- href 含文本: `response.xpath('//a[contains(@href, "image")]/@href').extract()`
- 内容含文本: `sel.xpath("//a[contains(.//text(), 'Next Page')]").extract()`


## 2. bs4系列

## 3. puppeteer/chrome

### 3.1 css

- 多个 class: $(".a.b"). 错误 $(".a .b")



### 3.2 xpath

- 多个 class, 仅使用一个 class 选择: `//div[contains(@class, ".a") and contains(text(), "4")]`
`