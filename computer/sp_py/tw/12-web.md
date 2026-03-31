# 12. Web 網路結構與 Server

Web 是現代網際網路的核心應用，從簡單的靜態網頁到複雜的單頁應用程式（Single Page Application），從社交媒體到電子商務，Web 技術已深入我們生活的各個層面。本章將深入探討 HTTP/HTTPS 協定的詳細規格、Web 伺服器的架構設計、負載平衡與反向代理、CDN 與快取策略，以及現代 Web 應用程式開發的實務知識。這些內容對於開發高效、安全、可擴展的 Web 應用至關重要。

## 12.1 HTTP/HTTPS 協定

### 12.1.1 HTTP 協定的演進

HTTP（HyperText Transfer Protocol）是 Web 的基礎應用層協定，由 Tim Berners-Lee 在 1990 年代初設計用於分發 HTML 文件。HTTP 的發展經歷了多個重要版本，每個版本都解決了前一代的某些限制並引入了新特性。

**HTTP/1.0（1996）**

HTTP/1.0 是第一個被廣泛採用的 HTTP 版本，定義了基本的客戶端-伺服器請求-回應模型。每個 HTTP 請求/回應對使用一個獨立的 TCP 連線。HTTP/1.0 的主要限制包括：

- 每個請求需要建立新的 TCP 連線，完成後立即關閉
- 頻繁的 TCP 握手導致顯著的延遲開銷
- 缺乏虛擬主機支援——多個網站可能共享同一 IP 位址
- 無法追蹤請求的相對上下文

**HTTP/1.1（1999）**

HTTP/1.1 是對 HTTP/1.0 的大幅修訂，引入了多項關鍵改進：

| 特性 | 說明 |
|------|------|
| 持久連線（Keep-Alive） | 預設使用同一 TCP 連線處理多個請求 |
| 管道化（Pipelining） | 客戶端可在收到回應前發送多個請求 |
| 分塊傳輸編碼 | 伺服器可流式傳輸回應 |
| 虛擬主機 | Host 頭部支援多網站共享 IP |
| 內容協商 | 用戶端和伺服器協商最佳內容格式 |
| 更好的快取支援 | ETag、If-Modified-Since |

HTTP/1.1 仍然有一些根本性限制：頭部重複（每次請求都需傳送相同的頭部）、管道化支援不足（HOL 阻塞問題）、單一請求-回應模型（伺服器不能主動推送資料）。

**HTTP/2（2015）**

HTTP/2 解決了 HTTP/1.1 的諸多限制，引入了革命性的改進：

| 特性 | 說明 |
|------|------|
| 二進制框架 | 將訊息分解為二進制幀，而非文字 |
| 多工（Multiplexing） | 單一連線上並行多個請求-回應 |
| 標頭壓縮（HPACK） | 使用霍夫曼編碼和索引表壓縮頭部 |
| 伺服器推送 | 伺服器可主動推送資源 |
| 流控制 | 每個流獨立的流量控制 |
| 優先級 | 客戶端可指定請求的優先順序 |

HTTP/2 的多工機制徹底解決了 HTTP/1.1 的頭部阻塞問題。單一 TCP 連線上可以並行傳輸任意數量的雙向流，每個流由多個幀組成，幀可以交錯傳輸而在接收端重新組裝。

**HTTP/3（2022）**

HTTP/3 是 HTTP 家族的最新成員，建立在 QUIC 協定之上，QUIC 本身是基於 UDP 實現的。HTTP/3 的主要動機是解決 TCP 的一些根本限制：

| 特性 | 說明 |
|------|------|
| 基於 UDP | 擺脫 TCP 的束縛，實現更靈活的傳輸控制 |
| 0-RTT 握手 | 對於曾經連接過的伺服器，無需等待來回就能傳送資料 |
| 無 TCP 頭部阻塞 | UDP 沒有 TCP 的 HOL 阻塞問題 |
| 連線遷移 | 網路切換（如 WiFi 切換到蜂巢）時連線不中斷 |
| 改進的擁塞控制 | 每個連線有自己的擁塞控制 |

