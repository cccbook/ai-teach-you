# 24. 計時器中斷——Preemptive Scheduling

## 24.1 為什麼需要搶佔式排程？

合作式多工的問題：
- 任務可能永遠不讓出 CPU
- 系統可能無回應

搶佔式多工的優點：
- OS 可以強制切換任務
- 更公平的 CPU 分配
- 更好的系統回應性

## 24.2 RISC-V 中斷機制

### 24.2.1 中斷類型

| 類型 | 名稱 | 說明 |
|------|------|------|
| 同步 | Exception | 指令執行時發生 |
| 非同步 | Interrupt | 外部設備觸發 |

非同步中斷分為：
- **Machine Timer Interrupt** (mti)：計時器中斷
- **Machine Software Interrupt** (msi)：軟體中斷
- **Machine External Interrupt** (mei)：外部中斷

### 24.2.2 關鍵 CSR

| CSR | 名稱 | 用途 |
|-----|------|------|
| mstatus | Machine Status | 全域中斷開關 |
| mie | Machine Interrupt Enable | 各類中斷使能 |
| mtvec | Machine Trap Vector | 中斷向量位址 |
| mip | Machine Interrupt Pending | 待處理中斷標誌 |
| mepc | Machine Exception PC | 例外發生時的 PC |
| mcause | Machine Cause | 例外/中斷原因 |

### 24.2.3 mstatus 暫存器

```
位元 3: MIE - Machine Interrupt Enable
       1 = 使能機器模式中斷
       0 = 停用機器模式中斷

位元 7: MPIE - Machine Previous Interrupt Enable
       保存進入中斷前的 MIE 值
```

### 24.2.4 mie 暫存器

```
位元 3: MTIE - Machine Timer Interrupt Enable
位元 7: MSIE - Machine Software Interrupt Enable  
位元 11: MEIE - Machine External Interrupt Enable
```

### 24.2.5 mcause 暫存器

```
位元 31: 中斷標誌
       1 = 非同步中斷 (Interrupt)
       0 = 同步例外 (Exception)

位元 0-30: 例外/中斷代碼
       3 = Machine Software Interrupt
       7 = Machine Timer Interrupt
       11 = Machine External Interrupt
```

## 24.3 計時器設定

### 24.3.1 RISC-V 計時器

RISC-V 使用兩個 CSR：
- **mtime**：計時器計數（64 位元）
- **mtimecmp**：計時器比較值（64 位元）

當 `mtime >= mtimecmp` 時，觸發計時器中斷。

### 24.3.2 計時器暫存器位址

在 QEMU virt 平台上：
```
#define CLINT_BASE 0x2000000
#define MTIME       (CLINT_BASE + 0xBFF8)  // 計時器計數
#define MTIMECMP    (CLINT_BASE + 0x4000)  // 比較值
```

### 24.3.3 計時器初始化

```c
// timer.h
extern void timer_init(void);
extern void timer_handler(void);
extern void timer_load(int interval);

// timer.c
#define CLINT_BASE 0x2000000
#define MTIME       ((uint64_t*) (CLINT_BASE + 0xBFF8))
#define MTIMECMP    ((uint64_t*) (CLINT_BASE + 0x4000))

void timer_init(void) {
    timer_load(100000);  // 設定初始間隔
}

void timer_load(int interval) {
    // 設定下次中斷時間
    *MTIMECMP = *MTIME + interval;
}
```

## 24.4 中斷處理

### 24.4.1 trap.s - 中斷向量

```asm
.align 4
.globl trap_vector
trap_vector:
    # 保存上下文到任務堆疊
    sw ra, 0(sp)
    sw sp, 4(sp)
    # ... 其他暫存器
    sw s11, 52(sp)
    
    # 呼叫 C 處理函式
    csrr a0, mepc          # 取得例外 PC
    csrr a1, mcause         # 取得例外原因
    jal ra, trap_handler
    
    # 恢復上下文
    lw ra, 0(sp)
    lw sp, 4(sp)
    # ... 其他暫存器
    lw s11, 52(sp)
    
    mret                    # 從中斷返回
```

### 24.4.2 trap.c - 中斷處理函式

