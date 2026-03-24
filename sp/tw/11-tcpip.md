# 11. TCP/IP 網路堆疊

## 11.1 OSI 與 TCP/IP 模型

[程式檔案：11-1-osi-tcpip.py](../_code/11/11-1-osi-tcpip.py)
```python
"""
OSI 與 TCP/IP 模型
"""

# OSI 7 層模型
print("""
=== OSI 7 層模型 ===

7. 應用層 (Application)     - HTTP, DNS, FTP
6. 表達層 (Presentation)    - JPEG, GIF, SSL/TLS
5. 會議層 (Session)        - RPC, NetBIOS
4. 傳輸層 (Transport)      - TCP, UDP
3. 網路層 (Network)        - IP, ICMP, ARP
2. 資料連結層 (Data Link)  - Ethernet, Wi-Fi
1. 實體層 (Physical)       - 電纜、光纖

=== TCP/IP 4 層模型 ===

4. 應用層   - HTTP, FTP, SMTP, DNS
3. 傳輸層   - TCP, UDP
2. 網路層   - IP, ICMP, ARP
1. 網路介面 - Ethernet, PPP
""")

# 封包封裝
class PacketEncapsulation:
    """封包封裝模擬"""
    
    def __init__(self):
        self.layers = []
    
    def add_data(self, data):
        """添加應用層資料"""
        self.layers.append(('Data', data))
    
    def add_transport(self, protocol):
        """添加傳輸層頭"""
        if protocol == 'TCP':
            header = {'src_port': 80, 'dst_port': 45678, 'seq': 100, 'ack': 0}
            self.layers.append(('TCP', header))
        elif protocol == 'UDP':
            header = {'src_port': 53, 'dst_port': 12345, 'length': 100}
            self.layers.append(('UDP', header))
    
    def add_network(self):
        """添加網路層頭"""
        header = {'src_ip': '192.168.1.100', 'dst_ip': '93.184.216.34', 'protocol': 6}
        self.layers.append(('IP', header))
    
    def add_link(self):
        """添加資料連結層"""
        header = {'src_mac': '00:1A:2B:3C:4D:5E', 'dst_mac': '11:22:33:44:55:66'}
        self.layers.append(('Ethernet', header))
    
    def get_packet(self):
        """取得完整封包"""
        return self.layers

# 測試封裝
packet = PacketEncapsulation()
packet.add_data("HTTP Request: GET / HTTP/1.1")
packet.add_transport('TCP')
packet.add_network()
packet.add_link()

print("=== 封包封裝 ===")
for layer, data in packet.get_packet():
    if isinstance(data, dict):
        print(f"{layer}: {data}")
    else:
        print(f"{layer}: {data}")
```

## 11.2 IP、TCP、UDP 協定

[程式檔案：11-2-ip-header.c](../_code/11/11-2-ip-header.c)
```c
// IP 封包結構

struct iphdr {
    unsigned char  ihl:4, version:4;
    unsigned char  tos;
    unsigned short tot_len;
    unsigned short id;
    unsigned short frag_off;
    unsigned char  ttl;
    unsigned char  protocol;
    unsigned short check;
    unsigned int   saddr;
    unsigned int   daddr;
    // options...
};

// TCP 標頭
struct tcphdr {
    unsigned short source;
    unsigned short dest;
    unsigned int   seq;
    unsigned int   ack;
    unsigned char  data_off:4, reserved:4;
    unsigned char  flags;
    unsigned short window;
    unsigned short check;
    unsigned short urgent;
};

// UDP 標頭
struct udphdr {
    unsigned short source;
    unsigned short dest;
    unsigned short len;
    unsigned short check;
};
```