HTTP/3 的部署正在快速增長，主要瀏覽器和 CDN 提供商都已支援。

### 12.1.2 HTTP 訊息格式

HTTP 是文字協定（除 HTTP/2 和 HTTP/3 的二進制框架外），訊息由起始行、頭部欄位、可選的訊息主體組成。

**HTTP 請求訊息格式**

```
GET /path/to/resource HTTP/1.1\r\n
Host: www.example.com\r\n
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)\r\n
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n
Accept-Language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7\r\n
Accept-Encoding: gzip, deflate, br\r\n
Connection: keep-alive\r\n
\r\n
```

- **請求行**：方法、請求 URI、HTTP 版本
- **頭部欄位**：鍵值對，提供請求的元資料
- **空行**：頭部結束標記
- **訊息主體**：POST/PUT 請求攜帶的資料

**HTTP 回應訊息格式**

```
HTTP/1.1 200 OK\r\n
Server: nginx/1.18.0\r\n
Date: Wed, 25 Mar 2026 10:00:00 GMT\r\n
Content-Type: text/html; charset=utf-8\r\n
Content-Length: 1234\r\n
Cache-Control: max-age=3600\r\n
ETag: "abc123"\r\n
\r\n
<!DOCTYPE html>
<html>...
```

- **狀態行**：HTTP 版本、狀態碼、原因短語
- **頭部欄位**：回應的元資料
- **空行**：頭部結束標記
- **訊息主體**：實際的內容（HTML、JSON、圖片等）

**HTTP/2 幀格式**

HTTP/2 將訊息分割為二進制幀，每個幀有固定的 9 位元組頭部：

```
+---------------+Packet Length-------------+
|  Length (24 bits)  | Type (8) | Flags (8) |
+---------------------+----------+-----------+
|              R |     Stream Identifier     |
|              (1)|         (31 bits)          |
+---------------------+-----------------------+
|               Frame Payload               |
+------------------------------------------+
```

主要幀類型包括：HEADERS（攜帶壓縮的頭部）、DATA（攜帶請求/回應主體）、SETTINGS（連線參數）、WINDOW_UPDATE（流量控制）等。

### 12.1.3 HTTP 狀態碼

HTTP 狀態碼是三位數字，用於表示伺服器對請求的處理結果。狀態碼分為五類：

| 類別 | 範圍 | 意義 | 典型原因 |
|------|------|------|----------|
| 1xx | 100-199 | 資訊性 | 伺服器正在處理請求 |
| 2xx | 200-299 | 成功 | 請求已成功處理 |
| 3xx | 300-399 | 重新導向 | 需要進一步操作完成請求 |
| 4xx | 400-499 | 客戶端錯誤 | 請求有語法錯誤或無法完成 |
| 5xx | 500-599 | 伺服器錯誤 | 伺服器處理請求時出錯 |

**常見的 2xx 狀態碼**

| 狀態碼 | 說明 | 使用場景 |
|--------|------|----------|
| 200 | OK | 請求成功，回應包含資源內容 |
| 201 | Created | 資源已成功創建（POST 結果） |
| 204 | No Content | 請求成功，但無回應內容 |
| 206 | Partial Content | 部分內容（如斷點續傳） |

**常見的 3xx 狀態碼**

| 狀態碼 | 說明 | 使用場景 |
|--------|------|----------|
| 301 | Moved Permanently | 資源永久移至新 URL |
| 302 | Found | 臨時重定向（POST 後不應使用） |
| 303 | See Other | 重定向到其他 URI（如 POST-Redirect-GET） |
| 304 | Not Modified | 快取未過期，無需重新傳輸內容 |
| 307 | Temporary Redirect | 臨時重定向，保持請求方法 |
| 308 | Permanent Redirect | 永久重定向，保持請求方法 |

**常見的 4xx 狀態碼**

| 狀態碼 | 說明 | 使用場景 |
|--------|------|----------|
| 400 | Bad Request | 請求語法錯誤或無效參數 |
| 401 | Unauthorized | 需要身份驗證 |
| 403 | Forbidden | 伺服器拒絕處理請求 |
| 404 | Not Found | 請求的資源不存在 |
| 405 | Method Not Allowed | 不支援該 HTTP 方法 |
| 409 | Conflict | 請求與伺服器狀態衝突 |
| 429 | Too Many Requests | 請求頻率超過限制 |

