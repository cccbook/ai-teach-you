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
