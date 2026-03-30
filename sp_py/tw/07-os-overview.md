# 7. 作業系統的結構

## 7.1 作業系統核心概念

### 7.1.1 作業系統的定義

作業系統（Operating System, OS）是管理電腦硬體資源並提供服務給應用程式的系統軟體。

**作業系統的目標**

| 目標 | 說明 |
|------|------|
| 方便性 | 提供友善的程式執行環境 |
| 效率 | 有效利用硬體資源 |
| 擴展性 | 支援新硬體和功能 |
| 保護 | 隔離並保護程式和資料 |

**作業系統的層次**

```
┌─────────────────────────────────────────────┐
│         應用程式                              │
│  (Word, Browser, Game...)                    │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│         系統呼叫介面                         │
│  (read, write, fork, exec...)              │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│         作業系統核心                          │
│  行程管理、記憶體、檔案系統、網路           │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│         硬體抽象層 (HAL)                    │
│  CPU、記憶體、I/O 裝置                      │
└─────────────────────────────────────────────┘
```

### 7.1.2 核心（Kernel）的概念

核心是作業系統最核心的部分，運行在核心模式（特權模式）。

**核心的特性**

| 特性 | 說明 |
|------|------|
| 常駐記憶體 | 核心始終在記憶體中 |
| 特權執行 | 可執行特殊硬體操作 |
| 保護機制 | 防止應用程式破壞系統 |

**核心的類型**

| 類型 | 說明 | 範例 |
|------|------|------|
| 單核心（Monolithic） | 所有核心功能在同一位址空間 | Linux, FreeBSD |
| 微核心（Microkernel） | 只保留核心功能，其他移到使用者空間 | Minix, QNX |
| 混合核心（Hybrid） | 介於兩者之間 | Windows NT, macOS |

### 7.1.3 系統呼叫（System Call）

系統呼叫是應用程式請求核心服務的介面。

**系統呼叫的類型**

| 類型 | 功能 | 範例 |
|------|------|------|
| 行程控制 | 建立、終止程序 | fork, exec, exit |
| 檔案管理 | 開啟、讀寫、關閉檔案 | open, read, write |
| 記憶體管理 | 配置、釋放記憶體 | mmap, brk |
| 通訊 | 程序間通訊 | pipe, socket, msgget |

```python
class Kernel:
    """簡化的核心模擬"""
    
    def __init__(self):
        self.processes = {}
        self.files = {}
        self.memory = bytearray(1024 * 1024)
        self.system_call_table = {
            1: self.sys_read,
            2: self.sys_write,
            3: self.sys_open,
            4: self.sys_close,
            5: self.sys_exit,
        }
    
    def system_call(self, number, args):
        handler = self.system_call_table.get(number)
        if handler:
            return handler(args)
        return -1
```

### 7.1.4 Shell 的概念

Shell 是使用者與核心之間的命令列介面。

```python
class Shell:
    """簡化的命令列直譯器"""
    
    def __init__(self, kernel):
        self.kernel = kernel
        self.running = True
    
    def execute(self, cmd):
        parts = cmd.strip().split()
        if not parts:
            return
        
        cmd, args = parts[0], parts[1:]
        
        if cmd == 'exit':
            self.running = False
            return
        
        if cmd == 'echo':
            print(' '.join(args))
            return
        
        if cmd == 'ls':
            print('file1.txt  file2.txt  dir/')
            return
```

## 7.2 程序與執行緒

### 7.2.1 程序（Process）的概念

程序是程式的執行個體，是作業系統資源分配的基本單位。

**程序的組成**

```
┌─────────────────────────────────────────────┐
│              程序控制區塊 (PCB)              │
│  - PID、狀態、優先級                        │
│  - 暫存器映像                              │
│  - 記憶體映射                              │
│  - 開啟的檔案                              │
│  - 訊息等                                  │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│              虛擬位址空間                   │
│  ┌─────────────────────────────────────┐  │
│  │           程式碼 (.text)             │  │
│  ├─────────────────────────────────────┤  │
│  │           資料 (.data)              │  │
│  ├─────────────────────────────────────┤  │
│  │           堆疊 (.stack)             │  │
│  └─────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

**PCB（Process Control Block）**

程序控制區塊是核心維護的資料結構，儲存程序的所有狀態資訊。

```python
class PCB:
    """程序控制區塊"""
    def __init__(self, pid, name):
        self.pid = pid
        self.name = name
        self.state = 'NEW'
        self.registers = {}
        self.memory = {}
        self.files = []
        self.parent = None
        self.children = []
        self.priority = 0