**常見的 5xx 狀態碼**

| 狀態碼 | 說明 | 使用場景 |
|--------|------|----------|
| 500 | Internal Server Error | 伺服器內部錯誤（未處理的異常） |
| 501 | Not Implemented | 不支援請求的功能 |
| 502 | Bad Gateway | 代理/閘道收到無效回應 |
| 503 | Service Unavailable | 伺服器暫時過載或維護中 |
| 504 | Gateway Timeout | 代理/閘道等待超時 |

### 12.1.4 HTTPS 原理

HTTPS（HTTP Secure）是 HTTP 的安全版本，通過 TLS（Transport Layer Security）協定提供加密、身份驗證和完整性保護。

**HTTPS 的三個目標**

| 目標 | 說明 | 實現機制 |
|------|------|----------|
| 機密性 | 防止竊聽者讀取傳輸內容 | 對稱加密（AES、ChaCha20） |
| 完整性 | 防止篡改傳輸內容 | 訊息認證碼（HMAC） |
| 認證 | 確認伺服器（和可選的客戶端）身份 | PKI 憑證 |

**TLS 協定層次**

```
┌────────────────────────────────────────┐
│            HTTP                         │
├────────────────────────────────────────┤
│            TLS 1.3                      │
│   ┌──────────────────────────────────┐ │
│   │ Handshake: 密鑰交換、身份驗證    │ │
│   │ Record: 加密、MAC、分片          │ │
│   └──────────────────────────────────┘ │
├────────────────────────────────────────┤
│            TCP                         │
├────────────────────────────────────────┤
│            IP                          │
└────────────────────────────────────────┘
```

**TLS 1.3 握手流程**

TLS 1.3 相比 TLS 1.2 大幅簡化了握手流程，將握手延遲從 2-RTT 減少到 1-RTT（對已知伺服器可達 0-RTT）：

```
客戶端                                              伺服器
   │                                                 │
   │ ──── ClientHello (supported_versions,          │
   │         key_share*, cipher_suites,             │
   │         signature_algorithms) ──────────────► │
   │     (*) 表示 TLS 1.3 新增                       │
   │                                                 │
   │      (此時客戶端已有早期資料（0-RTT）的密鑰)     │
   │                                                 │
   │ ◄──── ServerHello (selected_version,          │
   │         key_share, cipher_suite) ─────────── │
   │ ◄──── {Certificate, CertificateVerify,        │
   │         Finished}_keyshare                    │
   │                                                 │
   │ ──── {Finished}_keyshare ──────────────────► │
   │                                                 │
   │        (密鑰已確認，開始加密通訊)               │
```

TLS 1.3 的關鍵改進：

- 移除 RSA 金鑰交換（採用前向保密的 Diffie-Hellman）
- 簡化密碼套件協商
- 減少握手往返次數
- 移除 SHA-1 等不安全的雜湊演算法

**數位憑證與 PKI**

HTTPS 使用 X.509 數位憑證來驗證伺服器身份。憑證由受信任的憑證授權中心（CA）簽發：

```
憑證內容：
- 主體名稱 (Subject): www.example.com
- 發證機構 (Issuer): DigiCert Inc
- 公鑰: 0x12345678...
- 有效期: 2026-01-01 至 2027-01-01
- 擴展: SAN, Key Usage, ...
- CA 數位簽章: SHA256-RSA ...
```

用戶端驗證憑證的過程：

1. 檢查憑證是否由信任的 CA 簽發
2. 檢查憑證是否在有效期內
3. 檢查主體名稱是否與訪問的網站匹配
4. 檢查憑證是否已被撤銷（CRL/OCSP）

### 12.1.5 HTTP 頭部詳解

HTTP 頭部欄位提供了關於請求和回應的大量元資料，可以分為幾類：

**通用頭部（General Headers）**

