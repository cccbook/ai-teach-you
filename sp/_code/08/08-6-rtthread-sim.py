"""
RT-Thread 模擬
"""

class RTThread:
    """RT-Thread 任務類比"""
    
    def __init__(self, name, stack_size, priority):
        self.name = name
        self.stack_size = stack_size
        self.priority = priority
        self.state = 'ready'
        self.mailbox = []  # 郵箱
        self.semaphore = 0
    
    def send(self, message):
        """發送訊息"""
        if len(self.mailbox) < 10:
            self.mailbox.append(message)
            return True
        return False
    
    def receive(self):
        """接收訊息"""
        if self.mailbox:
            return self.mailbox.pop(0)
        return None

# RT-Thread 特性
print("""
=== RT-Thread 特性 ===

1. 微型核心
   - 核心精簡，約 3KB
   - 模組化設計

2. 命名管道（Named Pipe）
   - 建立點對點通訊

3. 訊息佇列
   - 記憶體池管理

4. 訊號
   - 同步與訊號處理

5. 事件
   - 多事件等待

6. 線程同步
   - 互斥鎖、訊號量、臨界區
""")

# RT-Thread 與 FreeRTOS 比較
print("""
=== RT-Thread vs FreeRTOS ===

| 特性       | RT-Thread     | FreeRTOS     |
|------------|--------------|--------------|
| 起源       | 中國         | 美國/英國    |
| 核心大小   | ~3KB         | ~5KB         |
| 任務數量   | 255          | 取決於 RAM   |
| 優先級     | 256          | 可配置       |
| 中文社群   | 強大         | 一般         |
| 檔系統    | 有           | 可選         |
| 網路堆疊   | 有           | 可選         |
""")