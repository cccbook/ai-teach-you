"""
雜湊表實作 (Hash Table Implementation)
=====================================
展示雜湊表（Hash Table）的各種實作方式。
雜湊表是一種使用雜湊函數將鍵映射到值的資料結構，提供平均 O(1) 的查詢效率。
"""

from typing import Any, Dict, List, Optional, Tuple, Callable
from collections import defaultdict
import time


class HashFunction:
    """雜湊函數"""
    
    @staticmethod
    def default_hash(key: Any) -> int:
        """預設雜湊函數"""
        if isinstance(key, str):
            hash_val = 0
            for i, char in enumerate(key):
                hash_val = (hash_val * 31 + ord(char)) & 0xFFFFFFFF
            return hash_val
        elif isinstance(key, int):
            return key & 0xFFFFFFFF
        else:
            return hash(str(key)) & 0xFFFFFFFF
    
    @staticmethod
    def djb2_hash(key: str) -> int:
        """DJB2 雜湊函數"""
        hash_val = 5381
        for char in key:
            hash_val = ((hash_val << 5) + hash_val) + ord(char)
        return hash_val & 0xFFFFFFFF
    
    @staticmethod
    def polynomial_rolling_hash(key: str, base: int = 31) -> int:
        """多項式滾動雜湊函數"""
        hash_val = 0
        for char in key:
            hash_val = (hash_val * base + ord(char)) & 0xFFFFFFFF
        return hash_val


class HashNode:
    """雜湊表節點"""
    
    def __init__(self, key: Any, value: Any):
        self.key = key
        self.value = value
        self.next: Optional['HashNode'] = None


class HashTableChaining:
    """使用鏈結法實現的雜湊表"""
    
    def __init__(self, capacity: int = 16, load_factor_threshold: float = 0.75):
        self.capacity = capacity
        self.size = 0
        self.load_factor_threshold = load_factor_threshold
        self.buckets: List[Optional[HashNode]] = [None] * capacity
    
    def _hash(self, key: Any) -> int:
        """計算雜湊值"""
        return HashFunction.default_hash(key) % self.capacity
    
    def _resize(self) -> None:
        """擴容"""
        new_capacity = self.capacity * 2
        new_buckets = [None] * new_capacity
        
        for bucket in self.buckets:
            current = bucket
            while current:
                new_index = HashFunction.default_hash(current.key) % new_capacity
                if new_buckets[new_index] is None:
                    new_buckets[new_index] = HashNode(current.key, current.value)
                else:
                    node = new_buckets[new_index]
                    while node.next:
                        node = node.next
                    node.next = HashNode(current.key, current.value)
                current = current.next
        
        self.buckets = new_buckets
        self.capacity = new_capacity
    
    def put(self, key: Any, value: Any) -> None:
        """插入或更新鍵值對"""
        if self.size / self.capacity >= self.load_factor_threshold:
            self._resize()
        
        index = self._hash(key)
        current = self.buckets[index]
        
        while current:
            if current.key == key:
                current.value = value
                return
            current = current.next
        
        new_node = HashNode(key, value)
        new_node.next = self.buckets[index]
        self.buckets[index] = new_node
        self.size += 1
    
    def get(self, key: Any, default: Any = None) -> Any:
        """取得值"""
        index = self._hash(key)
        current = self.buckets[index]
        
        while current:
            if current.key == key:
                return current.value
            current = current.next
        
        return default
    
    def remove(self, key: Any) -> bool:
        """移除鍵值對"""
        index = self._hash(key)
        current = self.buckets[index]
        previous = None
        
        while current:
            if current.key == key:
                if previous:
                    previous.next = current.next
                else:
                    self.buckets[index] = current.next
                self.size -= 1
                return True
            previous = current
            current = current.next
        
        return False
    
    def contains(self, key: Any) -> bool:
        """檢查鍵是否存在"""
        return self.get(key) is not None
    
    def keys(self) -> List[Any]:
        """取得所有鍵"""
        result = []
        for bucket in self.buckets:
            current = bucket
            while current:
                result.append(current.key)
                current = current.next
        return result
    
    def values(self) -> List[Any]:
        """取得所有值"""
        result = []
        for bucket in self.buckets:
            current = bucket
            while current:
                result.append(current.value)
                current = current.next
        return result
    
    def items(self) -> List[Tuple[Any, Any]]:
        """取得所有鍵值對"""
        result = []
        for bucket in self.buckets:
            current = bucket
            while current:
                result.append((current.key, current.value))
                current = current.next
        return result