| 頭部 | 說明 | 範例 |
|------|------|------|
| Date | 訊息創建時間 | `Date: Wed, 25 Mar 2026 10:00:00 GMT` |
| Cache-Control | 快取控制指示 | `Cache-Control: max-age=3600, no-cache` |
| Connection | 連線控制 | `Connection: keep-alive` |
| Transfer-Encoding | 傳輸編碼 | `Transfer-Encoding: chunked` |

**請求頭部（Request Headers）**

| 頭部 | 說明 | 範例 |
|------|------|------|
| Host | 目標主機 | `Host: www.example.com` |
| User-Agent | 用戶端標識 | `User-Agent: Mozilla/5.0...` |
| Accept | 可接受的內容類型 | `Accept: text/html, application/json` |
| Accept-Encoding | 可接受的編碼 | `Accept-Encoding: gzip, br` |
| Authorization | 認證憑證 | `Authorization: Bearer token123` |
| Cookie | HTTP Cookie | `Cookie: session=abc123` |

**回應頭部（Response Headers）**

| 頭部 | 說明 | 範例 |
|------|------|------|
| Content-Type | 內容類型 | `Content-Type: text/html; charset=utf-8` |
| Content-Length | 內容長度 | `Content-Length: 1234` |
| Content-Encoding | 內容編碼 | `Content-Encoding: gzip` |
| ETag | 資源版本標識 | `ETag: "abc123"` |
| Set-Cookie | 設定 Cookie | `Set-Cookie: session=xyz; HttpOnly` |
| Strict-Transport-Security | HSTS | `Strict-Transport-Security: max-age=31536000` |

## 12.2 Web Server 架構

### 12.2.1 Web 伺服器的基本功能

Web 伺服器的核心任務是接收 HTTP 請求、處理請求、返回 HTTP 回應。現代 Web 伺服器需要支援：

- 高並發連線處理
- 靜態檔案服務
- 動態內容生成
- SSL/TLS 終止
- 反向代理和負載平衡
- 請求/回應過濾和處理
- 日誌記錄
- 虛擬主機（多網站托管）

### 12.2.2 簡單 Web Server 實作

```python
# Python 實現的簡單 HTTP 伺服器
import socket
import threading
from datetime import datetime

class HTTPServer:
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.routes = {}
    
    def handle_request(self, client_socket, client_addr):
        """處理單個客戶端請求"""
        try:
            # 接收請求
            request = client_socket.recv(4096).decode('utf-8', errors='ignore')
            if not request:
                return
            
            # 解析請求行
            lines = request.split('\r\n')
            request_line = lines[0]
            method, path, version = request_line.split(' ')
            
            print(f"{datetime.now()} - {method} {path} from {client_addr}")
            
            # 路由處理
            if path in self.routes:
                status, content_type, response_body = self.routes[path]()
            else:
                status = "404 Not Found"
                content_type = "text/plain"
                response_body = b"Not Found"
            
            # 構造回應
            response_headers = (
                f"HTTP/1.1 {status}\r\n"
                f"Content-Type: {content_type}\r\n"
                f"Content-Length: {len(response_body)}\r\n"
                f"Connection: close\r\n"
                f"\r\n"
            ).encode('utf-8')
            
            client_socket.sendall(response_headers + response_body)
            
        except Exception as e:
            print(f"Error handling request: {e}")
        finally:
            client_socket.close()
    
    def route(self, path):
        """裝飾器：用於註冊路由處理函式"""
        def decorator(func):
            self.routes[path] = func
            return func
        return decorator
    
    def start(self):
        """啟動伺服器"""
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(128)
        print(f"Server listening on {self.host}:{self.port}")
        
        try:
            while True:
                client_socket, client_addr = self.server_socket.accept()
                thread = threading.Thread(
                    target=self.handle_request,
                    args=(client_socket, client_addr)
                )
                thread.daemon = True
                thread.start()
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            self.server_socket.close()

# 使用範例
app = HTTPServer()

@app.route('/')
def index():
    html = b"<html><body><h1>Hello, Web!</h1></body></html>"
    return "200 OK", "text/html", html

@app.route('/api/time')
def time():
    import json
    data = json.dumps({"time": datetime.now().isoformat()}).encode()
    return "200 OK", "application/json", data

app.start()
```

