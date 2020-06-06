---
layout: post
title:  python cookbook 阅读笔记
category: 技术
tags:  
    - python
keywords: 
description: 
---

# python cookbook 阅读笔记

## 第一章：数据结构和算法

### 1.1 队列 `deque`:

```python
from collections import deque

# 保留最后 10 个元素
previous_lines = deque(maxlen=10)

# 队列
q = deque([1, 2, 3])

q.appendleft(4)
q.popleft()

q.append(10)
q.pop(2)
```

### 1.2 查找最大或最小的 N 个元素

```python
import heapq
nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
print(heapq.nlargest(3, nums)) # Prints [42, 37, 23] 
print(heapq.nsmallest(3, nums)) # Prints [-4, 1, 2]

```

`heapq` 可以实现优先级队列.

### 1.3 `Counter` 找出 序列中出现次数最多的元素

```python
from collections import Counter 

words = []
for index in range(10):
    for _ in range(index + 1):
        words.append("index-{}".format(index))

# 出现频率最高的 3 个单词 
word_counts = Counter(words) 
top_three = word_counts.most_common(3) 
print(top_three)

```

## 第二章：字符串和文本

### 2.1 使用多个界定符分割字符串

```python
import re
line = 'asdf fjdk; afed, fjek,asdf, foo' 
print(re.split(r'[;,\s]\s*', line))  # ['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']

# 保留分隔符
fields = re.split(r'(;|,|\s)\s*', line)
print(fields)  # ['asdf', ' ', 'fjdk', ';', 'afed', ',', 'fjek', ',', 'asdf', ',', 'foo']
```

### 2.2 `fnmath` 实现 shell 通配符匹配功能

```python

from fnmatch import fnmatch, fnmatchcase

print(fnmatch('foo.txt', '*.txt'))  # True

print(fnmatch('foo.txt', '?oo.txt'))  # True

print(fnmatch('Dat45.csv', 'Dat[0-9]*'))  # True

# On Windows
print(fnmatch('foo.txt', '*.TXT'))  # True

# 完全匹配
print(fnmatchcase('foo.txt', '*.TXT'))  # False

```

### 2.3 字符串搜索和替换

```python

import re
text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'

print(re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', text))  # 'Today is 2012-11-27. PyCon starts 2013-3-13.'

```

忽略字符串大小写的搜索替换

```python
import re

text = 'UPPER PYTHON, lower python, Mixed Python'
print(re.findall('python', text, flags=re.IGNORECASE))  # ['PYTHON', 'python', 'Python']
print(re.sub('python', 'snake', text, flags=re.IGNORECASE))  # 'UPPER snake, lower snake, Mixed snake'

```

进阶: 替换字符串自动跟被匹配字符串的大小写保持一致

```python

import re

def matchcase(word):
    def replace(m):
        text = m.group()
        if text.isupper():
            return word.upper()
        elif text.islower():
            return word.lower()
        elif text[0].isupper():
            return word.capitalize()
        else:
            return word
    return replace      

text = 'UPPER PYTHON, lower python, Mixed Python'
print(re.sub('python', matchcase('snake'), text, flags=re.IGNORECASE)) 
# UPPER SNAKE, lower snake, Mixed Snake

```

多行匹配:

```python

import re

text1 = '/* this is a comment */'
text2 = '''/* this is a
multiline comment */
'''

# 不能匹配换行符 
re.compile(r'/\*(.*?)\*/').findall(text1)  # [' this is a comment ']
re.compile(r'/\*(.*?)\*/').findall(text2)  # []

# 匹配多行

# 方法一: 指定了一个非捕获组匹配
re.compile(r'/\*((?:.|\n)*?)\*/').findall(text2)
# [' this is a\n multiline comment ']

# 方法二: re.DOTALL
re.compile(r'/\*(.*?)\*/', re.DOTALL).findall(text2)
# [' this is a\n multiline comment ']

```


## 第四章：迭代器与生成器

### 4.1 手动遍历迭代器

```python

def manual_iter():
    with open('/etc/passwd') as f:
        try:
            while True:
                line = next(f)
                print(line, end='')
        except StopIteration:
            pass

```

