# 9. 執行時期環境

## 9.1 執行時期環境概述

執行時期環境（Runtime Environment）是程式執行時所需的軟體基礎設施，包括堆疊框架管理、函數呼叫約定、系統呼叫介面等。

## 9.2 堆疊框架

每個函數呼叫都會在堆疊上建立一個堆疊框架（Stack Frame），包含：
- 返回位址
- 保存的暫存器
- 區域變數
- 函數參數

[程式檔案：09-1-stack-frame.c](../_code/09/09-1-stack-frame.c)
```c
int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}
```

產生的 LLVM IR 展示遞迴函數的堆疊框架管理：

[程式檔案：09-1-stack-frame.ll](../_code/09/09-1-stack-frame.ll)
```llvm
define i32 @factorial(i32) #0 {
entry:
  %n.addr = alloca i32, align 4
  store i32 %0, i32* %n.addr, align 4
  %0 = load i32, i32* %n.addr, align 4
  %cmp = icmp sle i32 %0, 1
  br i1 %cmp, label %if.then, label %if.else
  ; ...
}
```

## 9.3 函數呼叫約定

### cdecl（C 呼叫約定）

x86-64 System V ABI：
- 整數參數：RDI, RSI, RDX, RCX, R8, R9
- 浮點數參數：XMM0-XMM7
- 返回值：RAX（整數），XMM0（浮點數）
- 呼叫者保存：RAX, RCX, RDX, RSI, RDI, R8-R11
- 被呼叫者保存：RBP, RBX, R12-R15

### 呼叫序列

```asm
# 呼叫者
pushq   %rbp            ; 保存舊框架指標
movq    %rsp, %rbp      ; 建立新框架
subq    $16, %rsp      ; 配置區域變數空間
# ... 設定參數 ...
callq   function       ; 呼叫函數
# ... 使用返回值 ...

# 被呼叫者
function:
    pushq   %rbp
    movq    %rsp, %rbp
    # ... 函數主體 ...
    popq    %rbp
    retq
```

## 9.4 堆疊記憶體配置

### alloca 指令

在 LLVM IR 中，`alloca` 用於配置堆疊上的記憶體：

```llvm
%ptr = alloca i32, align 4    ; 配置 4 位元組
store i32 10, i32* %ptr        ; 儲存值
%val = load i32, i32* %ptr    ; 載入值
```

### 記憶體對齊

```llvm
%x = alloca i32, align 8      ; 8 位元組對齊
%y = alloca double, align 16  ; 16 位元組對齊
```

## 9.5 系統呼叫

### printf 的實現

```c
printf("Result: %d\n", result);
```

在組合語言層面：

```asm
leaq    .Lstr(%rip), %rdi
movl    $result, %esi
xorl    %eax, %eax
callq   printf@PLT
```

## 9.6 例外處理

LLVM 提供例外處理的支援：

```llvm
invoke i32 @might_throw() 
    to label %normal unwind label %exception

normal:
    ; 正常返回
    br label %cleanup

exception:
    %phi = phi i32 [ 0, %entry ]
    ; 例外處理
    br label %cleanup

cleanup:
    ; 清理程式碼
    ret i32 %phi
```

## 9.7 本章小結

本章介紹了執行時期環境的核心概念：
- 堆疊框架的結構
- 函數呼叫約定
- 記憶體配置與對齊
- 系統呼叫介面
- 例外處理機制

## 練習題

1. 分析遞迴函數的堆疊使用情況。
2. 比較不同呼叫約定的差異。
3. 實作尾呼叫優化。
4. 研究 C++ 例外處理的實現機制。
