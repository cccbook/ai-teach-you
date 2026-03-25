# 10. Linux 作業系統與系統程式

Linux 是目前全球最廣泛使用的伺服器作業系統，同時也是超級電腦、嵌入式系統、雲端運算和行動裝置（透過 Android）的核心。Linux 的設計結合了傳統 Unix 的設計哲學和現代系統的需求，提供了一個穩定、高效且高度可定制的作業系統平台。本章將深入探討 Linux 核心的架構設計、系統呼叫機制、程序管理、程序間通訊、網路程式設計等核心主題，幫助讀者建立對 Linux 系統程式設計的全面理解。

## 10.1 Linux 核心架構

### 10.1.1 Linux 核心的設計哲學

Linux 核心是由 Linus Torvalds 於 1991 年發起的開源專案，經過三十多年的發展，已成為世界上最成功的自由軟體專案之一。Linux 的設計哲學深受 Unix 傳統影響，強調簡潔、模組化、以及「一切皆檔案」的抽象概念。

Linux 採用**單核心**（Monolithic Kernel）架構，這意味著作業系統的核心服務——包括行程排程、記憶體管理、檔案系統、網路堆疊、裝置驅動等——都運行在同一個位址空間中。與微核心設計相比，單核心設計的優勢在於核心空間的函式呼叫沒有程序間通訊的開銷，效能較高，且核心各子系統可以共享資料結構和緩衝區。

然而，單核心設計也有其缺點：核心錯誤可能導致整個系統崩潰，且修改任何核心元件通常需要重新編譯整個核心。Linux 透過**核心模組**（Kernel Module）機制來解決這些問題，使得大多數裝置驅動程式、檔案系統和網路協定可以在核心執行時動態載入和卸載，而無需重開機或重新編譯核心。

**單核心 vs 微核心的深入比較**

```
┌─────────────────────────────────────────────────────────────┐
│                        單核心架構                            │
│  ┌─────────────────────────────────────────────────────┐  │
│  │                  核心空間                           │  │
│  │  程序管理 │ 記憶體管理 │ 檔案系統 │ 網路 │ 驅動    │  │
│  └─────────────────────────────────────────────────────┘  │
│  優點：高效能、簡單  缺點：修改需重新編譯                  │
├─────────────────────────────────────────────────────────────┤
│                        微核心架構                            │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐            │
│  │  排程 │ │  IPC │ │  記憶 │ │  驅動 │ │ 檔案 │            │
│  │      │ │      │ │  管理 │ │      │ │ 系統 │            │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘            │
│          ↑                    ↑                    ↑      │
│      使用者空間服務行程（檔案系統、網路等）                │
│  優點：模組化、穩定性  缺點：IPC 開銷較大                  │
└─────────────────────────────────────────────────────────────┘
```

微核心設計將更多功能移到使用者空間，核心只保留最基本的功能（排程、基本 IPC、記憶體映射）。這種設計的理論優點是更好的穩定性和可擴展性——某個服務的失敗不會影響整個系統，可以單獨重啟該服務。然而，微核心的缺點是頻繁的 IPC 呼叫會帶來顯著的性能開銷。例如，Minix（微核心作業系統的典型代表）的設計者 Andrew Tanenbaum 後來也承認，微核心在實際應用中的效能劣勢是其主要缺點。

Linux 的單核心設計做出了務實的選擇：將大多數服務實作在核心空間，以獲得最佳效能，同時透過可載入模組提供擴展性。這種設計通常被稱為「模組化的單核心」，既保持了單核心的效率，又提供了類似微核心的彈性。

### 10.1.2 Linux 核心子系統

Linux 核心由多個相互協作的子系統構成，每個子系統負責特定的功能領域。

```
┌─────────────────────────────────────────────┐
│              系統呼叫介面                      │
├─────────────────────────────────────────────┤
│              程序排程子系統                    │
│              記憶體管理子系統                  │
│              虛擬檔案系統 (VFS)              │
│              網路堆疊                        │
│              程序間通訊 (IPC)                │
│              裝置驅動程式                     │
└─────────────────────────────────────────────┘
```

**程序排程子系統**（Process Scheduler）是 Linux 核心最核心的子系統之一，負責決定在任意時刻哪個行程或執行緒應該獲得 CPU 的使用權。Linux 的排程器經過多年演進，從最初的 O(1) 排程器，到 CFS（Completely Fair Scheduler，完全公平排程器），再到現在的多執行緒排程支援。Linux 的排程器設計目標是提供公平性、響應性和吞吐量之間的平衡。

