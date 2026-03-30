"""
垃圾回收機制實作
"""

# 1. 引用計數（Reference Counting）
class RefCountObject:
    def __init__(self, value):
        self.value = value
        self.ref_count = 0
    
    def __repr__(self):
        return f"Object({self.value}, ref={self.ref_count})"

class RefCountGC:
    def __init__(self):
        self.objects = {}
        self.next_id = 0
    
    def create(self, value):
        obj_id = self.next_id
        self.next_id += 1
        obj = RefCountObject(value)
        self.objects[obj_id] = obj
        return obj_id
    
    def reference(self, obj_id):
        if obj_id in self.objects:
            self.objects[obj_id].ref_count += 1
        return obj_id
    
    def dereference(self, obj_id):
        if obj_id in self.objects:
            obj = self.objects[obj_id]
            obj.ref_count -= 1
            if obj.ref_count == 0:
                del self.objects[obj_id]
                print(f"回收記憶體: {obj}")
    
    def collect(self):
        """手動觸發回收"""
        to_delete = [k for k, v in self.objects.items() if v.ref_count == 0]
        for k in to_delete:
            obj = self.objects[k]
            del self.objects[k]
            print(f"GC 回收: {obj}")

# 測試引用計數
gc = RefCountGC()
a = gc.create("Object A")  # 建立物件
b = gc.create("Object B")
print(f"初始: {gc.objects}")

gc.reference(a)  # a 被 b 引用
gc.reference(b)  # b 被 a 引用（循環引用）
print(f"引用後: {gc.objects}")

# 解除外部引用
gc.dereference(a)  # 外部不再引用 a
gc.dereference(b)  # 外部不再引用 b
print(f"解除引用後: {gc.objects}")

# 注意：循環引用無法被引用計數回收！
# 需要其他 GC 演算法（如 Mark-Sweep）來處理

# 2. 標記-清除（Mark-Sweep）演算法
class MarkSweepGC:
    def __init__(self):
        self.heap = []  # 堆記憶體
        self.roots = set()  # 根集合（全域變數、堆疊）
    
    def allocate(self, size):
        """配置記憶體"""
        obj = {'id': len(self.heap), 'size': size, 'marked': False, 'data': None}
        self.heap.append(obj)
        return obj['id']
    
    def mark(self, obj_id):
        """標記階段：標記所有可達物件"""
        obj = self.heap[obj_id]
        if obj['marked']:
            return
        obj['marked'] = True
        # 這裡需要追蹤物件的指標，簡化版本略過
    
    def sweep(self):
        """清除階段：回收未標記的物件"""
        freed = []
        for obj in self.heap:
            if not obj['marked']:
                freed.append(obj['id'])
                # 實際會呼叫 free() 釋放記憶體
        self.heap = [obj for obj in self.heap if obj['marked']]
        return freed
    
    def collect(self):
        """執行完整 GC"""
        # 1. 標記
        for root in self.roots:
            self.mark(root)
        # 2. 清除
        freed = self.sweep()
        # 3. 取消標記（為下次準備）
        for obj in self.heap:
            obj['marked'] = False
        print(f"GC 完成，回收 {len(freed)} 個物件")

# 3. 複製（Copying）GC
class CopyGC:
    def __init__(self, from_space, to_space):
        self.from_space = from_space  # ['from', 'to']
        self.to_space = to_space
        self.current_space = from_space
    
    def copy(self, obj):
        """將存活物件複製到 To Space"""
        # 簡化版本：直接移動
        new_obj = obj.copy()
        self.to_space.append(new_obj)
        return new_obj
    
    def collect(self):
        """GC 觸發時，交換空間並複製存活物件"""
        old_space = self.current_space
        new_space = self.to_space if self.current_space == self.from_space else self.from_space
        
        new_space.clear()
        for obj in old_space:
            if obj['alive']:  # 假設有方法判斷是否存活
                self.copy(obj)
        
        self.current_space = new_space
        print(f"GC 完成，存活物件數: {len(new_space)}")

# 測試
gc = CopyGC(['from', 'to'])
gc.from_space = [
    {'id': 1, 'alive': True},
    {'id': 2, 'alive': False},
    {'id': 3, 'alive': True},
]
gc.collect()
print(f"To Space: {gc.to_space}")