### 12.2.3 Nginx 架構

Nginx 是目前最流行的 Web 伺服器之一，以其高性能、低記憶體消耗和反向代理能力著稱。Nginx 採用了完全不同的架構設計，與傳統的 Apache 有本質區別。

**事件驅動、非阻塞 I/O 模型**

Nginx 採用事件驅動架構，使用非阻塞 I/O 和多路復用機制（epoll、kqueue、IOCP）。這種設計使得單個 worker 行程可以處理數千個並發連線，而無需為每個連線創建執行緒或程序。

```
┌────────────────────────────────────────────────────────────┐
│                    Master Process                          │
│  - 讀取和驗證配置                                          │
│  - 管理 worker 行程                                        │
│  - 監聽控制訊號                                            │
│  - 熱重載配置和二進制升級                                  │
└────────────────────────────────────────────────────────────┘
              │ fork/exec
              ▼
┌────────────────────────────────────────────────────────────┐
│  Worker Process 1    Worker Process 2    Worker Process N  │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   │
│  │ Event Loop   │   │ Event Loop   │   │ Event Loop   │   │
│  │ (epoll/kqueue)  │ (epoll/kqueue)  │ (epoll/kqueue)  │
│  └──────────────┘   └──────────────┘   └──────────────┘   │
│         │                 │                 │              │
│         └─────────────────┼─────────────────┘              │
│                           │                               │
│                           ▼                               │
│                  ┌─────────────────┐                      │
│                  │   Shared Memory  │                      │
│                  │ (快取、連線池) │                      │
│                  └─────────────────┘                      │
└────────────────────────────────────────────────────────────┘
```

**Nginx 設定範例**

```nginx
# 全域設定
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /run/nginx.pid;

events {
    worker_connections 10240;
    use epoll;
    multi_accept on;
}

http {
    # MIME 類型
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    # 日誌格式
    log_format main '$remote_addr - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent"';
    access_log /var/log/nginx/access.log main;
    
    # 效能優化
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    
    # Gzip 壓縮
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml application/json 
               application/javascript application/rss+xml;
    
    # 上游伺服器組
    upstream backend {
        least_conn;
        server 127.0.0.1:8080;
        server 127.0.0.1:8081;
        keepalive 32;
    }
    
    # 虛擬主機配置
    server {
        listen 80;
        server_name example.com www.example.com;
        
        # HTTP 強制跳轉到 HTTPS
        return 301 https://$server_name$request_uri;
    }
    
    server {
        listen 443 ssl http2;
        server_name example.com;
        
        # SSL 憑證
        ssl_certificate /etc/nginx/ssl/example.com.crt;
        ssl_certificate_key /etc/nginx/ssl/example.com.key;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
        ssl_prefer_server_ciphers off;
        
        # 安全頭部
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        
        # 靜態檔案服務
        location /static/ {
            alias /var/www/static/;
            expires 30d;
            add_header Cache-Control "public, immutable";
        }
        
        # 反向代理到上游
        location /api/ {
            proxy_pass http://backend;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_buffering off;
            proxy_request_buffering off;
        }
        
        # 健康檢查端點
        location /health {
            access_log off;
            return 200 "OK\n";
            add_header Content-Type text/plain;
        }
    }
}
```

### 12.2.4 常見 Web 伺服器比較

| 特性 | Nginx | Apache | Caddy |
|------|-------|--------|-------|
| 架構模型 | 事件驅動 | 程序/執行緒 | 事件驅動 |
| 記憶體效率 | 極高 | 中等 | 高 |
| 靜態內容效能 | 極高 | 高 | 高 |
| 動態內容 | 需配合 | 原生支援模組 | 需配合 |
| 設定複雜度 | 中等 | 中等 | 簡單（自動 HTTPS） |
| 熱重載 | 支援 | 支援 | 支援 |

## 12.3 負載平衡與反向代理

### 12.3.1 負載平衡概念

負載平衡（Load Balancing）是將工作負載分散到多個計算資源（如伺服器、叢集）上的技術，用於：

