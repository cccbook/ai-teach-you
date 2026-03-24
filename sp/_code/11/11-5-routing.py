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
