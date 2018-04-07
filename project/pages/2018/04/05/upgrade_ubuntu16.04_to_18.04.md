# 将Ubuntu16.04升级为Ubuntu18.04(development branch)

## 0.备份Ubuntu16.04

```
sudo tar vzcpf /media/Backup/ubuntu_`date +%Y%m%d_%H`.tar.gz --exclude=/proc --exclude=/dev --exclude=/mnt --exclude=/media --exclude=/lost+found --exclude=/cdrom --exclude=/tmp --exclude=/sys --exclude=/home --exclude=/run / > /media/Backup/ubuntu_`date +%Y%m%d_%H`.log 2> /media/Backup/ubuntu_`date +%Y%m%d_%H`.error

```

## 1.升级至Ubuntu18.04 (development branch)

```
sudo apt update 
sudo apt upgrade
sudo apt autoremove
sudo apt dist-upgrade

sudo apt install update-manager-core
sudo do-release-upgrade
sudo do-release-upgrade -d

sudo apt update && sudo apt -y dist-upgrade
```

然后重启电脑.

## 2.异常处理

### 2.1 shadowsocks出现`EVP_CIPHER_CTX_cleanup`错误
报错:
```
AttributeError: /usr/lib/x86_64-linux-gnu/libcrypto.so.1.1: undefined symbol: EVP_CIPHER_CTX_cleanup
```

原因:
ubuntu18.04中,openssl升级到了1.1.0b版本;而openssl在1.1.0版本中，废弃了EVP_CIPHER_CTX_cleanup函数.

解决方法[参考@suanite](https://www.jianshu.com/p/8151bfd9a760):

```
用vim打开文件：
vim /usr/local/lib/python3.6/dist-packages/shadowsocks/crypto/openssl.py
跳转到52行（shadowsocks2.8.2版本，其他版本搜索一下cleanup）；
将第52行libcrypto.EVP_CIPHER_CTX_cleanup.argtypes = (c_void_p,) 改为libcrypto.EVP_CIPHER_CTX_reset.argtypes = (c_void_p,)；
再搜索cleanup（全文件共2处，此处位于111行），将libcrypto.EVP_CIPHER_CTX_cleanup(self._ctx)改为libcrypto.EVP_CIPHER_CTX_reset(self._ctx)；
重新启动ss即可。
```
### 2.2 wifi定时重启

```
sudo crontab -e

# 文件最后加入一行
0 */15 * * * sudo modprobe -r rtl8723be && sleep 2 && sudo modprobe rtl8723be

```
 
## 3.删除多余软件

删除系统自带videos: `sudo apt remove totem totem-plugins`

删除系统自带gedit: `sudo apt remove gedit*`

删除系统自带libreoffice套件: `sudo apt remove libreoffice*`

删除不使用的包: `sudo apt autoremove`


## 4.功能设置

### 4.1 打字时禁用触摸板
[参考](https://askubuntu.com/questions/773595/how-can-i-disable-touchpad-while-typing-on-ubuntu-16-04-syndaemon-isnt-working):

*方案一:*
```
sudo add-apt-repository ppa:atareao/atareao
sudo apt update
sudo apt install touchpad-indicator
```
打开touchpad-indicator, 在Actions中启用Disable tochpad on typing, 禁用时间设为300ms.

- 成功实现功能.
- 缺点: 冻结鼠标时间>2s; 系统提示严重错误.


**方案二:**

```
synclient PalmDetect=1
```





