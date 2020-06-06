---
layout: post
title:  adb 命令 总结
category: 技术
tags:  
    - adb
    - android
keywords: 
description: 
---

# adb 命令 总结

## 1. adb 安装

可以参考 [mac 下安装 adb](../../../../2019/10/07/adb_install/index.html).

## 2. adb 常用命令

- 获取应用列表: `adb shell pm list packages`
- 彻底关闭应用:  `adb shell ps | grep <package_name> | awk '{print $2}' | xargs adb shell kill`
- 启动应用: `adb shell am start -n <package_name>/<package_name>.ui.RunScriptActivity`


## 3. adb 授权

### 3.1 为应用授权无障碍权限

```shell script
adb shell settings put secure enabled_accessibility_services <package_name>/<service_name>
```

### 3.2 为应用授权特定权限

```shell script

adb shell pm grant <package_name> android.permission.ACCESS_FINE_LOCATION
adb shell pm grant <package_name> android.permission.WRITE_EXTERNAL_STORAGE

```

如果需要自动获取 app 所需的权限, 可以这样操作:

```shell script

# 获取应用权限信息
adb shell dumpsys package  <package_name>

```

输出的信息包含:

```text

  requested permissions:
      android.permission.WRITE_EXTERNAL_STORAGE
      android.permission.READ_EXTERNAL_STORAGE
      android.permission.WAKE_LOCK
      ......
    install permissions:
      android.permission.MODIFY_AUDIO_SETTINGS: granted=true
      android.permission.MANAGE_ACCOUNTS: granted=true
      android.permission.WRITE_SYNC_SETTINGS: granted=true
      android.permission.RECEIVE_BOOT_COMPLETED: granted=true
      ......
```

获取 `requested permissions`, 减去 `install permissions` 中 `granted=true` 的权限, 即可得到需要授权的权限.




