# 7. 作業系統的結構

## 7.1 作業系統核心概念

[程式檔案：07-1-kernel.py](../_code/07/07-1-kernel.py)
```python
"""
作業系統核心概念模擬
"""

class Kernel:
    """簡化的核心模擬"""
    
    def __init__(self):
        self.processes = {}  # 程序表
        self.files = {}      # 檔案表
        self.memory = bytearray(1024 * 1024)  # 1MB 模擬記憶體
        self.system_call_table = {
            1: self.sys_read,
            2: self.sys_write,
            3: self.sys_open,
            4: self.sys_close,
            5: self.sys_exit,
        }
    
    def system_call(self, number, args):
        """系統呼叫處理"""
        handler = self.system_call_table.get(number)
        if handler:
            return handler(args)
        return -1
    
    def sys_read(self, args):
        fd, buf, n = args
        return 0
    
    def sys_write(self, args):
        fd, buf, n = args
        # 輸出到控制台
        print(buf[:n].decode() if isinstance(buf, bytes) else buf)
        return n
    
    def sys_open(self, args):
        path, flags = args
        fd = len(self.files)
        self.files[fd] = {'path': path, 'flags': flags}
        return fd
    
    def sys_close(self, args):
        fd = args[0]
        if fd in self.files:
            del self.files[fd]
        return 0
    
    def sys_exit(self, args):
        status = args[0]
        print(f"程式結束，退出碼: {status}")
        return 0

# Shell 概念
class Shell:
    """簡化的命令列直譯器"""
    
    def __init__(self, kernel):
        self.kernel = kernel
        self.running = True
    
    def parse_command(self, cmd):
        """解析命令"""
        parts = cmd.strip().split()
        if not parts:
            return None, []
        
        return parts[0], parts[1:]
    
    def execute(self, cmd):
        """執行命令"""
        cmd, args = self.parse_command(cmd)
        
        if cmd == 'exit':
            self.running = False
            return
        
        if cmd == 'echo':
            print(' '.join(args))
            return
        
        if cmd == 'ls':
            # 模擬 ls
            print('file1.txt  file2.txt  dir/')
            return
        
        print(f"命令未找到: {cmd}")
    
    def run(self):
        """執行 Shell"""
        while self.running:
            cmd = input('$ ')
            self.execute(cmd)

# 測試
kernel = Kernel()
shell = Shell(kernel)
# shell.run()  # 啟動互動式 Shell
print("核心初始化完成")
```

## 7.2 程序與執行緒

[程式檔案：07-2-process-thread.py](../_code/07/07-2-process-thread.py)
```python
"""
程序（Process）與執行緒（Thread）模擬
"""

import threading
import multiprocessing
import time

# 程序控制區塊（PCB）
class PCB:
    """程序控制區塊"""
    def __init__(self, pid, name):
        self.pid = pid
        self.name = name
        self.state = 'NEW'  # NEW, READY, RUNNING, BLOCKED, TERMINATED
        self.registers = {}  # 暫存器狀態
        self.memory = {}      # 記憶體空間
        self.files = []       # 開啟的檔案
        self.parent = None
        self.children = []
        self.priority = 0

# 程序實現
class Process:
    """程序類別"""
    next_pid = 1
    
    def __init__(self, name):
        self.pid = Process.next_pid
        Process.next_pid += 1
        self.name = name
        self.pcb = PCB(self.pid, name)
        self.threads = []
    
    def start(self):
        """啟動程序"""
        print(f"程序 {self.pid} ({self.name}) 啟動")
        self.pcb.state = 'RUNNING'
    
    def terminate(self):
        """終止程序"""
        print(f"程序 {self.pid} 終止")
        self.pcb.state = 'TERMINATED'

# 執行緒實現
class Thread:
    """執行緒類別"""
    def __init__(self, process, target):
        self.process = process
        self.target = target
        self.thread = threading.Thread(target=target)
    
    def start(self):
        self.thread.start()
    
    def join(self):
        self.thread.join()

# 多執行緒範例
def worker(name, delay):
    """工作者執行緒"""
    for i in range(3):
        print(f"執行緒 {name}: 第 {i+1} 次執行")
        time.sleep(delay)

# 建立多執行緒
threads = []
for i in range(3):
    t = threading.Thread(target=worker, args=(f"Worker-{i}", 0.5))
    threads.append(t)
    t.start()

# 等待所有執行緒完成
for t in threads:
    t.join()

print("所有執行緒完成")

# 多程序範例
def process_worker(shared_value):
    """多程序工作者"""
    import os
    pid = os.getpid()
    for i in range(3):
        shared_value.value += 1
        print(f"程序 {pid}: 計數 = {shared_value.value}")
        time.sleep(0.1)

# 使用共享記憶體
if __name__ == '__main__':
    shared = multiprocessing.Value('i', 0)
    
    processes = []
    for i in range(3):
        p = multiprocessing.Process(target=process_worker, args=(shared,))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    print(f"最終計數: {shared.value}")

# 程序 vs 執行緒
print("""
=== 程序 vs 執行緒 ===

程序:
- 獨立的位址空間
- 擁有獨立的資源（檔案、記憶體）
- 創建/銷毀成本較高
- 通訊需要 IPC（管道、訊息佇列）

執行緒:
- 共享程序的位址空間
- 共用資源（記憶體、檔案）
- 創建/銷毀成本較低
- 通訊直接共享資料（需同步）
""")
```