- **提高效能**：並行處理更多請求
- **提高可用性**：某節點故障不影響整體服務
- **可擴展性**：根據負載動態調整容量
- **地理分散**：將用戶導向最近的節點

### 12.3.2 負載平衡演算法

**靜態負載平衡**（不考慮伺服器當前狀態）

| 演算法 | 說明 | 優點 | 缺點 |
|--------|------|------|------|
| Round Robin | 輪流分配 | 簡單 | 不考慮伺服器差異 |
| Weighted Round Robin | 根據權重輪詢 | 支援異構伺服器 | 需要配置權重 |
| IP Hash | 對客戶端 IP 雜湊 | Session 親和性 | 不均衡 |
| Random | 隨機選擇 | 簡單 | 不確定性 |

**動態負載平衡**（考慮伺服器當前狀態）

| 演算法 | 說明 | 優點 | 缺點 |
|--------|------|------|------|
| Least Connections | 選擇連線數最少 | 自適應 | 計算開銷 |
| Weighted Least Connections | 考慮權重和連線數 | 精確 | 複雜 |
| Response Time | 根據回應時間選擇 | 使用者體驗 | 需要測量延遲 |
| Resource Based | 根據 CPU/記憶體選擇 | 自適應 | 需要監控 |

### 12.3.3 健康檢查

負載平衡器需要監控後端伺服器的健康狀態，自動移除故障節點：

| 檢查類型 | 說明 | 配置參數 |
|----------|------|----------|
| TCP 連線檢查 | 嘗試建立 TCP 連線 | 目標連接埠、超時 |
| HTTP/HTTPS 檢查 | 發送 HTTP GET 請求 | URL、路徑、預期狀態碼 |
| TLS 檢查 | 檢查 SSL 憑證 | 憑證過期警告 |
| 自定義檢查 | 執行腳本或命令 | 腳本路徑 |

```
配置範例（health_check 間隔 5 秒，超時 3 秒，失敗 2 次移除，成功 3 次恢復）：

health_check {
    interval 5s
    timeout 3s
    fails 2
    rises 3
    uri /health
    expected O
}
```

### 12.3.4 反向代理

反向代理位於客戶端和伺服器之間，代表伺服器處理請求。與正向代理（代表客戶端）相反：

- **正向代理**：客戶端 → 代理 → 網際網路 → 伺服器（客戶端匿名）
- **反向代理**：客戶端 → 代理 → 伺服器（伺服器匿名）

反向代理的用途：

| 用途 | 說明 |
|------|------|
| SSL 終止 | 在邊緣終止 TLS，在內部使用 HTTP |
| 負載平衡 | 分散請求到多個後端 |
| 快取靜態內容 | 減輕後端負載 |
| 壓縮 | 壓縮回應減少頻寬 |
| 安全過濾 | 過濾惡意請求 |
| A/B 測試 | 流量分割 |

## 12.4 CDN 與快取策略

### 12.4.1 CDN 原理

CDN（Content Delivery Network，內容傳遞網路）透過在全球部署邊緣節點，將內容分發到靠近用戶的位置，減少傳輸延遲。

```
┌─────────────────────────────────────────────────────────┐
│                      原始伺服器                          │
│                   (origin server)                       │
└────────────────────────┬────────────────────────────────┘
                         │ Origin Pull / Push
                         ▼
┌─────────────────────────────────────────────────────────┐
│                     CDN 骨幹網路                         │
│                  (POP: Points of Presence)              │
├─────────────────────────────────────────────────────────┤
│    PoP-1        PoP-2        PoP-3        PoP-N         │
│   (亞洲)       (美洲)       (歐洲)       (其他)         │
│    │              │              │              │        │
└────┼──────────────┼──────────────┼──────────────┼────────┘
     │              │              │              │
     ▼              ▼              ▼              ▼
┌────────┐     ┌────────┐     ┌────────┐     ┌────────┐
│ 用戶 A │     │ 用戶 B │     │ 用戶 C │     │ 用戶 D │
└────────┘     └────────┘     └────────┘     └────────┘
```

**CDN 工作模式**

