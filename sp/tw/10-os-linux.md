# 10. Linux 作業系統與系統程式

## 10.1 Linux 核心架構

[程式檔案：10-1-linux-kernel.c](../_code/10/10-1-linux-kernel.c)
```c
// Linux 核心模組範例

#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Author");
MODULE_DESCRIPTION("Hello World Kernel Module");

static int __init hello_init(void) {
    printk(KERN_INFO "Hello Kernel Module\n");
    return 0;
}

static void __exit hello_exit(void) {
    printk(KERN_INFO "Goodbye Kernel Module\n");
}

module_init(hello_init);
module_exit(hello_exit);

// Linux 核心子系統
/*
1. 程序排程子系統
   - CFS（完全公平排程器）
   - 實時排程

2. 記憶體管理
   - 分頁
   - 區域記憶體配置

3. 檔案系統
   - VFS（虛擬檔案系統）
   - ext4, Btrfs, XFS

4. 網路堆疊
   - TCP/IP
   - Socket 介面

5. 裝置驅動
   - 字元裝置
   - 區塊裝置
   - 網路裝置
*/
```

```python
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
|  (Applications)   |
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
```

## 10.2 System Call 與 API

[程式檔案：10-2-syscall.c](../_code/10/10-2-syscall.c)
```c
// Linux 系統呼叫範例

#include <unistd.h>
#include <sys/syscall.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>

int main() {
    // write() 系統呼叫
    const char *msg = "Hello, World!\n";
    syscall(SYS_write, 1, msg, 14);
    
    // read() 系統呼叫
    char buf[100];
    syscall(SYS_read, 0, buf, 100);
    
    // open() 系統呼叫
    int fd = syscall(SYS_open, "test.txt", O_RDONLY);
    
    // 透過 syscall() 直接呼叫
    long result = syscall(SYS_getpid);
    printf("PID: %ld\n", result);
    
    return 0;
}

// 使用封裝好的 libc 函數
void use_libc() {
    // open()
    int fd = open("file.txt", O_RDONLY);
    
    // read()
    char buf[1024];
    read(fd, buf, 1024);
    
    // write()
    write(STDOUT_FILENO, "Hello\n", 6);
    
    // close()
    close(fd);
}
```

[程式檔案：10-2-syscall.py](../_code/10/10-2-syscall.py)
```python
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
```

## 10.3 程序管理與 IPC

[程式檔案：10-3-ipc.c](../_code/10/10-3-ipc.c)
```c
// 程序間通訊（IPC）

// 1. 管道（Pipe）
#include <unistd.h>
#include <stdlib.h>

int main() {
    int pipefd[2];
    pipe(pipefd);  // 建立管道
    
    if (fork() == 0) {
        // 子程序
        close(pipefd[0]);  // 關閉讀取端
        write(pipefd[1], "Hello", 5);
        close(pipefd[1]);
    } else {
        // 父程序
        close(pipefd[1]);  // 關閉寫入端
        char buf[100];
        read(pipefd[0], buf, 100);
        close(pipefd[0]);
    }
    return 0;
}

// 2. 訊息佇列
#include <sys/msg.h>

struct msgbuf {
    long mtype;
    char mtext[100];
};

// 3. 共用記憶體
#include <sys/shm.h>

int shm_id = shmget(IPC_PRIVATE, 4096, IPC_CREAT | 0666);
char *shm = (char *)shmat(shm_id, NULL, 0);
shmdt(shm);
shmctl(shm_id, IPC_RMID, NULL);

// 4. 訊號
#include <signal.h>

void handler(int sig) {
    printf("收到訊號 %d\n", sig);
}
signal(SIGUSR1, handler);
raise(SIGUSR1);

// 5. 插槽（Socket）
#include <sys/socket.h>
#include <netinet/in.h>

int sock = socket(AF_INET, SOCK_STREAM, 0);
```

```python
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
```

## 10.4 網路堆疊與 Socket 程式設計

[程式檔案：10-4-socket.c](../_code/10/10-4-socket.c)
```c
// Linux Socket 程式設計

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>

// 伺服器端
int server() {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    
    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(8080);
    addr.sin_addr.s_addr = INADDR_ANY;
    
    bind(sock, (struct sockaddr *)&addr, sizeof(addr));
    listen(sock, 10);
    
    while (1) {
        int client = accept(sock, NULL, NULL);
        char buf[1024];
        read(client, buf, 1024);
        write(client, "HTTP/1.1 200 OK\r\n\r\n", 21);
        close(client);
    }
    
    close(sock);
    return 0;
}

// 用戶端
int client() {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    
    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(8080);
    inet_pton(AF_INET, "127.0.0.1", &addr.sin_addr);
    
    connect(sock, (struct sockaddr *)&addr, sizeof(addr));
    write(sock, "GET / HTTP/1.0\r\n\r\n", 19);
    
    char buf[1024];
    read(sock, buf, 1024);
    
    close(sock);
    return 0;
}
```