### 4.2 迭代器其他

- 关键魔法方法: `__iter__(self, )` 和 `__next__(self, )`
- 反向迭代: `__reversed__(self, )`, 使用 `reversed(iter)`
- 同时迭代多个序列: `for x, y in zip(x_iter, y_iter)`
- 依次迭代多个序列: `for x in itertools.chain(x1_iter, x2_iter, x3_iter)`
- 创建数据处理管道: 使用迭代器能简化逻辑
- 展开嵌套的序列: `yield from`

顺序迭代合并后的排序迭代对象: 性能更好

```python

import heapq
a = [1, 4, 7, 10]
b = [2, 5, 6, 11]
for c in heapq.merge(a, b):
    print(c)

# 1 2 4 5 6 7 10 11

```

## 第八章：类与对象

### 8.1 创建新的类或实例属性

```python

# Descriptor attribute for an integer type-checked attribute
class Integer:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]
    
    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError('Expected an int')
        instance.__dict__[self.name] = value
    
    def __delete__(self, instance):
        del instance.__dict__[self.name]            

class Point: 
    x = Integer('x') 
    y = Integer('y')
    
    def __init__(self, x, y):
        self.x = x
        self.y = y      

p = Point(2, 3)
print(p.x) # Calls Point.x.__get__(p,Point)

p.y = 5 # Calls Point.y.__set__(p, 5)
p.x = 2.3 # Calls Point.x.__set__(p, 2.3)
# raise TypeError

```

### 8.2 使用延迟计算属性

```python
import math


class lazyproperty:
    def __init__(self, func):
        self.func = func
    
    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            value = self.func(instance)
        
        setattr(instance, self.func.__name__, value)
        return value

class Circle:
    def __init__(self, radius):
        self.radius = radius

    @lazyproperty
    def area(self):
        print('Computing area')
        return math.pi * self.radius ** 2

    @lazyproperty
    def perimeter(self):
        print('Computing perimeter')
        return 2 * math.pi * self.radius

# 使用
c = Circle(4.0)

print(vars(c))  # {'radius': 4.0}

c.area
print(vars(c))  # {'area': 50.26548245743669, 'radius': 4.0}

del c.area
print(vars(c))  # {'radius': 4.0}

```

### 8.3 实现自定义容器

你想实现一个自定义的类来模拟内置的容器类功能，比如列表和字典。但是你不确定到底要实现哪些方法。

collections 定义了很多抽象基类，当你想自定义容器类的时候它们会非常有用。

比如你想让你的类支持迭代，那就让你的类继承 collections.Iterable 即可：

```python
import collections


class A(collections.Iterable):
    pass    

```

### 8.4 利用 Mixins 扩展类功能

```python

class LoggedMappingMixin:
    """
    Add logging to get/set/delete operations for debugging.
    """
    __slots__ = () # 混入类都没有实例变量，因为直接实例化混入类没有任何意义
    
    def __getitem__(self, key):
        print('Getting ' + str(key))
        return super().__getitem__(key)
    
    def __setitem__(self, key, value):
        print('Setting {} = {!r}'.format(key, value))
        return super().__setitem__(key, value)
    
    def __delitem__(self, key):
        print('Deleting ' + str(key))
        return super().__delitem__(key)

```

### 8.5 创建缓存实例

```python

import weakref


class CachedSpamManager:
    def __init__(self):
        self._cache = weakref.WeakValueDictionary()

    def get_spam(self, name):
        if name not in self._cache:
            s = Spam._new(name)
            self._cache[name] = s
        else:
            s = self._cache[name]
        return s

    def clear(self):
        self._cache.clear()

class Spam:
    def __init__(self, *args, **kwargs):
        raise RuntimeError("Can't instantiate directly")
    
    # Alternate constructor
    @classmethod
    def _new(cls, name):
        self = cls.__new__(cls)
        self.name = name
        return self

if __name__ == '__main__':
    cache = CachedSpamManager()
    a = cache.get_spam("a")
    b = cache.get_spam("b")
    c = cache.get_spam("a")
    print(a)
    print(b)
    print(c)
    assert a is not b
    assert a is c

```

## TODO

page 301

