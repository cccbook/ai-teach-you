# 垃圾回收 (Garbage Collection)

## 概述

垃圾回收（GC）是自動記憶體管理的一種機制，自動回收不再使用的記憶體。GC 消除了手動記憶體管理的負擔和錯誤（如記憶體洩漏、懸空指標），是現代語言如 Java、Python、Go 的核心特性。

## 歷史

- **1959**：John McCarthy 為 LISP 實現第一個 GC
- **1960s**：參照計數法出現
- **1970s**：標記-清除演算法
- **1990s**：世代收集器
- **現在**：多種 GC 演算法並存

## GC 演算法

### 1. 參照計數

```python
class RefCountGC:
    def __init__(self):
        self.objects = {}
    
    def allocate(self, obj):
        ref_count = 0
        self.objects[id(obj)] = {
            'obj': obj,
            'ref_count': 0
        }
        return obj
    
    def add_reference(self, obj):
        self.objects[id(obj)]['ref_count'] += 1
    
    def remove_reference(self, obj):
        obj_id = id(obj)
        self.objects[obj_id]['ref_count'] -= 1
        if self.objects[obj_id]['ref_count'] == 0:
            self.collect(obj_id)
    
    def collect(self, obj_id):
        print(f"收集物件: {obj_id}")
        del self.objects[obj_id]
```

### 2. 標記-清除

```python
class MarkSweepGC:
    def __init__(self):
        self.heap = []
        self.roots = set()
    
    def mark(self):
        # 從 root 開始標記所有可達物件
        marked = set()
        stack = list(self.roots)
        
        while stack:
            obj = stack.pop()
            if obj not in marked:
                marked.add(obj)
                for ref in obj.get_references():
                    if ref not in marked:
                        stack.append(ref)
        
        return marked
    
    def sweep(self, marked):
        # 收集未標記的物件
        for obj in self.heap:
            if obj not in marked:
                self.deallocate(obj)
    
    def collect(self):
        marked = self.mark()
        self.sweep(marked)
```

### 3. 標記-壓縮

```python
class MarkCompactGC:
    def compact(self, heap):
        # 將存活物件移到連續記憶體
        next_addr = 0
        live_objects = []
        
        # 標記並計算新位址
        for obj in heap:
            if obj.is_live():
                live_objects.append(obj)
                obj.new_addr = next_addr
                next_addr += obj.size
        
        # 移動物件並更新參照
        for obj in live_objects:
            self.move_object(obj, obj.new_addr)
        
        return live_objects
```

### 4. 世代收集

```python
class GenerationalGC:
    def __init__(self):
        # 年輕代：New, Old
        # 老年代：Tenured
        self.generations = [
            {'name': 'nursery', 'size': 4 * 1024 * 1024},
            {'name': 'young', 'size': 16 * 1024 * 1024},
            {'name': 'old', 'size': 64 * 1024 * 1024}
        ]
    
    def minor_collection(self):
        # 年輕代收集（頻繁）
        self.collect(self.generations[0], self.generations[1])
    
    def major_collection(self):
        # 老年代收集（較少）
        self.collect(self.generations[1], self.generations[2])
    
    def collect(self, source, target):
        # 將存活的物件提升到下一代
        pass
```

### 5. 增量式 GC

```python
class IncrementalGC:
    # 將 GC 工作分散到多個小步驟
    # 避免長暫停
    
    def collect_incrementally(self):
        if self.phase == 'mark':
            self.mark_phase()
            if self.is_mark_done():
                self.phase = 'sweep'
        
        elif self.phase == 'sweep':
            self.sweep_phase()
            if self.is_sweep_done():
                self.phase = 'done'
```

## GC 與程式語言

### Java GC

```java
// Java GC 選項
// -XX:+UseSerialGC       // 串行 GC
// -XX:+UseParallelGC     // 平行 GC
// -XX:+UseConcMarkSweepGC // CMS GC
// -XX:+UseG1GC          // G1 GC
// -XX:+UseZGC           // ZGC

// 記憶體區域
// Young Gen: Eden, Survivor
// Old Gen: Tenured
// Metaspace
```

### Python GC

```python
import gc

# 執行垃圾回收
gc.collect()

# 檢查物件
gc.get_objects()

# 禁用 GC
gc.disable()

# 啟用 GC
gc.enable()

# 查看參照計數
import sys
sys.getrefcount(obj)
```

### Go GC

```go
// Go GC 是標記-清除
// runtime.GC() 手動觸發

import "runtime"

func forceGC() {
    runtime.GC()
}

// GODEBUG=gctrace=1 查看 GC 訊息
```

## 為什麼學習 GC？

1. **記憶體管理**：理解自動記憶體管理
2. **效能優化**：GC 調優
3. **語言設計**：實現新語言
4. **除錯**：記憶體相關問題

## 參考資源

- "Garbage Collection: Algorithms for Automatic Dynamic Memory Management"
- "The Garbage Collection Handbook"
- 各語言 GC 文件
