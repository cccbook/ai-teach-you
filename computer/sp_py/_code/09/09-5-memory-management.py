"""
桌面系統的記憶體管理
"""

class DesktopMemoryManager:
    """桌面系統記憶體管理器"""
    
    def __init__(self):
        self.processes = {}
        self.swap_space = {}
        self.page_size = 4096
    
    def allocate_virtual(self, size):
        """配置虛擬記憶體"""
        pages_needed = (size + self.page_size - 1) // self.page_size
        return pages_needed * self.page_size
    
    def page_fault_handler(self, process_id, address):
        """頁缺失處理"""
        # 1. 檢查區段表
        # 2. 從磁碟載入頁面（或分配新頁）
        # 3. 更新分頁表
        print(f"頁缺失: 程序 {process_id}, 位址 {address}")
        return True
    
    def swap_out(self, process_id):
        """換出"""
        print(f"換出程序 {process_id} 到 swap")
    
    def swap_in(self, process_id):
        """換入"""
        print(f"換入程序 {process_id} 從 swap")

# Windows 記憶體管理
class WindowsMemoryManager:
    """Windows 記憶體管理"""
    
    def __init__(self):
        self.working_sets = {}
        self.page_priority = {}
    
    def set_working_set(self, pid, min_size, max_size):
        """設定工作集"""
        self.working_sets[pid] = {'min': min_size, 'max': max_size}
        print(f"程序 {pid} 工作集: {min_size}-{max_size} KB")
    
    def memory_manager_features(self):
        """記憶體管理特性"""
        print("""
=== Windows 記憶體管理 ===

1. 分頁管理
   - 請求式分頁
   - 工作集管理
   - 硬碟傾印

2. 虛擬記憶體
   - 4GB 虛擬位址空間（32位）
   - 分頁檔動態調整

3. 記憶體傾印
   - 完整傾印
   - 核心傾印
   - 主動態傾印
""")

# macOS 記憶體管理
class MacOSMemoryManager:
    """macOS 記憶體管理"""
    
    def __init__(self):
        self.compressed_memory = {}
    
    def compress_memory(self, process_id):
        """記憶體壓縮"""
        print(f"壓縮程序 {process_id} 的記憶體")
    
    def vm_features(self):
        """VM 特性"""
        print("""
=== macOS 虛擬記憶體 ===

1. 分頁
   - 延遲分頁
   - 壓縮記憶體（vm_compressor）

2. 共享記憶體
   - Zero-fill 頁面共享
   - Copy-on-write

3. 安全性
   - ASLR
   - DEP/NX
""")
