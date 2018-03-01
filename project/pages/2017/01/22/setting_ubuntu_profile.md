# ubuntu环境变量设置

设置/etc/profile

```
vim /etc/profile
```


在文件后面添加

```
#set zookeeper environment

export ZOOKEEPER_HOME=/home/mokiwi/zookeeper
export PATH=$PATH:$ZOOKEEPER_HOME/bin:$ZOOKEEPER_HOME/conf

```

保存退出，这时候新PATH还没有生效，执行下面命令

```
source /etc/profile
```

