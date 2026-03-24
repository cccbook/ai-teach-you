# 程序 (Process)

## 概述

程序是正在執行的程式實體，是作業系統進行資源分配和調度的基本單位。每個程序有自己的虛擬位址空間、檔案描述符、執行緒等資源。程序間相互隔離，透過 IPC 進行通訊。

## 歷史

- **1964**：Multics 引入程序概念
- **1970s**：Unix 程序模型
- **1990s**：POSIX 標準化
- **現在**：所有作業系統使用程序

## 程序結構

### 1. 程序控制區塊（PCB）

```c
struct task_struct {
    // 識別
    pid_t pid;
    pid_t tgid;
    char comm[TASK_COMM_LEN];
    
    // 狀態
    volatile long state;
    int exit_state;
    unsigned int flags;
    
    // 排程
    int prio;
    int static_prio;
    unsigned int policy;
    struct sched_entity se;
    
    // 記憶體
    struct mm_struct *mm;
    struct mm_struct *active_mm;
    
    // 檔案
    struct files_struct *files;
    
    // 信號
    struct signal_struct *signal;
    struct sighand_struct *sighand;
    
    // 執行緒
    struct thread_struct thread;
};
```

### 2. 程序狀態

```
        ┌──────────┐
        │  建立   │
        └────┬────┘
             │
        ┌────▼────┐
   ┌────│就緒(R) │────┐
   │    └────────┘    │
   │                 │
┌──▼────────┐    ┌───▼────────┐
│執行(Running)│    │執行(Running)│
└──┬────────┘    └───┬────────┘
   │      CPU        │    ┌──────┐
   │                 └────│ 阻塞 │
   │                      │(Wait)│
   │                      └──────┘
   │
┌──▼────────┐
│ 終止(Zombie)│
└────────────┘

R = Running / Ready
S = Sleeping (可中斷)
D = Sleeping (不可中斷)
T = Stopped
Z = Zombie
```

### 3. 建立程序

```c
// fork - 建立新程序
pid_t pid = fork();

if (pid == 0) {
    // 子程序
    printf("我是子程序\n");
} else if (pid > 0) {
    // 父程序
    printf("子程序 PID: %d\n", pid);
} else {
    // 錯誤
    perror("fork");
}

// vfork - 共享記憶體（已過時）
pid_t pid = vfork();

if (pid == 0) {
    execlp("./program", "program", NULL);
    _exit(0);
}
```

### 4. 執行新程式

```c
// exec - 替換當前程序的映像
char *args[] = {"ls", "-l", NULL};
char *envp[] = {NULL};

execv("/bin/ls", args);
// execvp - 使用 PATH
// execl - 使用列表而非陣列
```

### 5. 程序終止

```c
// 正常終止
void exit(int status);
// 或從 main 返回

// 異常終止
void abort(void);
void assert(int expression);

// 等待子程序
pid_t wait(int *status);
pid_t waitpid(pid_t pid, int *status, int options);
```

### 6. 程序間通訊

```c
// pipe - 管道
int pipefd[2];
pipe(pipefd);
write(pipefd[1], "hello", 5);
read(pipefd[0], buf, 5);

// FIFO
mkfifo("/tmp/myfifo", 0666);
```

## 程序監控

```bash
# 查看程序
ps
ps aux
ps -ef

# 即時監控
top
htop

# 程序樹
pstree
```

## 為什麼學習程序概念？

1. **多工**：並發執行基礎
2. **資源管理**：理解系統資源分配
3. **除錯**：程序相關問題
4. **系統程式設計**：daemon、IPC

## 參考資源

- "Advanced Programming in the UNIX Environment"
- POSIX 標準
- Linux man pages