## 7.3 行程排程

[程式檔案：07-3-scheduler.py](../_code/07/07-3-scheduler.py)
```python
"""
行程排程演算法
"""

import heapq
import random
import time

# 排程器介面
class Scheduler:
    def add_process(self, process):
        pass
    
    def next_process(self):
        pass

# 1. 先進先出（FIFO / FCFS）
class FCFSScheduler:
    """First-Come, First-Served"""
    
    def __init__(self):
        self.queue = []
    
    def add_process(self, process):
        self.queue.append(process)
    
    def next_process(self):
        if self.queue:
            return self.queue.pop(0)
        return None

# 2. 短工作優先（SJF）
class SJFScheduler:
    """Shortest Job First"""
    
    def __init__(self):
        self.queue = []  # (burst_time, process)
    
    def add_process(self, process):
        heapq.heappush(self.queue, (process.burst_time, process))
    
    def next_process(self):
        if self.queue:
            return heapq.heappop(self.queue)[1]
        return None

# 3. 時間片輪轉（Round Robin）
class RoundRobinScheduler:
    """Round Robin"""
    
    def __init__(self, time_quantum=2):
        self.queue = []
        self.time_quantum = time_quantum
    
    def add_process(self, process):
        process.remaining_time = process.burst_time
        self.queue.append(process)
    
    def next_process(self):
        if not self.queue:
            return None
        
        process = self.queue.pop(0)
        execute_time = min(self.time_quantum, process.remaining_time)
        process.remaining_time -= execute_time
        
        print(f"執行 {process.name} {execute_time} 單位時間")
        
        if process.remaining_time > 0:
            self.queue.append(process)
        
        return process

# 4. 優先級排程
class PriorityScheduler:
    """Priority Scheduling"""
    
    def __init__(self):
        self.queue = []  # (-priority, process)
    
    def add_process(self, process):
        heapq.heappush(self.queue, (-process.priority, process))
    
    def next_process(self):
        if self.queue:
            return heapq.heappop(self.queue)[1]
        return None

# 程序模擬類別
class Process:
    def __init__(self, name, burst_time, priority=0):
        self.name = name
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = 0

# 測試排程演算法
print("=== FCFS 排程 ===")
fcfs = FCFSScheduler()
for name, bt in [('P1', 5), ('P2', 3), ('P3', 8)]:
    fcfs.add_process(Process(name, bt))

total_time = 0
while fcfs.queue:
    p = fcfs.next_process()
    print(f"執行 {p.name} (burst={p.burst_time})")
    total_time += p.burst_time

print(f"總時間: {total_time}, 平均等待: {total_time / 3 - 5}")

print("\n=== Round Robin 排程 ===")
rr = RoundRobinScheduler(time_quantum=2)
for name, bt in [('P1', 5), ('P2', 3), ('P3', 8)]:
    rr.add_process(Process(name, bt))

while rr.queue:
    rr.next_process()

print("\n=== 優先級排程 ===")
ps = PriorityScheduler()
for name, bt, pri in [('P1', 5, 2), ('P2', 3, 1), ('P3', 8, 3)]:
    ps.add_process(Process(name, bt, pri))

while ps.queue:
    p = ps.next_process()
    print(f"執行 {p.name} (優先級={p.priority})")
```

