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