```

### 7.2.2 程序狀態與轉換

程序的生命週期中有多種狀態：

```
        ┌──────────────────────┐
        │                      │
        ▼                      │
┌──────────┐              ┌────────────┐
│   NEW    │──建立──→     │   READY    │
└──────────┘              └────────────┘
                               │
                               │排程器調度
                               ▼
                          ┌───────────┐
                          │  RUNNING   │
                          └───────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
        ┌──────────┐    ┌──────────┐    ┌────────────┐
        │  BLOCKED  │    │TERMINATED│    │   READY   │
        │  (等待I/O)│    └──────────┘    └────────────┘
        └──────────┘
```

**程序狀態說明**

| 狀態 | 說明 |
|------|------|
| NEW | 程序正在建立中 |
| READY | 等待 CPU 執行 |
| RUNNING | 正在 CPU 上執行 |
| BLOCKED | 等待 I/O 或事件 |
| TERMINATED | 程序已結束 |

### 7.2.3 執行緒（Thread）的概念

執行緒是 CPU 調度的基本單位，一個程序可含有多個執行緒。

**程序 vs 執行緒**

| 特性 | 程序 | 執行緒 |
|------|------|--------|
| 資源 | 獨立位址空間 | 共享所屬程序的資源 |
| 切換成本 | 較高（需切換位址空間） | 較低（共享資源） |
| 通訊 | 需要 IPC | 直接共享記憶體 |
| 建立速度 | 較慢 | 較快 |

```python
class Thread:
    """執行緒類別"""
    def __init__(self, process, target):
        self.process = process
        self.target = target
        self.thread = threading.Thread(target=target)
```

**多執行緒範例**

```python
import threading
import time

def worker(name, delay):
    for i in range(3):
        print(f"執行緒 {name}: 第 {i+1} 次執行")
        time.sleep(delay)

threads = []
for i in range(3):
    t = threading.Thread(target=worker, args=(f"Worker-{i}", 0.5))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("所有執行緒完成")
```

## 7.3 行程排程

### 7.3.1 排程的基本概念

行程排程（Process Scheduling）決定哪個 READY 程序獲得 CPU。

**排程的層次**

| 層次 | 說明 | 時間尺度 |
|------|------|----------|
| 長程排程 | 決定哪些程式進入系統 | 秒～分鐘 |
| 短程排程 | 決定哪個程序獲得 CPU | 毫秒 |
| 中程排程 | 調整系統負載 | 秒 |

**排程器的目標**

| 目標 | 說明 |
|------|------|
| CPU 利用率 | CPU 忙碌時間比例 |
| 產出量 | 單位時間完成的程序數 |
| 周轉時間 | 程序從提交到完成的總時間 |
| 等待時間 | 程序在 READY 佇列等待的時間 |
| 回應時間 | 從提交到首次回應的時間 |

### 7.3.2 常見排程演算法

**先來先服務（FCFS / FIFO）**

```python
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
```

特點：
- 簡單公平
- 可能導致周轉時間波動大
- 短程序可能等待長程序（Convoy Effect）

**最短工作優先（SJF）**

```python
class SJFScheduler:
    """Shortest Job First"""
    
    def __init__(self):
        self.queue = []
    
    def add_process(self, process):
        heapq.heappush(self.queue, (process.burst_time, process))
    
    def next_process(self):
        if self.queue:
            return heapq.heappop(self.queue)[1]
        return None
```

特點：
- 最小化平均等待時間
- 需要事先知道程式執行時間
- 可能導致長程式飢餓

**時間片輪轉（Round Robin）**

```python
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
```

特點：
- 時間片固定
- 互動式系統適用
- 回應時間可預期

**優先級排程**

```python
class PriorityScheduler:
    """Priority Scheduling"""
    
    def __init__(self):
        self.queue = []
    
    def add_process(self, process):
        heapq.heappush(self.queue, (-process.priority, process))
    
    def next_process(self):
        if self.queue:
            return heapq.heappop(self.queue)[1]
        return None
