---
layout: post
title: 使用parsel处理xml
category: 技术
tags: 
    - python
    - xml
    - xpath
keywords: 
description: 
---

# 使用parsel处理xml

## 1. xml解析

使用 `parsel`包处理解析 xml 数据:

``` 
from parsel import Selector
resp = Selector(text=self.xml, type="xml")
for e in resp.xpath('//node[@id="root"]'):
    print(e)

```

## 2. 删除 xml 节点

```python
import unittest

from parsel import Selector


class TestXmlEdit(unittest.TestCase):
    def setUp(self) -> None:
        self.xml = '''<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
        <hierarchy>
            <node id="root">
                <node index="0" id="AAA" bounds="[1, 1]">
                    <node index="0" id="a" />
                    <node index="1" id="b" />
                </node>
                <node index="1" id="AAA" bounds="[1, 1]">
                    <node index="0" id="A" />
                    <node index="1" id="B" />
                </node>
            </node>
        </hierarchy>
        '''

    def testParselRemove(self):
        """ """

        def iter_node(_node: Selector):
            print("node: tag {}, id {}, index {}, child_count {}".format(
                _node.root.tag, _node.attrib.get("id"), _node.attrib.get("index"), len(_node.root)
            ))
            if _node.attrib.get("id") == "A":
                print()
                pass
            for _sub_index, _sub_node in enumerate(_node.root):
                assert _node.root[_sub_index] is _sub_node
                _sub_selector = Selector(root=_sub_node, namespaces=_node.namespaces, type=_node.type)
                iter_node(_node=_sub_selector)

        def iter_then_remove_node(_node: Selector):
            _remove_list = []
            for _sub_node in _node.root:
                _sub_node_id = _sub_node.attrib.get("id")
                _sub_node_index = _sub_node.attrib.get("index")
                if _sub_node_id == "AAA" and _sub_node_index == "0":
                    _remove_list.append(_sub_node)
                else:
                    _sub_selector = Selector(root=_sub_node, namespaces=_node.namespaces, type=_node.type)
                    iter_then_remove_node(_node=_sub_selector)

            if _remove_list:
                for _sub_node in _remove_list:
                    print("remove node: tag {}, id {}, index {}".format(
                        _sub_node.tag, _sub_node.attrib.get("id"), _sub_node.attrib.get("index")
                    ))
                    _node.root.remove(_sub_node)

        root = Selector(text=self.xml, type="xml")
        iter_node(_node=root)

        node_list = []
        print("\n\n\nbefore:")
        for tree in root.xpath('//node[@id="AAA"]'):
            print(tree.attrib["id"], tree.attrib["bounds"])
            iter_node(tree)
            node_list.append(tree)

        # 删除节点
        print("\n\n\nremove node:")
        iter_then_remove_node(_node=root)

        # root.remove(node_list[0])  # 报错 ValueError: Element is not a child of this node.
        print("\n\n\nafter remove:")
        for tree in root.xpath('//node[@id="AAA"]'):
            print(tree.attrib["id"], tree.attrib["bounds"])
            iter_node(tree)
```


