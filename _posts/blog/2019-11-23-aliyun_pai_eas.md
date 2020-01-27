---
layout: post
title:  阿里云 PAI-EAS 试用报告
category: 技术
tags:  
    - gpt2
keywords: 
description: 
---

# 阿里云 PAI-EAS 试用报告

阿里云提供了[PAI-EAS](https://help.aliyun.com/document_detail/113696.html)模型推理部署方案。官方介绍：

```
在线推理是将算法模型应用至实际业务的重要环节。为了帮助用户更好的实现一站式端到端的算法应用，PAI平台针对在线推理场景提供了PAI EAS(Elastic Algorithm Service)在线预测服务，支持基于异构硬件(CPU/GPU)的模型加载和数据请求的实时响应。您可以通过多种部署方式将您的模型发布成为在线的restful API接口，同时我们提供的弹性扩缩、蓝绿部署等特性可以支撑您以最低的资源成本获取高并发、稳定的在线算法模型服务。
```

作为模型部署的候选方案， 我写了一个简单的试用报告，并提供一个[公网调用的示例](https://github.com/frkhit/aliyun-PAI-EAS), 方便其他人上手。

## 准备工作

- 开通 DataWorks
- 开通 PAI-EAS
- 开通 api 网关服务(如果要公网调用，必须开通此服务)
  
## 部署示例

实现目标： `client(python) -> 公网(API-GateWay) -> PAI-EAS(tensorflow) `。

完整代码见[aliyun-PAI-EAS](https://github.com/frkhit/aliyun-PAI-EAS)。

步骤：

### Step1 训练模型并导出 SavedModel格式

```
git clone https://github.com/frkhit/aliyun-PAI-EAS
cd aliyun-PAI-EAS

# install env
python -m pip install -r requirements.txt

# train
python train.py train

# export demo_simple
python train.py simple

# export demo_complex
python train.py complex

```

### Step2 PAI-EAS 部署模型

将 `demo_simple.zip` 及 `demo_complex.zip` 分别上传到 PAI-EAS, 并命名为 `demo_simple`, `demo_complex`。

模型运行情况如下：

![模型运行情况](/public/img/aliyun_pai_eas/pai_eas.png)

在打开模型的 `调用信息`， 在`公网调用地址`中，绑定公网。 


### Step3 本地调用 PAE-EAS 推理服务

分别获取两个模型的公网访问地址及授权码, 复制到`demo.py`中。

远程调用 PAI-EAS: `python call_pai_eas.py`。