```

特點：
- 高優先級程式先執行
- 可能導致低優先級程式飢餓
- 可配合老化（Aging）機制

### 7.3.3 多級回饋佇列（MLFQ）

MLFQ 結合多種排程策略，動態調整程式優先級。

**特點**
- 初始優先級較高
- 若使用完整時間片，降低優先級
- 若在時間片內放棄 CPU（I/O），維持或提升優先級

## 7.4 記憶體管理

### 7.4.1 記憶體管理的目標

記憶體管理負責分配和回收記憶體給程式。

**管理的目標**

| 目標 | 說明 |
|------|------|
| 保護 | 防止未授權存取 |
| 共享 | 允許程式共享記憶體 |
| 重定位 | 程式可在不同位址執行 |
| 抽象 | 隱藏硬體細節 |
| 效率 | 有效利用記憶體 |

### 7.4.2 連續記憶體配置

**固定分區**

記憶體劃分為固定大小的分區：

```
┌────────┬────────┬────────────────┬────────┐
│  分區1 │ 分區2  │     分區3      │ 分區4  │
│  64KB  │ 64KB   │     128KB      │ 64KB   │
└────────┴────────┴────────────────┴────────┘
```

問題：
- 內部碎片：分區內部未使用空間
- 外部碎片：分區之間的小空洞

**動態分區**

根據程式需求動態分配：

```
┌──────────────────────────────────────────┐
│  Process A │      │ Process B │         │
│  100KB     │      │   80KB    │         │
├──────────────────────────────────────────┤
│  釋放 Process A 後                        │
├──────────────┬───────────────────────────┤
│   空洞 100KB │ Process B │               │
└──────────────┴───────────┴────────────────┘
```

**配置策略**

| 策略 | 說明 | 優點 | 缺點 |
|------|------|------|------|
| 首次適合 | 使用第一個夠大的空洞 | 簡單快速 | 產生較多碎片 |
| 最佳適合 | 使用最小的夠大空洞 | 減少碎片 | 可能遍歷整個清單 |
| 最差適合 | 使用最大的空洞 | 減少大空洞產生 | 可能讓小程式無處可放 |

### 7.4.3 分頁（Paging）

分頁將虛擬記憶體和實體記憶體劃分為固定大小的頁面。

**分頁的優點**

| 優點 | 說明 |
|------|------|
| 無外部碎片 | 頁面可散布在任意實體頁框 |
| 記憶體共享 | 程式可共享同一頁框 |
| 簡化配置 | 頁面大小固定 |

**虛擬位址轉換**

```
虛擬位址 (32 位元)              實體位址
┌─────────────────┐             ┌─────────────────┐
│ 頁號 (20位) │ 偏移(12位) │   │ 頁框號 │  偏移   │
└─────────────────┘             └─────────────────┘
         │                              ▲
         ▼                              │
┌─────────────────┐                      │
│    分頁表查詢    │                      │
│ VPN → PFN      │                      │
└─────────────────┘                      │
         │                              │
         ▼                              │
    頁框號 ────────────────────────────┘
```

```python
class PageTable:
    """分頁表"""
    
    def __init__(self, page_size=4096):
        self.page_size = page_size
        self.pages = {}
    
    def translate(self, virtual_addr):
        vpn = virtual_addr // self.page_size
        offset = virtual_addr % self.page_size
        
        if vpn in self.pages:
            pfn = self.pages[vpn]
            return pfn * self.page_size + offset
        else:
            raise PageFault(f"虛擬頁 {vpn} 未映射")
