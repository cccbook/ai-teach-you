"""
雲端儲存與分散式系統
"""

import hashlib

# 分散式儲存
class DistributedStorage:
    """分散式儲存"""
    
    def __init__(self, num_nodes=3):
        self.nodes = [f"node-{i}" for i in range(num_nodes)]
        self.data = {}  # key -> [(node, data)]
        self.replication_factor = 2
    
    def put(self, key, value):
        """儲存資料"""
        # 簡單的資料分散：雜湊
        node_index = int(hashlib.md5(key.encode()).hexdigest(), 16) % len(self.nodes)
        
        nodes_to_store = []
        for i in range(self.replication_factor):
            idx = (node_index + i) % len(self.nodes)
            nodes_to_store.append(self.nodes[idx])
        
        self.data[key] = nodes_to_store
        print(f"儲存 '{key}' 到 {nodes_to_store}")
    
    def get(self, key):
        """取得資料"""
        if key in self.data:
            nodes = self.data[key]
            print(f"從 {nodes[0]} 讀取 '{key}'")
            return True
        return False
    
    def delete(self, key):
        """刪除資料"""
        if key in self.data:
            del self.data[key]
            print(f"刪除 '{key}'")

# CAP 定理
print("""
=== CAP 定理 ===

分散式系統最多只能滿足三個特性中的兩個：

C (Consistency) - 一致性
- 所有節點看到相同的資料

A (Availability) - 可用性
- 每個請求都會收到回應

P (Partition Tolerance) - 分區容錯
- 系統在網路分割時仍能運作

實際選擇:
- CP: 犧牲可用性 (如: ZooKeeper, etcd)
- AP: 犧牲一致性 (如: Cassandra, DynamoDB)
- CA: 不可能在分散式系統中實現
""")

# 一致性模型
print("""
=== 一致性模型 ===

1. 強一致性
   - 所有讀取都看到最新的寫入
   - 例: 傳統資料庫

2. 最終一致性
   - 最終會達到一致
   - 例: DynamoDB, Cassandra

3. 讀寫一致性
   - 讀取能看到自己寫入的結果
   - 例: Amazon S3

4. 因果一致性
   - 有因果關係的操作順序一致
   - 例: Cassandra (某些場景)
""")

# 分散式共識
print("""
=== 分散式共識 ===

Raft 共識演算法:
- Leader 選舉
- 日誌複製
- 安全性

Paxos:
- 提議-接受協議
- 更理論化

應用:
- 分散式鎖
- 服務發現
- 設定管理
""")

# 測試
storage = DistributedStorage(num_nodes=4)
storage.put("user:1", "John")
storage.put("user:2", "Jane")
storage.get("user:1")
storage.get("user:2")
storage.delete("user:1")