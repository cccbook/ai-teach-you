# 11. Clang 前端——C 語言到 LLVM IR

## 11.1 Clang 簡介

Clang 是 LLVM 專案的一部分，是一個 C/C++/Objective-C 的編譯器前端。它以速度快、錯誤訊息清晰聞名。

```bash
# 基本用法
clang hello.c -o hello

# 生成 LLVM IR
clang -S -emit-llvm hello.c -o hello.ll

# 生成 Bitcode
clang -c -emit-llvm hello.c -o hello.bc
```

## 11.2 LLVM IR 簡介

LLVM IR（Intermediate Representation）是 LLVM 使用的中介表示語言。它：
- 是靜態單例形式（SSA）
- 有無限的虛擬寄存器
- 是型別安全的
- 可讀性高

## 11.3 簡單程式的 IR

原始碼：
```c
long long fact(long long n) {
    if (n <= 1) return 1;
    return n * fact(n - 1);
}
```

LLVM IR：
```llvm
define i64 @fact(i64 %n) {
entry:
    %cmp = icmp sle i64 %n, 1
    br i1 %cmp, label %then, label %else

then:
    ret i64 1

else:
    %sub = sub i64 %n, 1
    %call = call i64 @fact(i64 %sub)
    %mul = mul i64 %n, %call
    ret i64 %mul
}
```

## 11.4 IR 基本結構

### 11.4.1 模組（Module）

```llvm
; 模組開始
source_filename = "test.c"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "riscv64-unknown-linux-gnu"

; 定義
@global_var = global i32 42
@str = private constant [13 x i8] c"Hello World\00"

; 函式定義
define i64 @fact(i64 %n) {
entry:
    ; 指令
    ret i64 0
}
```

### 11.4.2 型別系統

| IR 型別 | C 對應 | 說明 |
|---------|--------|------|
| `i8` | `char` | 8 位元整數 |
| `i16` | `short` | 16 位元整數 |
| `i32` | `int` | 32 位元整數 |
| `i64` | `long long` | 64 位元整數 |
| `float` | `float` | 單精度浮點 |
| `double` | `double` | 雙精度浮點 |
| `i8*` | `char*` |指標 |
| `[N x i8]` | `char[N]` | 陣列 |

### 11.4.3 函式型別

```llvm
@func = declare i32 @external_func(i32 %a, i64 %b)
define i64 @fact(i64 %n) { ... }
define void @void_func() { ... }
```

## 11.5 使用 Clang 生成 IR

### 11.5.1 基本命令

```bash
# 生成可讀的 IR（-S）
clang -S -emit-llvm fact.c -o fact.ll

# 生成 Bitcode（-c）
clang -c -emit-llvm fact.c -o fact.bc

# 顯示最佳化前的 IR
clang -S -emit-llvm -O0 fact.c -o fact_O0.ll

# 顯示最佳化後的 IR（使用 LLVM pass）
clang -S -emit-llvm -O2 fact.c -o fact_O2.ll
```

### 11.5.2 指定目標架構

```bash
# RISC-V 64 位元
clang -S -emit-llvm \
    --target=riscv64 \
    -march=rv64g \
    -mabi=lp64d \
    fact.c -o fact.ll
```

### 11.5.3 查看產生的 IR

```bash
cat fact.ll
```

## 11.6 IR 指令詳解

### 11.6.1 算術指令

```llvm
%add = add i64 %a, %b      ; 加法
%sub = sub i64 %a, %b      ; 減法
%mul = mul i64 %a, %b      ; 乘法
%sdiv = sdiv i64 %a, %b    ; 有號除法
%udiv = udiv i64 %a, %b    ; 無號除法
%srem = srem i64 %a, %b    ; 有號餘數
%urem = urem i64 %a, %b    ; 無號餘數
```

### 11.6.2 位元指令

