---
layout: post
title:  python logging 代码研读笔记
category: 技术
tags:  
    - python
    - logger
    - logging
keywords: 
description: 
---

# python logging 代码研读笔记

## 1. 可重入锁 `threading.RLock` 的使用

`logging` 库中, 使用 `threading.RLock` 实现线程安全.

引用[7. 使用RLock进行线程同步](https://python-parallel-programmning-cookbook.readthedocs.io/zh_CN/latest/chapter2/07_Thread_synchronization_with_RLock.html) 的说明:

```
如果你想让只有拿到锁的线程才能释放该锁，那么应该使用 RLock() 对象。

和 Lock() 对象一样， RLock() 对象有两个方法： acquire() 和 release() 。

当你需要在类外面保证线程安全，又要在类内使用同样方法的时候 RLock() 就很实用了。

```

## 2. `stream` 对象和文件操作线程安全


`logging` 包, 将 `file`, `sys.stderr`, `sys.stdout` 抽象为 `stream`:

`stream` 初始化:

```
# file
self.stream = open("file_name", "a", encoding="utf-8")

# stdout
self.stream = sys.stdout

# stderr
self.stream = sys.stderr

```

`stream` 写操作:

```
    def flush(self):
        self.acquire()
        try:
            if self.stream and hasattr(self.stream, "flush"):
                self.stream.flush()
        finally:
            self.release()


    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            # issue 35046: merged two stream.writes into one.
            stream.write(msg + self.terminator)
            self.flush()
        except RecursionError:  # See issue 36272
            raise
        except Exception:
            self.handleError(record)
```

`stream` 关闭:

```
    def close(self):
        """
        Closes the stream.
        """
        self.acquire()
        try:
            try:
                if self.stream:
                    try:
                        self.flush()
                    finally:
                        stream = self.stream
                        self.stream = None
                        if hasattr(stream, "close"):
                            stream.close()
            finally:
                # Issue #19523: call unconditionally to
                # prevent a handler leak when delay is set
                StreamHandler.close(self)
        finally:
            self.release()
```

多个 python 实例, 可以同时安全将日志写入到同一个文件中.

观察上述代码, logger 简单使用 追加模式 `a` 和 马上落盘 的方式, 实现写文件的多进程安全.


## 3. 日志文件回滚 

日志文件回滚相关代码如下:

``` 
    def emit(self, record):
        """
        Emit a record.

        Output the record to the file, catering for rollover as described
        in doRollover().
        """
        try:
            if self.shouldRollover(record):
                self.doRollover()
            logging.FileHandler.emit(self, record)
        except Exception:
            self.handleError(record)


    def doRollover(self):
        """
        Do a rollover, as described in __init__().
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        if self.backupCount > 0:
            for i in range(self.backupCount - 1, 0, -1):
                sfn = self.rotation_filename("%s.%d" % (self.baseFilename, i))
                dfn = self.rotation_filename("%s.%d" % (self.baseFilename,
                                                        i + 1))
                if os.path.exists(sfn):
                    if os.path.exists(dfn):
                        os.remove(dfn)
                    os.rename(sfn, dfn)
            dfn = self.rotation_filename(self.baseFilename + ".1")
            if os.path.exists(dfn):
                os.remove(dfn)
            self.rotate(self.baseFilename, dfn)
        if not self.delay:
            self.stream = self._open()

```

所以, 要实现多进程安全的 `RotatingFileHandler`, 可以利用 `fcntl` 文件锁, 确保回滚过程的安全.

