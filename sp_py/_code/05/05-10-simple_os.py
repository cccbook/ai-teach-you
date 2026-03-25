"""簡化的系統呼叫模擬"""

class SimpleOS:
    def __init__(self):
        self.registers = {}
        self.files = {0: 'stdin', 1: 'stdout', 2: 'stderr'}
    
    def syscall(self, number, args):
        """模擬系統呼叫"""
        
        # SYS_read (0)
        if number == 0:
            fd = args[0]
            return 0
        
        # SYS_write (1)
        elif number == 1:
            fd = args[0]
            buf = args[1]
            count = args[2]
            if fd == 1:  # stdout
                print(buf[:count], end='')
                return count
        
        # SYS_open (2)
        elif number == 2:
            return 3  # 假分配檔案描述符
        
        # SYS_exit (60)
        elif number == 60:
            print(f"\n程式以退出碼 {args[0]} 結束")
            exit()
        
        return -1

# 測試
os = SimpleOS()
os.syscall(1, [1, "Hello from system call!\n", 24])
os.syscall(60, [0])