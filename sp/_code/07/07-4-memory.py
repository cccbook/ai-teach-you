"""
記憶體管理：分頁、分段、虛擬記憶體
"""

# 1. 分頁管理
class PageTable:
    """分頁表"""
    
    def __init__(self, page_size=4096):
        self.page_size = page_size
        self.pages = {}  # 虛擬頁號 -> 實體頁框
    
    def translate(self, virtual_addr):
        """虛擬位址轉實體位址"""
        vpn = virtual_addr // self.page_size
        offset = virtual_addr % self.page_size
        
        if vpn in self.pages:
            pfn = self.pages[vpn]
            return pfn * self.page_size + offset
        else:
            # 頁fault
            raise PageFault(f"虛擬頁 {vpn} 未映射")

# 2. 記憶體分配
class MemoryAllocator:
    """記憶體分配器"""
    
    def __init__(self, total_size):
        self.total_size = total_size
        self.free_blocks = [(0, total_size)]
        self.allocated = {}
    
    def allocate(self, size, name):
        """分配記憶體"""
        for i, (addr, block_size) in enumerate(self.free_blocks):
            if block_size >= size:
                # 找到合适的區塊
                self.free_blocks.pop(i)
                
                if block_size > size:
                    self.free_blocks.append((addr + size, block_size - size))
                
                self.allocated[name] = (addr, size)
                return addr
        
        return None  # 記憶體不足
    
    def deallocate(self, name):
        """釋放記憶體"""
        if name in self.allocated:
            addr, size = self.allocated[name]
            
            # 合併相鄰的空闲區塊
            self.free_blocks.append((addr, size))
            self.free_blocks.sort()
            
            merged = []
            for addr, size in self.free_blocks:
                if merged and merged[-1][0] + merged[-1][1] == addr:
                    merged[-1] = (merged[-1][0], merged[-1][1] + size)
                else:
                    merged.append((addr, size))
            self.free_blocks = merged
            
            del self.allocated[name]

# 測試記憶體分配
allocator = MemoryAllocator(1000)
print("初始記憶體:", allocator.free_blocks)

allocator.allocate(100, 'process1')
print("分配 P1 100 bytes:", allocator.free_blocks)

allocator.allocate(200, 'process2')
print("分配 P2 200 bytes:", allocator.free_blocks)

allocator.deallocate('process1')
print("釋放 P1:", allocator.free_blocks)

allocator.allocate(150, 'process3')
print("分配 P3 150 bytes:", allocator.free_blocks)

# 3. 虛擬記憶體 - 頁面置換
class VirtualMemory:
    """虛擬記憶體系統"""
    
    def __init__(self, num_frames):
        self.frames = [None] * num_frames
        self.page_table = {}
        self.page_faults = 0
    
    def access(self, page):
        """存取頁面"""
        if page in self.page_table:
            # 命中
            return self.page_table[page]
        else:
            # 頁 fault
            self.page_faults += 1
            return self.load_page(page)
    
    def load_page(self, page):
        """載入頁面"""
        # 找空框架或置換
        free_frame = None
        for i, frame in enumerate(self.frames):
            if frame is None:
                free_frame = i
                break
        
        if free_frame is None:
            free_frame = self.lru_replace(page)
        
        self.frames[free_frame] = page
        self.page_table[page] = free_frame
        return free_frame
    
    def lru_replace(self, page):
        """LRU 頁面置換"""
        # 簡化的 LRU：替换第一個框架
        return 0
    
    def hit_rate(self, total_access):
        return (total_access - self.page_faults) / total_access

# 測試虛擬記憶體
vm = VirtualMemory(num_frames=3)
accesses = [1, 2, 3, 1, 4, 1, 2, 3, 5, 1]

for page in accesses:
    vm.access(page)

print(f"總存取: {len(accesses)}, 頁 fault: {vm.page_faults}")
print(f"命中率: {vm.hit_rate(len(accesses)):.2%}")
