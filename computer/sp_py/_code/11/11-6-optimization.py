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
