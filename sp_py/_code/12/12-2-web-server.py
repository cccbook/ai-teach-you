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
