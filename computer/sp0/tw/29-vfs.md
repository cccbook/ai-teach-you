# 29. 虛擬檔案系統——VFS 抽象層

## 29.1 為什麼需要 VFS？

VFS（Virtual File System）提供統一的介面，讓不同檔案系統可以共存：

```
┌─────────────────────────────────────────┐
│         應用程式                         │
│    (open, read, write, close)           │
└─────────────────────────────────────────┘
                    │
                    ↓
┌─────────────────────────────────────────┐
│     VFS (虛擬檔案系統介面)              │
└─────────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        ↓           ↓           ↓
┌───────────┐ ┌───────────┐ ┌───────────┐
│   ext2     │ │   xv6fs   │ │  /proc    │
│  檔案系統  │ │  檔案系統  │ │  虛擬檔案  │
└───────────┘ └───────────┘ └───────────┘
```

## 29.2 xv6 的檔案抽象

xv6 定義了統一的檔案介面：

```c
// file.h
struct file {
    enum { FD_NONE, FD_PIPE, FD_INODE, FD_DEVICE } type;
    int ref;               // 引用計數
    char readable;         // 可讀
    char writable;         // 可寫
    struct pipe *pipe;     // 管道
    struct inode *ip;      // inode
    uint off;              // 檔案位移
    short major;           // 設備號
};
```

## 29.3 系統呼叫介面

### 29.3.1 open

```c
// sysfile.c
int
sys_open(void) {
    char path[MAXPATH];
    int omode;
    
    if (argstr(0, path) < 0 || argint(1, &omode) < 0)
        return -1;
    
    struct inode *ip;
    begin_op();
    
    if (omode & O_CREATE) {
        ip = create(path, T_FILE, 0, 0);
    } else {
        ip = namei(path);
        if (ip == 0) {
            end_op();
            return -1;
        }
    }
    
    // 分配 file 結構
    struct file *f = filealloc();
    if (f == 0) {
        iunlockput(ip);
        end_op();
        return -1;
    }
    
    f->type = FD_INODE;
    f->ip = ip;
    f->off = 0;
    f->readable = !(omode & O_WRONLY);
    f->writable = (omode & O_WRONLY) || (omode & O_RDWR);
    
    // 返回檔案描述符
    return fdalloc(f);
}
```

### 29.3.2 read/write

```c
int
sys_read(void) {
    int fd;
    uint64 p;
    
    if (argfd(0, &fd, &f) < 0 || argint(1, (int*)&p) < 0)
        return -1;
    
    return fileread(f, p, args->n);
}

int
sys_write(void) {
    int fd;
    uint64 p;
    
    if (argfd(0, &fd, &f) < 0 || argint(1, (int*)&p) < 0)
        return -1;
    
    return filewrite(f, p, args->n);
}
```

## 29.4 設備檔案

### 29.4.1 主設備號和次設備號

```c
// major 和 minor 識別設備
// major: 設備類型
// minor: 具體設備例項
```

### 29.4.2 設備操作

```c
struct devsw {
    int (*read)(int, uint64, int);
    int (*write)(int, uint64, int);
};

struct devsw devsw[NDEV];
```

## 29.5 管道

管道是 VFS 抽象的另一個例子：

```c
struct pipe {
    struct spinlock lock;
    char data[PIPESIZE];
    uint nread;          // 已讀取
    uint nwrite;         // 已寫入
    int readopen;        // 讀取端開啟
    int writeopen;       // 寫入端開啟
};
```

### 29.5.1 pipe() 系統呼叫

```c
int
sys_pipe(void) {
    uint64 fdarray;
    if (argaddr(0, &fdarray) < 0) return -1;
    
    struct pipe *pi = pipealloc();
    if (pi == 0) return -1;
    
    // 分配兩個檔案描述符
    if (fdalloc(pi->read_file) < 0 || fdalloc(pi->write_file) < 0) {
        pipeclose(pi);
        return -1;
    }
    
    // 返回 [read_fd, write_fd]
    if (copyout(p->pagetable, fdarray, read_fd, sizeof(int)) < 0)
        return -1;
    if (copyout(p->pagetable, fdarray + 4, write_fd, sizeof(int)) < 0)
        return -1;
    
    return 0;
}
```

## 29.6 檔案描述符表

每個行程有自己的檔案描述符表：

```c
struct proc {
    // ...
    struct file *ofile[NOFILE];  // 行程的開啟檔案表
    // ...
};
```

### 29.6.1 fdalloc

```c
int
fdalloc(struct file *f) {
    int fd;
    for (fd = 0; fd < NOFILE; fd++) {
        if (p->ofile[fd] == 0) {
            p->ofile[fd] = f;
            return fd;
        }
    }
    return -1;
}
```

## 29.7 標準檔案描述符

開機時設定的標準描述符：

```
fd 0: stdin  (標準輸入)
fd 1: stdout (標準輸出)
fd 2: stderr (標準錯誤)
```

## 29.8 完整 I/O 流程

```
應用程式
    ↓ open("file", O_RDONLY)
VFS layer (sys_open)
    ↓
inode layer (namei, ilock)
    ↓
buffer cache (Bread, bwrite)
    ↓
磁碟
```

## 29.9 小結

本章節我們學習了：
- VFS 的概念和優點
- xv6 的檔案抽象
- open/read/write 實現
- 設備檔案
- 管道的實現
- 檔案描述符表

## 29.10 習題

1. 實現 lseek() 系統呼叫
2. 實現 dup() 和 dup2()
3. 比較 xv6 和 Linux 的 VFS
4. 實現 rename() 系統呼叫
5. 研究零拷貝 I/O 的可能性
