# RISC-V

## 概述

RISC-V 是一種開源的指令集架構（ISA），於 2010 年在 UC Berkeley 開發。作為開源標準，RISC-V 不受專利限制，廣受學術界和產業界歡迎，被視為未來物聯網和客製化晶片的理想選擇。

## 歷史

- **2010**：UC Berkeley 開始設計
- **2015**：RISC-V 基金會成立
- **2019**：RISC-V International 成立
- **現在**：數百家廠商支援

## RISC-V 模組化設計

### 1. 基本擴展

```
RV32I / RV64I  ; 基本整數指令集（必須）
M              ; 整數乘除法
A              ; 原子操作
F              ; 單精度浮點
D              ; 雙精度浮點
C              ; 壓縮指令（16-bit）
```

### 2. 暫存器

```asm
; RV32I 暫存器
x0              ; 零暫存器（常數 0）
x1 = ra         ; 返回位址
x2 = sp         ; 堆疊指標
x3 = gp         ; 全域指標
x4 = tp         ; 執行緒指標
x5-x7 = t0-t2   ; 暫存器
x8 = fp / s0    ; 框架/保存暫存器
x9 = s1         ; 保存暫存器
x10-x11 = a0-a1 ; 函數參數/返回值
x12-x17 = a2-a7 ; 函數參數
x18-x27 = s2-s11; 保存暫存器
x28-x31 = t3-t6 ; 暫存器

; 浮點暫存器（RV32F）
ft0-ft7         ; 暫存器
fa0-fa1         ; 參數/返回值
fs0-fs11        ; 保存暫存器
ft8-ft31        ; 暫存器
```

## 基本指令

### 1. 整數運算

```asm
add x3, x1, x2      ; x3 = x1 + x2
addi x3, x1, 10    ; x3 = x1 + 10
sub x3, x1, x2     ; x3 = x1 - x2
mul x3, x1, x2     ; x3 = x1 * x2
div x3, x1, x2     ; x3 = x1 / x2
rem x3, x1, x2     ; x3 = x1 % x2
```

### 2. 邏輯與移位

```asm
and x3, x1, x2      ; x3 = x1 & x2
or x3, x1, x2      ; x3 = x1 | x2
xor x3, x1, x2     ; x3 = x1 ^ x2
slli x3, x1, 4     ; x3 = x1 << 4
srli x3, x1, 4     ; x3 = x1 >> 4 (邏輯)
srai x3, x1, 4     ; x3 = x1 >> 4 (算術)
```

### 3. 記憶體操作

```asm
lw x1, 0(x2)       ; x1 = memory[x2+0]
lui x1, 0x12345    ; x1 = 0x12345 << 12
auipc x1, 0        ; x1 = PC + (立即數 << 12)

; 載入與儲存
lb x1, 0(x2)       ; 載入 byte
lh x1, 0(x2)       ; 載入 halfword
lw x1, 0(x2)       ; 載入 word
sd x1, 0(x2)       ; 儲存 doubleword
sw x1, 0(x2)       ; 儲存 word
```

### 4. 控制流

```asm
beq x1, x2, label      ; if (x1 == x2) goto label
bne x1, x2, label     ; if (x1 != x2) goto label
blt x1, x2, label     ; if (x1 < x2) goto label
bge x1, x2, label     ; if (x1 >= x2) goto label

jal x1, label         ; x1 = PC+4; goto label (函數呼叫)
jalr x1, 0(x2)       ; x1 = PC+4; PC = x2
```

### 5. 完整範例

```asm
.section .text
.globl _start

_start:
    li x5, 5           ; x5 = 5 (立即數)
    li x6, 3           ; x6 = 3
    add x5, x5, x6     ; x5 = x5 + x6
    
    li x8, 60          ; exit 系統呼叫
    li x7, 0           ; 退出碼
    ecall              ; 系統呼叫
```

## 擴展指令

### 1. 原子操作（RV32A）

```asm
amoadd.w x5, x6, (x7)     ; atomic add
amoswap.w x5, x6, (x7)    ; atomic swap
lr.w x5, (x7)             ; load-reserve
sc.w x5, x6, (x7)         ; store-conditional
```

### 2. 壓縮指令（RV32C）

```asm
; 16-bit 壓縮版本
c.addi x5, 10     ; 短 immediate add
c.lw x5, 0(x6)    ; 短 load word
c.sw x5, 0(x6)    ; 短 store word
c.j label         ; 短跳轉
c.beqz x5, label  ; 條件跳轉
```

## 為什麼學習 RISC-V？

1. **開源自由**：無專利費用
2. **教學價值**：簡單清晰的設計
3. **客製化**：靈活的擴展機制
4. **物聯網**：未來主流架構之一

## 參考資源

- RISC-V Specification
- RISC-V International
- "Computer Organization and Design RISC-V Edition"
