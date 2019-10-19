---
layout: post
title:  openresty使用笔记
category: 技术
tags:  docker, openresty
keywords: 
description: 
---

# openresty使用笔记

## 1. 配置 openresty 环境

通过 docker-compose 安装 openresty

docker-compose.yml 配置如下：

```
version: '3.7'
services:
  nginx:
    image: openresty/openresty
    container_name: nginx
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - "./openresty_setting.conf:/usr/local/openresty/nginx/conf/nginx.conf:ro"
      - "/var/log:/var/log"
    environment:
      TZ: Asia/Shanghai
    networks:
      - nginx-web


networks:
  nginx-web:
    driver: bridge

```

openresty 配置实例, `openresty_setting.conf`文件如下：

```
# nginx.conf  --  docker-openresty
#
# This file is installed to:
#   `/usr/local/openresty/nginx/conf/nginx.conf`
# and is the file loaded by nginx at startup,
# unless the user specifies otherwise.
#
# It tracks the upstream OpenResty's `nginx.conf`, but removes the `server`
# section and adds this directive:
#     `include /etc/nginx/conf.d/*.conf;`
#
# The `docker-openresty` file `nginx.vh.default.conf` is copied to
# `/etc/nginx/conf.d/default.conf`.  It contains the `server section
# of the upstream `nginx.conf`.
#
# See https://github.com/openresty/docker-openresty/blob/master/README.md#nginx-config-files
#

user root;
worker_processes  auto;

#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

#pid        logs/nginx.pid;


events {
    worker_connections  1024;
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

	# include /etc/nginx/mime.types;
	include       /usr/local/openresty/nginx/conf/mime.types;    
	default_type application/octet-stream;

	##
	# Logging Settings
	##

	access_log /var/log/nginx/access.log;
	error_log /var/log/nginx/error.log;

	##
	# Gzip Settings
	##

	gzip on;
    gzip_static on;
	# gzip_vary on;
	gzip_proxied any;
	gzip_comp_level 4;
	gzip_buffers 16 8k;
	gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

	##
	# Virtual Host Configs
	##

	##################################
    # demo.com
    ##################################
    server {
        listen 443 ssl http2;
        server_name demo.com;

        location / {
             proxy_pass http://django:6000;
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
        server_name demo.com;
        rewrite ^(.*)$ https://$host$1 permanent;
    }
}

```

## 2. 使用 lua 在请求 header 上写入请求到达时的时间戳


```
http {

    server {
            listen 80;

            location / {
                    rewrite_by_lua '
                        ngx.req.set_header("RTIME", ngx.req.start_time()*1000)
                    ';

                    proxy_set_header X-Real-IP $remote_addr;
                    proxy_pass http://127.0.0.1:8888;
            }
    }
}

```