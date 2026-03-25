"""
Python Socket 程式設計
"""

import socket

# TCP 伺服器
def tcp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', 8080))
    sock.listen(5)
    
    print("TCP 伺服器 listening on port 8080")
    
    while True:
        client, addr = sock.accept()
        print(f"連線來自: {addr}")
        
        data = client.recv(1024)
        print(f"收到: {data}")
        
        client.send(b"HTTP/1.1 200 OK\r\n\r\nHello!")
        client.close()

# TCP 用戶端
def tcp_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 8080))
    
    sock.send(b"GET / HTTP/1.0\r\n\r\n")
    response = sock.recv(1024)
    print(f"回應: {response}")
    
    sock.close()

# UDP 伺服器
def udp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 8081))
    
    print("UDP 伺服器 listening on port 8081")
    
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"收到: {data} 從 {addr}")
        
        sock.sendto(b"ACK", addr)

# UDP 用戶端
def udp_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(b"Hello", ('127.0.0.1', 8081))
    sock.close()

# 執行
print("嘗試連線...")
# 注意：需要先啟動伺服器才能連線
# tcp_server() 或 udp_server() 需先執行

# Socket 選項
print("""
=== Socket 選項 ===

SOL_SOCKET 層:
- SO_REUSEADDR: 重複使用位址
- SO_KEEPALIVE: 保持連線
- SO_SNDBUF: 傳送緩衝區大小
- SO_RCVBUF: 接收緩衝區大小

IPPROTO_TCP 層:
- TCP_NODELAY: 禁用 Nagle 演算法
- TCP_QUICKACK: 快速 ACK
""")
