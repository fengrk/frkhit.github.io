# python3安装mysql

执行
```
pip3 install mysqlclient
```

报错：

```
OSError: mysql_config not found
```

解决：
```
sudo apt-get install libmysqlclient-dev
```
再次执行

```
pip3 install mysqlclient
```



