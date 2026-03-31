# ARM (Advanced RISC Machines)

## 概述

ARM 是一種精簡指令集計算（RISC）架構，廣泛用於行動裝置、嵌入式系統和物聯網。ARM 以低功耗著稱，幾乎所有智慧手機和平板電腦都使用 ARM 處理器。Apple 的 M 系列晶片也基於 ARM。

## 歷史

- **1985**：Acorn 推出 ARM1 原型
- **1990**：ARM 公司成立
- **2005**：ARMv6
- **2011**：ARMv8（64-bit）
- **2020**：ARMv9
- **現在**：行動裝置主流架構

## ARM 暫存器

### 1. ARM64 (AArch64) 暫存器

```asm
; 通用暫存器（64-bit）
x0-x30          ; 函數參數和返回值
sp              ; 堆疊指標
pc              ; 程式計數器
xzr             ; 零暫存器（唯讀）

; 32-bit 部分
w0-w30          ; 低 32 位元
wzr             ; 32-bit 零暫存器

; 特殊暫存器
x29 = fp        ; 框架指標
x30 = lr        ; 連結暫存器
```

### 2. ARM32 暫存器

```asm
; ARMv7 暫存器
r0-r12          ; 通用暫存器
r13 = sp        ; 堆疊指標
r14 = lr        ; 連結暫存器
r15 = pc        ; 程式計數器
cpsr            ; 程式狀態暫存器
```

## 基本指令

### 1. 資料處理

```asm
; 算術
add x0, x1, x2      ; x0 = x1 + x2
add x0, x1, #5      ; x0 = x1 + 5
sub x0, x1, x2      ; x0 = x1 - x2
mul x0, x1, x2      ; x0 = x1 * x2

; 邏輯
and x0, x1, x2      ; x0 = x1 & x2
orr x0, x1, x2      ; x0 = x1 | x2
eor x0, x1, x2      ; x0 = x1 ^ x2
mov x0, x1          ; x0 = x1

; 移位
lsl x0, x1, #4      ; x0 = x1 << 4
lsr x0, x1, #4      ; x0 = x1 >> 4
asr x0, x1, #4      ; 算術右移
```

### 2. 記憶體操作

```asm
; 載入/儲存
ldr x0, [x1]        ; x0 = *x1
str x0, [x1]        ; *x1 = x0
ldp x0, x1, [x2]    ; 載入一對
stp x0, x1, [x2]    ; 儲存一對

; 立即數偏移
ldr x0, [x1, #8]    ; x0 = *(x1 + 8)
str x0, [x1, #-8]   ; *(x1 - 8) = x0

; 註冊偏移
ldr x0, [x1, x2]    ; x0 = *(x1 + x2)
```

### 3. 控制流

```asm
; 跳轉
b label             ; 無條件跳轉
beq label           ; 等於跳轉
bne label           ; 不等於跳轉
bl label            ; 跳轉並連結（函數呼叫）

; 條件標誌
cbz x0, label       ; x0 為 0 跳轉
cbnz x0, label      ; x0 不為 0 跳轉

; 函數返回
ret                 ; 返回（返回到 lr）
```

### 4. 函數框架

```asm
; 函數 prologue
stp x29, x30, [sp, #-16]!
mov x29, sp

; 函數 epilogue
ldp x29, x30, [sp], #16
ret

; 系統呼叫
mov x8, 60          ; exit 系統呼叫號
mov x0, 0           ; 退出碼
svc #0              ; 系統呼叫
```

### 5. 完整範例

```asm
.section .text
.globl _start

_start:
    mov x0, 5
    mov x1, 3
    add x0, x0, x1
    
    mov x8, 93      ; exit
    svc #0

// 等價 C 程式：
// int main() { return 5 + 3; }
```

## 條件執行

```asm
; ARM 條件標誌
; N (negative), Z (zero), C (carry), V (overflow)

; 條件後綴
eq  ; 等於
ne  ; 不等於
gt  ; 大於
lt  ; 小於
ge  ; 大於等於
le  ; 小於等於

; 條件執行指令
csel x0, x1, x2, eq  ; 如果 eq，x0 = x1 否則 x0 = x2
```

## ARM 的特點

1. **RISC 設計**：固定長度指令，LOAD/STORE 架構
2. **條件執行**：大多数指令可條件執行
3. **移位配合**：移位可與指令組合
4. **精簡**：指令數量少，功耗低

## 為什麼學習 ARM？

1. **行動開發**：手機/平板主流架構
2. **嵌入式系統**：物聯網設備
3. **Apple 生態**：M 系列晶片
4. **逆向工程**：行動應用分析

## 參考資源

- ARM Architecture Reference Manual
- "ARM Assembly Language Programming"
- ARM Developer Documentation
