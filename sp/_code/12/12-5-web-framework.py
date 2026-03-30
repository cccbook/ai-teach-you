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
