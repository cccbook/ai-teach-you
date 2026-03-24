# 12. Web 網路結構與 Server

## 12.1 HTTP/HTTPS 協定

[程式檔案：12-1-http-protocol.py](../_code/12/12-1-http-protocol.py)
```python
"""
HTTP 協定實作
"""

import socket
import ssl

# HTTP 請求
class HTTPRequest:
    """HTTP 請求類別"""
    
    METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS']
    
    def __init__(self, method='GET', path='/', version='HTTP/1.1'):
        self.method = method
        self.path = path
        self.version = version
        self.headers = {}
        self.body = None
    
    def add_header(self, key, value):
        """新增標頭"""
        self.headers[key] = value
    
    def to_bytes(self):
        """轉換為位元組"""
        request = f"{self.method} {self.path} {self.version}\r\n"
        
        for key, value in self.headers.items():
            request += f"{key}: {value}\r\n"
        
        request += "\r\n"
        
        if self.body:
            request += self.body
        
        return request.encode()

# HTTP 回應
class HTTPResponse:
    """HTTP 回應類別"""
    
    STATUS_CODES = {
        200: 'OK',
        201: 'Created',
        204: 'No Content',
        301: 'Moved Permanently',
        302: 'Found',
        400: 'Bad Request',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found',
        500: 'Internal Server Error',
        502: 'Bad Gateway',
        503: 'Service Unavailable',
    }
    
    def __init__(self, status_code=200, body='', content_type='text/html'):
        self.status_code = status_code
        self.body = body
        self.content_type = content_type
        self.headers = {}
    
    def add_header(self, key, value):
        """新增標頭"""
        self.headers[key] = value
    
    def to_bytes(self):
        """轉換為位元組"""
        status = self.STATUS_CODES.get(self.status_code, 'Unknown')
        response = f"HTTP/1.1 {self.status_code} {status}\r\n"
        
        self.headers['Content-Type'] = self.content_type
        self.headers['Content-Length'] = len(self.body)
        
        for key, value in self.headers.items():
            response += f"{key}: {value}\r\n"
        
        response += "\r\n"
        response += self.body
        
        return response.encode()

# HTTP 用戶端
class HTTPClient:
    """HTTP 用戶端"""
    
    def __init__(self):
        self.socket = None
    
    def request(self, method, url, headers=None, body=None):
        """發送 HTTP 請求"""
        # 解析 URL
        if url.startswith('https://'):
            return self.request_https(method, url, headers, body)
        else:
            return self.request_http(method, url, headers, body)
    
    def request_http(self, method, url, headers=None, body=None):
        """HTTP 請求"""
        import urllib.parse
        
        parsed = urllib.parse.urlparse(url)
        host = parsed.hostname
        port = parsed.port or 80
        path = parsed.path or '/'
        
        if parsed.query:
            path += '?' + parsed.query
        
        # 建立連線
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        
        # 發送請求
        request = HTTPRequest(method, path)
        request.add_header('Host', host)
        request.add_header('Connection', 'close')
        
        if headers:
            for key, value in headers.items():
                request.add_header(key, value)
        
        if body:
            request.body = body
            request.add_header('Content-Length', str(len(body)))
        
        self.socket.send(request.to_bytes())
        
        # 接收回應
        response_data = b''
        while True:
            chunk = self.socket.recv(4096)
            if not chunk:
                break
            response_data += chunk
        
        self.socket.close()
        
        return response_data.decode()
    
    def request_https(self, method, url, headers=None, body=None):
        """HTTPS 請求"""
        import urllib.parse
        
        parsed = urllib.parse.urlparse(url)
        host = parsed.hostname
        port = parsed.port or 443
        path = parsed.path or '/'
        
        if parsed.query:
            path += '?' + parsed.query
        
        # 建立 SSL 連線
        context = ssl.create_default_context()
        self.socket = context.wrap_socket(socket.socket(socket.AF_INET), 
                                           server_hostname=host)
        self.socket.connect((host, port))
        
        # 發送請求
        request = HTTPRequest(method, path)
        request.add_header('Host', host)
        
        if headers:
            for key, value in headers.items():
                request.add_header(key, value)
        
        if body:
            request.body = body
        
        self.socket.send(request.to_bytes())
        
        # 接收回應
        response_data = b''
        while True:
            chunk = self.socket.recv(4096)
            if not chunk:
                break
            response_data += chunk
        
        self.socket.close()
        
        return response_data.decode()

# 測試
client = HTTPClient()
# response = client.request('GET', 'http://example.com/')
# print(response[:500])

# HTTP/2 特性
print("""
=== HTTP/1.1 vs HTTP/2 vs HTTP/3 ===

HTTP/1.1:
- 持續連線 (Keep-Alive)
- 管線化 (Pipelining)
- 區塊傳輸編碼
- 主機標頭 (Virtual Hosting)

HTTP/2:
- 二進制框架
- 多工 (Multiplexing)
- 標頭壓縮 (HPACK)
- 伺服器推送
- 優先權

HTTP/3:
- QUIC 協定
- 0-RTT 連線
- 連線遷移
- 無頭阻塞
""")
```

