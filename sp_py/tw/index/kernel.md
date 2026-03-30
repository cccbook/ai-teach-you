# 核心 (Kernel)

## 概述

作業系統核心（Kernel）是作業系統的核心部分，負責管理硬體資源、處理系統呼叫、協調程序執行等。Kernel 是系統最底層的軟體，直接與硬體互動，為上層應用程式提供抽象介面。

## 歷史

- **1964**：MIT 開發 Multics
- **1969**：Ken Thompson 開發 Unix 原型
- **1991**：Linus Torvalds 發布 Linux
- **現在**：Linux、Windows NT、macOS XNU

## Kernel 功能

### 1. 程序管理

```c
// Linux 核心程序結構
struct task_struct {
    unsigned long state;
    int pid;
    unsigned int flags;
    struct mm_struct *mm;
    struct files_struct *files;
    struct signal_struct *signal;
    // ...
};
```

### 2. 記憶體管理

```c
// 記憶體管理
void *kmalloc(size_t size, gfp_t flags);
void kfree(void *ptr);
void *vmalloc(size_t size);

// 頁面管理
struct page *alloc_page(gfp_t gfp_mask);
void free_page(struct page *page);
```

### 3. 設備管理

```c
// 字符設備驅動
static int my_open(struct inode *inode, struct file *file);
static int my_release(struct inode *inode, struct file *file);
static ssize_t my_read(struct file *file, char __user *buf, 
                       size_t count, loff_t *ppos);

static struct file_operations my_fops = {
    .owner = THIS_MODULE,
    .open = my_open,
    .read = my_read,
    .release = my_release,
};
```

### 4. 檔案系統

```c
// VFS 超級區塊
struct super_block {
    struct list_head s_list;
    dev_t s_dev;
    unsigned long s_blocksize;
    struct super_operations *s_op;
    struct dentry *s_root;
    // ...
};

// 檔案操作
struct file_operations {
    int (*open)(struct inode *, struct file *);
    ssize_t (*read)(struct file *, char __user *, size_t, loff_t *);
    ssize_t (*write)(struct file *, const char __user *, size_t, loff_t *);
    int (*release)(struct inode *, struct file *);
};
```

### 5. 系統呼叫

```c
// 定義系統呼叫
asmlinkage long sys_mycall(int param) {
    printk("系統呼叫: %d\n", param);
    return 0;
}

// 系統呼叫表
static sys_call_ptr_t sys_call_table[__NR_syscalls] = {
    [__NR_read] = sys_read,
    [__NR_write] = sys_write,
    [__NR_mycall] = sys_mycall,
};
```

### 6. 中斷處理

```c
// 中斷處理
static irqreturn_t my_interrupt(int irq, void *dev_id) {
    // 處理中斷
    return IRQ_HANDLED;
}

// 註冊中斷
request_irq(irq_num, my_interrupt, IRQF_SHARED, "mydev", &my_dev);
```

## Kernel 類型

### 1. 宏内核（Monolithic）

```
┌─────────────────────────────┐
│         Kernel Space        │
│  ┌─────┬─────┬─────┬─────┐ │
│  │ 檔案│ 網路│ 記憶│ 設備│ │
│  │系統 │ 系統│ 管理│ 驅動│ │
│  └─────┴─────┴─────┴─────┘ │
├─────────────────────────────┤
│         User Space         │
└─────────────────────────────┘

Linux, Unix
```

### 2. 微內核（Microkernel）

```
┌─────────────┐     ┌─────────────┐
│ User Process│     │ User Process│
├─────────────┤     ├─────────────┤
│    IPC      │     │    IPC      │
├─────────────┴─────┴─────────────┤
│   微內核核心                    │
│  (行程管理、記憶體、IPC)        │
├─────────────────────────────────┤
│    驅動程式（在用戶空間）        │
└─────────────────────────────────┘

MINIX, QNX
```

### 3. 混合內核

```
┌─────────────────────────────┐
│      Kernel Space          │
│   核心 + 某些服務           │
├─────────────────────────────┤
│      User Space            │
└─────────────────────────────┘

Windows NT, macOS XNU
```

## 為什麼學習 Kernel？

1. **系統程式設計**：理解作業系統運作
2. **驅動程式開發**：硬體支援
3. **安全研究**：系統安全
4. **效能優化**：核心調優

## 參考資源

- "Linux Kernel Development"
- "Understanding the Linux Kernel"
- Linux 核心原始碼
