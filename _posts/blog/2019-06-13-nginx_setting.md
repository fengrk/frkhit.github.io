---
layout: post
title: nginx 配置
category: 技术
tags: nginx
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

## 3. 反向代理

``` 
server {

    listen 80;

    server_name www.b.com;

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