**記憶體管理子系統**（Memory Manager）負責管理系統的虛擬記憶體和實體記憶體。它維護核心和所有行程的虛擬位址空間，翻譯虛擬位址到實體位址，管理分頁置換，並實現記憶體保護和共享機制。Linux 的記憶體管理採用了分頁式管理，支援 4KB、2MB、1GB 等多種分頁大小。

**虛擬檔案系統**（Virtual File System, VFS）是 Linux 檔案系統架構的核心。VFS 定義了一套統一的介面，使得多種不同的檔案系統（如 ext4、XFS、Btrfs、FAT、NTFS 等）可以在 Linux 中共存。應用程式透過 VFS 介面操作檔案，無需關心底層具體使用哪種檔案系統。

**網路堆疊**（Network Stack）實作了 TCP/IP 協定族的各層。從實體層的網路驅動，到鏈路層的 Ethernet 框架處理，到網路層的 IP 路由，再到傳輸層的 TCP/UDP，再到應用層的各種網路服務，Linux 提供了完整且高度可配置的网络功能。

**程序間通訊子系統**（IPC）提供了多種程序間通訊機制，包括管道、訊號、共享記憶體、訊息佇列、訊號燈等。這些機制允許獨立的行程相互交換資料和同步操作。

**裝置驅動程式子系統**統一管理各類硬體裝置。Linux 將裝置分為字元裝置、區塊裝置和網路裝置三大類，每類都有對應的驅動程式介面和框架。統一的驅動程式模型簡化了新硬體的支援添加。

### 10.1.3 Linux 核心模組

核心模組是 Linux 提供的一種擴展核心功能的機制，允許在系統執行時動態載入和卸載程式碼，而無需重新編譯核心或重開機。這種設計使得：

- 裝置驅動程式可以在需要的時候載入，不需要時卸載
- 新的檔案系統支援可以按需添加
- 網路協定可以在執行時啟用或停用
- 核心除錯更加方便，可以載入偵錯模組

核心模組的開發與使用者空間程式有顯著不同。模組運行在核心空間，具有最高權限，但任何錯誤都可能導致系統崩潰。以下是一個完整的最簡核心模組範例：

```c
// 最簡 Linux 核心模組
#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Example");
MODULE_DESCRIPTION("A Simple Hello World Module");
MODULE_VERSION("1.0");

static int __init hello_init(void) {
    printk(KERN_INFO "Hello Kernel Module\n");
    printk(KERN_DEBUG "Module loaded at address: %px\n", hello_init);
    return 0;
}

static void __exit hello_exit(void) {
    printk(KERN_INFO "Goodbye Kernel Module\n");
}

module_init(hello_init);
module_exit(hello_exit);
```

模組的編譯需要核心標頭檔和 Makefile：

```makefile
obj-m += hello.o

KDIR ?= /lib/modules/$(shell uname -r)/build

all:
    $(MAKE) -C $(KDIR) M=$(PWD) modules

clean:
    $(MAKE) -C $(KDIR) M=$(PWD) clean
```

核心模組與核心通訊的主要方式是透過 `/proc` 和 `/sys` 檔案系統，以及設備節點。`printk()` 是核心空間的輸出函式，輸出會寫入核心環形緩衝區，可通過 `dmesg` 命令查看。

**模組依賴管理**

複雜的模組通常依賴其他模組提供的符號。例如，一個網卡驅動程式可能依賴核心的記憶體分配和網路堆疊介面。Linux 核心維護一個模組依賴圖，透過 `modprobe` 載入模組時會自動解析並載入所需的依賴模組。`lsmod` 命令顯示目前已載入的模組，`modinfo` 顯示模組的詳細資訊。

## 10.2 System Call 與 API

### 10.2.1 系統呼叫的機制

系統呼叫是使用者空間程式與核心通訊的正式介面。當應用程式需要核心提供的服務——如讀寫檔案、建立行程、配置網路等——時，它透過系統呼叫向核心發出請求。系統呼叫提供了受保護的、有定義的進入核心的通道，防止應用程式直接存取硬體或破壞系統穩定性。

**x86-64 系統呼叫約定**

在 x86-64 架構上，Linux 使用 `syscall` 指令觸發系統呼叫。這是一種比傳統的 `int 0x80` 中斷機制更高效的途徑。`syscall` 指令的設計专门针对快速系統呼叫，减少了上下文切換的開銷。