```python
"""
Python Socket 程式設計
"""

import socket

# TCP 伺服器
def tcp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', 8080))
    sock.listen(5)
    
    print("TCP 伺服器 listening on port 8080")
    
    while True:
        client, addr = sock.accept()
        print(f"連線來自: {addr}")
        
        data = client.recv(1024)
        print(f"收到: {data}")
        
        client.send(b"HTTP/1.1 200 OK\r\n\r\nHello!")
        client.close()

# TCP 用戶端
def tcp_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 8080))
    
    sock.send(b"GET / HTTP/1.0\r\n\r\n")
    response = sock.recv(1024)
    print(f"回應: {response}")
    
    sock.close()

# UDP 伺服器
def udp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 8081))
    
    print("UDP 伺服器 listening on port 8081")
    
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"收到: {data} 從 {addr}")
        
        sock.sendto(b"ACK", addr)

# UDP 用戶端
def udp_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(b"Hello", ('127.0.0.1', 8081))
    sock.close()

# 執行
print("嘗試連線...")
# 注意：需要先啟動伺服器才能連線
# tcp_server() 或 udp_server() 需先執行

# Socket 選項
print("""
=== Socket 選項 ===

SOL_SOCKET 層:
- SO_REUSEADDR: 重複使用位址
- SO_KEEPALIVE: 保持連線
- SO_SNDBUF: 傳送緩衝區大小
- SO_RCVBUF: 接收緩衝區大小

IPPROTO_TCP 層:
- TCP_NODELAY: 禁用 Nagle 演算法
- TCP_QUICKACK: 快速 ACK
""")
```

## 10.5 效能分析工具

[程式檔案：10-5-perf.c](../_code/10/10-5-perf.c)
```c
// C 效能分析範例

#include <stdio.h>
#include <time.h>

// 手動計時
void manual_timing() {
    clock_t start = clock();
    
    // 要測量的程式碼
    for (int i = 0; i < 1000000; i++) {
        // 做一些工作
    }
    
    clock_t end = clock();
    printf("花費時間: %.3f 秒\n", 
           (double)(end - start) / CLOCKS_PER_SEC);
}

// 使用 gettimeofday
#include <sys/time.h>

void timing_with_gettimeofday() {
    struct timeval start, end;
    gettimeofday(&start, NULL);
    
    // 測量程式碼
    
    gettimeofday(&end, NULL);
    double elapsed = (end.tv_sec - start.tv_sec) + 
                    (end.tv_usec - start.tv_usec) / 1000000.0;
    printf("花費時間: %.6f 秒\n", elapsed);
}
```

```python
"""
Linux 效能分析工具模擬
"""

import time

# 1. time 命令
def time_command():
    """模擬 time 命令"""
    start = time.time()
    
    # 執行命令
    result = "命令輸出"
    
    end = time.time()
    elapsed = end - start
    
    print(f"real\t{elapsed:.3f}s")
    print(f"user\t{elapsed * 0.8:.3f}s")
    print(f"sys\t{elapsed * 0.2:.3f}s")

# 2. strace 概念
def strace_concept():
    """strace 系統追蹤"""
    print("""
=== strace 追蹤系統呼叫 ===

$ strace -e trace=open,read,write ls

open(".", O_RDONLY|O_DIRECTORY) = 3
getdents(3, [...], 32768)      = 208
write(1, "file1\\nfile2\\n", 14) = 14
""")

# 3. perf 概念
def perf_concept():
    """perf CPU 效能分析"""
    print("""
=== perf 工具 ===

$ perf record ./program
$ perf report

Samples: 1000 of event 'cycles'
  33.33%  program  [.] loop
  25.00%  program  [.] compute
  16.67%  libc    [.] malloc
""")

# 4. gprof 概念
def gprof_concept():
    """gprof 程式剖析"""
    print("""
=== gprof 剖析 ===

每個函數呼叫次數和時間：

  %   cumulative   self              self    total
 time   seconds   seconds    calls  ms/call  ms/call  name
 25.00      0.25     0.25    10000   0.03    0.03  process
 50.00      0.75     0.50     5000   0.10    0.10  data
""")

# 5. top/htop
def top_concept():
    """top 程序監控"""
    print("""
=== top 輸出 ===

PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND
1234 root      20   0   10240   4096   2048 R  25.0  2.0   0:05.23 program
5678 mysql     20   0  512000 102400  8192 S  10.0  5.0   1:23.45 mysqld
""")

# 實作簡單的 profiler
class SimpleProfiler:
    """簡單的性能分析器"""
    
    def __init__(self):
        self.timings = {}
    
    def profile(self, func, *args):
        """執行並計時"""
        import time
        start = time.perf_counter()
        
        result = func(*args)
        
        end = time.perf_counter()
        elapsed = end - start
        
        name = func.__name__
        if name not in self.timings:
            self.timings[name] = {'count': 0, 'total': 0}
        
        self.timings[name]['count'] += 1
        self.timings[name]['total'] += elapsed
        
        return result
    
    def report(self):
        """輸出報告"""
        print("\n=== 性能報告 ===")
        print(f"{'函數':<20} {'呼叫次數':>10} {'總時間(s)':>12} {'平均(ms)':>12}")
        print("-" * 56)
        
        for name, data in self.timings.items():
            count = data['count']
            total = data['total']
            avg = total / count * 1000
            print(f"{name:<20} {count:>10} {total:>12.4f} {avg:>12.2f}")

# 測試 profiler
def slow_function():
    time.sleep(0.01)
    return "done"

def fast_function():
    total = 0
    for i in range(10000):
        total += i
    return total

profiler = SimpleProfiler()
for _ in range(10):
    profiler.profile(slow_function)

for _ in range(100):
    profiler.profile(fast_function)

profiler.report()
```