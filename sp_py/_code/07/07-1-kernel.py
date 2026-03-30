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