## 12.2 Web Server 架構

[程式檔案：12-2-web-server.py](../_code/12/12-2-web-server.py)
```python
"""
Web Server 實作
"""

import socket
import threading
from datetime import datetime
import os

class WebServer:
    """簡單的 Web 伺服器"""
    
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False
        self.routes = {}
    
    def start(self):
        """啟動伺服器"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        
        print(f"Web 伺服器啟動於 http://{self.host}:{self.port}")
        
        while self.running:
            try:
                self.server_socket.settimeout(1.0)
                client_socket, addr = self.server_socket.accept()
                print(f"連線來自: {addr}")
                
                # 處理請求
                thread = threading.Thread(target=self.handle_request, 
                                         args=(client_socket,))
                thread.start()
            except socket.timeout:
                continue
            except KeyboardInterrupt:
                break
    
    def handle_request(self, client_socket):
        """處理 HTTP 請求"""
        try:
            request_data = b''
            while True:
                chunk = client_socket.recv(4096)
                if not chunk:
                    break
                request_data += chunk
                if b'\r\n\r\n' in request_data:
                    break
            
            request_text = request_data.decode('utf-8', errors='ignore')
            lines = request_text.split('\r\n')
            
            if not lines:
                return
            
            # 解析請求行
            request_line = lines[0].split()
            if len(request_line) < 2:
                return
            
            method = request_line[0]
            path = request_line[1]
            
            # 路由處理
            response = self.route_handler(method, path, request_data)
            
            # 發送回應
            client_socket.send(response)
            
        except Exception as e:
            print(f"處理錯誤: {e}")
        finally:
            client_socket.close()
    
    def route_handler(self, method, path, request_data):
        """路由處理"""
        # 檢查自訂路由
        if path in self.routes:
            handler = self.routes[path]
            return handler(method, request_data)
        
        # 靜態檔案服務
        if path == '/':
            path = '/index.html'
        
        file_path = 'public' + path
        
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return self.serve_file(file_path)
        
        # 404
        return self.not_found()
    
    def serve_file(self, file_path):
        """提供檔案"""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # 根據副檔名判斷 content-type
            ext = os.path.splitext(file_path)[1]
            content_type = {
                '.html': 'text/html',
                '.css': 'text/css',
                '.js': 'application/javascript',
                '.json': 'application/json',
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.gif': 'image/gif',
            }.get(ext, 'text/plain')
            
            response = HTTPResponse(200, content.decode('utf-8', errors='ignore'), content_type)
            response.add_header('Server', 'SimpleWebServer/1.0')
            
            return response.to_bytes()
        
        except Exception as e:
            return self.error_response(500, str(e))
    
    def add_route(self, path, handler):
        """新增路由"""
        self.routes[path] = handler
    
    def not_found(self):
        """404 回應"""
        return HTTPResponse(404, '<h1>404 Not Found</h1>').to_bytes()
    
    def error_response(self, code, message):
        """錯誤回應"""
        return HTTPResponse(code, f'<h1>{code} Error</h1><p>{message}</p>').to_bytes()

# Nginx 比較
print("""
=== 簡單 Server vs Nginx ===

簡單 Server:
- 單執行緒/程序
- 同步阻塞
- 適合開發測試
- 效能有限

Nginx:
- 事件驅動架構
- 非阻塞 I/O
- 反向代理
- 負載平衡
- 快取靜態檔案

Nginx 設定範例:
server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://backend;
    }
    
    location /static/ {
        root /var/www;
        expires 30d;
    }
}
""")
```

## 12.3 負載平衡與反向代理

