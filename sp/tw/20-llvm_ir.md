# 20. LLVM IR——現代編譯器的中間表示

## 20.1 LLVM IR 簡介

LLVM IR（Intermediate Representation）是 LLVM 編譯器框架的核心。它是一種：
- **靜態單例形式 (SSA)**：每個變數只被賦值一次
- **型別安全**：所有值都有明確的型別
- **可讀**：幾乎像組語但更抽象

## 20.2 LLVM IR 基本語法

### 20.2.1 模組結構

```llvm
; ModuleID = 'module_name'
source_filename = "filename.c"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

; 全域變數
@global_var = global i32 42
@str = private constant [13 x i8] c"Hello World\00"

; 函式定義
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

declare i32 @printf(i8*, ...)
```

## 20.3 基本型別

| IR 型別 | C 對應 | 大小 |
|---------|--------|------|
| `i1` | `_Bool` | 1 位元 |
| `i8` | `char` | 8 位元 |
| `i16` | `short` | 16 位元 |
| `i32` | `int` | 32 位元 |
| `i64` | `long long` | 64 位元 |
| `half` | `__fp16` | 16 位元 |
| `float` | `float` | 32 位元 |
| `double` | `double` | 64 位元 |
| `void` | `void` | - |

## 20.4 複合型別

```llvm
; 指標
i32*                    ; int*
i8*                     ; char*

; 陣列
[10 x i32]              ; int[10]
[4 x i8]                ; char[4]

; 結構體
%struct.Point = type { i64, i64 }  ; struct Point { long long x, y; }

; 向量 (SIMD)
<4 x float>             ; __m128
```

## 20.5 全域符號

```llvm
; 常量
@pi = constant double 3.141592653589793

; 全域變數
@counter = global i32 0
@counter = uninitialized global i32 0

; 唯讀全域變數
@msg = constant [13 x i8] c"Hello World\00"
```

## 20.6 指令分類

### 20.6.1 二元運算

```llvm
; 算術
%add = add i32 %a, %b
%sub = sub i32 %a, %b
%mul = mul i32 %a, %b
%sdiv = sdiv i32 %a, %b      ; 有號除法
%udiv = udiv i32 %a, %b      ; 無號除法
%srem = srem i32 %a, %b      ; 有號餘數
%urem = urem i32 %a, %b      ; 無號餘數

; 位元
%and = and i32 %a, %b
%or  = or  i32 %a, %b
%xor = xor i32 %a, %b
%shl = shl i32 %a, %b
%lshr = lshr i32 %a, %b     ; 邏輯右移
%ashr = ashr i32 %a, %b     ; 算術右移
```

### 20.6.2 比較指令

```llvm
; 設定條件碼 (Set on Condition)
; 結果是 i1 (1 或 0)

%eq  = icmp eq   i32 %a, %b    ; ==
%ne  = icmp ne   i32 %a, %b    ; !=
%slt = icmp slt  i32 %a, %b    ; <  (signed)
%ult = icmp ult  i32 %a, %b    ; <  (unsigned)
%sle = icmp sle  i32 %a, %b    ; <= (signed)
%ule = icmp ule  i32 %a, %b    ; <= (unsigned)
%sgt = icmp sgt  i32 %a, %b    ; >  (signed)
%ugt = icmp ugt  i32 %a, %b    ; >  (unsigned)
%sge = icmp sge  i32 %a, %b    ; >= (signed)
%uge = icmp uge  i32 %a, %b    ; >= (unsigned)

; 浮點比較
%fcmp = fcmp oeq float %a, %b  ; ordered equal
%fcmp = fcmp one float %a, %b   ; ordered not equal
%fcmp = fcmp olt float %a, %b   ; ordered less than
```

### 20.6.3 記憶體指令

```llvm
; 配置本地空間 (在棧上)
%ptr = alloca i32              ; int* ptr = alloca(int);
%ptr = alloca i32, align 4     ; 4 位元組對齊

; 載入
%val = load i32, i32* %ptr     ; int val = *ptr;

; 儲存
store i32 %val, i32* %ptr      ; *ptr = val;

; 取元素指標
%elem = getelementptr i32, i32* %arr, i64 %idx
%val = load i32, i32* %elem
```

### 20.6.4 GetElementPtr (GEP)

GEP 是 LLVM 中計算指標偏移的標準方式：

```llvm
; 陣列元素
%arr = alloca [10 x i32]
%idx = load i64, i64* %idx_ptr
%elem_ptr = getelementptr [10 x i32], [10 x i32]* %arr, i64 0, i64 %idx
%val = load i32, i32* %elem_ptr

; 結構體成員
%pt = alloca %struct.Point
%x_ptr = getelementptr %struct.Point, %struct.Point* %pt, i64 0, i32 0
store i64 10, i64* %x_ptr
```

### 20.6.5 控制流

```llvm
; 無條件跳躍
br label %dest

; 條件跳躍
%cmp = icmp eq i32 %a, %b
br i1 %cmp, label %then, label %else

; PHI 節點 (SSA form)
%result = phi i32 [ %val1, %label1 ], [ %val2, %label2 ]
```

### 20.6.6 PHI 節點

PHI 節點根據前身塊選擇值：