```

### 7.4.4 區段（Segmentation）

區段將程式劃分為邏輯上相關的區塊：程式碼、資料、堆疊等。

**區段表**

```
┌────────────┬────────┬──────────────┐
│ 基址      │ 界限   │ 保護位元     │
├────────────┼────────┼──────────────┤
│ 程式碼    │ 0      │ 4096         │ R/X │
│ 資料      │ 4096   │ 2048         │ R/W │
│ 堆疊      │ 8192   │ 4096         │ R/W │
└────────────┴────────┴──────────────┘
```

### 7.4.5 虛擬記憶體

虛擬記憶體讓程式使用比實體記憶體更大的位址空間。

**分頁置換演算法**

| 演算法 | 說明 |
|--------|------|
| FIFO | 移除最舊的頁面 |
| LRU | 移除最久未使用的頁面 |
| LFU | 移除使用次數最少的頁面 |
| 隨機 | 隨機選擇移除頁面 |

```python
class VirtualMemory:
    """虛擬記憶體系統"""
    
    def __init__(self, num_frames):
        self.frames = [None] * num_frames
        self.page_table = {}
        self.page_faults = 0
    
    def access(self, page):
        if page in self.page_table:
            return self.page_table[page]
        else:
            self.page_faults += 1
            return self.load_page(page)
    
    def load_page(self, page):
        free_frame = None
        for i, frame in enumerate(self.frames):
            if frame is None:
                free_frame = i
                break
        
        if free_frame is None:
            free_frame = self.lru_replace(page)
        
        self.frames[free_frame] = page
        self.page_table[page] = free_frame
        return free_frame
    
    def hit_rate(self, total_access):
        return (total_access - self.page_faults) / total_access
```

## 7.5 檔案系統

### 7.5.1 檔案系統的抽象

檔案系統將位元組序列組織為具名的檔案，提供持久儲存。

**檔案系統的目標**

| 目標 | 說明 |
|------|------|
| 方便性 | 提供直觀的檔案抽象 |
| 效率 | 快速存取檔案 |
| 安全性 | 保護檔案免受未授權存取 |
| 可靠性 | 防止資料遺失 |

### 7.5.2 檔案系統的結構

**i-node 結構**

每個檔案有一個 i-node（索引節點）儲存元資料：

```python
class Inode:
    def __init__(self, inumber):
        self.inumber = inumber
        self.type = 'file'
        self.size = 0
        self.blocks = []
        self.permissions = 0o644
        self.links = 1
```

**目錄結構**

目錄將檔案名稱映射到 i-node：

```
目錄檔案內容：
┌────────┬────────────┐
│ "."   │ → 此目錄的 inode │
│ ".."  │ → 父目錄的 inode │
│ "a.txt"│ → a.txt 的 inode │
│ "b.dat"│ → b.dat 的 inode │
└────────┴────────────┘
```

### 7.5.3 常見檔案系統

| 檔案系統 | 平台 | 特點 |
|----------|------|------|
| ext4 | Linux | 預設 Linux 檔案系統，日誌支援 |
| NTFS | Windows | Windows 預設，壓縮、加密 |
| APFS | macOS | Apple 預設，副本寫入、加密 |
| FAT32 | 通用 | 簡單相容，4GB 檔案限制 |
| Btrfs | Linux | 快照、檢查碼、線上壓縮 |

### 7.5.4 FAT32 檔案系統

FAT（File Allocation Table）使用表格追蹤叢集使用情況：

```python
class FAT32:
    """簡化的 FAT32 檔案系統"""
    
    def __init__(self, size):
        self.fat = [0] * (size // 512)
        self.root_dir = {}
    
    def allocate_cluster(self):
        for i, entry in enumerate(self.fat):
            if entry == 0:
                self.fat[i] = 0xFFFFFFFF
                return i
        return -1
    
    def write_file(self, filename, data):
        clusters_needed = (len(data) + 511) // 512
        chain = []
        
        for _ in range(clusters_needed):
            cluster = self.allocate_cluster()
            if cluster == -1:
                break
            chain.append(cluster)
        
        self.root_dir[filename] = {'chain': chain, 'size': len(data)}
        print(f"檔案 {filename} 使用叢集: {chain}")
```

### 7.5.5 檔案系統操作

```python
import os

def file_operations():
    os.makedirs('test_dir/sub_dir', exist_ok=True)
    
    with open('test_dir/file.txt', 'w') as f:
        f.write('Hello, File System!')
    
    with open('test_dir/file.txt', 'r') as f:
        content = f.read()
        print(content)
    
    print(os.listdir('test_dir'))
    
    stat = os.stat('test_dir/file.txt')
    print(f"大小: {stat.st_size}, 修改時間: {stat.st_mtime}")
    
    os.remove('test_dir/file.txt')
    os.rmdir('test_dir/sub_dir')
    os.rmdir('test_dir')
```
