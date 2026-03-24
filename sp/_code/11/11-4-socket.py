"""
Socket 程式設計深入
"""

import socket

# 完整的 TCP 伺服器
class TCPServer:
    """TCP 伺服器"""
    
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
        self.server_socket = None
    
    def start(self):
        """啟動伺服器"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"伺服器 listening on {self.host}:{self.port}")
    
    def handle_client(self, client_socket):
        """處理客戶端"""
        request = client_socket.recv(1024)
        print(f"收到: {request.decode()}")
        
        response = "HTTP/1.1 200 OK\r\nContent-Length: 13\r\n\r\nHello, World!"
        client_socket.send(response.encode())
        client_socket.close()
    
    def run(self):
        """執行伺服器"""
        self.start()
        while True:
            client, addr = self.server_socket.accept()
            print(f"連線來自: {addr}")
            self.handle_client(client)

# TCP 客戶端
class TCPClient:
    """TCP 客戶端"""
    
    def __init__(self, host='127.0.0.1', port=8080):
        self.host = host
        self.port = port
        self.socket = None
    
    def connect(self):
        """連線"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        print(f"連線到 {self.host}:{self.port}")
    
    def send(self, message):
        """傳送訊息"""
        self.socket.send(message.encode())
    
    def receive(self):
        """接收訊息"""
        return self.socket.recv(1024)
    
    def close(self):
        """關閉"""
        self.socket.close()

# Socket 選項
print("""
=== Socket 選項 ===

伺服器:
- SO_REUSEADDR: 允許重複使用位址（重啟伺服器）
- SO_KEEPALIVE: 檢測連線是否存活
- TCP_NODELAY: 禁用 Nagle，減少延遲
- SO_BACKLOG: 排隊的最大連線數

客戶端:
- SO_TIMEOUT: 逾時時間
- TCP_NODELAY: 禁用延遲
""")

# 執行流程示意
print("=== TCP Socket 流程 ===")
print("""
伺服器:
socket() -> bind() -> listen() -> accept() -> read()/write() -> close()

客戶端:
socket() -> connect() -> write()/read() -> close()
""")

# TCP 狀態圖
print("=== TCP 狀態圖 ===")
print("""
CLOSED -> SYN_SENT -> ESTABLISHED -> FIN_WAIT -> CLOSED
         <- SYN_RCVD <-             <- CLOSE_WAIT <-

伺服器:
CLOSED -> LISTEN -> SYN_RCVD -> ESTABLISHED -> CLOSE_WAIT -> CLOSED
""")
