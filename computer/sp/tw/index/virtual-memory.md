# 虛擬記憶體 (Virtual Memory)

## 概述

虛擬記憶體是作業系統提供的一種記憶體管理機制，讓程式可以使用比實際物理記憶體更大的位址空間。虛擬記憶體透過分頁機制實現，提供程序間的記憶體隔離，並簡化程式設計。

## 歷史

- **1962**：Multics 首次提出
- **1974**：IBM 發布 VM 作業系統
- **1987**：Linux 支援交換空間
- **現在**：所有現代作業系統使用虛擬記憶體

## 虛擬記憶體機制

### 1. 基礎概念

```
程式看到的位址空間          實際物理記憶體
┌─────────────┐          ┌─────────────┐
│   0x1000    │          │  0xA000     │
│  (虛擬)     │  ────→   │  (物理)     │
│             │   MMU    │             │
│   0x2000    │          │  0xB000     │
│  (虛擬)     │  ────→   │  (物理)     │
└─────────────┘          └─────────────┘

每個程式有自己的虛擬位址空間，互不干擾
```

### 2. 虛擬記憶體優點

```c
// 1. 更大的位址空間
// 32-bit: 4GB 虛擬空間
// 64-bit: 巨大空間

// 2. 記憶體隔離
// 每個程序有自己的頁表
// 防止非法存取其他程序記憶體

// 3. 簡化程式設計
// 不需關心物理記憶體配置
// 連續的虛擬位址空間

// 4. 記憶體共享
// 共享庫可以映射到不同程序
// 寫時複製（COW）
```

### 3. VM 區域（VMA）

```c
struct vm_area_struct {
    struct mm_struct *vm_mm;
    unsigned long vm_start;
    unsigned long vm_end;
    struct vm_area_struct *vm_next, *vm_prev;
    pgprot_t vm_page_prot;
    unsigned long vm_flags;
    
    struct file *vm_file;
    unsigned long vm_pgoff;
    struct vm_operations_struct *vm_ops;
};

// VM 標誌
#define VM_READ      0x00000001
#define VM_WRITE     0x00000002
#define VM_EXEC      0x00000004
#define VM_SHARED    0x00000008
#define VM_MAYREAD   0x00000010
#define VM_MAYWRITE  0x00000020
#define VM_MAYEXEC   0x00000040
```

### 4. 記憶體配置

```c
// 使用 mmap 配置虛擬記憶體
void *mmap(void *addr, size_t len, int prot, int flags,
           int fd, off_t offset);

// 範例：匿名映射
void *mem = mmap(NULL, 4096, PROT_READ | PROT_WRITE,
                 MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);

// 範例：檔案映射
void *file_mem = mmap(NULL, 4096, PROT_READ, MAP_SHARED,
                      fd, 0);
```

### 5. 分頁錯誤

```c
// 需求分頁
void do_page_fault(struct pt_regs *regs, unsigned long addr) {
    struct vm_area_struct *vma;
    struct page *page;
    
    vma = find_vma(current->mm, addr);
    if (!vma || addr < vma->vm_start)
        return -1;
    
    // 頁面不在記憶體中
    page = alloc_page(GFP_KERNEL);
    if (!page)
        return -1;
    
    // 載入資料
    if (vma->vm_file)
        read_page_from_file(page, vma->vm_file, addr);
    else
        zero_page(page);
    
    // 建立映射
    set_pte(vma->vm_mm, addr, page, vma->vm_page_prot);
}
```

### 6. 交換空間

```c
// Linux 交換空間管理
// 檢查可用交換空間
long vm_total_pages;
long total_swap = get_nr_swap_pages();

// 換出頁面
int try_to_swap_out(struct page *page) {
    // 找尋可換出的頁面
    // 寫入交換空間
    // 更新頁表
    
    return 1;
}
```

### 7. 寫時複製（COW）

```c
// fork() 後的寫時複製
int do_fork(unsigned long flags) {
    // 複製頁表，但標記為唯讀
    copy_page_tables(tmp, current->mm);
    
    return pid;
}

// 當寫入發生時
void handle_cow_fault(struct vm_area_struct *vma,
                      unsigned long address) {
    // 分配新頁面
    struct page *new_page = alloc_page(GFP_KERNEL);
    
    // 複製內容
    copy_page(new_page, old_page);
    
    // 設定為可寫
    set_pte(vma->vm_mm, address, new_page, prot);
}
```

## 監控虛擬記憶體

```bash
# Linux 查看記憶體使用
free -h

# 虛擬記憶體統計
cat /proc/meminfo

# 程式記憶體映射
pmap -x <pid>
```

## 為什麼學習虛擬記憶體？

1. **作業系統**：核心概念
2. **效能調優**：了解交換行為
3. **除錯**：記憶體相關問題
4. **安全**：理解隔離機制

## 參考資源

- "Operating Systems: Three Easy Pieces"
- "Understanding the Linux Kernel"
- Linux 原始碼 mm/ 目錄