```python
"""
TCP/UDP 協定模擬
"""

import random

# TCP 連線管理
class TCPConnection:
    """TCP 連線狀態機"""
    
    def __init__(self):
        self.state = 'CLOSED'
        self.seq = random.randint(0, 1000000)
        self.ack = 0
    
    def connect(self):
        """三次握手"""
        print("=== TCP 三次握手 ===")
        
        # SYN
        self.state = 'SYN_SENT'
        seq = self.seq
        print(f"客戶端 -> 伺服器: SYN, seq={seq}")
        
        # SYN-ACK
        self.state = 'SYN_RCVD'
        server_seq = random.randint(0, 1000000)
        print(f"伺服器 -> 客戶端: SYN, ACK, seq={server_seq}, ack={seq+1}")
        
        # ACK
        self.state = 'ESTABLISHED'
        print(f"客戶端 -> 伺服器: ACK, seq={seq+1}, ack={server_seq+1}")
        self.seq = seq + 1
        self.ack = server_seq + 1
    
    def close(self):
        """四次揮手"""
        print("\n=== TCP 四次揮手 ===")
        
        # FIN
        print(f"客戶端 -> 伺服器: FIN, seq={self.seq}")
        self.state = 'FIN_WAIT_1'
        
        # ACK
        print(f"伺服器 -> 客戶端: ACK, ack={self.seq+1}")
        self.state = 'FIN_WAIT_2'
        
        # FIN
        print(f"伺服器 -> 客戶端: FIN, seq={self.ack}")
        self.state = 'CLOSE_WAIT'
        
        # ACK
        print(f"客戶端 -> 伺服器: ACK, seq={self.seq+1}")
        self.state = 'TIME_WAIT'
        
        # 等待 2MSL 後關閉
        self.state = 'CLOSED'

# 滑動視窗
class SlidingWindow:
    """TCP 滑動視窗"""
    
    def __init__(self, size=4):
        self.size = size
        self.window = []
        self.base = 0
        self.next_seq = 0
    
    def send(self, data):
        """傳送資料"""
        if len(self.window) < self.size:
            seq = self.next_seq
            self.window.append({'seq': seq, 'data': data, 'acked': False})
            self.next_seq += 1
            print(f"傳送: seq={seq}, data={data}")
            return True
        else:
            print("視窗滿，等待 ACK")
            return False
    
    def ack(self, ack_num):
        """處理 ACK"""
        for pkt in self.window:
            if pkt['seq'] < ack_num:
                pkt['acked'] = True
        print(f"收到 ACK: {ack_num}")

# UDP vs TCP
print("""
=== UDP vs TCP ===

| 特性      | UDP              | TCP              |
|-----------|-----------------|------------------|
| 連線      | 無連線           | 有連線           |
| 可靠性    | 不可靠           | 可靠             |
| 順序      | 無序             | 有序             |
| 速度      | 快               | 較慢             |
| 額外開銷  | 小 (8 bytes)     | 大 (20 bytes)   |
| 應用      | DNS, VoIP       | HTTP, Email     |

UDP 簡單快速，適合即時應用或查詢/回應模式
TCP 可靠有序，適合需要資料完整性的應用
""")

# 測試 TCP
conn = TCPConnection()
conn.connect()
conn.close()
```

## 11.3 Socket 程式設計

[程式檔案：11-4-socket.py](../_code/11/11-4-socket.py)
```python
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
```

## 11.4 網路層級與路由

