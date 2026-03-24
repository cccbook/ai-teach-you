# 22. 從特權模式切換——Context Switch 基礎

## 22.1 什麼是 Context Switch？

Context Switch（上下文切換）是作業系統將 CPU 從一個任務切換到另一個任務的過程。

```
任務 A                          任務 B
   │                               │
   │  ┌─────────────────────┐      │
   │  │ 1. 保存任務 A 的狀態 │      │
   │  │ 2. 載入任務 B 的狀態 │      │
   │  └─────────────────────┘      │
   │                               │
   ↓                               ↓
CPU 執行任務 A                  CPU 執行任務 B
```

## 22.2 任務狀態

任務的狀態包含：
- **程式計數器 (PC)**：下一條要執行的指令
- **堆疊指標 (SP)**：任務的堆疊頂端
- **通用暫存器**：s0-s11（保存的暫存器）

## 22.3 程式碼結構

### 22.3.1 結構定義 (os.h)

```c
#include "riscv.h"

extern int os_main(void);
```

### 22.3.2 Context 結構 (riscv.h)

定義在 riscv.h 中：
```c
struct context {
    reg_t ra;
    reg_t sp;
    reg_t s0;
    reg_t s1;
    // ... s2-s11
};
```

### 22.3.3 任務程式 (user.c)

```c
void user_task0(void) {
    lib_puts("Task0: Context Switch Success !\n");
    while (1) {}
}
```

### 22.3.4 OS 主程式 (os.c)

```c
#include "os.h"

#define STACK_SIZE 1024
reg_t task0_stack[STACK_SIZE];  // 任務的堆疊
struct context ctx_os;           // OS 的上下文
struct context ctx_task;         // 任務的上下文

extern void sys_switch();

void user_task0(void) {
    lib_puts("Task0: Context Switch Success !\n");
    while (1) {}
}

int os_main(void) {
    lib_puts("OS start\n");
    
    // 初始化任務上下文
    ctx_task.ra = (reg_t) user_task0;           // 返回位址 = 任務入口
    ctx_task.sp = (reg_t) &task0_stack[STACK_SIZE-1];  // 堆疊頂端
    
    // 切換到任務
    sys_switch(&ctx_os, &ctx_task);
    
    return 0;
}
```

## 22.4 Context Switch 實作

### 22.4.1 sys.s - 組合語言

```asm
# ============ 巨集定義 ==================
.macro ctx_save base
    sw ra, 0(\base)     # 保存返回位址
    sw sp, 4(\base)     # 保存堆疊指標
    sw s0, 8(\base)     # 保存 s0
    sw s1, 12(\base)    # 保存 s1
    # ... s2-s11 同樣處理
    sw s11, 52(\base)
.endm

.macro ctx_load base
    lw ra, 0(\base)     # 恢復返回位址
    lw sp, 4(\base)     # 恢復堆疊指標
    lw s0, 8(\base)     # 恢復 s0
    lw s1, 12(\base)    # 恢復 s1
    # ... s2-s11 同樣處理
    lw s11, 52(\base)
.endm
# =========================================

# Context Switch 函式
# void sys_switch(struct context *old, struct context *new);
#
# 保存目前狀態到 old，載入 new 的狀態

.globl sys_switch
.align 4
sys_switch:
    ctx_save a0          # 保存舊上下文 (a0 = old)
    ctx_load a1          # 載入新上下文 (a1 = new)
    ret                  # 返回，相當於跳到 new->ra
```

## 22.5 切換流程圖