```llvm
; C code:
; int foo(int x) {
;     if (x > 0) return x;
;     else return -x;
; }

define i32 @foo(i32 %x) {
entry:
    %cmp = icmp sgt i32 %x, 0
    br i1 %cmp, label %then, label %else

then:
    ret i32 %x

else:
    %neg = sub i32 0, %x
    ret i32 %neg
}

; 沒有 PHI，因為兩個分支都 return
```

複雜例子（迴圈）：
```llvm
loop:
    %i_old = phi i32 [ 0, %entry ], [ %i_new, %loop ]
    ; ... loop body ...
    %i_new = add i32 %i_old, 1
    %cmp = icmp slt i32 %i_new, %n
    br i1 %cmp, label %loop, label %exit
```

### 20.6.7 函式呼叫

```llvm
; 直接呼叫
%result = call i32 @add(i32 %a, i32 %b)

; 指標呼叫
%fp = load i32 (i32, i32)*, i32 (i32, i32)** @func_ptr
%result = call i32 %fp(i32 %a, i32 %b)

; 宣告外部函式
declare i32 @printf(i8*, ...)
declare void @exit(i32)

; 可變參數
declare i32 @scanf(i8*, ...)
```

### 20.6.8 Select

```llvm
%max = select i1 %cmp, i32 %a, i32 %b
; 相當於: %max = %cmp ? %a : %b;
```

## 20.7 完整範例

### 20.7.1 C 程式

```c
#include <stdio.h>

long long sum_array(long long *arr, int n) {
    long long sum = 0;
    for (int i = 0; i < n; i++) {
        sum += arr[i];
    }
    return sum;
}

int main() {
    long long data[] = {1, 2, 3, 4, 5};
    printf("%lld\n", sum_array(data, 5));
    return 0;
}
```

### 20.7.2 產生的 LLVM IR

```llvm
@.str = private constant [4 x i8] c"%lld\0A\00"

define i64 @sum_array(i64* %arr, i32 %n) {
entry:
    %sum = alloca i64, align 8
    %i = alloca i32, align 4
    store i64 0, i64* %sum, align 8
    store i32 0, i32* %i, align 4
    br label %for.cond

for.cond:
    %i_val = load i32, i32* %i
    %cmp = icmp slt i32 %i_val, %n
    br i1 %cmp, label %for.body, label %for.end

for.body:
    %sum_val = load i64, i64* %sum
    %i_val2 = load i32, i32* %i
    %idxprom = sext i32 %i_val2 to i64
    %arrayidx = getelementptr i64, i64* %arr, i64 %idxprom
    %val = load i64, i64* %arrayidx
    %add = add i64 %sum_val, %val
    store i64 %add, i64* %sum
    br label %for.inc

for.inc:
    %i_val3 = load i32, i32* %i
    %inc = add i32 %i_val3, 1
    store i32 %inc, i32* %i
    br label %for.cond

for.end:
    %result = load i64, i64* %sum
    ret i64 %result
}

define i32 @main() {
entry:
    %data = alloca [5 x i64], align 8
    %arraydecay = getelementptr [5 x i64], [5 x i64]* %data, i64 0, i64 0
    call void @llvm.memset.p0i8.i64(i8* align 8 %arraydecay, i8 0, i64 40, i1 false)
    %sum = call i64 @sum_array(i64* %arraydecay, i32 5)
    %call = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str, i64 0, i64 0), i64 %sum)
    ret i32 0
}

declare i32 @printf(i8*, ...)
declare void @llvm.memset.p0i8.i64(i8*, i8, i64, i1)
```

## 20.8 使用 Clang 生成 IR

```bash
# 生成可讀 IR
clang -S -emit-llvm -O0 foo.c -o foo.ll

# 生成 Bitcode
clang -c -emit-llvm foo.c -o foo.bc

# 指定目標
clang -S -emit-llvm --target=riscv64 foo.c -o foo.ll

# 顯示最佳化後的 IR
clang -S -emit-llvm -O2 foo.c -o foo_O2.ll
```

## 20.9 使用 opt 優化

```bash
# 基本最佳化
opt -O2 foo.ll -S -o foo_opt.ll

# 查看 passes
opt --help | grep -i pass

# 特定最佳化
opt -mem2reg foo.ll -S -o foo_reg2mem.ll  ; 註冊提升
opt -gvn foo.ll -S -o foo_gvn.ll          ; 全域值編號
opt -dce foo.ll -S -o foo_dce.ll          ; 死碼消除
```

## 20.10 使用 lli 執行 IR

```bash
# 直接執行 IR
lli foo.ll

# 或執行 Bitcode
lli foo.bc
```

## 20.11 小結

本章節我們學習了：
- LLVM IR 的基本語法
- 型別系統（基本和複合）
- 二元運算和比較指令
- 記憶體指令（alloca, load, store, gep）
- 控制流指令
- PHI 節點和 SSA form
- 函式呼叫
- 使用 Clang 和 opt 工具

## 20.12 習題

1. 用 `clang -S -emit-llvm` 生成一個包含結構體的程式的 IR
2. 研究 PHI 節點如何實現 SSA form
3. 用 `opt` 實驗不同的最佳化 passes
4. 實現一個簡單的 LLVM IR 到 x86 的編譯器
5. 研究 `getelementptr` 指令的各種用法