[程式檔案：11-5-routing.py](../_code/11/11-5-routing.py)
```python
"""
網路層級與路由
"""

import random

# IP 位址類別
class IPAddress:
    """IP 位址"""
    
    CLASSES = {
        'A': (range(1, 128), '255.0.0.0', '0.0.0.0'),
        'B': (range(128, 192), '255.255.0.0', '0.0.0.0'),
        'C': (range(192, 224), '255.255.255.0', '0.0.0.0'),
        'D': (range(224, 240), 'N/A', '多播'),
        'E': (range(240, 256), 'N/A', '實驗'),
    }
    
    @staticmethod
    def get_class(ip):
        """取得 IP 類別"""
        first_octet = int(ip.split('.')[0])
        for cls, (range_obj, mask, _) in IPAddress.CLASSES.items():
            if first_octet in range_obj:
                return cls, mask
        return 'Unknown', 'Unknown'
    
    @staticmethod
    def is_private(ip):
        """檢查是否為私有 IP"""
        first = int(ip.split('.')[0])
        if first == 10:
            return True
        if first == 172 and 16 <= int(ip.split('.')[1]) <= 31:
            return True
        if first == 192 and int(ip.split('.')[1]) == 168:
            return True
        return False

# 路由表
class RoutingTable:
    """路由表"""
    
    def __init__(self):
        self.routes = []
    
    def add_route(self, destination, netmask, gateway, interface):
        """新增路由"""
        self.routes.append({
            'dest': destination,
            'mask': netmask,
            'gateway': gateway,
            'interface': interface
        })
    
    def lookup(self, dest_ip):
        """查詢路由"""
        best_route = None
        longest_match = -1
        
        for route in self.routes:
            if self.match(dest_ip, route['dest'], route['mask']):
                mask_bits = self.netmask_to_bits(route['mask'])
                if mask_bits > longest_match:
                    longest_match = mask_bits
                    best_route = route
        
        return best_route
    
    @staticmethod
    def match(ip, network, mask):
        """匹配 IP 和網路"""
        ip_parts = list(map(int, ip.split('.')))
        net_parts = list(map(int, network.split('.')))
        mask_parts = list(map(int, mask.split('.')))
        
        for i in range(4):
            if (ip_parts[i] & mask_parts[i]) != (net_parts[i] & mask_parts[i]):
                return False
        return True
    
    @staticmethod
    def netmask_to_bits(mask):
        """網路遮罩轉位元"""
        parts = list(map(int, mask.split('.')))
        return sum(bin(p).count('1') for p in parts)

# 測試
print("=== IP 位址 ===")
ip = "192.168.1.100"
cls, mask = IPAddress.get_class(ip)
print(f"{ip} 是 Class {cls}, 網路遮罩: {mask}")
print(f"私有 IP: {IPAddress.is_private(ip)}")

rt = RoutingTable()
rt.add_route('0.0.0.0', '0.0.0.0', '192.168.1.1', 'eth0')
rt.add_route('192.168.1.0', '255.255.255.0', '0.0.0.0', 'eth0')
rt.add_route('10.0.0.0', '255.0.0.0', '0.0.0.0', 'eth1')

route = rt.lookup('192.168.1.50')
print(f"路由: {route}")
```

## 11.5 網路效能優化

[程式檔案：11-6-optimization.py](../_code/11/11-6-optimization.py)
```python
"""
網路效能優化
"""

# TCP 最佳化
class TCPOptimization:
    """TCP 最佳化技術"""
    
    @staticmethod
    def nagle_algorithm():
        """Nagle 演算法 - 減少小封包"""
        print("""
=== Nagle 演算法 ===

目的: 減少小封包數量
原理: 等待 ACK 後才發送下一個
缺點: 增加延遲

禁用: setsockopt(sock, IPPROTO_TCP, TCP_NODELAY, 1)
""")
    
    @staticmethod
    def congestion_control():
        """擁塞控制"""
        print("""
=== TCP 擁塞控制 ===

1. 慢啟動 (Slow Start)
   - 指數增加 CWND

2. 擁塞避免 (Congestion Avoidance)
   - 線性增加 CWND

3. 快速重傳 (Fast Retransmit)
   - 3 個Duplicate ACK後重傳

4. 快速恢復 (Fast Recovery)
   - 維持 CWND
""")
    
    @staticmethod
    def keepalive():
        """Keep-alive"""
        print("""
=== Keep-Alive ===

作用: 檢測連線是否存活
預設: 2小時 idle 後開始
間隔: 75秒 探測一次
重試: 9 次後認為斷線
""")

# 效能調校
def network_tuning():
    """網路效能調校"""
    print("""
=== Linux 網路調校 ===

# 增加 buffer
sysctl -w net.core.rmem_max=16777216
sysctl -w net.core.wmem_max=16777216

# TCP 視窗
sysctl -w net.ipv4.tcp_window_scaling=1
sysctl -w net.ipv4.tcp_rmem="4096 87380 6291456"
sysctl -w net.ipv4.tcp_wmem="4096 16384 6291456"

# 禁用 SYN cookie（高負載時）
sysctl -w net.ipv4.tcp_syncookies=0

# 增加連線數
sysctl -w net.core.somaxconn=65535
""")

# 測量工具
print("=== 網路測量工具 ===")
print("""
ping        - 測量延遲
traceroute - 追蹤路由
netstat    - 連線統計
ss         - Socket 統計
iperf3     - 頻寬測試
tcpdump    - 封包擷取
""")
```