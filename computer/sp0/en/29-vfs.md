# 29. Virtual File System——VFS Abstraction Layer

## 29.1 Why VFS?

VFS (Virtual File System) provides a unified interface, allowing different file systems to coexist:

```
┌─────────────────────────────────────────┐
│         Application                      │
│    (open, read, write, close)           │
└─────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────┐
│     VFS (Virtual File System Interface) │
└─────────────────────────────────────────┘
                     │
         ┌───────────┼───────────┐
         ↓           ↓           ↓
┌───────────┐ ┌───────────┐ ┌───────────┐
│   ext2     │ │   xv6fs   │ │  /proc    │
│  filesystem │ │  filesystem │ │  virtual  │
└───────────┘ └───────────┘ └───────────┘
```

## 29.2 xv6 File Abstraction

xv6 defines a unified file interface:

```c
// file.h
struct file {
    enum { FD_NONE, FD_PIPE, FD_INODE, FD_DEVICE } type;
    int ref;               // Reference count
    char readable;         // Readable
    char writable;         // Writable
    struct pipe *pipe;     // Pipe
    struct inode *ip;      // inode
    uint off;              // File offset
    short major;           // Device number
};
```

## 29.3 System Call Interface

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
    
    // Allocate file structure
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
    
    // Return file descriptor
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

## 29.4 Device Files

### 29.4.1 Major and Minor Device Numbers

```c
// major and minor identify device
// major: device type
// minor: specific device instance
```

### 29.4.2 Device Operations

```c
struct devsw {
    int (*read)(int, uint64, int);
    int (*write)(int, uint64, int);
};

struct devsw devsw[NDEV];
```

## 29.5 Pipes

Pipes are another example of VFS abstraction:

```c
struct pipe {
    struct spinlock lock;
    char data[PIPESIZE];
    uint nread;          // Bytes read
    uint nwrite;         // Bytes written
    int readopen;        // Read end open
    int writeopen;       // Write end open
};
```

### 29.5.1 pipe() System Call

```c
int
sys_pipe(void) {
    uint64 fdarray;
    if (argaddr(0, &fdarray) < 0) return -1;
    
    struct pipe *pi = pipealloc();
    if (pi == 0) return -1;
    
    // Allocate two file descriptors
    if (fdalloc(pi->read_file) < 0 || fdalloc(pi->write_file) < 0) {
        pipeclose(pi);
        return -1;
    }
    
    // Return [read_fd, write_fd]
    if (copyout(p->pagetable, fdarray, read_fd, sizeof(int)) < 0)
        return -1;
    if (copyout(p->pagetable, fdarray + 4, write_fd, sizeof(int)) < 0)
        return -1;
    
    return 0;
}
```

## 29.6 File Descriptor Table

Each process has its own file descriptor table:

```c
struct proc {
    // ...
    struct file *ofile[NOFILE];  // Process's open file table
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

## 29.7 Standard File Descriptors

Standard descriptors set at boot:

```
fd 0: stdin  (Standard Input)
fd 1: stdout (Standard Output)
fd 2: stderr (Standard Error)
```

## 29.8 Complete I/O Flow

```
Application
    ↓ open("file", O_RDONLY)
VFS layer (sys_open)
    ↓
inode layer (namei, ilock)
    ↓
buffer cache (Bread, bwrite)
    ↓
Disk
```

## 29.9 Summary

In this chapter we learned:
- VFS concept and benefits
- xv6 file abstraction
- open/read/write implementation
- Device files
- Pipe implementation
- File descriptor table

## 29.10 Exercises

1. Implement lseek() system call
2. Implement dup() and dup2()
3. Compare xv6 and Linux VFS
4. Implement rename() system call
5. Research zero-copy I/O possibilities