| 暫存器 | 用途 | 說明 |
|--------|------|------|
| rax | 系統呼叫號/返回值 | 輸入時攜帶系統呼叫號；輸出時攜帶返回值 |
| rdi | 第一個參數 | 指向第一個參數 |
| rsi | 第二個參數 | 指向第二個參數 |
| rdx | 第三個參數 | 指向第三個參數 |
| r10 | 第四個參數 | 用於替代 rcx（因為 syscall 會覆蓋 rcx） |
| r8 | 第五個參數 | 指向第五個參數 |
| r9 | 第六個參數 | 指向第六個參數 |

當 CPU 執行 `syscall` 指令時：

1. 儲存當前指令指標 (rip) 到 rcx
2. 儲存目前的 RFLAGS 到 r11
3. 載入新的指令指標到 RIP（從 IA32_LSTAR MSR 讀取）
4. 載入新的堆疊指標到 RSP（從 IA32_STAR MSR 讀取）
5. 切換到核心模式（CPL = 0）

核心的系統呼叫分派表（syscall table）根據 rax 中的系統呼叫號跳轉到對應的處理函式。處理完成後，結果返回到 rax，CPU 執行 `sysret` 指令返回使用者模式。

**從 API 到系統呼叫的層級**

```
┌───────────────────────────────────────┐
│        應用程式                        │
│   printf("Hello");                    │
└──────────────┬────────────────────────┘
               │ 函式呼叫
               ▼
┌───────────────────────────────────────┐
│        glibc (GNU C Library)          │
│   write() 包裝函式                    │
│   → 將參數載入暫存器                  │
│   → 執行 syscall 指令                 │
└──────────────┬────────────────────────┘
               │ 系統呼叫
               ▼
┌───────────────────────────────────────┐
│        Linux 核心                      │
│   sys_write() 處理函式                │
│   → 驗證參數                          │
│   → 呼叫 VFS 層                       │
│   → 返回結果                          │
└───────────────────────────────────────┘
```

### 10.2.2 常見系統呼叫

Linux 定義了數百個系統呼叫，以下是一些最常用的分類：

**檔案操作系統呼叫**

```c
#include <unistd.h>
#include <sys/syscall.h>

int main() {
    // 使用 glibc 包裝函式
    const char *msg = "Hello!\n";
    write(STDOUT_FILENO, msg, 7);
    
    // 直接使用 syscall（用於底層控制或系統程式設計教學）
    syscall(SYS_write, STDOUT_FILENO, msg, 7);
    
    // 讀取系統呼叫
    char buf[100];
    ssize_t n = read(STDIN_FILENO, buf, 100);
    
    // 取得程序 ID
    pid_t pid = getpid();
    
    return 0;
}
```

**行程控制系統呼叫**

| 系統呼叫 | 功能 |
|---------|------|
| clone() | 建立新行程/執行緒（POSIX thread 的基礎） |
| execve() | 以新程式替換當前行程 |
| exit() | 終止當前行程 |
| wait4() | 等待行程狀態改變 |
| getpid() | 取得行程 ID |
| getppid() | 取得父行程 ID |
| getuid() | 取得使用者 ID |
| geteuid() | 取得有效使用者 ID |

**記憶體管理系統呼叫**

| 系統呼叫 | 功能 |
|---------|------|
| mmap() | 映射檔案或裝置到記憶體 |
| munmap() | 解除記憶體映射 |
| mprotect() | 設定記憶體區域的保護屬性 |
| brk()/sbrk() | 改變資料段大小 |
| madvise() | 向核心提供記憶體使用建議 |

**時間相關系統呼叫**

| 系統呼叫 | 功能 |
|---------|------|
| gettimeofday() | 取得目前時間 |
| clock_gettime() | 取得指定時鐘的時間 |
| nanosleep() | 高精度睡眠 |
| alarm() | 設定鬧鐘 |

### 10.2.3 API 與系統呼叫的關係

理解 API 與系統呼叫的區別是系統程式設計的基礎。API（應用程式介面）是應用程式使用的函式介面，而系統呼叫是進入核心的實際機制。

| 層次 | 說明 | 範例 |
|------|------|------|
| 應用程式 | 使用者程式碼呼叫 | `printf("Hello")` |
| glibc 函式庫 | C 標準庫包裝 | `fwrite()` → 緩衝 → `write()` |
| 系統呼叫介面 | 核心標頭定義 | `syscall(SYS_write, ...)` |
| 核心 | 實際處理 | `sys_write()` |

值得注意的是：

1. **並非所有 API 都對應系統呼叫**：例如 `strcpy()`、`malloc()`、`printf()` 等純記憶體操作的函式完全在函式庫中實現，不需要系統呼叫。