## 7.4 記憶體管理

[程式檔案：07-4-memory.py](../_code/07/07-4-memory.py)
```python
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
```

## 7.5 檔案系統

[程式檔案：07-5-filesystem.py](../_code/07/07-5-filesystem.py)
```python
"""
檔案系統實現
"""

import os

# 索引節點（inode）結構
class Inode:
    def __init__(self, inumber):
        self.inumber = inumber
        self.type = 'file'  # file, directory
        self.size = 0
        self.blocks = []
        self.permissions = 0o644
        self.links = 1
    
    def add_block(self, block_num):
        self.blocks.append(block_num)
        self.size = 512

# 目錄項目
class DirEntry:
    def __init__(self, name, inumber):
        self.name = name
        self.inumber = inumber

# 簡化的檔案系統
class SimpleFileSystem:
    def __init__(self, total_blocks=100):
        self.total_blocks = total_blocks
        self.free_blocks = set(range(total_blocks))
        self.inodes = [None] * 20  # 最多20個 inode
        self.root_inode = self.create_inode('directory')
    
    def create_inode(self, itype):
        """建立 inode"""
        for i, inode in enumerate(self.inodes):
            if inode is None:
                self.inodes[i] = Inode(i)
                self.inodes[i].type = itype
                return i
        return -1
    
    def allocate_block(self):
        """分配區塊"""
        if self.free_blocks:
            return self.free_blocks.pop()
        return -1
    
    def create_file(self, path):
        """建立檔案"""
        parts = path.split('/')
        parent = self.root_inode
        
        # 找到父目錄
        for part in parts[:-1]:
            if not part:
                continue
            # 搜尋子目錄...
        
        # 建立新 inode
        inumber = self.create_inode('file')
        inode = self.inodes[inumber]
        
        # 分配區塊
        block = self.allocate_block()
        if block >= 0:
            inode.add_block(block)
        
        return inumber
    
    def read_file(self, inumber):
        """讀取檔案"""
        inode = self.inodes[inumber]
        return f"內容: {inode.size} bytes, {len(inode.blocks)} blocks"

# 練習：使用 os 模組操作檔案
def file_operations():
    """檔案操作練習"""
    
    # 建立目錄結構
    os.makedirs('test_dir/sub_dir', exist_ok=True)
    
    # 寫入檔案
    with open('test_dir/file.txt', 'w') as f:
        f.write('Hello, File System!')
    
    # 讀取檔案
    with open('test_dir/file.txt', 'r') as f:
        content = f.read()
        print(content)
    
    # 列舉目錄
    print(os.listdir('test_dir'))
    
    # 取得檔案資訊
    stat = os.stat('test_dir/file.txt')
    print(f"大小: {stat.st_size}, 修改時間: {stat.st_mtime}")
    
    # 刪除
    os.remove('test_dir/file.txt')
    os.rmdir('test_dir/sub_dir')
    os.rmdir('test_dir')

# FAT32 風格的檔案系統模擬
class FAT32:
    """簡化的 FAT32 檔案系統"""
    
    def __init__(self, size):
        self.fat = [0] * (size // 512)  # 檔案配置表
        self.root_dir = {}
    
    def allocate_cluster(self):
        """配置叢集"""
        for i, entry in enumerate(self.fat):
            if entry == 0:
                self.fat[i] = 0xFFFFFFFF  # End of chain
                return i
        return -1
    
    def write_file(self, filename, data):
        """寫入檔案"""
        clusters_needed = (len(data) + 511) // 512
        chain = []
        
        for _ in range(clusters_needed):
            cluster = self.allocate_cluster()
            if cluster == -1:
                break
            chain.append(cluster)
        
        self.root_dir[filename] = {
            'chain': chain,
            'size': len(data)
        }
        
        print(f"檔案 {filename} 使用叢集: {chain}")
        return chain
    
    def read_file(self, filename):
        """讀取檔案"""
        if filename in self.root_dir:
            info = self.root_dir[filename]
            print(f"讀取 {filename}: {info['size']} bytes, 叢集: {info['chain']}")
        else:
            print(f"檔案不存在: {filename}")

# 測試
fat = FAT32(10000)
fat.write_file('test.txt', 'Hello FAT32!')
fat.read_file('test.txt')
```