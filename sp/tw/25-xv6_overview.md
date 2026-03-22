# 25. xv6 架構總覽——UNIX v6 的 RISC-V 移植

## 25.1 什麼是 xv6？

xv6 是 MIT 作業系統課程的教學用作業系統：
- 起源於 UNIX v6（1976 年 Ken Thompson 和 Dennis Ritchie 設計）
- 由 MIT 移植到 RISC-V 架構
- 設計用於教學目的

原始碼位置：[_code/xv6/](../_code/xv6/)

## 25.2 xv6 的設計目標

xv6 不是為了效能或功能完整，而是：
- **簡潔**：易於理解和學習
- **完整**：包含作業系統的核心概念
- **真實**：使用真實的 UNIX 概念

## 25.3 目錄結構

```
xv6/
├── kernel/              # 核心程式碼
│   ├── main.c         # 入口點
│   ├── proc.c         # 行程管理
│   ├── vm.c           # 虛擬記憶體
│   ├── printf.c       # printf 實現
│   ├── trap.c         # 中斷處理
│   ├── sleeplock.c    # 睡眠鎖
│   ├── bio.c          # 區塊 I/O 層
│   ├── fs.c           # 檔案系統
│   ├── log.c          # 日誌系統
│   ├── file.c         # 檔案抽象層
│   └── ...
├── user/               # 使用者程式
│   ├── ulib.c         # 使用者庫
│   ├── printf.c       # 使用者 printf
│   ├── init.c         # 第一個使用者程式
│   └── ...
├── Makefile
└── mkfs/              # 檔案系統鏡像工具
```

## 25.4 核心概念

### 25.4.1 行程（Process）

xv6 中的基本執行單位：
- 每個行程有自己的記憶體空間
- 支援傳統的 fork/exec/wait 系统呼叫

### 25.4.2 檔案系統

- 簡化的 UNIX v6 檔案系統
- 支持目錄、普通檔案、設備檔案
- 日誌系統確保一致性

### 25.4.3 虛擬記憶體

- 基於分頁的虛擬記憶體
- 核心和使用者空間分離

## 25.5 核心資料結構

### 25.5.1 行程結構 (proc.h)

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

### 25.5.2 檔案結構 (file.h)

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

## 25.6 建置和執行

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

### 25.6.2 執行 xv6

```bash
cd _code/xv6
make qemu
```

## 25.7 與 mini-riscv-os 的比較

| 特性 | mini-riscv-os | xv6 |
|------|---------------|-----|
| 規模 | ~500 行 | ~10000 行 |
| 功能 | 極簡 | 較完整 |
| 行程管理 | 簡單 | 完整 fork/exec |
| 檔案系統 | 無 | 有 |
| 虛擬記憶體 | 無 | 有 |
| 系統呼叫 | 無 | 有 |
| 用途 | 教學 | 大學課程 |

## 25.8 xv6 的設計哲學

1. **簡潔勝於功能**：每個概念都應該簡單
2. **程式碼即文件**：好的程式碼應該自解釋
3. **一致性**：類似的概念應該用類似的實現

## 25.9 小結

本章節我們學習了：
- xv6 的起源和設計目標
- xv6 的目錄結構
- 核心資料結構（proc、file）
- 建置和執行方式
- 與 mini-riscv-os 的比較

## 25.10 習題

1. 閱讀 xv6/Makefile 了解建置流程
2. 比較 xv6 和 Linux 的差異
3. 研究 xv6 的版本歷史（從 Unix v6 到現代）
4. 在 xv6 上運行使用者程式
5. 研究 MIT 6.S081 課程
