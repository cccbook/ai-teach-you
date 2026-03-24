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