```c
reg_t trap_handler(reg_t epc, reg_t cause) {
    reg_t return_pc = epc;
    reg_t cause_code = cause & 0xfff;
    
    if (cause & 0x80000000) {  // 非同步中斷
        switch (cause_code) {
        case 7:  // 計時器中斷
            timer_handler();
            break;
        default:
            lib_puts("Unknown interrupt!\n");
            break;
        }
    } else {  // 同步例外
        lib_puts("Sync exception!\n");
    }
    
    return return_pc;
}
```

## 24.5 計時器中斷處理

### 24.5.1 timer_handler

```c
void timer_handler(void) {
    // 設定下次中斷
    timer_load(100000);
    
    // 計時器中斷時，強制切換到 OS
    // OS 的排程器會選擇下一個任務
}
```

## 24.6 搶佔式排程整合

### 24.6.1 trap.c 完整實現

```c
reg_t trap_handler(reg_t epc, reg_t cause) {
    reg_t return_pc = epc;
    reg_t cause_code = cause & 0xfff;
    
    if (cause & 0x80000000) {
        switch (cause_code) {
        case 3:  // 軟體中斷
            lib_puts("Software interrupt!\n");
            break;
        case 7:  // 計時器中斷
            lib_puts("Timer interrupt!\n");
            timer_handler();
            // 返回 OS 而不是任務
            return_pc = (reg_t)&os_kernel;
            break;
        case 11:  // 外部中斷
            lib_puts("External interrupt!\n");
            break;
        }
    }
    return return_pc;
}
```

### 24.6.2 trap_init

```c
void trap_init(void) {
    // 設定中斷向量
    w_mtvec((reg_t)trap_vector);
    
    // 使能計時器中斷
    w_mstatus(r_mstatus() | MSTATUS_MIE);
    w_mie(r_mie() | MIE_MTIE);  // 使能機器計時器中斷
}
```

## 24.7 搶佔式排程流程

```
                    計時器中斷觸發
                          │
                          ↓
              ┌───────────────────────────┐
              │ trap_vector (asm)        │
              │   保存任務上下文          │
              └───────────────────────────┘
                          │
                          ↓
              ┌───────────────────────────┐
              │ trap_handler (C)        │
              │   timer_handler()       │
              │   return_pc = os_kernel │
              └───────────────────────────┘
                          │
                          ↓
              ┌───────────────────────────┐
              │ 恢復上下文 (asm)          │
              │ mret → 返回 os_kernel    │
              └───────────────────────────┘
                          │
                          ↓
              ┌───────────────────────────┐
              │ os_kernel()              │
              │   排程下一個任務          │
              │   task_go(&tasks[next])  │
              └───────────────────────────┘
```

## 24.8 與合作式排程的比較

| 特性 | 合作式 | 搶佔式 |
|------|--------|--------|
| 切換時機 | 任務自願讓出 | 計時器中斷 |
| 公平性 | 不公平 | 公平 |
| 複雜度 | 簡單 | 複雜 |
| 即時性 | 低 | 高 |

## 24.9 執行測試

```bash
cd _code/mini-riscv-os/04-TimerInterrupt
make
make qemu
```

或搶佔式排程：
```bash
cd _code/mini-riscv-os/05-Preemptive
make
make qemu
```

## 24.10 mret 指令

`mret` 是從機器模式中斷返回的指令：

```asm
mret
```

相當於：
```
mepc = pc
mstatus.MPIE → mstatus.MIE  # 恢復中斷狀態
pc = mepc                     # 跳回中斷發生時的 PC
```

## 24.11 小結

本章節我們學習了：
- RISC-V 中斷機制
- mstatus、mie、mcause 等 CSR
- 計時器設定（mtime/mtimecmp）
- 中斷向量處理
- trap_handler 的實現
- 搶佔式排程的流程

## 24.12 習題

1. 實現動態調整時間片大小
2. 為什麼需要保存和恢復所有 s 暫存器？
3. 研究中斷嵌套的可能性和實現
4. 實現統計每個任務的 CPU 使用時間
5. 比較 RISC-V 的中斷機制和 ARM Cortex-M
