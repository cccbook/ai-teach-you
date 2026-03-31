"""
CDN 與快取
"""

import time
import random

class Cache:
    """快取"""
    
    def __init__(self, max_size=100, ttl=3600):
        self.max_size = max_size
        self.ttl = ttl  # Time To Live（秒）
        self.cache = {}
    
    def get(self, key):
        """取得"""
        if key in self.cache:
            entry = self.cache[key]
            
            # 檢查過期
            if time.time() - entry['time'] > self.ttl:
                del self.cache[key]
                return None
            
            return entry['value']
        
        return None
    
    def set(self, key, value):
        """設定"""
        # 清理過期項目
        self.cleanup()
        
        # 檢查大小
        if len(self.cache) >= self.max_size:
            # LRU 淘汰
            oldest = min(self.cache.keys(), 
                       key=lambda k: self.cache[k]['time'])
            del self.cache[oldest]
        
        self.cache[key] = {'value': value, 'time': time.time()}
    
    def cleanup(self):
        """清理過期"""
        now = time.time()
        expired = [k for k, v in self.cache.items() 
                   if now - v['time'] > self.ttl]
        for k in expired:
            del self.cache[k]

# HTTP 快取控制
class HTTPCache:
    """HTTP 快取控制"""
    
    @staticmethod
    def cache_control(max_age, public=True):
        """Cache-Control 頭"""
        directive = f"max-age={max_age}"
        if public:
            directive = "public, " + directive
        else:
            directive = "private, " + directive
        return directive
    
    @staticmethod
    def etag(content):
        """ETag 生成"""
        import hashlib
        return hashlib.md5(content.encode()).hexdigest()

# CDN 模擬
class CDN:
    """CDN 模擬"""
    
    def __init__(self):
        self.edge_servers = {}
        self.origin_server = 'origin.example.com'
        self.cache = Cache()
    
    def register_edge(self, location, address):
        """註冊邊緣伺服器"""
        self.edge_servers[location] = {
            'address': address,
            'cache': Cache(max_size=1000, ttl=3600)
        }
    
    def get_closest_edge(self, client_ip):
        """取得最近的邊緣伺服器"""
        # 簡單模擬：隨機選擇
        locations = list(self.edge_servers.keys())
        return random.choice(locations)
    
    def request(self, client_ip, path):
        """CDN 請求"""
        # 取得最近的邊緣伺服器
        edge = self.get_closest_edge(client_ip)
        edge_cache = self.edge_servers[edge]['cache']
        
        # 檢查快取
        content = edge_cache.get(path)
        if content:
            print(f"快取命中: {edge}")
            return content
        
        # 回源獲取
        print(f"回源: {self.origin_server}")
        content = f"Content from {self.origin_server}"
        
        # 快取
        edge_cache.set(path, content)
        
        return content

# 測試
cache = Cache(ttl=1)
cache.set('key1', 'value1')
print(cache.get('key1'))  # 命中
time.sleep(1.1)
print(cache.get('key1'))  # 過期

print("\n=== HTTP 快取 ===")
print("""
Cache-Control:
- max-age=3600: 快取有效期
- no-cache: 每次驗證
- no-store: 不快取
- private: 僅瀏覽器快取
- public: 共享快取

ETag: 內容雜湊
Last-Modified: 修改時間
Vary: 根據 header 區分
""")
