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
