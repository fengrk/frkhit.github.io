---
layout: post
title: mac 配置
category: 技术
tags: mac, osx
keywords: 
description: 
---

# mac 配置

## 1. 禁用 git-credential-osxkeychain

```
git config --local credential.helper && git config --local --unset credential.helper
git config --global credential.helper && git config --global --unset credential.helper
git config --system credential.helper && git config --system --unset credential.helper
```
