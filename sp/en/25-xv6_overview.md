# 25. xv6 Architecture Overview——UNIX v6 on RISC-V

## 25.1 What is xv6?

xv6 is a teaching operating system used in MIT's operating system courses:
- Originally derived from UNIX v6 (1976, designed by Ken Thompson and Dennis Ritchie)
- Ported to RISC-V architecture by MIT
- Designed for educational purposes

Source code location: [_code/xv6/](../_code/xv6/)

## 25.2 xv6 Design Goals

xv6 is not designed for performance or feature completeness, but rather:
- **Simplicity**: Easy to understand and learn
- **Completeness**: Includes core OS concepts
- **Realism**: Uses real UNIX concepts

## 25.3 Directory Structure

```
xv6/
├── kernel/              # Kernel code
│   ├── main.c         # Entry point
│   ├── proc.c         # Process management
│   ├── vm.c           # Virtual memory
│   ├── printf.c       # printf implementation
│   ├── trap.c         # Interrupt handling
│   ├── sleeplock.c    # Sleep locks
│   ├── bio.c          # Block I/O layer
│   ├── fs.c           # File system
│   ├── log.c          # Logging system
│   ├── file.c         # File abstraction layer
│   └── ...
├── user/               # User programs
│   ├── ulib.c         # User library
│   ├── printf.c       # User printf
│   ├── init.c         # First user program
│   └── ...
├── Makefile
└── mkfs/              # File system image tools
```

## 25.4 Core Concepts

### 25.4.1 Process

Basic execution unit in xv6:
- Each process has its own memory space
- Supports traditional fork/exec/wait system calls

### 25.4.2 File System

- Simplified UNIX v6 file system
- Supports directories, regular files, device files
- Logging system ensures consistency

### 25.4.3 Virtual Memory

- Page-based virtual memory
- Kernel and user space separation

## 25.5 Kernel Data Structures

### 25.5.1 Process Structure (proc.h)

```c
// proc.h
struct proc {
    struct spinlock lock;
    
    // p Lock must be held when accessing these fields:
    uint64_t sz;              // Size of process memory (bytes)
    pagetable_t pagetable;   // User page table
    char *kstack;            // Bottom of kernel stack for this process
    enum procstate state;    // Process state
    int pid;                 // Process ID
    struct proc *parent;     // Parent process
    struct trapframe *tf;    // data page for trampoline.S
    struct context *context;  // swtch() here to run process
    void *chan;              // If non-zero, sleeping on chan
    int killed;               // If non-zero, have been killed
    int xstate;              // Exit status to be returned to parent's wait
    int priority;            // Scheduling priority
    char name[16];           // Process name (debugging)
};
```

### 25.5.2 File Structure (file.h)

```c
struct file {
    enum { FD_NONE, FD_PIPE, FD_INODE, FD_DEVICE } type;
    int ref;                 // Reference count
    char readable;
    char writable;
    struct pipe *pipe;        // FD_PIPE
    struct inode *ip;        // FD_INODE and FD_DEVICE
    uint off;                // FD_INODE
    short major;             // FD_DEVICE
};
```

## 25.6 Building and Running

### 25.6.1 Makefile

```makefile
KERNEL=kernel
USER=usertests
MKFS=mkfs/mkfs
...

all:
    $(MAKE) -C kernel
    $(MAKE) -C user

qemu: all
    qemu-system-riscv64 \
        -machine virt \
        -nographic \
        -kernel kernel/kernel \
        -append "root=Device:number=1" \
        -drive file=fs.img,if=none,format=raw,id=h0 \
        -device virtio-blk-device,drive=h0,serial=foobar
```

### 25.6.2 Running xv6

```bash
cd _code/xv6
make qemu
```

## 25.7 Comparison with mini-riscv-os

| Feature | mini-riscv-os | xv6 |
|---------|---------------|-----|
| Size | ~500 lines | ~10000 lines |
| Functionality | Minimal | More complete |
| Process management | Simple | Complete fork/exec |
| File system | None | Yes |
| Virtual memory | None | Yes |
| System calls | None | Yes |
| Purpose | Teaching | University course |

## 25.8 xv6 Design Philosophy

1. **Simplicity over features**: Every concept should be simple
2. **Code as documentation**: Good code should be self-explanatory
3. **Consistency**: Similar concepts should have similar implementations

## 25.9 Summary

In this chapter we learned:
- xv6 origins and design goals
- xv6 directory structure
- Core data structures (proc, file)
- Build and run methods
- Comparison with mini-riscv-os

## 25.10 Exercises

1. Read xv6/Makefile to understand the build process
2. Compare xv6 and Linux differences
3. Research xv6 version history (from Unix v6 to modern)
4. Run user programs on xv6
5. Research MIT 6.S081 course