2. **一個 API 可能觸發多個系統呼叫**：例如 `printf()` 可能觸發多次 `write()` 系統呼叫（視緩衝區情況）。

3. **某些系統呼叫沒有對應的 glibc 包裝**：如 `perf_event_open()`、`setns()` 等新系統呼叫，需要直接使用 `syscall()`。

## 10.3 程序管理與 IPC

### 10.3.1 程序生命週期

在 Linux 中，每個程式執行個體都是一個行程（process）。行程是資源分配的基本單位——每個行程有自己的虛擬位址空間、檔案描述符、執行緒表、訊號處理器等。

**建立程序：fork()**

`fork()` 是 Unix 系統建立新行程的傳統方式。它的行為比較特殊：在父行程中返回子行程的 PID，在子行程中返回 0；如果失敗則返回 -1。

```c
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    pid_t pid = fork();
    
    if (pid < 0) {
        perror("fork failed");
        return 1;
    }
    
    if (pid == 0) {
        // 子行程
        printf("Child: PID = %d, Parent PID = %d\n", 
               getpid(), getppid());
        execlp("ls", "ls", "-l", NULL);
        perror("execlp failed");
        _exit(127);
    } else {
        // 父行程
        int status;
        waitpid(pid, &status, 0);
        printf("Child %d exited with status %d\n", 
               pid, WEXITSTATUS(status));
    }
    
    return 0;
}
```

Linux 的 `fork()` 採用了**寫時拷貝**（Copy-on-Write, COW）策略。在 `fork()` 時，父子行程共享同一份記憶體分頁，只有當任一方嘗試寫入某個分頁時，核心才會為該分頁建立一份拷貝。這使得 `fork()` 操作極為高效，特別適合現代的工作負載。對於需要完整拷貝記憶體的情況（如 `fork()` 後立即 `exec()`），Linux 還優化了分頁共享。

**執行新程式：exec() 系列**

`fork()` 只複製當前程式。要執行一個全新的程式，需要在 fork 之後呼叫 `exec()` 系列函式之一。`execve()` 是實際的系統呼叫，其他變體（`execl()`、`execvp()`、`execle()` 等）都是對它的包裝。

| exec 變體 | 參數格式 | 是否搜尋 PATH |
|-----------|---------|--------------|
| execl() | 可變參數列表 | 否 |
| execv() | 指標陣列 | 否 |
| execlp() | 可變參數列表 | 是 |
| execvp() | 指標陣列 | 是 |
| execle() | 可變參數列表 + 環境 | 否 |

### 10.3.2 執行緒

執行緒是 CPU 排程的基本單位。在同一行程中的執行緒共享虛擬位址空間、全域變數、檔案描述符等資源，但每個執行緒有自己的暫存器狀態和堆疊。

Linux 的執行緒實作有兩種歷史：

1. **LinuxThreads**：早期使用程序模擬執行緒，現在已廢棄
2. **NPTL**（Native POSIX Threads Library）：現在的標準，使用 `clone()` 系統呼叫和 `CLONE_THREAD` 旗標建立真正的執行緒

```c
#include <pthread.h>
#include <stdio.h>
#include <unistd.h>

void* thread_func(void* arg) {
    int id = *(int*)arg;
    printf("Thread %d starting\n", id);
    sleep(1);
    printf("Thread %d finishing\n", id);
    return NULL;
}

int main() {
    pthread_t threads[3];
    int ids[3] = {1, 2, 3};
    
    // 建立執行緒
    for (int i = 0; i < 3; i++) {
        pthread_create(&threads[i], NULL, thread_func, &ids[i]);
    }
    
    // 等待執行緒結束
    for (int i = 0; i < 3; i++) {
        pthread_join(threads[i], NULL);
    }
    
    printf("All threads finished\n");
    return 0;
}
```

**編譯執行緒程式**：`gcc -pthread program.c -o program`

### 10.3.3 管道（Pipe）

管道是 Unix 系統中最基本的程序間通訊機制，提供單向位元組流。管道有兩端：一端用於寫入，一端用於讀取。

**匿名管道**

匿名管道用於有親屬關係的行程（父子、兄弟）之間通訊：

```c
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    int pipefd[2];
    pipe(pipefd);  // 建立管道：[0] 讀端, [1] 寫端
    
    pid_t pid = fork();
    
    if (pid == 0) {
        // 子行程：讀取管道
        close(pipefd[1]);  // 關閉不需要的寫端
        
        char buf[256];
        ssize_t n = read(pipefd[0], buf, sizeof(buf));
        printf("Child received: %.*s\n", (int)n, buf);
        
        close(pipefd[0]);
    } else {
        // 父行程：寫入管道
        close(pipefd[0]);  // 關閉不需要的讀端
        
        const char *msg = "Hello from parent!";
        write(pipefd[1], msg, strlen(msg));
        
        close(pipefd[1]);
        wait(NULL);
    }
    
    return 0;
}
```

