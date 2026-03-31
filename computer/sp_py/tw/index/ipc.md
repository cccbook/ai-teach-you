# 程序間通訊 (IPC)

## 概述

程序間通訊（IPC）允許不同程序交換資料和協調工作。IPC 是作業系統的基礎設施，用於客戶端-伺服器、通訊、程序同步等場景。

## 歷史

- **1970s**：Unix 引入管道
- **1980s**：訊息佇列、共享記憶體
- **1990s**：POSIX 標準化
- **現在**：多種 IPC 機制

## IPC 機制

### 1. 管道

```c
// 匿名管道
int pipefd[2];
pipe(pipefd);

if (fork() == 0) {
    // 子程序：寫入
    close(pipefd[0]);
    write(pipefd[1], "hello", 5);
} else {
    // 父程序：讀取
    close(pipefd[1]);
    read(pipefd[0], buf, 5);
}
```

### 2. FIFO（命名管道）

```bash
# 創建 FIFO
mkfifo /tmp/myfifo

# 程序 A
int fd = open("/tmp/myfifo", O_WRONLY);
write(fd, "data", 4);

// 程序 B
int fd = open("/tmp/myfifo", O_RDONLY);
read(fd, buf, 4);
```

### 3. 訊息佇列

```c
#include <sys/msg.h>

struct msgbuf {
    long mtype;
    char mtext[100];
};

// 發送
struct msgbuf msg = {.mtype = 1, .mtext = "hello"};
msgsnd(msgid, &msg, sizeof(msg.mtext), 0);

// 接收
msgrcv(msgid, &msg, sizeof(msg.mtext), 1, 0);
```

### 4. 共享記憶體

```c
#include <sys/shm.h>

// 建立共享記憶體
int shmid = shmget(IPC_PRIVATE, 4096, IPC_CREAT | 0666);
char *shm = shmat(shmid, NULL, 0);

// 使用
strcpy(shm, "共享資料");

// 分離
shmdt(shm);

// 刪除
shmctl(shmid, IPC_RMID, NULL);
```

### 5. 信號量

```c
#include <sys/sem.h>

// 建立信號量
int semid = semget(IPC_PRIVATE, 1, IPC_CREAT | 0666);
semctl(semid, 0, SETVAL, 1);

// P 操作（等待）
struct sembuf p = {0, -1, 0};
semop(semid, &p, 1);

// V 操作（釋放）
struct sembuf v = {0, 1, 0};
semop(semid, &v, 1);
```

### 6. 訊號

```c
#include <signal.h>

// 自訂訊號處理
void handler(int signum) {
    printf("收到訊號 %d\n", signum);
}

signal(SIGUSR1, handler);

// 發送訊號
kill(pid, SIGUSR1);
```

### 7. Socket

```c
// Unix Domain Socket
int sockfd = socket(AF_UNIX, SOCK_STREAM, 0);

struct sockaddr_un addr;
addr.sun_family = AF_UNIX;
strcpy(addr.sun_path, "/tmp/socket");

bind(sockfd, (struct sockaddr *)&addr, sizeof(addr));
listen(sockfd, 5);

int client = accept(sockfd, NULL, NULL);
```

### 8. mmap

```c
// 檔案映射
int fd = open("data.bin", O_RDWR);
void *mem = mmap(NULL, 4096, PROT_READ | PROT_WRITE,
                 MAP_SHARED, fd, 0);

memcpy(mem, "data", 4);
msync(mem, 4096, MS_SYNC);

munmap(mem, 4096);
```

## 選擇 IPC 機制

| 機制 | 速度 | 適用場景 |
|------|------|----------|
| pipe | 快 | 父子程序通訊 |
| FIFO | 快 | 无关进程 |
| mmap | 最快 | 大量資料共享 |
| socket | 中 | 網路/跨主機 |
| msg | 慢 | 訊息交換 |

## 為什麼學習 IPC？

1. **程序協作**：多程序協作
2. **系統設計**：用戶端/伺服器
3. **同步**：資源同步
4. **效能**：選擇合適機制

## 參考資源

- "Advanced Programming in the UNIX Environment"
- POSIX IPC
- Linux man pages
