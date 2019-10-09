---
layout: post
title:  docker挂载目录异常
category: 技术
tags:  docker
keywords: 
description: 
---

# docker挂载目录异常

场景如下：

docker 以数据卷的方式挂载 目录/文件， 如  `-v /opt/code:/code`。

当宿主的目录`/opt/code`以如下方式执行数据更新后，容器中的目录 `/code` 数据全部消失：

```
rm -rf /opt/code/
mkdir -p /opt/code
echo -n > /opt/code/new.data
```

原因是，容器挂载，只认文件`inode`。当宿主机的目录被删除再重建后，目录`inode`变化。容器挂载的`inode`所对应的宿主文件已经消失，故而数据为空。