**命名管道（FIFO）**

命名管道是一種特殊檔案，允許無親屬關係的行程之間通訊：

```bash
mkfifo /tmp/myfifo

# 終端 1：讀取
cat < /tmp/myfifo

# 終端 2：寫入
echo "Hello" > /tmp/myfifo
```

### 10.3.4 訊號量（Semaphore）

訊號量是一種用於程序同步和互斥的計數器。Linux 支援兩種訊號量：

1. **System V 訊號量**：較老，功能強大但複雜
2. **POSIX 訊號量**：較簡潔，現在更推薦使用

```c
#include <semaphore.h>
#include <pthread.h>
#include <stdio.h>
#include <unistd.h>

sem_t sem;

void* worker(void* arg) {
    int id = *(int*)arg;
    
    sem_wait(&sem);  // P 操作：遞減計數，若為零則阻塞
    printf("Thread %d entered critical section\n", id);
    sleep(1);
    printf("Thread %d leaving critical section\n", id);
    sem_post(&sem);  // V 操作：遞增計數
    
    return NULL;
}

int main() {
    sem_init(&sem, 0, 1);  // 初始值為 1，二元訊號量
    
    pthread_t threads[5];
    int ids[5];
    
    for (int i = 0; i < 5; i++) {
        ids[i] = i;
        pthread_create(&threads[i], NULL, worker, &ids[i]);
    }
    
    for (int i = 0; i < 5; i++) {
        pthread_join(threads[i], NULL);
    }
    
    sem_destroy(&sem);
    return 0;
}
```

### 10.3.5 共用記憶體

共用記憶體是最快的程序間通訊方式，因為它不需要核心作為中介——行程可以直接讀寫共享的記憶體區域。

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/shm.h>
#include <sys/ipc.h>
#include <unistd.h>

int main() {
    // 建立共享記憶體區段
    int shm_id = shmget(IPC_PRIVATE, 4096, IPC_CREAT | 0666);
    if (shm_id < 0) {
        perror("shmget failed");
        return 1;
    }
    
    pid_t pid = fork();
    
    if (pid == 0) {
        // 子行程：附加共享記憶體並寫入
        char *shm = (char*)shmat(shm_id, NULL, 0);
        if (shm == (char*)-1) {
            perror("shmat failed");
            return 1;
        }
        
        sprintf(shm, "Written by child at %ld", (long)time(NULL));
        printf("Child wrote: %s\n", shm);
        
        shmdt(shm);  // 脫離共享記憶體
    } else {
        // 父行程：附加共享記憶體並讀取
        sleep(1);  // 等待子行程寫入
        char *shm = (char*)shmat(shm_id, NULL, SHM_RDONLY);
        if (shm == (char*)-1) {
            perror("shmat failed");
            return 1;
        }
        
        printf("Parent read: %s\n", shm);
        
        shmdt(shm);
        wait(NULL);
        
        // 清理共享記憶體
        shmctl(shm_id, IPC_RMID, NULL);
    }
    
    return 0;
}
```

**共享記憶體 + 訊號量同步**

共用記憶體本身不提供同步機制。通常需要搭配訊號量使用，以防止競爭條件：

```c
#include <semaphore.h>

// 共享的訊號量和共享記憶體
sem_t *sem;
int shm_id;
struct {
    sem_t *sem;
    int data;
} *shared;

void setup_shared() {
    key_t key = ftok("/tmp", 'R');
    shm_id = shmget(key, sizeof(*shared), IPC_CREAT | 0666);
    shared = shmat(shm_id, NULL, 0);
    
    key = ftok("/tmp", 'S');
    sem = sem_open("mysem", O_CREAT, 0666, 1);
}
```

### 10.3.6 訊息佇列

訊息佇列允許行程以訊息為單位交換資料，而非位元組流：

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/msg.h>

struct msgbuf {
    long mtype;
    char mtext[100];
};

int main() {
    int msgid = msgget(IPC_PRIVATE, IPC_CREAT | 0666);
    
    if (fork() == 0) {
        // 子行程：發送訊息
        struct msgbuf msg = {.mtype = 1};
        sprintf(msg.mtext, "Hello from child, PID=%d", getpid());
        msgsnd(msgid, &msg, sizeof(msg.mtext), 0);
    } else {
        // 父行程：接收訊息
        struct msgbuf msg;
        msgrcv(msgid, &msg, sizeof(msg.mtext), 1, 0);
        printf("Parent received: %s\n", msg.mtext);
        wait(NULL);
        msgctl(msgid, IPC_RMID, NULL);
    }
    
    return 0;
}
```

