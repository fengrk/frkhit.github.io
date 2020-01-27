---
layout: post
title: nginx 配置
category: 技术
tags: 
    - nginx
keywords: 
description: 
---

# nginx 配置

## 1. http2开启

环境 ubuntu18.04 + nginx1.14(apt 自带)

`/etc/nginx/nginx.conf` 配置，关键是`SSL Settings`下配置ssl证书信息

```
user www-data;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
        worker_connections 768;
        # multi_accept on;
}

http {

        ##
        # Basic Settings
        ##

        sendfile on;
        tcp_nopush on;
        tcp_nodelay on;
        keepalive_timeout 65;
        types_hash_max_size 2048;
        # server_tokens off;

        # server_names_hash_bucket_size 64;
        # server_name_in_redirect off;

        include /etc/nginx/mime.types;
        default_type application/octet-stream;

        ##
        # SSL Settings
        ##

        ssl_certificate  /etc/nginx/cert/b.com.pem;
        ssl_certificate_key /etc/nginx/cert/b.com.key;
        ssl_session_timeout 5m;
        ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_prefer_server_ciphers on;

        ##
        # Logging Settings
        ##

        access_log /var/log/nginx/access.log;
        error_log /var/log/nginx/error.log;

        ##
        # Gzip Settings
        ##

        gzip on;

        # gzip_vary on;
        # gzip_proxied any;
        # gzip_comp_level 6;
        # gzip_buffers 16 8k;
        # gzip_http_version 1.1;
        # gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

        ##
        # Virtual Host Configs
        ##

        include /etc/nginx/conf.d/*.conf;
        include /etc/nginx/sites-enabled/*;
}

```

服务配置，新建`/etc/nginx/site-avalable/x.conf`文件，写入如下信息：

```
server {
    listen 443 ssl http2;
    server_name www.b.com;
    ssl on;
    root /var/www/b.com;
    index index.html index.htm;
    ssl_certificate  /etc/nginx/cert/b.com.pem;
    ssl_certificate_key /etc/nginx/cert/b.com.key;
    ssl_session_timeout 5m;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_prefer_server_ciphers on;
    location / {
        index index.html index.htm;
    }
}
server {
    listen 80;
    server_name www.b.com;
    rewrite ^(.*)$ https://$host$1 permanent;
}
```

## 2. 重定向

- 强制使用https

```
server {
    listen 80;
    server_name www.b.com;
    rewrite ^(.*)$ https://$host$1 permanent;
}
```

- path 转 子域名

```
rewrite ^/blog/(.*)$  https://blog.b.com/$1 permanent;
```

- 修改网址并使用新网址进行其他操作

```
# 反向代理的例子
location /blog/ {
    rewrite ^/blog/(.*)$ /$1 break; # 去除blog
    proxy_pass http://127.0.0.1:6000; 
} 
```

## 3. 反向代理

``` 
server {

    listen 443 ssl http2;
    server_name www.b.com;
    
    ssl on;
    ssl_certificate  /etc/nginx/cert/b.com.pem;
    ssl_certificate_key /etc/nginx/cert/b.com.key;
    ssl_session_timeout 5m;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_prefer_server_ciphers on;
    
    client_max_body_size 20M;

    location /static/ {
        alias   /var/www/b.com/static/;
    }
    
    location / {
         proxy_pass http://127.0.0.1:6000;
         proxy_set_header Host $host;
         proxy_set_header X-Real-IP $remote_addr;
         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
         proxy_send_timeout 600;
         proxy_connect_timeout 600;
         proxy_read_timeout 600;    
    } 
}
```

## 4. 将`/admin/*`路径所有请求分流到另一台服务器上

将 `django` 服务挂载到 `www.b.com/admin/` 下，`www.b.com`同时由多个服务器提供独立的服务。

为使 nginx 能正确区分来自`django`的请求（静态、动态），`django`服务强制客户端在请求的`cookies`上标识`{"svr": "django"}`。

具体配置如下：

```
server {
    listen 443 ssl http2;
    server_name www.b.com;
    
    # other setting ...
    
    location / {
        set $dj '1';
        
        if ($cookie_svr ~* ^.django.*$ ){
             set $dj 1$dj ;
        }
        if ($request_uri ~* ^/admin/.*$ ){
            set $dj '1' ;
        }

        if ($dj = '11' ){
           rewrite ^/(.*)$ /admin/$1 permanent;
        }

        index index.html index.htm;
    }

    # admin
    location /admin/ {
         rewrite ^/admin/(.*)$ /$1 break;
         proxy_pass http://127.0.0.1:8000;
         proxy_set_header Host $host;
         proxy_set_header X-Real-IP $remote_addr;
         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
         proxy_send_timeout 600;
         proxy_connect_timeout 600;
         proxy_read_timeout 600;
    }

}
server {
    listen 80;
    server_name www.b.com;
    rewrite ^(.*)$ https://$host$1 permanent;
}
```

注意:
- `nginx`下`if`不能嵌套，没有`else`
- 通过`$cookie_svr`可以获取到`svr`的值
- 要正确使用`rewrite`的停止标志(`last`, `break`, `permanent`)


## 5. 负载均衡

通过 `nginx` 的 `stream` 实现负载均衡

```

user root;
worker_processes  auto;

events {
    worker_connections  1024;
}


stream {
	log_format lbs '$remote_addr -> $upstream_addr [$time_local] '
                 '$protocol $status $bytes_sent $bytes_received '
                 '$session_time  "$upstream_connect_time"';

    access_log /var/log/nginx/access.log  lbs ;
    open_log_file_cache off;

	upstream backend {
        hash $remote_addr consistent;
        server backend-1:18888;
        server backend-2:18888;
        server backend-3:18888;
        server backend-4:18888;
	}

    server {
        listen 18888;
        listen 18888 udp;

		proxy_pass backend;
    }
```


## 6. try_files

```
server {
    ...

    location ^~ /static/html/ {
        alias /opt/code/pages/html/;
        try_files $uri /static/html/index.html;
   }
}
```

## 7. `location + if`

``` 
server {
    location ^~ /static/html/ {
        if ($url ~* \.(png|jpg)$ ){
            rewrite ^/(.*)$ https://my-bucket.oss-cn-shenzhen.aliyuncs.com/$1 permanent;
        }
        alias /opt/code/pages/html/;
        try_files $uri /static/html/index.html;
    }
}
```
