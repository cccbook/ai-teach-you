"""
Linux 系統呼叫模擬
"""

class LinuxSyscall:
    """Linux 系統呼叫模擬"""
    
    def __init__(self):
        self.fd_table = {0: 'stdin', 1: 'stdout', 2: 'stderr'}
        self.next_fd = 3
    
    # 檔案相關
    def sys_open(self, pathname, flags):
        """開啟檔案"""
        fd = self.next_fd
        self.next_fd += 1
        self.fd_table[fd] = pathname
        print(f"open(\"{pathname}\") = {fd}")
        return fd
    
    def sys_read(self, fd, count):
        """讀取"""
        if fd in self.fd_table:
            print(f"read({fd}, {count})")
            return f"data from {self.fd_table[fd]}"
        return -1
    
    def sys_write(self, fd, data):
        """寫入"""
        if fd in self.fd_table:
            print(f"write({fd}, {len(data)} bytes)")
            return len(data)
        return -1
    
    def sys_close(self, fd):
        """關閉"""
        if fd in self.fd_table:
            del self.fd_table[fd]
            print(f"close({fd})")
            return 0
        return -1
    
    # 程序相關
    def sys_getpid(self):
        """取得 PID"""
        return 1000
    
    def sys_getuid(self):
        """取得 UID"""
        return 1000
    
    def sys_fork(self):
        """分叉"""
        pid = 2000
        print(f"fork() = {pid}")
        return pid
    
    def sys_execve(self, filename):
        """執行"""
        print(f"execve(\"{filename}\")")
    
    def sys_exit(self, status):
        """退出"""
        print(f"exit({status})")
    
    # 記憶體相關
    def sys_mmap(self, addr, length, prot, flags, fd, offset):
        """映射記憶體"""
        print(f"mmap({length} bytes)")
        return 0x7f0000000000
    
    def sys_mprotect(self, addr, length, prot):
        """保護記憶體"""
        print(f"mprotect({addr}, {length})")

# 練習：使用 Python 模擬 strace
def strace_simulation():
    """模擬 strace 輸出"""
    print("""
=== strace 輸出範例 ===

execve("./a.out", ["./a.out"], 0x7fff...) = 0
brk(NULL)                               = 0x55a00000
mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f0000000000
open("test.txt", O_RDONLY)              = 3
read(3, "Hello World", 4096)            = 11
write(1, "Hello World", 11)             = 11
close(3)                                 = 0
exit_group(0)                           = ?
+++ exited with 0 +++
""")

# API vs System Call
print("""
=== API vs System Call ===

API (Application Programming Interface):
- 程式設計師使用的介面
- 例: open(), read(), write()

System Call:
- 核心提供的介面
- 例: sys_open, sys_read, sys_write

關係：
  Application → glibc → syscall → Kernel
""")
