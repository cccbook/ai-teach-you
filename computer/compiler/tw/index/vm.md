# 虛擬機 (Virtual Machine)

## 概述

虛擬機是軟體實現的 CPU，能夠執行特定格式的位元碼（Bytecode）。

## 虛擬機 vs 硬體 CPU

| 特性 | 虛擬機 | 硬體 CPU |
|-----|-------|---------|
| 實現方式 | 軟體 | 硬體 |
| 可移植性 | 高 | 低 |
| 執行速度 | 較慢 | 較快 |
| 靈活性 | 高 | 低 |

## 常見虛擬機

### 1. JVM (Java Virtual Machine)

執行 Java 位元碼：

```java
// 編譯後產生 .class 檔案
// JVM 執行 .class 檔案
```

### 2. .NET CLR

執行 C# 位元碼（IL）。

### 3. WebAssembly VM

執行 WebAssembly 位元碼。

## 虛擬機元件

### 1. 指令集

```c
typedef enum {
    OP_LOAD,
    OP_STORE,
    OP_ADD,
    OP_SUB,
    OP_MUL,
    OP_JMP,
    OP_HALT
} OpCode;
```

### 2. 堆疊

用於儲存運算元和中間結果。

### 3. 記憶體管理

配置和管理執行時記憶體。

## JIT 編譯

虛擬機可以使用 JIT（Just-In-Time）編譯提升效能：

```
位元碼 → 解譯執行 → 熱點偵測 → JIT 編譯 → 機器碼執行
```

## 參考資源

- [第 12 章：JIT 編譯與虛擬機](../12-jit.md)