[程式檔案：12-3-load-balancer.py](../_code/12/12-3-load-balancer.py)
```python
"""
負載平衡器
"""

import random

class LoadBalancer:
    """負載平衡器"""
    
    def __init__(self, algorithm='round_robin'):
        self.servers = []
        self.algorithm = algorithm
        self.current_index = 0
        self.server_weights = {}
    
    def add_server(self, server, weight=1):
        """新增伺服器"""
        self.servers.append(server)
        self.server_weights[server] = weight
    
    def get_server(self):
        """取得伺服器"""
        if not self.servers:
            return None
        
        if self.algorithm == 'round_robin':
            server = self.servers[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.servers)
            return server
        
        elif self.algorithm == 'random':
            return random.choice(self.servers)
        
        elif self.algorithm == 'least_connections':
            return min(self.servers, key=lambda s: self.get_connection_count(s))
        
        elif self.algorithm == 'weighted':
            return self.weighted_choice()
        
        return self.servers[0]
    
    def weighted_choice(self):
        """加權選擇"""
        total = sum(self.server_weights.values())
        r = random.uniform(0, total)
        cumsum = 0
        for server in self.servers:
            cumsum += self.server_weights[server]
            if r <= cumsum:
                return server
        return self.servers[0]
    
    def get_connection_count(self, server):
        """取得連線數（模擬）"""
        return random.randint(1, 100)

# 健康檢查
class HealthCheck:
    """健康檢查"""
    
    def __init__(self, interval=5):
        self.interval = interval
        self.servers = {}
    
    def add_server(self, server):
        """新增伺服器"""
        self.servers[server] = {'healthy': True, 'failures': 0}
    
    def check(self, server):
        """檢查伺服器健康"""
        # 模擬健康檢查
        import random
        healthy = random.random() > 0.1  # 90% 機率健康
        
        if server in self.servers:
            if healthy:
                self.servers[server]['failures'] = 0
                self.servers[server]['healthy'] = True
            else:
                self.servers[server]['failures'] += 1
                if self.servers[server]['failures'] >= 3:
                    self.servers[server]['healthy'] = False
        
        return self.servers.get(server, {}).get('healthy', False)

# 反向代理
class ReverseProxy:
    """反向代理"""
    
    def __init__(self):
        self.load_balancer = LoadBalancer()
        self.health_check = HealthCheck()
    
    def forward(self, request):
        """轉發請求"""
        # 健康檢查
        server = self.load_balancer.get_server()
        
        if not self.health_check.check(server):
            # 嘗試下一個伺服器
            for _ in range(len(self.load_balancer.servers)):
                server = self.load_balancer.get_server()
                if self.health_check.check(server):
                    break
        
        print(f"轉發到: {server}")
        return server

# 測試
lb = LoadBalancer(algorithm='round_robin')
lb.add_server('server1:8000', weight=3)
lb.add_server('server2:8000', weight=2)
lb.add_server('server3:8000', weight=1)

for _ in range(6):
    print(f"選擇: {lb.get_server()}")

print("\n=== 負載平衡演算法 ===")
print("1. Round Robin - 輪詢")
print("2. Least Connections - 最少連線")
print("3. IP Hash - 來源 IP 雜湊")
print("4. Weighted - 加權")
print("5. Random - 隨機")
```

## 12.4 CDN 與快取策略

