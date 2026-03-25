# 分頁 (Paging)

## 概述

分頁是虛擬記憶體管理的一種機制，將虛擬記憶體和實體記憶體劃分為固定大小的頁面（通常 4KB）。分頁允許程式使用不連續的虛擬位址空間，同時實現記憶體保護和共享。

## 歷史

- **1962**：Fritz 首次提出分頁概念
- **1974**：Multics 實現分頁
- **1985**：Intel 80386 分頁硬體
- **現在**：所有現代作業系統使用分頁

## 分頁結構

### 1. 多級頁表

```
虛擬位址
  ↓
[頁目錄指標] → 頁目錄 (PGD)
  ↓
[頁目錄]     → 頁表中間 (PMD)
  ↓
[頁表]       → 頁表條目 (PTE)
  ↓
[頁表條目]   → 實體頁框
  ↓
實體位址 = 頁框號 × 頁面大小 + 頁內偏移
```

### 2. 頁面大小

```c
// 常見頁面大小
#define PAGE_SHIFT   12
#define PAGE_SIZE    (1 << PAGE_SHIFT)  // 4KB
#define PAGE_MASK    (~(PAGE_SIZE - 1))

// 大頁面支援
2MB 頁面：PAGE_SHIFT + 9 = 21
1GB 頁面：PAGE_SHIFT + 9 + 9 = 30
```

### 3. 頁表條目結構

```c
// x86-64 頁表條目
typedef struct {
    uint64_t present : 1;
    uint64_t writable : 1;
    uint64_t user : 1;
    uint64_t pwt : 1;
    uint64_t pcd : 1;
    uint64_t accessed : 1;
    uint64_t dirty : 1;
    uint64_t pat : 1;
    uint64_t global : 1;
    uint64_t available : 3;
    uint64_t page_frame : 40;
    uint64_t nx : 1;
    uint64_t available : 7;
    uint64_t reserved : 12;
} pte_t;
```

### 4. 建立分頁映射

```c
// 建立虛擬到實體映射
void map_page(uint64_t virtual_addr, uint64_t physical_addr,
              uint64_t flags) {
    uint64_t pgd_index = (virtual_addr >> 39) & 0x1FF;
    uint64_t pmd_index = (virtual_addr >> 30) & 0x1FF;
    uint64_t pte_index = (virtual_addr >> 21) & 0x1FF;
    uint64_t page_index = (virtual_addr >> 12) & 0x1FF;
    
    pgd_t *pgd = get_pgd();
    pmd_t *pmd = (pgd + pgd_index);
    pte_t *pte = (pmd + pmd_index);
    
    // 設定 PTE
    pte->present = 1;
    pte->writable = (flags & PROT_WRITE) ? 1 : 0;
    pte->page_frame = physical_addr >> 12;
    pte->nx = (flags & PROT_EXEC) ? 0 : 1;
    
    // 使 TLB 無效
    invalidate_tlb(virtual_addr);
}
```

### 5. 頁面錯誤處理

```c
// 處理分頁錯誤
int handle_page_fault(unsigned long address, int error_code) {
    struct vm_area_struct *vma;
    
    // 查詢 VMA
    vma = find_vma(current->mm, address);
    if (!vma)
        return -1;
    
    // 檢查錯誤類型
    if (error_code & 0x01) {
        // 寫入保護
        if (!(vma->vm_flags & VM_WRITE))
            return -1;
        // COW 處理
        do_wp_page(vma, address);
    } else {
        // 讀取/執行保護
        if (error_code & 0x10) {
            // 執行保護
        }
        // 需求分頁
        do_page_fault(vma, address);
    }
    
    return 0;
}
```

### 6. 交換（Swapping）

```c
// 頁面置換演算法 - LRU

struct page {
    unsigned long flags;
    struct list_head lru;
    atomic_t _refcount;
};

// 換出頁面
void swap_out(struct page *page) {
    // 寫回磁碟
    write_to_swap(page);
    // 清除頁表
    clear_page_table(page);
    // 標記為不在記憶體
    page->flags &= ~PG_incore;
}
```

## 分頁優化

### 1. 大頁面

```bash
# Linux 大頁面
# 暫時大頁面
echo 1024 > /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages

# 透明大頁面
echo always > /sys/kernel/mm/transparent_hugepage/enabled
```

### 2. 記憶體壓縮

```c
// zswap - 記憶體壓縮
// 當交換空間不足時使用
```

## 為什麼學習分頁？

1. **作業系統核心**：虛擬記憶體實現
2. **效能優化**：大頁面、TLB
3. **安全**：記憶體隔離
4. **除錯**：記憶體相關問題

## 參考資源

- Intel 開發者手冊 Vol. 3
- "Operating Systems: Three Easy Pieces"
- Linux 核心原始碼
