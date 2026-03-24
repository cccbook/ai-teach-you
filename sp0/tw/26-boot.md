# 26. 開機程序——從 BIOS 到核心

## 26.1 開機流程概述

xv6 的開機流程：

```
QEMU 載入 kernel/kernel
         ↓
 entry.S (核心入口)
         ↓
 start.c (機器模式設定)
         ↓
 main.c (核心初始化)
         ↓
 user init (第一個使用者行程)
```

## 26.2 核心入口 (entry.S)

```asm
# kernel/entry.S
    .section .text
    .globl _entry
_entry:
    # 設定暫存器
    la sp, bootstacktop    # 設定堆疊
    tail main              # 跳到 main
    .section .data
    .globl bootstack
bootstack:
    .space 4096 * 4       # 4KB 核心堆疊
    .globl bootstacktop
bootstacktop:
```

## 26.3 核心初始化 (start.c)

在 C 程式碼執行前，必須設定：

```c
// kernel/start.c
void start() {
    // 設定機器模式計時器
    // ...
    
    // 設定 MIE 使能計時器中斷
    w_mie(r_mie() | MIE_MEIE | MIE_MTIE | MIE_MSIE);
    
    // 設定返回到 S 模式
    unsigned long x = r_mstatus();
    x &= ~MSTATUS_MPP_MASK;  // 清除 MPP
    x |= MSTATUS_MPP_S;       // 設定 MPP 為 Supervisor
    w_mstatus(x);
    
    // 設定 mepc 為 main
    w_mepc((uint64_t)main);
    
    // 設定分頁
    w_satp(MAKE_SATP(kernel_pagetable));
    
    // 刷新 TLB
    sfence_vma();
    
    // 返回到 S 模式，會跳到 main()
    asm volatile("mret");
}
```

## 26.4 主初始化 (main.c)

```c
// kernel/main.c
extern char end[];  // 核心結束位址

int main() {
    // 初始化各種子系統
    consoleinit();    // 主控台
    printfinit();     // printf
    pinit();          // 行程表
    binit();          // 區塊 I/O
    loginit();        // 日誌
    fileinit();       // 檔案表
    fsinit();         // 檔案系統
    
    // 讀取開機參數
    binit();
    
    // 開機行程
    userinit();
    
    // 排程器
    scheduler();
}
```

## 26.5 第一個使用者行程

```c
// kernel/proc.c
void userinit(void) {
    struct proc *p = allocproc();
    
    // 設定初始程式碼
    p->pagetable = proc_pagetable(p);
    
    // 複製 initcode 到行程空間
    uvminit(p->pagetable, initcode, sizeof(initcode));
    p->sz = PGSIZE;
    
    // 設定使用者堆疊
    p->tf->sp = PGSIZE;
    
    // 設定返回位址
    p->tf->epc = 0;  // 從位址 0 開始執行
    
    safestrcpy(p->name, "initcode", sizeof(p->name));
    p->state = RUNNABLE;
}
```

## 26.6 排程器

```c
// scheduler() 選擇下一個執行的行程
void scheduler(void) {
    struct proc *p;
    
    for (;;) {
        // 找出可執行的行程
        for (p = proc; p < &proc[NPROC]; p++) {
            acquire(&p->lock);
            if (p->state == RUNNABLE) {
                p->state = RUNNING;
                p->pid = ...;
                
                // 切換到行程
                swtch(&c->context, &p->context);
                
                // 行程返回後，繼續尋找
            }
            release(&p->lock);
        }
    }
}
```

## 26.7 中斷返回到使用者

```c
// kernel/trampoline.S
.globl uservec
uservec:
    # 儲存使用者狀態
    # ...
    ret

.globl userret
userret:
    # 恢復使用者狀態
    # ...
    sret
```

## 26.8 小結

本章節我們學習了：
- xv6 的開機流程
- 核心入口點設定
- 機器模式到主管模式的轉換
- 核心初始化序列
- 第一個使用者行程的建立
- 排程器的工作方式

## 26.9 習題

1. 追蹤 xv6 的開機日誌
2. 研究 mstatus.MPP 的意義
3. 為什麼需要 trampoline 頁面？
4. 分析 scheduler() 如何實現 Round-Robin
5. 研究 xv6 如何初始化分頁表
