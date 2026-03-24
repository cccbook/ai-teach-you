"""
負載平衡器
"""

import random

class LoadBalancer:
    """負載平衡器"""
    
    def __init__(self, algorithm='round_robin'):
        self.servers = []
        self.algorithm = algorithm
        self.current_index = 0
        self.server_weights = {}
    
    def add_server(self, server, weight=1):
        """新增伺服器"""
        self.servers.append(server)
        self.server_weights[server] = weight
    
    def get_server(self):
        """取得伺服器"""
        if not self.servers:
            return None
        
        if self.algorithm == 'round_robin':
            server = self.servers[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.servers)
            return server
        
        elif self.algorithm == 'random':
            return random.choice(self.servers)
        
        elif self.algorithm == 'least_connections':
            return min(self.servers, key=lambda s: self.get_connection_count(s))
        
        elif self.algorithm == 'weighted':
            return self.weighted_choice()
        
        return self.servers[0]
    
    def weighted_choice(self):
        """加權選擇"""
        total = sum(self.server_weights.values())
        r = random.uniform(0, total)
        cumsum = 0
        for server in self.servers:
            cumsum += self.server_weights[server]
            if r <= cumsum:
                return server
        return self.servers[0]
    
    def get_connection_count(self, server):
        """取得連線數（模擬）"""
        return random.randint(1, 100)

# 健康檢查
class HealthCheck:
    """健康檢查"""
    
    def __init__(self, interval=5):
        self.interval = interval
        self.servers = {}
    
    def add_server(self, server):
        """新增伺服器"""
        self.servers[server] = {'healthy': True, 'failures': 0}
    
    def check(self, server):
        """檢查伺服器健康"""
        # 模擬健康檢查
        import random
        healthy = random.random() > 0.1  # 90% 機率健康
        
        if server in self.servers:
            if healthy:
                self.servers[server]['failures'] = 0
                self.servers[server]['healthy'] = True
            else:
                self.servers[server]['failures'] += 1
                if self.servers[server]['failures'] >= 3:
                    self.servers[server]['healthy'] = False
        
        return self.servers.get(server, {}).get('healthy', False)

# 反向代理
class ReverseProxy:
    """反向代理"""
    
    def __init__(self):
        self.load_balancer = LoadBalancer()
        self.health_check = HealthCheck()
    
    def forward(self, request):
        """轉發請求"""
        # 健康檢查
        server = self.load_balancer.get_server()
        
        if not self.health_check.check(server):
            # 嘗試下一個伺服器
            for _ in range(len(self.load_balancer.servers)):
                server = self.load_balancer.get_server()
                if self.health_check.check(server):
                    break
        
        print(f"轉發到: {server}")
        return server

# 測試
lb = LoadBalancer(algorithm='round_robin')
lb.add_server('server1:8000', weight=3)
lb.add_server('server2:8000', weight=2)
lb.add_server('server3:8000', weight=1)

for _ in range(6):
    print(f"選擇: {lb.get_server()}")

print("\n=== 負載平衡演算法 ===")
print("1. Round Robin - 輪詢")
print("2. Least Connections - 最少連線")
print("3. IP Hash - 來源 IP 雜湊")
print("4. Weighted - 加權")
print("5. Random - 隨機")
