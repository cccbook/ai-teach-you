# 系統呼叫 (System Call)

## 概述

系統呼叫是使用者程式與作業系統核心之間的介面。透過系統呼叫，應用程式可以請求核心提供服務，如檔案操作、程序管理、網路通訊等。系統呼叫是使用者空間進入核心空間的唯一合法入口。

## 歷史

- **1969**：Unix 系統呼叫設計
- **1978**：DOS 系統呼叫
- **1991**：Linux 系統呼叫
- **現在**：每個 OS 有自己的系統呼叫介面

## 常見系統呼叫

### 1. 程序管理

```c
#include <unistd.h>

// fork - 建立程序
pid_t pid = fork();

// exec - 執行新程式
execlp("ls", "ls", "-l", NULL);

// exit - 終止程序
_exit(0);

// getpid/getppid
pid_t pid = getpid();
pid_t ppid = getppid();
```

### 2. 檔案操作

```c
#include <fcntl.h>
#include <unistd.h>

// open
int fd = open("file.txt", O_RDONLY);

// read
char buf[100];
ssize_t n = read(fd, buf, 100);

// write
write(fd, "hello", 5);

// close
close(fd);
```

### 3. 目錄操作

```c
#include <dirent.h>

DIR *dir = opendir("/tmp");
struct dirent *entry;

while ((entry = readdir(dir)) != NULL) {
    printf("%s\n", entry->d_name);
}

closedir(dir);

// mkdir
mkdir("/tmp/newdir", 0755);

// rmdir
rmdir("/tmp/newdir");
```

### 4. 程序屬性

```c
#include <sys/resource.h>

// 取得資源限制
struct rlimit limit;
getrlimit(RLIMIT_NOFILE, &limit);

// 設定資源限制
limit.rlim_cur = 1024;
setrlimit(RLIMIT_NOFILE, &limit);

// 取得使用者資訊
uid_t uid = getuid();
gid_t gid = getgid();
```

### 5. 記憶體管理

```c
#include <sys/mman.h>

// mmap
void *mem = mmap(NULL, 4096, PROT_READ | PROT_WRITE,
                 MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);

// munmap
munmap(mem, 4096);

// brk
void *old_brk = brk(new_addr);
```

### 6. 時間

```c
#include <time.h>

// time
time_t now = time(NULL);
printf("%s", ctime(&now));

// gettimeofday
struct timeval tv;
gettimeofday(&tv, NULL);
printf("%ld.%06d\n", tv.tv_sec, tv.tv_usec);
```

## 系統呼叫實作

### 1. x86-64 系統呼叫

```asm
; 系統呼叫：syscall
; 系統呼叫號在 rax
; 參數在 rdi, rsi, rdx, r10, r8, r9

mov rax, 60       ; exit 系統呼叫號
mov rdi, 0        ; 退出碼
syscall           ; 觸發系統呼叫
```

### 2. ARM64 系統呼叫

```asm
; 系統呼叫：svc #0
; 系統呼叫號在 x8
; 參數在 x0-x5

mov x8, 93        ; exit 系統呼叫號
mov x0, 0         ; 退出碼
svc #0            ; 觸發系統呼叫
```

### 3. 系統呼叫表

```c
// Linux 系統呼叫表 (sys_call_table)
asmlinkage long (*sys_call_table[__NR_syscalls])(...) = {
    [__NR_read] = sys_read,
    [__NR_write] = sys_write,
    [__NR_open] = sys_open,
    [__NR_close] = sys_close,
    [__NR_fork] = sys_fork,
    [__NR_execve] = sys_execve,
    [__NR_exit] = sys_exit,
    // ...
};
```

### 4. 自訂系統呼叫

```c
// Linux 模組方式添加系統呼叫
#include <linux/module.h>
#include <linux/kernel.h>

asmlinkage long sys_mycall(int param) {
    printk(KERN_INFO "mycall: %d\n", param);
    return param;
}
```

## 為什麼學習系統呼叫？

1. **理解核心**：使用者/核心介面
2. **系統程式設計**：低階 API
3. **效能**：減少系統呼叫開銷
4. **安全**：理解權限控制

## 參考資源

- Linux man syscalls(2)
- "Linux Kernel Development"
- "Understanding the Linux Kernel"