| 模式 | 說明 | 延遲 | 負載 |
|------|------|------|------|
| Origin Pull | 首次請求時從源拉取 | 首次慢 | 源伺服器 |
| Origin Push | 內容主動推送到 CDN | 首次快 | 發布時 |

### 12.4.2 HTTP 快取

HTTP 快取是減少網路請求、加快頁面載入的關鍵技術。

**Cache-Control 頭部**

| 指示詞 | 說明 |
|--------|------|
| `max-age=<seconds>` | 客戶端願意接受的最大緩存時間 |
| `s-maxage=<seconds>` | 共享快取（如 CDN）的最大緩存時間 |
| `no-cache` | 每次使用前必須向伺服器驗證 |
| `no-store` | 完全禁止快取（包括記憶體） |
| `private` | 只能在客戶端（瀏覽器）快取 |
| `public` | 可被任何快取儲存 |
| `must-revalidate` | 過期後必須重新驗證 |

**快取層級**

```
┌─────────────────────────────────────────────────────────┐
│                    瀏覽器快取                           │
│  - Disk Cache: 持久化快取                              │
│  - Memory Cache: 記憶體快取，關閉視窗清除                │
└────────────────────────┬────────────────────────────────┘
                         │ miss
                         ▼
┌─────────────────────────────────────────────────────────┐
│                    CDN/Proxy 快取                        │
│  - 邊緣節點快取                                        │
│  - 區域性快取                                          │
└────────────────────────┬────────────────────────────────┘
                         │ miss
                         ▼
┌─────────────────────────────────────────────────────────┐
│                    應用程式快取                          │
│  - Redis、Memcached                                    │
│  - 資料庫查詢結果                                       │
└────────────────────────┬────────────────────────────────┘
                         │ miss
                         ▼
┌─────────────────────────────────────────────────────────┐
│                      資料庫                              │
└─────────────────────────────────────────────────────────┘
```

### 12.4.3 條件請求

條件請求允許客戶端在資源未變更時避免下載完整內容：

**If-Modified-Since / Last-Modified**

```
客戶端請求：
GET /style.css HTTP/1.1
If-Modified-Since: Wed, 25 Mar 2026 10:00:00 GMT

伺服器回應（資源未變更）：
HTTP/1.1 304 Not Modified
Cache-Control: max-age=3600

伺服器回應（資源已變更）：
HTTP/1.1 200 OK
Last-Modified: Thu, 26 Mar 2026 10:00:00 GMT
Content-Length: 1234

[完整內容]
```

**If-None-Match / ETag**

ETag 是伺服器為資源生成的唯一標識符，通常基於內容雜湊：

```
客戶端請求：
GET /api/data.json HTTP/1.1
If-None-Match: "abc123"

伺服器回應（資源未變更）：
HTTP/1.1 304 Not Modified
ETag: "abc123"

伺服器回應（資源已變更）：
HTTP/1.1 200 OK
ETag: "def456"
Content-Length: 5678

[完整內容]
```

## 12.5 網頁應用程式開發

### 12.5.1 Web 框架演進

Web 開發框架經歷了從 CGI 到現代全端框架的演進：

**第一代：CGI（Common Gateway Interface）**

最早的動態 Web 技術，每個請求fork一個新程序：

```c
// C CGI 範例
#include <stdio.h>
int main() {
    printf("Content-Type: text/html\n\n");
    printf("<html><body>Hello, %s!</body></html>", getenv("QUERY_STRING"));
}
```

**第二代：mod_perl、PHP**

嵌入式指令碼語言，在伺服器程序內執行：

```php
<?php
$name = $_GET['name'];
echo "<html><body>Hello, $name!</body></html>";
?>
```

**第三代：MVC 框架**

Model-View-Controller 架構，分離關注點：

```
請求 → 路由 → 控制器 → 模型 → 視圖 → 回應
         ↓
       中間件（認證、日誌等）
```

### 12.5.2 現代 Web 框架比較

