# C 語言

## 概述

C 語言是一種通用的過程式程式語言，1972 年由 Dennis Ritchie 在貝爾實驗室發明。C 語言是系統程式設計的主流語言，也是編譯器教學的理想語言。

## 歷史

- 1972 年：Dennis Ritchie 發明 C 語言
- 1978 年：K&R C (The C Programming Language)
- 1989 年：ANSI C (C89)
- 1999 年：C99 標準
- 2011 年：C11 標準
- 2018 年：C17 標準

## C 語言特點

### 1. 低階存取能力

```c
int* ptr = (int*)0x1000;
*ptr = 42;
```

### 2. 高效率

直接對應機器指令，幾乎沒有執行時開銷。

### 3. 可移植性

標準化的語法，幾乎所有平台都有 C 編譯器。

### 4. 簡潔的語法

相對較少的關鍵字和控制結構。

## 範例程式

```c
#include <stdio.h>

int add(int a, int b) {
    return a + b;
}

int main() {
    int result = add(10, 20);
    printf("Result: %d\n", result);
    return 0;
}
```

## C 語言在編譯器的角色

C 語言常被用作編譯器教學的範例語言：

1. 語法簡單明確
2. 指標概念有助於理解記憶體
3. 編譯器工具鏈成熟
4. 可直接產生 LLVM IR

## 參考資源

- ISO C Standard: https://www.iso.org/standard/74528.html
- C Reference: https://en.cppreference.com/
