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
