---
layout: post
title:  jieba RPC 服务
category: 技术
tags:  
    - python
    - docker
    - rpc
keywords: 
description: 
---

# jieba RPC 服务

web项目中使用到 `jieba` 分词服务。当使用多实例的方式部署服务时，每个实例（进程）都会加载 `jieba` 服务，导致内存使用紧张。

尝试单独启用一个 `jieba` 实例：server 实例通过 `rpc` 的方式，调用 `jieba` 分词服务，从而降低内存使用。

项目源码见[docker-practice/jieba](https://github.com/frkhit/docker-practice/tree/master/jieba).

## 1. 使用 grpc

安装必要的包：
 
``` pip install grpcio grpcio-tools ```

配置 protobuf 文件：

```
// jieba_service.proto
syntax = "proto3";

service JiebaService {
    rpc cut(CutRequest) returns (CutReply) {}
}

message CutRequest {
    string sentence = 1;
    bool  cut_all = 2;
    bool  HMM = 3;
    bool  use_paddle = 4;
}

message CutReply {
    string seg_list = 1;
}
```

生成 python 文件：

```
python -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I. jieba_service.proto
```

## 2. 启用 `jieba` 分词服务

安装包： `pip3 install jieba paddlepaddle-tiny==1.6.1 `

配置 `jieba_server.py`:

```
import json
import time
from concurrent import futures

import grpc
import jieba

import jieba_service_pb2
import jieba_service_pb2_grpc


class JiebaService(jieba_service_pb2_grpc.JiebaServiceServicer):

    def cut(self, request: jieba_service_pb2.CutRequest, context) -> jieba_service_pb2.CutReply:
        seg_list = jieba.lcut(sentence=request.sentence, use_paddle=request.use_paddle, cut_all=request.cut_all, HMM=request.HMM)
        return jieba_service_pb2.CutReply(seg_list=json.dumps([seg for seg in seg_list]))


def serve():
    # 启动 rpc 服务
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    jieba_service_pb2_grpc.add_JiebaServiceServicer_to_server(JiebaService(), server)
    server.add_insecure_port('[::]:10000')
    server.start()
    try:
        while True:
            time.sleep(60 * 60 * 24)  # one day in seconds
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
```

启用服务：

```python3 jieba_server.py```


## 3. 客户端调用 `jieba` 分词服务

客户端配置， `jieba_client.py`:

```
import json
import random
import grpc

import jieba_service_pb2
import jieba_service_pb2_grpc


def jieba_cut(rpc_channel, sentence: str, cut_all: bool = False, HMM: bool = True, use_paddle: bool = False) -> [str]:
    """ """
    # 调用 rpc 服务
    stub = jieba_service_pb2_grpc.JiebaServiceStub(rpc_channel)
    response = stub.cut(jieba_service_pb2.CutRequest(
        sentence=sentence,
        use_paddle=use_paddle,
        cut_all=cut_all,
        HMM=HMM
    ))
    return json.loads(response.seg_list)


def run():
    # 连接 rpc 服务器
    channel = grpc.insecure_channel('jieba:10000')

    # 调用 rpc 服务
    count = 0
    flag = random.randint(5, 20)
    seg_list = None
    with open("/data.txt", "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            seg_list = jieba_cut(
                rpc_channel=channel,
                sentence=line,
                use_paddle=False,
                cut_all=True,
            )
            count += 1
            if count % flag == 0:
                print("result is {}".format(seg_list))

    if seg_list:
        print("result is {}".format(seg_list))


if __name__ == '__main__':
    run()
```

同时启动多个客户端，测试 `jieba` 并发性：

```
docker-compose up --scale jieba-test=3  -d
```
