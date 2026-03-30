"""
程序管理與 IPC 模擬
"""

# 管道
class Pipe:
    """管道"""
    
    def __init__(self):
        self.read_end = None
        self.write_end = None
    
    def create(self):
        """建立管道"""
        self.read_end = ['read_buffer']
        self.write_end = self.read_end
        print("建立管道")
        return self
    
    def write(self, data):
        """寫入"""
        if self.write_end:
            self.write_end[0] = data
            print(f"寫入: {data}")
    
    def read(self):
        """讀取"""
        if self.read_end:
            return self.read_end[0]

# 訊息佇列
class MessageQueue:
    """訊息佇列"""
    
    def __init__(self):
        self.queue = []
    
    def send(self, message, msgtype=1):
        """發送"""
        self.queue.append({'type': msgtype, 'data': message})
        print(f"發送訊息: {message}")
    
    def receive(self, msgtype=1):
        """接收"""
        for msg in self.queue:
            if msg['type'] == msgtype:
                self.queue.remove(msg)
                return msg['data']
        return None

# 共用記憶體
class SharedMemory:
    """共用記憶體"""
    
    def __init__(self, size):
        self.size = size
        self.data = bytearray(size)
        self.attached = []
    
    def attach(self, process_id):
        """附加"""
        self.attached.append(process_id)
        print(f"程序 {process_id} 附加共用記憶體")
        return self.data
    
    def write(self, offset, data):
        """寫入"""
        for i, b in enumerate(data):
            self.data[offset + i] = b
    
    def read(self, offset, length):
        """讀取"""
        return bytes(self.data[offset:offset+length])

# 練習：訊號處理
class Signal:
    """訊號處理"""
    
    SIGNALS = {
        1: 'SIGHUP',   # 掛起
        2: 'SIGINT',   # 中斷
        9: 'SIGKILL',  # 終止
        15: 'SIGTERM'  # 終止
    }
    
    handlers = {}
    
    @staticmethod
    def signal(sig, handler):
        """設定訊號處理器"""
        Signal.handlers[sig] = handler
        print(f"設定訊號 {sig} ({Signal.SIGNALS.get(sig, 'UNKNOWN')})")
    
    @staticmethod
    def raise_signal(sig):
        """觸發訊號"""
        if sig in Signal.handlers:
            print(f"觸發訊號 {sig}")
            Signal.handlers[sig]()
        else:
            print(f"訊號 {sig} 無處理器")

# 測試 IPC
pipe = Pipe().create()
pipe.write("Hello from parent!")
data = pipe.read()
print(f"收到: {data}")

mq = MessageQueue()
mq.send("Message 1", 1)
mq.send("Message 2", 1)
print(f"接收: {mq.receive(1)}")

shm = SharedMemory(1024)
shm.attach(100)
shm.write(0, b"Shared data")
print(f"讀取: {shm.read(0, 11)}")

Signal.signal(2, lambda: print("處理中斷訊號"))
Signal.raise_signal(2)
