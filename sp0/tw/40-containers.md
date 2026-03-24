# 40. 容器技術——namespace 與 cgroup

## 40.1 容器 vs 虛擬機

| 特性 | 容器 | 虛擬機 |
|------|------|---------|
| 隔離層級 | 作業系統 | 硬體 |
| 啟動速度 | 秒級 | 分級 |
| 效能 | 接近原生 | 開銷較大 |
| 資源隔離 | namespace, cgroup | 完整虛擬化 |

## 40.2 Linux Namespace

Namespace 隔離系統資源。

| Namespace | 隔離內容 |
|-----------|----------|
| PID | 行程 ID |
| Network | 網路設備 |
| Mount | 掛載點 |
| IPC | 訊號、共享記憶體 |
| UTS | 主機名稱 |
| User | 使用者 ID |

### 40.2.1 API

```c
// 建立 namespace
int unshare(int flags);
int setns(int fd, int nstype);

// /proc/PID/ns 目錄
ls /proc/self/ns/
```

### 40.2.2 範例

```c
unshare(CLONE_NEWPID | CLONE_NEWUTS);
execlp("bash", "bash", NULL);
```

## 40.3 cgroup

cgroup 控制資源使用。

### 40.3.1 子系統

| 控制器 | 控制資源 |
|--------|----------|
| cpu | CPU 時間分配 |
| memory | 記憶體限制 |
| blkio | I/O 頻寬 |
| cpuset | CPU 核心分配 |

### 40.3.2 設定限制

```bash
# 建立 cgroup
mkdir /sys/fs/cgroup/memory/mylimit

# 設定記憶體限制 (100MB)
echo 104857600 > /sys/fs/cgroup/memory/mylimit/memory.limit_in_bytes

# 將行程加入 group
echo $PID > /sys/fs/cgroup/memory/mylimit/tasks
```

## 40.4 Docker 基礎

### 40.4.1 基本操作

```bash
# 執行容器
docker run -it ubuntu bash

# 建立映像
docker build -t myapp .

# 列出容器
docker ps -a
```

### 40.4.2 Dockerfile

```dockerfile
FROM ubuntu:latest
COPY . /app
WORKDIR /app
RUN make
CMD ["./app"]
```

## 40.5 小結

本章節我們學習了：
- 容器與 VM 的比較
- Linux Namespace 的概念
- cgroup 資源控制
- Docker 基礎

## 40.6 習題

1. 使用 unshare 創建隔離環境
2. 研究 containerd 和 runc
3. 比較 Docker 和 Kubernetes