```llvm
%and = and i64 %a, %b       ; 位元 AND
%or = or i64 %a, %b        ; 位元 OR
%xor = xor i64 %a, %b      ; 位元 XOR
%shl = shl i64 %a, %b      ; 左移
%lshr = lshr i64 %a, %b    ; 邏輯右移
%ashr = ashr i64 %a, %b    ; 算術右移
```

### 11.6.3 比較指令

```llvm
%cmp = icmp eq i64 %a, %b     ; ==
%cmp = icmp ne i64 %a, %b     ; !=
%cmp = icmp slt i64 %a, %b    ; < (signed)
%cmp = icmp ult i64 %a, %b    ; < (unsigned)
%cmp = icmp sgt i64 %a, %b    ; > (signed)
%cmp = icmp sge i64 %a, %b    ; >= (signed)
```

### 11.6.4 記憶體指令

```llvm
%val = load i64, i64* %ptr        ; 載入
store i64 %val, i64* %ptr         ; 儲存
%addr = alloca i64                ; 配置本地空間
%addr = getelementptr i64, i64* %arr, i64 %idx  ; 取元素位址
```

### 11.6.5 控制流

```llvm
br label %dest              ; 無條件跳躍
br i1 %cond, label %if, label %else  ; 條件跳躍

%sel = select i1 %cond, i64 %a, i64 %b  ; 條件選擇

switch i64 %val, label %default [
    i64 0, label %case0
    i64 1, label %case1
]
```

## 11.7 完整範例分析

原始碼：
```c
#include <stdio.h>

int add(int a, int b) {
    return a + b;
}

int main() {
    int x = 10;
    int y = 20;
    int z = add(x, y);
    printf("%d + %d = %d\n", x, y, z);
    return 0;
}
```

產生的 IR：
```llvm
@.str = private constant [21 x i8] c"%d + %d = %d\0A\00"

define i32 @add(i32 %a, i32 %b) {
entry:
    %add = add i32 %a, %b
    ret i32 %add
}

define i32 @main() {
entry:
    %x = alloca i32
    %y = alloca i32
    %z = alloca i32
    store i32 10, i32* %x
    store i32 20, i32* %y
    %x_val = load i32, i32* %x
    %y_val = load i32, i32* %y
    %call = call i32 @add(i32 %x_val, i32 %y_val)
    store i32 %call, i32* %z
    %x_val2 = load i32, i32* %x
    %y_val2 = load i32, i32* %y
    %z_val = load i32, i32* %z
    %call2 = call i32 (i8*, ...) @printf(i8* getelementptr...)
    ret i32 0
}

declare i32 @printf(i8*, ...)
```

## 11.8 Clang 的其他功能

### 11.8.1 靜態分析

```bash
# 靜態分析
clang --analyze hello.c

# 使用 scan-build
scan-build clang hello.c -o hello
```

### 11.8.2 語法檢查

```bash
# 只做語法和語意檢查，不生成檔案
clang -fsyntax-only hello.c

# 顯示錯誤和警告
clang -Wall -Wextra -pedantic hello.c
```

### 11.8.3 依賴追蹤

```bash
# 生成依賴關係
clang -MM hello.c

# 生成系統框架依賴
clang -MMD -MF hello.d -c hello.c
```

## 11.9 使用 llvm-dis 查看 Bitcode

```bash
# Bitcode → IR
llvm-dis fact.bc -o fact_from_bc.ll

# 格式化輸出
llvm-dis fact.bc -o - | clang-format
```

## 11.10 小結

本章節我們學習了：
- Clang 編譯器前端的基本用法
- LLVM IR 的型別系統
- IR 的基本結構和指令
- 如何使用 Clang 生成和查看 IR
- IR 與 C 原始碼的對應關係

## 11.11 習題

1. 用 `clang -S -emit-llvm` 生成 cpy0 中 `fact.c` 的 IR
2. 比較 `-O0`、`-O1`、`-O2`、`-O3` 生成的 IR 有何不同
3. 為 cpy0 的 C 程式生成 RISC-V 目標的 IR
4. 研究 `getelementptr` 指令的用法
5. 寫一個簡單的 LLVM IR 程式並用 `lli` 執行