class HashTableOpenAddressing:
    """使用開放定址法實現的雜湊表"""
    
    class _Entry:
        def __init__(self, key: Any = None, value: Any = None):
            self.key = key
            self.value = value
            self.is_empty = True
            self.is_deleted = False
    
    def __init__(self, capacity: int = 16):
        self.capacity = capacity
        self.size = 0
        self.table: List['_Entry'] = [self._Entry() for _ in range(capacity)]
    
    def _hash(self, key: Any, attempt: int = 0) -> int:
        """計算雜湊值（線性探測）"""
        base = HashFunction.default_hash(key)
        return (base + attempt) % self.capacity
    
    def _quadratic_hash(self, key: Any, attempt: int) -> int:
        """二次探測"""
        base = HashFunction.default_hash(key)
        return (base + attempt * attempt) % self.capacity
    
    def _double_hash(self, key: Any, attempt: int) -> int:
        """雙重雜湊"""
        base = HashFunction.default_hash(key)
        step = 1 + (base % (self.capacity - 1))
        return (base + attempt * step) % self.capacity
    
    def put(self, key: Any, value: Any) -> None:
        """插入或更新鍵值對"""
        if self.size >= self.capacity * 0.8:
            self._resize()
        
        for attempt in range(self.capacity):
            index = self._double_hash(key, attempt)
            entry = self.table[index]
            
            if entry.is_empty or entry.is_deleted:
                entry.key = key
                entry.value = value
                entry.is_empty = False
                entry.is_deleted = False
                self.size += 1
                return
            elif entry.key == key:
                entry.value = value
                return
        
        raise RuntimeError("雜湊表已滿")
    
    def get(self, key: Any, default: Any = None) -> Any:
        """取得值"""
        for attempt in range(self.capacity):
            index = self._double_hash(key, attempt)
            entry = self.table[index]
            
            if entry.is_empty:
                return default
            if not entry.is_deleted and entry.key == key:
                return entry.value
        
        return default
    
    def remove(self, key: Any) -> bool:
        """移除鍵值對"""
        for attempt in range(self.capacity):
            index = self._double_hash(key, attempt)
            entry = self.table[index]
            
            if entry.is_empty:
                return False
            if not entry.is_deleted and entry.key == key:
                entry.is_deleted = True
                self.size -= 1
                return True
        
        return False
    
    def _resize(self) -> None:
        """擴容"""
        old_table = self.table
        self.capacity *= 2
        self.table = [self._Entry() for _ in range(self.capacity)]
        self.size = 0
        
        for entry in old_table:
            if not entry.is_empty and not entry.is_deleted:
                self.put(entry.key, entry.value)


class BloomFilter:
    """布隆過濾器 - 空間效率高的機率性資料結構"""
    
    def __init__(self, expected_items: int, false_positive_rate: float = 0.01):
        self.expected_items = expected_items
        self.false_positive_rate = false_positive_rate
        
        self.size = int(-expected_items * (false_positive_rate ** 0.5))
        self.num_hashes = int(-(false_positive_rate ** 0.5))
        
        self.bit_array = [False] * self.size
    
    def _hashes(self, item: str) -> List[int]:
        """計算多個雜湊值"""
        hash1 = HashFunction.djb2_hash(item)
        hash2 = hash(item)
        
        return [(hash1 + i * hash2) % self.size for i in range(self.num_hashes)]
    
    def add(self, item: str) -> None:
        """加入元素"""
        for idx in self._hashes(item):
            self.bit_array[idx] = True
    
    def contains(self, item: str) -> bool:
        """檢查元素是否存在"""
        return all(self.bit_array[idx] for idx in self._hashes(item))


class HashMap(Dict):
    """基於內建 dict 的雜湊表包裝"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def put(self, key: Any, value: Any) -> None:
        """插入或更新"""
        self[key] = value
    
    def get_or_default(self, key: Any, default: Any = None) -> Any:
        """取得值，若不存在則返回預設值"""
        return self.get(key, default)


def demo_hash_table():
    """演示雜湊表"""
    print("=== 雜湊表實作範例演示 ===")
    print()
    
    print("1. 鏈結法雜湊表:")
    ht = HashTableChaining()
    ht.put("name", "Alice")
    ht.put("age", 25)
    ht.put("city", "Taipei")
    
    print(f"   取得 name: {ht.get('name')}")
    print(f"   取得 age: {ht.get('age')}")
    print(f"   取得 city: {ht.get('city')}")
    print(f"   所有鍵: {ht.keys()}")
    print(f"   大小: {ht.size}")
    print()
    
    print("2. 開放定址法雜湊表:")
    oa = HashTableOpenAddressing()
    oa.put("apple", 100)
    oa.put("banana", 200)
    oa.put("orange", 150)
    
    print(f"   取得 apple: {oa.get('apple')}")
    print(f"   取得 banana: {oa.get('banana')}")
    print(f"   大小: {oa.size}")
    print()
    
    print("3. 布隆過濾器:")
    bf = BloomFilter(expected_items=1000)
    words = ["hello", "world", "test", "python"]
    
    for word in words:
        bf.add(word)
    
    print(f"   包含 'hello': {bf.contains('hello')}")
    print(f"   包含 'world': {bf.contains('world')}")
    print(f"   包含 'missing': {bf.contains('missing')}")


if __name__ == "__main__":
    demo_hash_table()
