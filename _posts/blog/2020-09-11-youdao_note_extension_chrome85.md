---
layout: post
title:  Chrome85下有道云笔记插件异常
category: 技术
tags:  
    - chrome
keywords: 
description: 
---

# Chrome85下有道云笔记插件异常

Chrome 升级到 85.0.4183.102 版本后, 有道云笔记插件失效.

## 有道云笔记插件无法打开(chrome85)

F12 调试, 点击有道云插件后, 报错

```
Access to XMLHttpRequest at 'https://note.youdao.com/yws/mapi/user?method=get' from origin 'https://mp.weixin.qq.com' has been blocked by CORS policy: 
Response to preflight request doesn't pass access control check: No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

怀疑是 chrome 85 新特性引起的, 搜索后找到官方文档: [Changes to Cross-Origin Requests in Chrome Extension Content Scripts](https://www.chromium.org/Home/chromium-security/extension-content-script-fetches)

经测试, 有效的设置为:

打开: `chrome://flags/#cors-for-content-scripts`, 设置为 `Disabled`

## 需要登录且收藏失败(chrome85前)

该问题发生在 chrome85 版本前, 记录以前的解决方案.

参考: [Chrome80 网页剪报收藏笔记每次都需要登录且收藏失败报错](https://tieba.baidu.com/p/6549122973)

打开: `chrome://flags/#same-site-by-default-cookies`, 设置 为 `Disabled`.

## chrome85 下最终设置结果

效果图:

![效果图](../../../../public/img/chrome85_settings/chrome85_setting.png )