### 10.3.7 IPC 機制比較

| 機制 | 方向 | 同步需求 | 適用場景 |
|------|------|----------|----------|
| 管道 | 單向 | 讀取端阻塞直到有資料 | 父子行程間的簡單通訊 |
| FIFO | 單向 | 讀取端阻塞直到有資料 | 無親屬關係行程間的通訊 |
| 訊號量 | 不適用 | 用於同步 | 互斥、資源計數 |
| 共享記憶體 | 雙向 | 需另外同步 | 大量資料的高效共享 |
| 訊息佇列 | 雙向 | 接收端阻塞 | 離散的訊息交換 |
| Socket | 雙向 | 可設為非阻塞 | 網路通訊、跨主機通訊 |

## 10.4 網路堆疊與 Socket 程式設計

### 10.4.1 Socket 程式設計模型

Socket 是網路通訊的基礎抽象。Linux 的 Socket API 源自 Berkeley Unix，是 TCP/IP 網路程式設計的標準介面。

**TCP 伺服器模型**

TCP 是面向連接的可靠傳輸協定。伺服器需要：建立 socket、綁定位址、監聽連線、接受連線、處理客戶端、關閉連線。

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define PORT 8080
#define BUFFER_SIZE 1024

int main() {
    int server_fd, client_fd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_len = sizeof(client_addr);
    char buffer[BUFFER_SIZE];
    
    // 1. 建立 socket
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }
    
    // 2. 設定 socket 選項（重用位址）
    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
    
    // 3. 綁定位址
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(PORT);
    
    if (bind(server_fd, (struct sockaddr*)&server_addr, 
             sizeof(server_addr)) < 0) {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }
    
    // 4. 監聽連線
    if (listen(server_fd, 10) < 0) {
        perror("listen failed");
        exit(EXIT_FAILURE);
    }
    
    printf("Server listening on port %d\n", PORT);
    
    // 5. 接受連線處理迴圈
    while (1) {
        client_fd = accept(server_fd, 
                          (struct sockaddr*)&client_addr, 
                          &client_len);
        if (client_fd < 0) {
            perror("accept failed");
            continue;
        }
        
        printf("Connection from %s:%d\n",
               inet_ntoa(client_addr.sin_addr),
               ntohs(client_addr.sin_port));
        
        // 處理客戶端請求
        ssize_t n = read(client_fd, buffer, BUFFER_SIZE - 1);
        if (n > 0) {
            buffer[n] = '\0';
            printf("Received: %s\n", buffer);
            
            // 回傳響應
            const char *response = "HTTP/1.1 200 OK\r\n"
                                   "Content-Length: 2\r\n"
                                   "\r\n"
                                   "OK";
            write(client_fd, response, strlen(response));
        }
        
        close(client_fd);
    }
    
    close(server_fd);
    return 0;
}
```

**TCP 客戶端模型**

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int main(int argc, char *argv[]) {
    const char *server_ip = "127.0.0.1";
    int port = 8080;
    
    if (argc > 1) server_ip = argv[1];
    if (argc > 2) port = atoi(argv[2]);
    
    // 1. 建立 socket
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        perror("socket failed");
        return 1;
    }
    
    // 2. 連接伺服器
    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    inet_pton(AF_INET, server_ip, &server_addr.sin_addr);
    
    if (connect(sock, (struct sockaddr*)&server_addr, 
                sizeof(server_addr)) < 0) {
        perror("connect failed");
        return 1;
    }
    
    printf("Connected to %s:%d\n", server_ip, port);
    
    // 3. 發送資料
    const char *msg = "Hello, Server!";
    write(sock, msg, strlen(msg));
    
    // 4. 接收回應
    char buffer[1024];
    ssize_t n = read(sock, buffer, sizeof(buffer) - 1);
    if (n > 0) {
        buffer[n] = '\0';
        printf("Server response: %s\n", buffer);
    }
    
    close(sock);
    return 0;
}
```

### 10.4.2 Socket 選項與最佳化

Linux 提供多種 Socket 選項用於調整通訊行為：