[程式檔案：12-4-cdn-cache.py](../_code/12/12-4-cdn-cache.py)
```python
"""
CDN 與快取
"""

import time

class Cache:
    """快取"""
    
    def __init__(self, max_size=100, ttl=3600):
        self.max_size = max_size
        self.ttl = ttl  # Time To Live（秒）
        self.cache = {}
    
    def get(self, key):
        """取得"""
        if key in self.cache:
            entry = self.cache[key]
            
            # 檢查過期
            if time.time() - entry['time'] > self.ttl:
                del self.cache[key]
                return None
            
            return entry['value']
        
        return None
    
    def set(self, key, value):
        """設定"""
        # 清理過期項目
        self.cleanup()
        
        # 檢查大小
        if len(self.cache) >= self.max_size:
            # LRU 淘汰
            oldest = min(self.cache.keys(), 
                       key=lambda k: self.cache[k]['time'])
            del self.cache[oldest]
        
        self.cache[key] = {'value': value, 'time': time.time()}
    
    def cleanup(self):
        """清理過期"""
        now = time.time()
        expired = [k for k, v in self.cache.items() 
                   if now - v['time'] > self.ttl]
        for k in expired:
            del self.cache[k]

# HTTP 快取控制
class HTTPCache:
    """HTTP 快取控制"""
    
    @staticmethod
    def cache_control(max_age, public=True):
        """Cache-Control 頭"""
        directive = f"max-age={max_age}"
        if public:
            directive = "public, " + directive
        else:
            directive = "private, " + directive
        return directive
    
    @staticmethod
    def etag(content):
        """ETag 生成"""
        import hashlib
        return hashlib.md5(content.encode()).hexdigest()

# CDN 模擬
class CDN:
    """CDN 模擬"""
    
    def __init__(self):
        self.edge_servers = {}
        self.origin_server = 'origin.example.com'
        self.cache = Cache()
    
    def register_edge(self, location, address):
        """註冊邊緣伺服器"""
        self.edge_servers[location] = {
            'address': address,
            'cache': Cache(max_size=1000, ttl=3600)
        }
    
    def get_closest_edge(self, client_ip):
        """取得最近的邊緣伺服器"""
        # 簡單模擬：隨機選擇
        locations = list(self.edge_servers.keys())
        return random.choice(locations)
    
    def request(self, client_ip, path):
        """CDN 請求"""
        # 取得最近的邊緣伺服器
        edge = self.get_closest_edge(client_ip)
        edge_cache = self.edge_servers[edge]['cache']
        
        # 檢查快取
        content = edge_cache.get(path)
        if content:
            print(f"快取命中: {edge}")
            return content
        
        # 回源獲取
        print(f"回源: {self.origin_server}")
        content = f"Content from {self.origin_server}"
        
        # 快取
        edge_cache.set(path, content)
        
        return content

# 測試
cache = Cache(ttl=1)
cache.set('key1', 'value1')
print(cache.get('key1'))  # 命中
time.sleep(1.1)
print(cache.get('key1'))  # 過期

print("\n=== HTTP 快取 ===")
print("""
Cache-Control:
- max-age=3600: 快取有效期
- no-cache: 每次驗證
- no-store: 不快取
- private: 僅瀏覽器快取
- public: 共享快取

ETag: 內容雜湊
Last-Modified: 修改時間
Vary: 根據 header 區分
""")
```

## 12.5 網頁應用程式開發

[程式檔案：12-5-web-framework.py](../_code/12/12-5-web-framework.py)
```python
"""
Web 框架比較
"""

# Flask 風格的框架
class Flask:
    """簡化的 Flask 框架"""
    
    def __init__(self):
        self.routes = {}
        self.before_requests = []
        self.after_requests = []
    
    def route(self, path):
        """裝飾器"""
        def decorator(func):
            self.routes[path] = func
            return func
        return decorator
    
    def before_request(self, func):
        """請求前"""
        self.before_requests.append(func)
    
    def after_request(self, func):
        """請求後"""
        self.after_requests.append(func)
    
    def run(self, host='0.0.0.0', port=5000):
        """執行"""
        from http.server import HTTPServer, BaseHTTPRequestHandler
        
        app = self
        
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.handle_request('GET')
            
            def do_POST(self):
                self.handle_request('POST')
            
            def handle_request(self, method):
                # 執行 before_request
                for func in app.before_requests:
                    func()
                
                # 路由
                handler = app.routes.get(self.path)
                if handler:
                    response = handler()
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html')
                    self.end_headers()
                    self.wfile.write(response.encode())
                else:
                    self.send_response(404)
                    self.wfile.write(b'Not Found')
                
                # 執行 after_request
                for func in app.after_requests:
                    func()
        
        server = HTTPServer((host, port), Handler)
        print(f"Flask 風格伺服器 on port {port}")
        server.serve_forever()

# 使用範例
app = Flask()

@app.route('/')
def index():
    return '<h1>Hello, World!</h1>'

@app.route('/api/user')
def get_user():
    import json
    return json.dumps({'name': 'John', 'age': 30})

@app.route('/hello/<name>')
def hello(name):
    return f'<h1>Hello, {name}!</h1>'

# 前端框架比較
print("""
=== 前端框架 ===

React:
- 虛擬 DOM
- 元件化
- Hooks
- 生態豐富

Vue:
- 雙向綁定
- 單一檔案元件
- 較平緩的學習曲線

Angular:
- 完整框架
- TypeScript
- 依賴注入

Svelte:
- 編譯時框架
- 無虛擬 DOM
- 更小的 bundle
""")

# RESTful API
print("""
=== RESTful API ===

GET    /users        - 取得所有使用者
GET    /users/1      - 取得 ID=1 的使用者
POST   /users        - 新增使用者
PUT    /users/1      - 更新使用者
DELETE /users/1      - 刪除使用者

回應格式:
{
    "status": "success",
    "data": {...},
    "message": "..."
}
""")
```

## 程式碼範例

請參考：[sp/_code/12-1-http-client.py](sp/_code/12-1-http-client.py) - HTTP 用戶端實作