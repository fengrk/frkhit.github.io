---
layout: post
title:  使用 markdown 制作 ppt
category: 技术
tags:  
    - markdown
    - ppt
    - reveal
    - vscode
keywords: 
description: 
---

# 使用 markdown 制作 ppt

[reveal.js](https://github.com/hakimel/reveal.js/)提供了一种利用 markdown 生成 ppt 的方法。

可以使用[vscode](https://github.com/microsoft/vscode)及[vscode-reveal](https://github.com/evilz/vscode-reveal)插件，搭建书写环境。

## 1. 环境配置

安装过程:

- 安装 `vscode`
- 打开`vscode`, 安装插件 `vscode-reveal`


## 2. 示例

步骤一、在 `vscode` 中新建 `sample.md`， 并写入如下内容: 

```
---
theme : "night"
transition: "slide"
highlightTheme: "monokai"
logoImg: "logo.png"
slideNumber: false
title: "XXX调研报告"
---

<style type="text/css">
  .reveal p {
    text-align: left;
  }
  .reveal ul {
    display: block;
  }
  .reveal ol {
    display: block;
  }
</style>

# XXX调研报告

---

##  1. 概述

---

##  2. 行业现状

```

示例要点：

- ppt 基本配置
- ppt 样式写在 style 中


步骤二、通过快键键`Command + Shift + P` 选择 `Revealjs: Open presentation in browser`, 即可在浏览器中预览ppt。也可以通过选择 `Revealjs: Export in PDF`, 导出 pdf 文件。