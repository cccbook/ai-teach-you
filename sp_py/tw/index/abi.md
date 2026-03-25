# ABI (Application Binary Interface)

## 概述

ABI 定義了應用程式和作業系統之間的低層級介面，規範了函數呼叫約定、系統呼叫、資料結構佈局等。與 API 不同，ABI 關注二進制層面的相容性，確保不同編譯器編譯的程式碼可以相互操作。

## 歷史

- **1980s**：早期 Unix 系統開始標準化
- **1990s**：C++ ABI 出現
- **2010s**：ARM ABI 標準化
- **現在**：每個平台有各自的 ABI

## 函數呼叫約定

### 1. x86-64 System V ABI

```asm
; 參數傳遞順序（從左到右）
; rdi, rsi, rdx, rcx, r8, r9
; 剩餘參數透過堆疊

; 函數呼叫過程：
; 1. 參數放入暫存器
; 2. call function  (push 返回位址)
; 3. 函數 prologue
; 4. 返回值在 rax (或 rax:rdx for 128-bit)

; 呼叫方保存：rax, rcx, rdx, rsi, rdi, r8-r11
; 被呼叫方保存：rbx, rbp, r12-r15
```

### 2. ARM64 AAPCS64

```asm
; 參數傳遞
; x0-x7: 前 8 個參數
; 多餘參數在堆疊上

; 返回值
; x0: 第一返回值
; x1-x7: 更多返回值

; 呼叫方保存：x19-x28
; 被呼叫方保存：x19-x28
```

### 3. 資料對齊

```c
struct Data {
    char c;      // offset 0
    int i;       // offset 4 (可能需要對齊到 4)
    long long l; // offset 8
};

// 結構體大小通常是最大成員的倍數
```

## 系統呼叫介面

### 1. Linux x86-64

```asm
; 系統呼叫：syscall 指令
; 系統呼叫號：rax
; 參數：rdi, rsi, rdx, r10, r8, r9
; 返回值：rax

; write(fd, buf, count)
mov rax, 1        ; write 系統呼叫號
mov rdi, 1        ; fd = 1 (stdout)
lea rsi, [rel msg] ; buf
mov rdx, 13       ; count
syscall
```

### 2. Linux ARM64

```asm
; 系統呼叫：svc #0
; 系統呼叫號：x8
; 參數：x0-x5
; 返回值：x0

mov x8, 64        ; exit 系統呼叫號
mov x0, 0         ; 退出碼
svc #0
```

## 符號名稱修飾

### 1. C++ 名稱修飾

```c++
// 原始
int function(int a, double b);
int class::method(int);

// 修飾後（可能的格式）
_Z8functionid
_ZN5class6methodEi
```

### 2. 函數指標

```c
// 函數指標類型
typedef int (*func_ptr)(int, int);
func_ptr f = &add;
```

## 為什麼學習 ABI？

1. **跨語言**：混合 C/C++ 和其他語言
2. **系統程式設計**：驅動程式開發
3. **效能優化**：理解呼叫開銷
4. **除錯**：二進制相容性問題

## 參考資源

- System V ABI
- ARM AAPCS64
- "Linkers and Loaders"
