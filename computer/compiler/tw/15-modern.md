# 15. 現代編譯器架構

## 15.1 LLVM 架構

LLVM（Low Level Virtual Machine）是現代編譯器的代表架構，採用模組化設計：

```
           ┌─────────────────┐
           │   Frontend     │
           │  (Clang, swift)│
           └────────┬────────┘
                    │ LLVM IR
                    ▼
           ┌─────────────────┐
           │   Optimizer     │
           │    (opt)        │
           └────────┬────────┘
                    │ LLVM IR
                    ▼
           ┌─────────────────┐
           │   Backend       │
           │    (llc)        │
           └────────┬────────┘
                    │
                    ▼
              目標機器碼
```

## 15.2 Clang - C/C++ 編譯器前端

Clang 是 LLVM 的 C/C++ 編譯器前端，特点：
- 快速編譯
- 優秀的錯誤訊息
- 兼容 GCC

```bash
# 基本編譯
clang source.c -o program

# 產生 IR
clang -S -emit-llvm source.c -o source.ll

# 產生位元碼
clang -c -emit-llvm source.c -o source.bc
```

## 15.3 GCC 架構

GCC（GNU Compiler Collection）是另一個重要的編譯器：

```
        ┌─────────────┐
        │  Frontend  │
        │  (C, C++)  │
        └─────┬───────┘
              │ GENERIC
              ▼
        ┌─────────────┐
        │  GIMPLE     │
        └─────┬───────┘
              │ RTL
              ▼
        ┌─────────────┐
        │   Backend   │
        └─────────────┘
```

## 15.4 LLVM IR 範例

[程式檔案：15-1-llvm-architecture.c](../_code/15/15-1-llvm-architecture.c)
```c
int fibonacci(int n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}
```

產生的 LLVM IR：

[程式檔案：15-1-llvm-architecture.ll](../_code/15/15-1-llvm-architecture.ll)
```llvm
define i32 @fibonacci(i32) #0 {
entry:
  %n.addr = alloca i32, align 4
  store i32 %0, i32* %n.addr, align 4
  %0 = load i32, i32* %n.addr, align 4
  %cmp = icmp sle i32 %0, 1
  br i1 %cmp, label %if.then, label %if.else
  ; ...
}
```

## 15.5 多語言編譯器

### Rust 編譯器（rustc）

使用 LLVM 作為後端：
- 前端：rustc
- 中間表示：MIR -> LLVM IR
- 後端：LLVM

### Swift 編譯器

- 前端：Swift Compiler
- 中間表示：SIL -> LLVM IR
- 後端：LLVM

### GraalVM

- Truffle 框架
- 自疫 JIT 編譯
- 多語言支援

## 15.6 雲端編譯服務

### Compiler Explorer

線上編譯器工具：
- 即時查看編譯結果
- 多語言支援
- 多版本選擇

### LLVM Build Bot

持續整合編譯測試。

## 15.7 未來趨勢

### MLIR

Multi-Level Intermediate Representation：
- 多層次 IR
- 可擴展的編譯器基礎設施
- 支援領域特定語言

```mlir
func @add(%a: tensor<4xf32>, %b: tensor<4xf32>) -> tensor<4xf32> {
    %c = arith.addf %a, %b : tensor<4xf32>
    return %c : tensor<4xf32>
}
```

### JIT 編譯

- 更高的執行效率
- 彈性的優化策略

### 協作編譯

- 分散式編譯
- 雲端資源利用

## 15.8 本章小結

本章介紹了現代編譯器架構：
- LLVM 架構與設計
- Clang 編譯器前端
- GCC 架構
- 多語言編譯器
- 未來趨勢（MLIR、JIT）

## 練習題

1. 比較 LLVM 和 GCC 的架構差異。
2. 研究 MLIR 的設計理念。
3. 探索編譯器優化對效能的影響。
4. 設計一個領域特定語言的編譯器。
