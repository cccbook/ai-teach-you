# 程式碼優化 (Optimization)

## 概述

程式碼優化是編譯器中改進程式碼效能的階段，目標是產生更快速或更小的執行碼。

## 優化等級

| 等級 | 描述 | 適用場景 |
|-----|------|---------|
| -O0 | 無優化 | 調試 |
| -O1 | 基本優化 | 快速編譯 |
| -O2 | 標準優化 | 發布版本 |
| -O3 | 激進優化 | 極致效能 |
| -Os | 大小優化 | 嵌入式系統 |

## 常見優化技術

### 1. 常數折疊（Constant Folding）

在編譯時計算常數表達式：

```c
// 優化前
int a = 2 + 3;

// 優化後
int a = 5;
```

### 2. 死程式碼消除（Dead Code Elimination）

移除不會執行的程式碼：

```c
// 優化前
int unused = 100;
return 42;

// 優化後
return 42;
```

### 3. 函數內聯（Function Inlining）

將函數呼叫展開為函數主體：

```c
// 優化前
int add(int a, int b) { return a + b; }
int main() { return add(1, 2); }

// 優化後
int main() { return 3; }
```

### 4. 共同子表達式消除（CSE）

消除重複的計算：

```c
// 優化前
int a = x + y;
int b = x + y;

// 優化後
int temp = x + y;
int a = temp;
int b = temp;
```

## 參考資源

- [第 7 章：程式碼優化](../07-optimization.md)
