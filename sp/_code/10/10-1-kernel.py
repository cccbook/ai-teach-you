"""
Linux 核心模擬
"""

class LinuxKernel:
    """Linux 核心模擬"""
    
    def __init__(self):
        self.modules = []
        self.processes = []
        self.filesystems = {}
        self.devices = {}
    
    def load_module(self, name):
        """載入核心模組"""
        print(f"載入核心模組: {name}")
        self.modules.append(name)
    
    def unload_module(self, name):
        """卸載核心模組"""
        if name in self.modules:
            self.modules.remove(name)
            print(f"卸載核心模組: {name}")
    
    def create_process(self, name):
        """建立程序"""
        pid = len(self.processes)
        self.processes.append({'pid': pid, 'name': name, 'state': 'running'})
        print(f"建立程序: {name} (PID: {pid})")
    
    def register_filesystem(self, name, operations):
        """註冊檔案系統"""
        self.filesystems[name] = operations
        print(f"註冊檔案系統: {name}")

# Linux 核心架構圖
print("""
=== Linux 核心架構 ===

+-------------------+
|   User Space      |
|  (Applications)  |
+-------------------+
        |  System Calls
+-------------------+
|   Kernel Space    |
|  +-------------+   |
|  | System Call|   |
|  | Interface  |   |
|  +-------------+   |
|  | File System |   |
|  | Process     |   |
|  | Memory      |   |
|  | Network     |   |
|  | Device Drv  |   |
|  +-------------+   |
+-------------------+
        |  Device Drivers
+-------------------+
|   Hardware        |
+-------------------+
""")
