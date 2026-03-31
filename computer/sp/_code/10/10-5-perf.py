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
