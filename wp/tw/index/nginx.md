# Nginx

## 概述

Nginx 是一款高效能的 Web 伺服器，也可用作反向代理、負載均衡器和 HTTP 快取。

## 基本概念

### 與 Apache 比較

| 特性 | Nginx | Apache |
|------|-------|--------|
| 架構 | 事件驅動、非阻塞 | 行程/執行緒驅動 |
| 效能 | 高併發、低記憶體 | 穩定、相容性廣 |
| 靜態內容 | 優秀 | 良好 |
| 動態內容 | 需配合後端 | 原生支援 |
| 設定 | 簡潔 | 複雜但彈性 |

### 工作原理

```
                    ┌─────────────┐
    Request ───────►│   Nginx     │
                    │             │
                    │  upstream   │
                    │   servers  │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
         ┌────▼────┐ ┌────▼────┐ ┌────▼────┐
         │  Server  │ │  Server  │ │  Server  │
         │    1     │ │    2     │ │    3     │
         └─────────┘ └─────────┘ └─────────┘
```

## 基本設定

### 安裝與啟動

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nginx

# macOS
brew install nginx

# 基本操作
sudo nginx              # 啟動
sudo nginx -s reload    # 重新載入設定
sudo nginx -s stop      # 停止
sudo nginx -t           # 測試設定檔
```

### 設定檔結構

```nginx
# /etc/nginx/nginx.conf
worker_processes auto;
error_log /var/log/nginx/error.log;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    access_log /var/log/nginx/access.log;
    
    sendfile on;
    
    # 其他設定檔
    include /etc/nginx/conf.d/*.conf;
}
```

### 靜態網站

```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/html;
    
    index index.html index.htm;
    
    location / {
        try_files $uri $uri/ =404;
    }
    
    location /images/ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

## 反向代理

### 基本設定

```nginx
server {
    listen 80;
    server_name api.example.com;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### FastAPI 應用

```nginx
server {
    listen 80;
    server_name api.example.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        
        # 超時設定
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

## 負載均衡

### 輪詢（預設）

```nginx
upstream backend {
    server 127.0.0.1:3000;
    server 127.0.0.1:3001;
    server 127.0.0.1:3002;
}

server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://backend;
    }
}
```

### 加權輪詢

```nginx
upstream backend {
    server 127.0.0.1:3000 weight=3;
    server 127.0.0.1:3001 weight=2;
    server 127.0.0.1:3002 weight=1;
}
```

### 健康檢查

```nginx
upstream backend {
    server 127.0.0.1:3000;
    server 127.0.0.1:3001;
    server 127.0.0.1:3002;
}

server {
    ...
    location / {
        proxy_pass http://backend;
        proxy_next_upstream error timeout http_500 http_502 http_503;
    }
}
```

## SSL/TLS 設定

### Let's Encrypt 免費憑證

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d example.com -d www.example.com
```

### 強制 HTTPS

```nginx
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com;
    
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    
    location / {
        proxy_pass http://localhost:3000;
    }
}
```

## 快取設定

```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m 
                 max_size=1g inactive=60m use_temp_path=off;

server {
    ...
    location / {
        proxy_cache my_cache;
        proxy_cache_valid 200 60m;
        proxy_cache_valid 404 1m;
        add_header X-Cache-Status $upstream_cache_status;
    }
}
```

## 常用命令

```bash
# 測試設定
nginx -t

# 重新載入
nginx -s reload

# 停止
nginx -s stop

# 查看版本
nginx -v

# 顯示編譯參數
nginx -V
```

## 參考資源

- [Nginx 官方網站](https://nginx.org/)
- [Nginx 文件](https://nginx.org/en/docs/)
- [Nginx Ultimate Guide](https://docs.nginx.com/)