```
                    sys_switch(&ctx_os, &ctx_task)
                                    │
                                    ↓
                        ┌───────────────────────┐
                        │ ctx_save(ctx_os)      │
                        │   保存 ra → ctx_os.ra │
                        │   保存 sp → ctx_os.sp │
                        │   保存 s0 → ctx_os.s0 │
                        │   ...                 │
                        └───────────────────────┘
                                    │
                                    ↓
                        ┌───────────────────────┐
                        │ ctx_load(ctx_task)    │
                        │   恢復 ra = ctx_task.ra │
                        │   恢復 sp = ctx_task.sp │
                        │   恢復 s0 = ctx_task.s0 │
                        │   ...                 │
                        └───────────────────────┘
                                    │
                                    ↓
                                ret
                                    │
                                    ↓
                    跳到 ctx_task.ra = user_task0
                                    │
                                    ↓
                        user_task0() 開始執行
```

## 22.6 為什麼要保存這些暫存器？

RISC-V 呼叫約定：
- **Caller-saved** (t0-t6, a0-a7, ra)：呼叫者負責保存
- **Callee-saved** (s0-s11)：被呼叫者負責保存

`sys_switch` 是一個普通函式呼叫，編譯器會：
- Caller-saved：由於是 call 指令呼叫，ra 已經自動保存
- Callee-saved：如果我們要保持這些值，必須手動保存

我們保存 s0-s11，因為任務可能會使用它們，而任務切換不應該破壞這些值。

## 22.7 任務堆疊

### 22.7.1 堆疊配置

```
高位址
+------------------+  ← task0_stack[STACK_SIZE-1]
|  (堆疊頂端)      |  ← ctx_task.sp 指向這裡
|  ...             |
|  (堆疊成長方向)   |
|  ...             |
|                  |
+------------------+  ← task0_stack[0]
低位址
```

### 22.7.2 為什麼要給任務獨立堆疊？

如果任務和 OS 共用堆疊：
- 任務函式返回時，會回到 OS 的程式碼
- 任務呼叫函式時，會污染 OS 的堆疊
- 巢狀呼叫會造成混亂

## 22.8 執行流程分析

### 初始狀態
```
ctx_os:  (未初始化)
ctx_task: {
    ra = user_task0,    // 任務入口
    sp = &task0_stack[STACK_SIZE-1],
    s0-s11 = 0
}
```

### 執行 sys_switch

1. 儲存目前狀態：
```
ctx_os: {
    ra = (sys_switch 返回後的位址),
    sp = (當前 sp),
    s0-s11 = (當前值)
}
```

2. 載入任務狀態：
```
sp = &task0_stack[STACK_SIZE-1]  // 切換堆疊
ra = user_task0                    // 設定返回位址
s0-s11 = 0                         // 初始化為 0
```

3. ret 指令執行：
```
pc = ra = user_task0  // 跳到 user_task0
```

## 22.9 與 xv6 的比較

xv6-riscv 的 `swtch.S` 幾乎相同：

```asm
# xv6-riscv/swtch.S
.globl swtch
swtch:
    sd ra, 0(a0)
    sd sp, 8(a0)
    sd s0, 16(a0)
    # ... 其他 s 暫存器
    ld ra, 0(a1)
    ld sp, 8(a1)
    ld s0, 16(a1)
    # ... 其他 s 暫存器
    ret
```

主要差異：
- xv6 使用 64 位元 (`sd`/`ld`)
- mini-riscv-os 使用 32 位元 (`sw`/`lw`)

## 22.10 實際執行

```bash
cd _code/mini-riscv-os/02-ContextSwitch
make
make qemu
```

輸出：
```
OS start
Task0: Context Switch Success !
```

## 22.11 小結

本章節我們學習了：
- Context Switch 的概念
- 任務狀態的組成（PC、SP、s0-s11）
- Context 結構的定義
- sys_switch 函式的實作
- 任務獨立堆疊的必要性
- 從 OS 切換到任務的完整流程

## 22.12 習題

1. 為什麼 sys_switch 要保存 ra？有什麼用？
2. 嘗試添加 s0 的保存和恢復
3. 修改程式讓任務 A 和任務 B 來回切換
4. 為什麼不能只保存/恢復 sp？
5. 研究 C 語言的 `setjmp`/`longjmp` 與 context switch 的關係
