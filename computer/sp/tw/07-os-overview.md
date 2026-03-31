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

[_code/07/07_01_kernel.c](_code/07/07_01_kernel.c)

```c
#include <stdio.h>
#include <string.h>

typedef struct {
    int pid;
    char name[32];
    char state[16];
} Process;

int main() {
    Process p1 = {1, "init", "RUNNING"};
    Process p2 = {2, "shell", "READY"};
    
    printf("Process 1: PID=%d, Name=%s, State=%s\n", p1.pid, p1.name, p1.state);
    printf("Process 2: PID=%d, Name=%s, State=%s\n", p2.pid, p2.name, p2.state);
    
    return 0;
}
```

### 7.1.4 Shell 的概念

Shell 是使用者與核心之間的命令列介面。

[_code/07/07_02_shell.c](_code/07/07_02_shell.c)

```c
#include <stdio.h>
#include <string.h>

int main() {
    printf("Simple Shell\n");
    printf("Commands: echo, ls, exit\n");
    
    char cmd[128];
    while (1) {
        printf("$ ");
        if (fgets(cmd, sizeof(cmd), stdin) != NULL) {
            cmd[strcspn(cmd, "\n")] = 0;
            if (strcmp(cmd, "exit") == 0) break;
            if (strcmp(cmd, "ls") == 0) printf("file1.txt  file2.txt\n");
            else if (strcmp(cmd, "echo hello") == 0) printf("hello\n");
            else if (strlen(cmd) > 0) printf("Unknown command\n");
        }
    }
    
    return 0;
}
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

[_code/07/07_03_pcb.c](_code/07/07_03_pcb.c)

```c
#include <stdio.h>
#include <string.h>

typedef struct {
    int pid;
    char name[32];
    char state[16];
    int priority;
} PCB;

int main() {
    PCB pcb = {1, "main", "NEW", 0};
    printf("PCB: PID=%d, Name=%s, State=%s, Priority=%d\n", 
           pcb.pid, pcb.name, pcb.state, pcb.priority);
    return 0;
}
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

[_code/07/07_08_thread_implementation.c](_code/07/07_08_thread_implementation.c)

```c
#include <stdio.h>

typedef struct {
    int tid;
    char name[32];
    pthread_t handle;
    void* stack;
} Thread;

int main() {
    printf("=== Thread Implementation ===\n\n");
    
    printf("Thread structure:\n");
    printf("  typedef struct {\n");
    printf("      int tid;           // Thread ID\n");
    printf("      char name[32];    // Thread name\n");
    printf("      pthread_t handle;  // POSIX thread handle\n");
    printf("      void* stack;      // Stack pointer\n");
    printf("  } Thread;\n\n");
    
    printf("Process vs Thread:\n");
    printf("+------------------+------------------+\n");
    printf("|     Process       |     Thread       |\n");
    printf("+------------------+------------------+\n");
    printf("| Separate address  | Shared address   |\n");
    printf("| space             | space            |\n");
    printf("| Higher overhead   | Lower overhead   |\n");
    printf("| IPC required      | Direct sharing   |\n");
    printf("+------------------+------------------+\n");
    
    return 0;
}
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

[_code/07/07_04_fcfs_scheduler.c](_code/07/07_04_fcfs_scheduler.c)

```c
#include <stdio.h>

typedef struct { int pid; char name[16]; int burst; } Process;

Process queue[10];
int front = 0, rear = 0;

void enqueue(Process p) { queue[rear++] = p; }
Process* dequeue() { return (front < rear) ? &queue[front++] : NULL; }

int main() {
    enqueue((Process){1, "P1", 10});
    enqueue((Process){2, "P2", 5});
    
    Process *p = dequeue();
    printf("FCFS: Running %s (burst %d)\n", p->name, p->burst);
    
    p = dequeue();
    printf("FCFS: Running %s (burst %d)\n", p->name, p->burst);
    
    return 0;
}
```

特點：
- 簡單公平
- 可能導致周轉時間波動大
- 短程序可能等待長程序（Convoy Effect）

**最短工作優先（SJF）**

[_code/07/07_09_sjf_scheduler.c](_code/07/07_09_sjf_scheduler.c)

```c
#include <stdio.h>

typedef struct {
    int pid;
    char name[16];
    int burst_time;
} Process;

int main() {
    printf("=== SJF Scheduler ===\n\n");
    
    Process procs[] = {
        {1, "P1", 10},
        {2, "P2", 5},
        {3, "P3", 8},
        {4, "P4", 3}
    };
    
    printf("Scheduling order (shortest first):\n");
    printf("  P4 (3) -> P2 (5) -> P3 (8) -> P1 (10)\n\n");
    
    printf("Properties:\n");
    printf("  + Minimizes average waiting time\n");
    printf("  - Requires knowing burst time\n");
    printf("  - Long jobs may starve\n");
    
    return 0;
}
```

**時間片輪轉（Round Robin）**

[_code/07/07_05_priority_scheduler.c](_code/07/07_05_priority_scheduler.c)

```c
#include <stdio.h>

