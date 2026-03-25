"""
RTOS 任務排程模擬
"""

import time
from enum import Enum

class TaskState(Enum):
    CREATED = "created"
    READY = "ready"
    RUNNING = "running"
    BLOCKED = "blocked"
    SUSPENDED = "suspended"

class Task:
    """RTOS 任務"""
    
    def __init__(self, name, priority, period, function):
        self.name = name
        self.priority = priority  # 數字越小優先級越高
        self.period = period     # 執行週期 (秒)
        self.function = function
        self.state = TaskState.READY
        self.next_run = 0
        self.worst_case_execution = 0
    
    def run(self):
        """執行任務"""
        self.state = TaskState.RUNNING
        print(f"[{self.name}] 開始執行 (優先級: {self.priority})")
        
        # 執行任務工作
        try:
            self.function()
        except Exception as e:
            print(f"任務執行錯誤: {e}")
        
        self.state = TaskState.READY
        print(f"[{self.name}] 執行完成")
    
    def wait(self, delay):
        """任務延遲"""
        self.state = TaskState.BLOCKED
        time.sleep(delay)
        self.state = TaskState.READY

# RTOS 排程器
class RTOSScheduler:
    """即時排程器"""
    
    def __init__(self, scheduler_type="fixed_priority"):
        self.tasks = []
        self.scheduler_type = scheduler_type
    
    def add_task(self, task):
        """加入任務"""
        self.tasks.append(task)
    
    def schedule(self):
        """排程任務"""
        # 固定優先級排程
        if self.scheduler_type == "fixed_priority":
            self.tasks.sort(key=lambda t: t.priority)
        
        # Rate Monotonic Scheduling (RMS)
        elif self.scheduler_type == "rms":
            self.tasks.sort(key=lambda t: t.period)
        
        # Earliest Deadline First (EDF)
        elif self.scheduler_type == "edf":
            self.tasks.sort(key=lambda t: t.next_run)
    
    def run(self, duration):
        """執行排程器"""
        start_time = time.time()
        
        while time.time() - start_time < duration:
            self.schedule()
            
            # 執行就緒任務
            for task in self.tasks:
                if task.state == TaskState.READY:
                    task.run()
                    break
            
            time.sleep(0.1)

# 測試
def sensor_task():
    """感測器任務"""
    print("  -> 讀取感測器資料")

def control_task():
    """控制任務"""
    print("  -> 執行控制邏輯")

def display_task():
    """顯示任務"""
    print("  -> 更新顯示")

rtos = RTOSScheduler(scheduler_type="fixed_priority")
rtos.add_task(Task("Sensor", priority=1, period=0.1, function=sensor_task))
rtos.add_task(Task("Control", priority=2, period=0.2, function=control_task))
rtos.add_task(Task("Display", priority=3, period=0.5, function=display_task))

print("=== RTOS 排程模擬 ===")
rtos.run(duration=1.0)

# 即時性分析
print("\n=== 即時性分析 ===")
print("固定優先級:")
print("  - 高優先級任務會搶占低優先級任務")
print("  - 可能產生優先級反轉")

print("\nRMS (Rate Monotonic):")
print("  - 週期越短，優先級越高")
print("  - 可行性條件: U <= n(2^(1/n) - 1)")