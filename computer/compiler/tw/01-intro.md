# 1. 編譯器簡介

## 1.1 編譯器的歷史

編譯器（Compiler）是一種將高階語言翻譯成低階語言（通常是機器語言或組合語言）的程式。編譯器的發展可以追溯到 1950 年代，當時 Fortran 成為第一個被廣泛使用的高階語言。

重要的歷史里程碑：
- 1957 年：Fortran 編譯器問世，第一個成功的編譯器
- 1968 年：首次提出「優化編譯器」的概念
- 1977 年：Ada 語言編譯器採用新的編譯技術
- 1987 年：GCC（GNU Compiler Collection）發布
- 2003 年：LLVM 專案啟動

## 1.2 編譯器的工作流程

現代編譯器通常分為前端和後端兩大部分：

```
原始程式碼 (C/C++)
        │
        ▼
    ┌─────────┐
    │ 詞法分析  │  (Lexical Analysis)
    └─────────┘
        │
        ▼
    ┌─────────┐
    │ 語法分析  │  (Syntax Analysis / Parsing)
    └─────────┘
        │
        ▼
    ┌─────────┐
    │ 語意分析  │  (Semantic Analysis)
    └─────────┘
        │
        ▼
   ┌──────────┐
   │ 中間碼生成 │  (IR Generation)
   └──────────┘
        │
        ▼
   ┌──────────┐
   │ 程式碼優化 │  (Optimization)
   └──────────┘
        │
        ▼
   ┌──────────┐
   │ 目標碼生成│  (Code Generation)
   └──────────┘
        │
        ▼
    目的檔/執行檔
```

### 前端（Frontend）

前端負責解析原始程式碼，包括：
- **詞法分析**：將原始字元序列轉換為 Token 串流
- **語法分析**：檢查程式碼是否符合語法規則，建立語法樹
- **語意分析**：進行類型檢查、作用域分析

### 後端（Backend）

後端負責將中間碼翻譯為目標機器碼：
- **中間碼生成**：建立與機器無關的中間表示
- **優化**：進行各種效能優化
- **目標碼生成**：產生特定硬體的機器碼

## 1.3 LLVM 架構概述

LLVM（Low Level Virtual Machine）是一個現代化的編譯器架構，提供一套統一的中間表示（IR），可以在多種目標平台上進行優化和程式碼生成。

[程式檔案：01-1-hello.c](../_code/01/01-1-hello.c)
```c
#include <stdio.h>

int main() {
    printf("Hello, World!\n");
    return 0;
}
```

使用 clang 編譯產生 LLVM IR：

[程式檔案：01-1-hello.ll](../_code/01/01-1-hello.ll)
```llvm
; ModuleID = '01-1-hello.c'
source_filename = "01-1-hello.c"
target datalayout = "e-m:o-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-apple-darwin"

@.str = private unnamed_addr constant [14 x i8] c"Hello, World!\0A\00", align 1

define i32 @main() #0 {
entry:
  %retval = alloca i32, align 4
  %printf.addr = alloca i8*, align 8
  store i32 0, i32* %retval, align 4
  store i8* getelementptr inbounds ([14 x i8], [14 x i8]* @.str, i32 0, i32 0), i8** %printf.addr, align 8
  %call = call i32 @printf(i8* getelementptr inbounds ([14 x i8], [14 x i8]* @.str, i32 0, i32 0))
  ret i32 0
}

declare i32 @printf(i8*) #1
```

## 1.4 使用 clang 和 opt 工具

clang 是 LLVM 的 C/C++ 編譯器前端，可以產生 LLVM IR。常用的命令：

```bash
# 產生 LLVM IR（未優化）
clang -S -emit-llvm -O0 hello.c -o hello.ll

# 產生 LLVM IR（優化）
clang -S -emit-llvm -O2 hello.c -o hello_opt.ll

# 使用 opt 工具進行優化
opt -S -O2 hello.ll -o hello_optimized.ll

# 產生目的檔
clang -c hello.c -o hello.o

# 產生執行檔
clang hello.c -o hello
```

讓我們看一個簡單的加法函數，比較不同優化等級產生的 IR：

[程式檔案：01-2-compiler-stages.c](../_code/01/01-2-compiler-stages.c)
```c
#include <stdio.h>

int add(int a, int b) {
    return a + b;
}

int main() {
    int result = add(5, 3);
    printf("Result: %d\n", result);
    return 0;
}
```

使用 `-O0`（無優化）產生的 IR 會有很多載入/儲存指令，而使用 `-O2` 優化後，編譯器會進行常數折疊，直接計算 `5 + 3 = 8`。

## 1.5 本章小結

本章介紹了編譯器的基本概念和 LLVM 架構。編譯器是將高階語言翻譯成機器碼的重要工具，其核心包括：
- 前端：詞法分析、語法分析、語意分析
- 中間表示：LLVM IR 是現代編譯器的核心
- 後端：優化與目標碼生成

LLVM 提供了完整的編譯器工具鏈，是學習編譯器原理的最佳平台。

## 練習題

1. 使用 clang 編譯一個簡單的 C 程式，產生不同優化等級的 LLVM IR。
2. 比較 `-O0`、`-O1`、`-O2`、`-O3` 產生的 IR 有何差異。
3. 使用 `opt` 工具嘗試不同的優化 Pass。
