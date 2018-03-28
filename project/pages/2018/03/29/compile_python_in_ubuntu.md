# Ubuntu16.04下源码安装python3.6

通过apt安装的python3.6, 执行`import sqlite3`时出现错误:

```
ModuleNotFoundError: No module named '_sqlite3'
```

为减少类似错误,重新通过源码安装python3.6.

## 解决方案

github上的[DCIPy.sh](https://gist.github.com/PapyrusThePlant/6877b82253df79c290416a5200c018d6)脚本,实现了python源码及必要的库下载,源码编译与安装功能.

基于DCIPy.sh, 完成python3.6.4自动安装代码:

```
# 下载脚本
wget -c -O DCIPy.sh 'https://gist.githubusercontent.com/PapyrusThePlant/6877b82253df79c290416a5200c018d6/raw/d8294369f13cd79e93499fde1085073aa29fa06d/DCIPy.sh'

# 权限
chmod +x DCIPy.sh

# 安装python3.6.4
./DCIPy.sh 3.6.4

# 更新python3
sudo rm /usr/bin/python3 && sudo ln /usr/local/bin/python3 /usr/bin/python3

# 确认
python3 --version
```

## 致谢
感谢[@PapyrusThePlant](https://gist.github.com/PapyrusThePlant/6877b82253df79c290416a5200c018d6)贡献的DCIPy.sh!