| 選項 | 層次 | 說明 |
|------|------|------|
| SO_REUSEADDR | SOL_SOCKET | 允許重用處於 TIME_WAIT 狀態的位址 |
| SO_REUSEPORT | SOL_SOCKET | 允許多個 socket 綁定同一埠口（負載均衡） |
| SO_KEEPALIVE | SOL_SOCKET | 啟用 TCP 保持連線檢測 |
| SO_LINGER | SOL_SOCKET | 控制 close() 的行為 |
| TCP_NODELAY | IPPROTO_TCP | 禁用 Nagle 演算法，降低延遲 |
| TCP_QUICKACK | IPPROTO_TCP | 禁用延遲 ACK |
| SO_RCVBUF | SOL_SOCKET | 設定接收緩衝區大小 |
| SO_SNDBUF | SOL_SOCKET | 設定傳送緩衝區大小 |

**高效能 TCP 設定範例**

```c
void optimize_tcp_socket(int sock) {
    int opt;
    
    // 禁用 Nagle 演算法（低延遲場景）
    opt = 1;
    setsockopt(sock, IPPROTO_TCP, TCP_NODELAY, &opt, sizeof(opt));
    
    // 快速 ACK
    opt = 1;
    setsockopt(sock, IPPROTO_TCP, TCP_QUICKACK, &opt, sizeof(opt));
    
    // 增大緩衝區
    int buf_size = 256 * 1024;  // 256KB
    setsockopt(sock, SOL_SOCKET, SO_RCVBUF, &buf_size, sizeof(buf_size));
    setsockopt(sock, SOL_SOCKET, SO_SNDBUF, &buf_size, sizeof(buf_size));
    
    // 設定保持連線
    opt = 1;
    setsockopt(sock, SOL_SOCKET, SO_KEEPALIVE, &opt, sizeof(opt));
    
    // TCP keepalive 參數
    int keepidle = 60;
    int keepintvl = 10;
    int keepcnt = 3;
    setsockopt(sock, IPPROTO_TCP, TCP_KEEPIDLE, &keepidle, sizeof(keepidle));
    setsockopt(sock, IPPROTO_TCP, TCP_KEEPINTVL, &keepintvl, sizeof(keepintvl));
    setsockopt(sock, IPPROTO_TCP, TCP_KEEPCNT, &keepcnt, sizeof(keepcnt));
}
```

### 10.4.3 UDP 程式設計

UDP 是無連接的不可靠傳輸協定，適用於對延遲敏感或可容忍少量遺失的場景：

```c
// UDP 伺服器
int udp_server() {
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    
    struct sockaddr_in addr = {
        .sin_family = AF_INET,
        .sin_port = htons(9000),
        .sin_addr.s_addr = INADDR_ANY
    };
    
    bind(sock, (struct sockaddr*)&addr, sizeof(addr));
    
    char buffer[1024];
    struct sockaddr_in client_addr;
    socklen_t len = sizeof(client_addr);
    
    // recvfrom 會阻塞直到收到資料
    ssize_t n = recvfrom(sock, buffer, sizeof(buffer), 0,
                        (struct sockaddr*)&client_addr, &len);
    
    printf("Received %zd bytes from %s:%d\n",
           n, inet_ntoa(client_addr.sin_addr),
           ntohs(client_addr.sin_port));
    
    // 回覆客戶端
    sendto(sock, buffer, n, 0, (struct sockaddr*)&client_addr, len);
    
    close(sock);
    return 0;
}
```

### 10.4.4 非阻塞 I/O 與事件驅動

對於需要同時處理大量連線的伺服器，阻塞式 I/O 效率較低。可採用以下策略：

**非阻塞 I/O**

```c
#include <fcntl.h>

int set_nonblocking(int fd) {
    int flags = fcntl(fd, F_GETFL, 0);
    if (flags == -1) return -1;
    return fcntl(fd, F_SETFL, flags | O_NONBLOCK);
}
```

**多路復用：select/poll**

```c
#include <sys/select.h>

void event_loop(int listen_fd) {
    fd_set read_fds, master;
    int max_fd = listen_fd;
    
    FD_ZERO(&master);
    FD_SET(listen_fd, &master);
    
    while (1) {
        read_fds = master;
        int n = select(max_fd + 1, &read_fds, NULL, NULL, NULL);
        
        for (int fd = 0; fd <= max_fd && n > 0; fd++) {
            if (FD_ISSET(fd, &read_fds)) {
                n--;
                
                if (fd == listen_fd) {
                    // 新連線
                    int client = accept(listen_fd, NULL, NULL);
                    set_nonblocking(client);
                    FD_SET(client, &master);
                    if (client > max_fd) max_fd = client;
                } else {
                    // 客戶端資料
                    char buf[1024];
                    ssize_t r = read(fd, buf, sizeof(buf));
                    if (r <= 0) {
                        close(fd);
                        FD_CLR(fd, &master);
                    } else {
                        // 處理資料...
                        write(fd, buf, r);  // echo
                    }
                }
            }
        }
    }
}
```

