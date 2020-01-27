---
layout: post
title:  FFmpeg 使用总结
category: 技术
tags:  
    - FFmpeg
keywords: 
description: 
---

# FFmpeg 使用总结

## 1. 提取音频

```
# 提取 mp3 音轨
ffmpeg -y -i input.mp4 -write_xing 0 output.mp3
```

## 2. 音频转码

```
# mp3 转 pcm
ffmpeg -y -i input.mp3 -acodec pcm_s16le -f s16le -ac 1 -ar 16k ouput.wav
```