int main() {
    printf("Round Robin Scheduler:\n");
    printf("1. Each process gets a time quantum\n");
    printf("2. If quantum expires, process goes to back of queue\n");
    printf("3. Fair scheduling, good for interactive systems\n");
    return 0;
}
```

特點：
- 時間片固定
- 互動式系統適用
- 回應時間可預期

**優先級排程**

[_code/07/07_05_priority_scheduler.c](_code/07/07_05_priority_scheduler.c)

```c
#include <stdio.h>

int main() {
    printf("Priority Scheduler:\n");
    printf("Processes added with priorities (lower = higher priority)\n");
    printf("Always schedules highest priority ready process\n");
    printf("May cause starvation of low priority processes\n");
    return 0;
}
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

[_code/07/07_06_page_table.c](_code/07/07_06_page_table.c)

```c
#include <stdio.h>

#define PAGE_SIZE 4096

int translate(int vpn, int frame) {
    return frame * PAGE_SIZE;
}

int main() {
    int vpn = 10;
    int frame = 5;
    int offset = 100;
    
    int virt = vpn * PAGE_SIZE + offset;
    int phys = translate(vpn, frame) + offset;
    
    printf("Virtual: 0x%x -> Physical: 0x%x\n", virt, phys);
    return 0;
}
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

[_code/07/07_07_virtual_memory.c](_code/07/07_07_virtual_memory.c)

```c
#include <stdio.h>

int frames[16] = {0};

int access_page(int page) {
    if (frames[page]) return page;
    
    for (int i = 0; i < 16; i++) {
        if (!frames[i]) {
            frames[i] = page + 1;
            return i;
        }
    }
    return -1;
}

int main() {
    printf("Accessing pages: 1, 2, 1, 3\n");
    int f1 = access_page(1);
    int f2 = access_page(2);
    int f3 = access_page(1);
    int f4 = access_page(3);
    
    printf("Page faults: %d\n", (f1>=0)+(f2>=0)+(f3>=0)+(f4>=0));
    return 0;
}
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

[_code/07/07_10_inode.c](_code/07/07_10_inode.c)

```c
#include <stdio.h>

typedef struct {
    int inumber;
    char type;
    int size;
    int blocks[15];
    short permissions;
    int links;
} Inode;

int main() {
    printf("=== i-node Structure ===\n\n");
    
    printf("Inode structure:\n");
    printf("  int inumber;           // Inode number\n");
    printf("  char type;             // File type\n");
    printf("  int size;              // Size in bytes\n");
    printf("  int blocks[15];       // Direct block pointers\n");
    printf("  short permissions;     // Access permissions\n");
    printf("  int links;             // Hard link count\n\n");
    
    printf("Directory structure:\n");
    printf("  +--------+--------------------+\n");
    printf("  | Name   | i-node pointer     |\n");
    printf("  +--------+--------------------+\n");
    printf("  | \".\"    | -> This directory  |\n");
    printf("  | \"..\"   | -> Parent directory|\n");
    printf("  +--------+--------------------+\n");
    
    return 0;
}
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

[_code/07/07_11_fat32.c](_code/07/07_11_fat32.c)

```c
#include <stdio.h>

#define FAT_FREE 0
#define FAT_EOF 0xFFFFFFFF

typedef struct {
    unsigned int* fat;
    int fat_size;
} FAT;

int main() {
    printf("=== FAT32 File System ===\n\n");
    
    printf("FAT structure:\n");
    printf("  Each entry = 32 bits (4 bytes)\n");
    printf("  FAT[0] = Reserved\n");
    printf("  FAT[1] = Reserved\n");
    printf("  FAT[2..n] = Cluster status\n\n");
    
    printf("Cluster values:\n");
    printf("  0x00000000 = Free cluster\n");
    printf("  0xFFFFFFFF = EOF marker\n");
    printf("  0x0000000x = Next cluster in chain\n\n");
    
    printf("Example: File with 3 clusters\n");
    printf("  Cluster chain: 5 -> 12 -> 23 -> EOF\n");
    printf("  FAT[5] = 12\n");
    printf("  FAT[12] = 23\n");
    printf("  FAT[23] = 0xFFFFFFFF\n");
    
    return 0;
}
```

### 7.5.5 檔案系統操作

[_code/07/07_12_file_operations.c](_code/07/07_12_file_operations.c)

```c
#include <stdio.h>
#include <sys/stat.h>
#include <unistd.h>

int main() {
    printf("=== File System Operations ===\n\n");
    
    printf("Common POSIX operations:\n");
    printf("  mkdir(\"dir\", 0755);     // Create directory\n");
    printf("  rmdir(\"dir\");           // Remove directory\n");
    printf("  fopen(\"file\", \"r\");   // Open file\n");
    printf("  stat(\"file\", &st);     // Get metadata\n");
    printf("  unlink(\"file\");         // Remove file\n\n");
    
    printf("Example in C:\n");
    printf("  FILE* f = fopen(\"test.txt\", \"w\");\n");
    printf("  fputs(\"Hello\", f);\n");
    printf("  fclose(f);\n\n");
    
    printf("struct stat fields:\n");
    printf("  st_size  - File size\n");
    printf("  st_mtime - Modification time\n");
    printf("  st_uid   - Owner UID\n");
    printf("  st_gid   - Owner GID\n");
    
    return 0;
}
```
