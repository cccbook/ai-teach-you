# 30. 記憶體管理——分頁與交換

## 30.1 分頁基礎

分頁將虛擬記憶體劃分為固定大小的區塊（頁）：

```
虛擬記憶體                    實體記憶體
┌──────────────┐            ┌──────────────┐
│ Page 0       │ ────────→ │ Frame 3     │
│ Page 1       │ ────────→ │ Frame 1     │
│ Page 2       │ ────────→ │ Frame 5     │
│ Page 3       │            │ Frame 2     │
└──────────────┘            └──────────────┘
      4KB                        4KB
```

## 30.2 RISC-V 分頁

### 30.2.1 分頁大小

xv6 使用 4KB 頁面（Sv39）。

### 30.2.2 分頁表條目 (PTE)

```c
// 頁面表條目格式
#define PTE_V  0x001  // Valid (有效)
#define PTE_R  0x002  // Read
#define PTE_W  0x004  // Write
#define PTE_X  0x008  // Execute
#define PTE_U  0x010  // User
#define PTE_G  0x020  // Global
#define PTE_A  0x040  // Accessed
#define PTE_D  0x080  // Dirty
```

### 30.2.3 三層分頁

```
VPN[2] (9 bits) ──→ 第二層頁目錄 (512 個條目)
VPN[1] (9 bits) ──→ 第一層頁目錄 (512 個條目)
VPN[0] (9 bits) ──→ 頁框號 (PPN)
Offset (12 bits) ──→ 頁內偏移
```

## 30.3 xv6 分頁表管理

### 30.3.1 建立行程分頁表

```c
pagetable_t
proc_pagetable(struct proc *p) {
    pagetable_t pagetable;
    
    // 配置第一層頁目錄
    pagetable = uvmcreate();
    if (pagetable == 0) return 0;
    
    // 配置 trampoline 頁（用於中斷）
    if (mappages(pagetable, TRAMPOLINE, PGSIZE, 
                 (uint64)trampoline, PTE_R | PTE_X) < 0) {
        uvmfree(pagetable, 0);
        return 0;
    }
    
    // 配置陷阱向量頁
    if (mappages(pagetable, TRAPFRAME, PGSIZE, 
                 (uint64)p->tf, PTE_R | PTE_W) < 0) {
        // ...
    }
    
    return pagetable;
}
```

### 30.3.2 uvmcreate

```c
pagetable_t
uvmcreate(void) {
    pagetable_t pagetable;
    pagetable = (pagetable_t) kalloc();
    if (pagetable == 0) return 0;
    memset(pagetable, 0, PGSIZE);
    return pagetable;
}
```

## 30.4 記憶體配置

### 30.4.1 sbrk

```c
int
sys_sbrk(void) {
    int addr;
    int n;
    
    if (argint(0, &n) < 0) return -1;
    
    addr = myproc()->sz;
    if (n < 0) {
        if (growproc(n) < 0) return -1;
    } else if (growproc(n) < 0) {
        return -1;
    }
    return addr;
}

int
growproc(int n) {
    uint64 sz = p->sz;
    if (n > 0) {
        if ((sz = uvmalloc(p->pagetable, sz, sz + n)) == 0) {
            return -1;
        }
    } else if (n < 0) {
        sz = uvmdealloc(p->pagetable, sz, sz + n);
    }
    p->sz = sz;
    return 0;
}
```

## 30.5 分頁錯誤處理

### 30.5.1 陷阱處理

```c
void
usertrap(void) {
    // ...
    if (r_scause() == 8) {
        // 系統呼叫
        syscall();
    } else if (r_scause() == 13 || r_scause() == 15) {
        // 載入/儲存頁錯誤
        uint64 va = r_stval();
        if (va >= p->sz || 
            (r_scause() == 15 && !uva_to_pa(p->pagetable, va))) {
            p->killed = 1;
        }
    }
    // ...
}
```

## 30.6 核心和使用者空間

### 30.6.1 記憶體佈局

```
┌────────────────────────────────────────┐
│ USYSCALL (TRAPFRAME)                  │ 0x3fffff000
├────────────────────────────────────────┤
│                                        │
│     使用者空間                         │ 0 ... p->sz
│                                        │
├────────────────────────────────────────┤
│     空隙                               │
├────────────────────────────────────────┤
│                                        │
│     核心空間                           │ 0x80000000 ...
│                                        │
└────────────────────────────────────────┘
```

### 30.6.2 核心頁表

核心有獨立的頁表：
- 映射所有實體記憶體
- 應用程式無法存取

## 30.7 Copy-on-Write (COW)

xv6 沒有實現 COW，但概念如下：

### 30.7.1 fork() 優化

```c
// 原本的 fork：
uvmcopy(p->pagetable, np->pagetable, p->sz);  // 完整拷貝

// COW fork：
// 1. 只拷貝頁表，不拷貝資料
// 2. 將父子頁表都設為唯讀
// 3. 寫入時觸發頁錯誤
// 4. 頁錯誤處理：分配新頁、拷貝、設為可寫
```

## 30.8 交換（Swapping）

xv6 沒有實現交換（swap）。如果沒有足夠記憶體，會導致記憶體不足錯誤。

## 30.9 小結

本章節我們學習了：
- 分頁的基本概念
- RISC-V Sv39 分頁機制
- xv6 的分頁表管理
- sbrk() 和 growproc()
- 頁錯誤處理
- 核心/使用者空間分離

## 30.10 習題

1. 研究 Sv48 和 Sv57 分頁
2. 實現 Copy-on-Write fork
3. 實現 mmap() 系統呼叫
4. 比較分頁和分段
5. 研究 TLB 刷新策略
