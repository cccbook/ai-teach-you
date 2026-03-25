# MMU (Memory Management Unit)

## 概述

MMU（記憶體管理單元）是 CPU 中負責記憶體位址轉換和存取控制的硬體單元。MMU 支援虛擬記憶體，提供程序間的記憶體隔離、讓程式使用比實際物理記憶體更大的位址空間，並實現記憶體保護。

## 歷史

- **1960s**：IBM 引入分頁概念
- **1974**：Intel 8086（沒有 MMU）
- **1985**：Intel 80386 引入 MMU
- **現在**：所有現代 CPU 內建 MMU

## MMU 功能

### 1. 位址轉換

```
虛擬位址 → MMU → 實體位址
```

```c
// 虛擬位址結構（典型 32-bit）
// [31:22] 目錄索引 (10 bits)
// [21:12] 頁表索引 (10 bits)
// [11:0]  頁內偏移  (12 bits)

// 64-bit 簡化
// [63:39] 頁目錄指標 (PDPTE)
// [38:30] 頁目錄 (PDE)
// [29:21] 頁表 (PTE)
// [20:12] 大頁
// [11:0]  偏移
```

### 2. 頁面保護

```c
// 頁表條目權限
PTE_PRESENT = 0x01   // 頁面存在
PTE_WRITABLE = 0x02  // 可寫
PTE_USER = 0x04      // 用戶態可訪問
PTE_NX = 0x8000000000000000 // 無執行

// 檢查存取權限
if (!(pte & PTE_PRESENT)) {
    // 頁面錯誤
}
if (!(pte & PTE_WRITABLE) && write_access) {
    // 寫入保護錯誤
}
```

### 3. TLB（Translation Lookaside Buffer）

```c
// TLB 是一種硬體快取
// 儲存最近使用的虛擬到實體位址映射

// TLB 條目結構
struct TLBEntry {
    uint64_t virtual_page;
    uint64_t physical_frame;
    uint8_t  valid;
    uint8_t  dirty;
    uint8_t  access_rights;
};

// TLB 操作
void invalidate_tlb_entry(uint64_t vaddr);
void flush_tlb_all();
```

### 4. MMU 初始化（ARM64 範例）

```asm
; 設定頁表基底位址
mov x0, xzr
msr ttbr0_el1, x0    ; 清除 TLB

; 設定 TCR（Translation Control Register）
mov x0, #(0b01 << 0)  ; T0SZ = 4 (48-bit VA)
orr x0, x0, #(0b10 << 8)  ; EPD1
msr tcr_el1, x0

; 啟用 MMU
mrs x0, sctlr_el1
orr x0, x0, #1        ; M 位元
msr sctlr_el1, x0

; 指令同步
dsb ish
isb
```

### 5. Linux 頁表操作

```c
// Linux 核心頁表
typedef struct {
    unsigned long pte;
} pte_t;

// 建立頁表
pgd_t *pgd_alloc(struct mm_struct *mm);
pud_t *pud_alloc(pgd_t *pgd, unsigned long addr);
pmd_t *pmd_alloc(pud_t *pud, unsigned long addr);
pte_t *pte_alloc(pmd_t *pmd, unsigned long addr);

// 設定頁面權限
void set_pte(pte_t *ptep, pte_t pteval);
void set_pte_at(struct mm_struct *mm, unsigned long addr,
                pte_t *ptep, pte_t pteval);
```

### 6. 頁面錯誤處理

```c
// 頁面錯誤處理常式
void handle_page_fault(struct pt_regs *regs, unsigned long addr,
                       unsigned long error_code) {
    // error_code:
    // bit 0: 0=讀, 1=寫
    // bit 1: 0=對齊, 1=保護
    // bit 2: 0=使用者, 1=核心
    
    if (error_code & 0x01) {
        // 寫入錯誤 -> 可能是 COW
    }
    
    // 檢查是否為有效的虛擬位址
    if (!access_ok(addr)) {
        // 段錯誤
        do_sigbus();
        return;
    }
    
    // 處理分頁錯誤
    do_page_fault(regs, addr, error_code);
}
```

## 為什麼學習 MMU？

1. **作業系統**：理解虛擬記憶體
2. **系統程式設計**：驅動程式開發
3. **安全**：記憶體保護機制
4. **效能**：TLB 命中率優化

## 參考資源

- Intel/AMD 系統編程指南
- ARM 架構參考手冊
- "Understanding the Linux Kernel"