**epoll（Linux 特有）**

epoll 是 Linux 特有的高效 I/O 事件通知機制，比 select/poll 更適合處理大量檔案描述符：

```c
#include <sys/epoll.h>

#define MAX_EVENTS 1024

void epoll_server() {
    int epfd = epoll_create1(0);
    struct epoll_event ev, events[MAX_EVENTS];
    
    // 監聽 listen socket
    ev.events = EPOLLIN;
    ev.data.fd = listen_fd;
    epoll_ctl(epfd, EPOLL_CTL_ADD, listen_fd, &ev);
    
    while (1) {
        int n = epoll_wait(epfd, events, MAX_EVENTS, -1);
        
        for (int i = 0; i < n; i++) {
            int fd = events[i].data.fd;
            
            if (fd == listen_fd) {
                // 新連線
                int client = accept(listen_fd, NULL, NULL);
                ev.events = EPOLLIN | EPOLLET;  // 邊緣觸發
                ev.data.fd = client;
                epoll_ctl(epfd, EPOLL_CTL_ADD, client, &ev);
            } else {
                // 客戶端資料
                char buf[4096];
                ssize_t r = read(fd, buf, sizeof(buf));
                if (r > 0) {
                    write(fd, buf, r);
                } else {
                    close(fd);
                    epoll_ctl(epfd, EPOLL_CTL_DEL, fd, NULL);
                }
            }
        }
    }
}
```

## 10.5 效能分析工具

### 10.5.1 strace

`strace` 是 Linux 下的系統呼叫追蹤工具，對於理解程式行為和偵錯非常有用：

```bash
# 追蹤特定類型的系統呼叫
strace -e trace=open,read,write,close ls /tmp

# 追蹤網路相關系統呼叫
strace -e trace=network -e write ./program 2>&1 | grep "write(1"

# 顯示時間戳
strace -t ls

# 顯示相對時間
strace -r ls

# 統計每種系統呼叫的次數和耗時
strace -c ./program
```

`strace` 的輸出範例：

```
open(".", O_RDONLY|O_DIRECTORY) = 3
getdents(3, [{d_ino=786432, d_off=1048577, d_reclen=24, d_name=".", ...}, ...], 32768) = 208
write(1, "file1\nfile2\n", 14) = 14
```

### 10.5.2 perf

`perf` 是 Linux 核心提供的效能分析工具，可用於 CPU 效能、熱點分析、硬體事件監控等：

```bash
# 列出可用的效能事件
perf list

# 記錄程式執行並生成資料檔案
perf record -g ./program

# 顯示熱點函式
perf report

# 即時顯示熱點
perf top

# 顯示呼叫圖
perf record --call-graph dwarf ./program
perf report --call-graph
```

### 10.5.3 gprof

`gprof` 是 GCC 的程式剖析工具，需要在編譯時啟用：

```bash
# 編譯時啟用剖析（使用 -pg 選項）
gcc -pg -g -O2 program.c -o program

# 執行後會生成 gmon.out
./program

# 檢視剖析結果
gprof ./program gmon.out
```

`gprof` 輸出包括：

- **flat profile**：每個函式花費的時間
- **call graph**：函式之間的呼叫關係
- **時間分析**：函式佔用的時間百分比

### 10.5.4 程序監控工具

```bash
# top：即時顯示程序資源使用
top
# 常用操作：
#   P：按 CPU 排序
#   M：按記憶體排序
#   1：顯示每個 CPU 核心
#   k：殺死程序

# htop：更友善的互動式監控（需要安裝）
htop

# vmstat：虛擬記憶體統計
vmstat 1  # 每秒更新

# iostat：磁碟 I/O 統計
iostat -x 1

# netstat：網路連線統計
netstat -tunapl

# ss：現代的 socket 統計（更快）
ss -tunapl
```

### 10.5.5 記憶體分析工具

```bash
# valgrind：記憶體錯誤偵測
valgrind --leak-check=full ./program

# AddressSanitizer：在編譯時啟用
gcc -fsanitize=address -g program.c -o program

# 查看行程記憶體使用
cat /proc/$PID/status | grep -E "Vm|Rss"

# pmap：顯示行程的記憶體映射
pmap -x $PID
```
