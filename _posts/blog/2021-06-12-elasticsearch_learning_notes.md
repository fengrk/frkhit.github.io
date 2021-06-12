---
layout: post title: elasticsearch 学习笔记 category: 技术 tags:
- elasticsearch keywords:
description:
---

# elasticsearch 学习笔记

## 1. 客户端

### 1.1 python 客户端

安装依赖: `elasticsearch-dsl==7.3.0 elasticsearch==7.12.0`

客户端连接:

```python

from elasticsearch import AsyncElasticsearch

ES_HOST: str = ""
ES_TIMEOUT: int = 60
es_client = AsyncElasticsearch(hosts=[ES_HOST], timeout=ES_TIMEOUT)

```

## 2. 创建索引

### 2.1 创建索引

示例:

```
PUT demo_index
{
  "settings": {
    "index": {
      "number_of_shards": "3",
      "number_of_replicas": "0"
    }
  },
  "mappings": {
    "properties": {
      "mid": {
        "type": "long"
      },
      "status": {
        "type": "integer"
      },
      "userName": {
        "fields": {
          "keyword": {
            "type": "keyword"
          }
        },
        "type": "text"
      },
      "tags": {
        "properties": {
          "tagId": {
            "type": "long"
          },
          "tagName": {
            "fields": {
              "keyword": {
                "type": "keyword"
              }
            },
            "type": "text"
          },
          "tagType": {
            "fields": {
              "keyword": {
                "type": "keyword"
              }
            },
            "type": "text"
          },
          "updateTime": {
            "type": "long"
          }
        },
        "type": "nested"
      }
    }
  }
}

# 获取当前 mapping
GET /demo_index/_mapping

```

### 2.2 字段类型定义

python 环境中定义 模型:

```python

import typing  # noqa

from elasticsearch_dsl import Document, Keyword, Long, Text, Integer, Nested, InnerDoc


class Tag(InnerDoc):
    tagId = Long()
    tagName = Text(fields={'keyword': Keyword()})
    tagType = Text(fields={'keyword': Keyword()})
    updateTime = Long()


class Model(Document):
    mid = Long()
    status = Integer()
    userName = Text(fields={'keyword': Keyword()})
    tags = Nested(Tag, multi=True)


```

python 中 可以利用 `Document.init` 方法, 直接在代码中创建索引.

更合适的方法时, 通过 Kibana 显式地 使用 `2.1 创建索引` 中的 api 创建索引.

一个根据 模型(Document) 创建 api 配置的方法:

```python

def build_index_config(model: typing.Type[Document], index_name: str, number_of_shards=3) -> dict:
    """ """

    def create_settings(model_cls: typing.Type[Document]):
        i = model_cls._index

        config = i.to_dict()

        return config

    def create_index(_index_name: str, model_cls: typing.Type[Document], _number_of_shards=3):
        index_name = _index_name

        Index = type("Index", (), dict(
            name=index_name, settings={"number_of_shards": _number_of_shards, }
        ))

        model: typing.Type[Document] = type(model_cls.__name__, (model_cls,), {
            'Index': Index,
        })

        _index_name = model._index._name

        return create_settings(model_cls=model)

    return create_index(_index_name=index_name, model_cls=model, _number_of_shards=number_of_shards)


print(build_index_config(Model, index_name='demo_index', number_of_shards=3))

```

### 2.3 新增字段

```
PUT /demo_index/_mapping
{
    "properties": {
      "count": {
        "type": "integer"
      }
    }
}

```

## 3. 基本的CRUD

### 3.1 搜索示例

```
# 搜索所有
GET /demo_index/_search
{
  "query": {
    "match_all": {}
  },
  "_source": ["mid", "userName"],
  "size": 100
}

# tags
GET /demo_index/_search
{
  "query": {
    "nested": {
      "path": "tags",
      "query": {
        "terms": {
          "tags.tagName.keyword": [
            "商品"
          ]
        }
      }
    }
  }
}

# 范围
GET /demo_index/_search
{
  "query": {
    "range": {"count":{"gt": 0} }
  }
}

GET /demo_index/_search
{
  "query": {
    "term": {"userName.keyword": "admin" }
  }
}

# 排除部分字段
GET demo_index/_search
{
  "query": {
    "match_all": {}
  },
  "_source":{
    "exclude": ["tags"]
  }
}

```

### 3.2 更新操作示例

``` 

POST /demo_index/_update_by_query
{
  "script": {
    "inline": "ctx._source.count = 0",
    "lang": "painless"
  },
  "query": {
    "match_all": {}
  }
}


POST /demo_index/_update_by_query
{
  "script": {
    "inline": "ctx._source.tags = []",
    "lang": "painless"
  },
  "query": {
    "match_all": {}
  }
}

```

### 3.3 删除

``` 
POST /demo_index/_delete_by_query
{
  "query": {
    "match_all": {}
  }
}
```

## 4. painless 脚本

## 5. python使用实践

### 5.1 基本使用

搜索 `es.search`:

```python

query_dict = {
    "query": {
        "match_all": {}
    },
    "size": 1,
    "_source": ["tags", "mid"]
}

data = await es_client.search(index="demo_index", body=query_dict, )

for doc in data["hits"]["hits"]:
    yield Model(**doc["_source"])

```

更新 `es.update_by_query`:

```python

body = {
    "script": {
        "source": "ctx._source.count = 0",
        "params": {},
        "lang": "painless"
    },
    "query": {
        "match_all": {}

    }
}

await es_client.update_by_query(body=body, index="demo_index", conflicts="proceed")

```

删除 `es.delete_by_query`:

```python

await es_client.delete_by_query(
    index="demo_index",
    body={
        "query": {
            "bool": {
                "must": [
                    {"term": {"mid": 10}}
                ]
            }
        }
    },
    refresh=True,
)

```

### 5.2 遍历操作

使用 `async_scan` 实现:

```python

res_list = []
async for doc in async_scan(
        client=es_client,
        query={
            "query": {
                "match_all": {}
            }
        },
        index="demo_index"
):
    res_list.append(Model(**doc["_source"]))

```

使用 `search_after` 实现:

```python

query_dict = {
    "query": {
        "match_all": {}
    }
}
sort_list = ["mid:desc"]  # 需要提供一个 unique 字段

raw_query_dict = dict(query_dict)

_sort = None
max_size = 200
query_dict["size"] = max_size
all_count = 0
mid_seen = set()

while True:
    _query_dict = dict(query_dict)
    if _sort:
        _query_dict["search_after"] = _sort

    data = await es_client.search(index="demo_index", body=_query_dict, sort=sort_list)

    _count = 0
    for doc in data["hits"]["hits"]:
        yield Model(**doc["_source"])
        _sort = doc['sort']
        _count += 1    
    
    if _count < max_size:
        break

count_info = await es_client.count(index="demo_index", body=raw_query_dict)

if count_info.get("count") != all_count:
    logging.warning(f"es.count {count_info.get('count')} != yield_count {all_count}!")

```

### 5.3 批量操作





