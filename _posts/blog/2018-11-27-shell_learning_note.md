---
layout: post
title: shell 学习笔记
category: 技术
tags: ubuntu, shell
keywords: 
description: 
---

# shell学习笔记

## 1. 一个命令的结果填充到另一个命令中
ssh例子:

```
# 获取远程服务器的 ip, 并 ssh连接到该服务器上
ssh foo@$(cat /data/ip.result)
```

docker例子:

```
# 删除所有仓库名为 redis 的镜像：
docker image rm $(docker image ls -q redis)
```
## 2. sudo执行echo命令

```
sudo sh -c "echo '{
  \"registry-mirrors\": [\"https://registry.docker-cn.com\"]
}' >> /etc/docker/daemon.json"
```
## 3. 清空文件

```echo -n > ~/xx.conf```

## 4. 常用命令

```
# 查看磁盘使用
df -lh

# 查看当前目录所占空间
du -sh ./

```

## 5. ssh命令

```
# 上传文件
scp ./local.file ubuntu@host:/remote/remote.file

# 下载文件
scp ubuntu@host:/remote/remote.file ./local.file
```

## 6. 获取本机ip
获取本机ip:

```
 ifconfig|sed -n '/inet addr/s/^[^:]*:\([0-9.]\{7,15\}\) .*/\1/p'
```

获取当前虚拟机ip:

```
 ifconfig|sed -n '/inet addr/s/^[^:]*:\([0-9.]\{7,15\}\) .*/\1/p' | grep 192.168
```

## 7. 设置屏幕亮度为0

```
[[ "$(cat /sys/class/backlight/intel_backlight/brightness)" -ne "0" ]] && (echo 0 | sudo tee /sys/class/backlight/intel_backlight/brightness)
```

## 8. 复杂命令示例

来源[docker配置](https://github.com/frkhit/docker-python/blob/py36-selenium-chrome/Dockerfile)

```
ARG CHROME_VERSION="google-chrome-stable"
ARG CHROME_DRIVER_VERSION
RUN apt-get update -qqy \

  # install chrome
  && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
  && apt-get update -qqy \
  && apt-get -qqy install ${CHROME_VERSION:-google-chrome-stable} \
  && rm /etc/apt/sources.list.d/google-chrome.list \

  # install chrome drive
  && if [ -z "$CHROME_DRIVER_VERSION" ]; \
  then CHROME_MAJOR_VERSION=$(google-chrome --version | sed -E "s/.* ([0-9]+)(\.[0-9]+){3}.*/\1/") \
    && CHROME_DRIVER_VERSION=$(wget --no-verbose -O - "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_MAJOR_VERSION}"); \
  fi \
  && echo "Using chromedriver version: "$CHROME_DRIVER_VERSION \
  && wget --no-verbose -O /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip \
  && rm -rf /opt/selenium/chromedriver \
  && unzip /tmp/chromedriver_linux64.zip -d /opt/selenium \
  && rm /tmp/chromedriver_linux64.zip \
  && mv /opt/selenium/chromedriver /opt/selenium/chromedriver-$CHROME_DRIVER_VERSION \
  && chmod 755 /opt/selenium/chromedriver-$CHROME_DRIVER_VERSION \
  && ln -fs /opt/selenium/chromedriver-$CHROME_DRIVER_VERSION /usr/bin/chromedriver \

  # install fonts
  && apt-get -qqy install ttf-wqy-zenhei ttf-wqy-microhei fonts-droid-fallback fonts-arphic-ukai fonts-arphic-uming \
  
  # install selenium
  && pip install --upgrade selenium \
  && rm -rf /root/.cache/pip/* \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/*
```