| 框架 | 語言 | 特點 | 適用場景 |
|------|------|------|----------|
| Express | JavaScript | 簡單、彈性、龐大生態 | 輕量 API、Node.js 應用 |
| Flask | Python | 輕量、簡單、靈活 | 微服務、原型開發 |
| Django | Python | 全功能、ORM、管理介面 | 企業級 Web 應用 |
| Spring Boot | Java | 企業級、依賴注入 | 大型企業應用 |
| Rails | Ruby | 慣例優於設定、內建功能 | 快速開發 |
| Next.js | JavaScript | React SSR/SSG | 全端 React 應用 |
| FastAPI | Python | 自動 API 文件、非同步 | 高效能 API |

### 12.5.3 RESTful API 設計

REST（Representational State Transfer）是一種 Web 服務架構風格，基於 HTTP 的語義：

**REST 約束**

| 約束 | 說明 |
|------|------|
| 客戶-伺服器架構 | 關注點分離 |
| 無狀態 | 每個請求包含所有必要資訊 |
| 可快取 | 回應可標記為可/不可快取 |
| 統一介面 | 資源透過 URI 識別 |
| 分層系統 | 客戶不知道是否直接連接終端伺服器 |

**RESTful API 設計範例**

| 方法 | URI | 意義 | 範例 |
|------|-----|------|------|
| GET | /users | 取得使用者列表 | `GET /users?page=1&limit=10` |
| GET | /users/{id} | 取得特定使用者 | `GET /users/123` |
| POST | /users | 創建新使用者 | `POST /users {name: "John"}` |
| PUT | /users/{id} | 完全更新使用者 | `PUT /users/123 {name: "Jane", email: "..."}` |
| PATCH | /users/{id} | 部分更新 | `PATCH /users/123 {name: "NewName"}` |
| DELETE | /users/{id} | 刪除使用者 | `DELETE /users/123` |

**RESTful API 最佳實踐**

1. **使用名詞而非動詞**： `/users` 而非 `/getUsers`
2. **使用 HTTP 方法**：GET 讀取、POST 創建、PUT 完全更新、PATCH 部分更新、DELETE 刪除
3. **使用複數名詞**： `/users` 而非 `/user`
4. **使用 HTTP 狀態碼**：200 OK、201 Created、400 Bad Request、404 Not Found 等
5. **提供分頁**： `GET /users?page=1&limit=20`
6. **錯誤處理**：一致的錯誤格式 `{"error": "message", "code": "ERROR_CODE"}`
7. **版本控制**： `/api/v1/users` 或 Header 中的 `Accept: application/vnd.api+json`

### 12.5.4 GraphQL vs REST

GraphQL 是 REST 的替代方案，提供更靈活的客戶端資料查詢：

```graphql
# GraphQL 查詢 - 客戶端指定需要的欄位
query {
  user(id: 123) {
    name
    email
    posts(first: 5) {
      title
      createdAt
    }
  }
}
```

| 特性 | REST | GraphQL |
|------|------|----------|
| 資料獲取 | 多個端點 | 單一端點 |
| 欄位選擇 | 固定回應格式 | 客戶端選擇欄位 |
| 快取 | HTTP 標準快取 | 需要額外處理 |
| 學習曲線 | 簡單 | 較陡 |
| 生態系統 | 成熟 | 成長中 |

### 12.5.5 WebSocket 即時通訊

HTTP 是請求-回應模型，伺服器無法主動推送資料。WebSocket 提供了雙向、全雙工的通訊通道：

```javascript
// WebSocket 客戶端
const ws = new WebSocket('wss://example.com/ws');

ws.onopen = () => {
    console.log('WebSocket connected');
    ws.send(JSON.stringify({type: 'subscribe', channel: 'prices'}));
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};

ws.onclose = () => {
    console.log('WebSocket disconnected');
};
```

**WebSocket 與 HTTP/2 的比較**

| 特性 | WebSocket | HTTP/2 |
|------|------------|---------|
| 方向 | 雙向 | 雙向（伺服器推送） |
| 瀏覽器支援 | 廣泛 | 廣泛 |
| 頭部開銷 | 僅連線時 | 每幀有小頭部 |
| 應用場景 | 即時遊戲、聊天 | 聊天、通知 |
| 代理支援 | 需升級 | 原生支援 |
