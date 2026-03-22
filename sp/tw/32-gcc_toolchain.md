# 32. GCC 工具鏈——從原始碼到執行檔

## 32.1 GCC 工具鏈概述

GNU Compiler Collection (GCC) 是 GNU 計畫的核心編譯器：

```
原始碼 ──→ 預處理器 ──→ 編譯器 ──→ 組譯器 ──→ 連結器 ──→ 執行檔
  .c          .i           .s        .o        a.out
```

## 32.2 編譯流程

### 32.2.1 完整編譯

```bash
gcc hello.c -o hello
```

### 32.2.2 分步執行

```bash
# 預處理
gcc -E hello.c -o hello.i

# 編譯（不組譯）
gcc -S hello.c -o hello.s

# 組譯（不連結）
gcc -c hello.c -o hello.o

# 連結
gcc hello.o -o hello
```

## 32.3 GCC 重要選項

### 32.3.1 警告選項

```bash
gcc -Wall hello.c       # 所有警告
gcc -Wextra hello.c     # 額外警告
gcc -Werror hello.c     # 警告視為錯誤
gcc -pedantic hello.c   # ISO C 警告
```

### 32.3.2 最佳化選項

```bash
gcc -O0 hello.c         # 無最佳化
gcc -O1 hello.c         # 基本最佳化
gcc -O2 hello.c         # 標準最佳化
gcc -O3 hello.c         # 積極最佳化
gcc -Os hello.c         # 大小最佳化
gcc -Ofast hello.c      # 快速最佳化（含浮點）
```

### 32.3.3 除錯選項

```bash
gcc -g hello.c                      # 生成除錯資訊
gcc -g3 hello.c                     # 包含巨集定義
gcc -ggdb hello.c                    # GDB 專用格式
```

## 32.4 連結庫

### 32.4.1 靜態連結

```bash
gcc -static hello.c -o hello_static
```

### 32.4.2 動態連結

```bash
gcc -shared foo.c -o libfoo.so
gcc -L. -lfoo main.c -o main
```

### 32.4.3 搜尋路徑

```bash
gcc -I./include hello.c     # 標頭搜尋路徑
gcc -L./lib hello.c         # 庫搜尋路徑
```

## 32.5 目標架構

### 32.5.1 指定目標

```bash
gcc -target riscv64-unknown-elf hello.c
```

### 32.5.2 交叉編譯

```bash
# 在 x86_64 上編譯 RISC-V
riscv64-unknown-elf-gcc hello.c -o hello.rv
```

## 32.6 靜態分析

### 32.6.1 使用編譯器

```bash
gcc -fsyntax-only hello.c        # 只做語法檢查
gcc -fanalyzer hello.c           # 靜態分析
```

### 32.6.2 其他工具

```bash
# 連結時間最佳化
gcc -flto hello.c -o hello

# 設定虛擬函式閾值
gcc -fvirtual-function-elimination hello.c
```

## 32.7 實用技巧

### 32.7.1 條件編譯

```bash
# 定義巨集
gcc -DDEBUG=1 hello.c -o hello

# 取消巨集
gcc -UMY_MACRO hello.c -o hello
```

### 32.7.2 版本資訊

```bash
__DATE__    # 編譯日期
__TIME__    # 編譯時間
__FILE__    # 原始檔名
__LINE__    # 行號
__VERSION__ # GCC 版本
```

## 32.8 小結

本章節我們學習了：
- GCC 工具鏈的完整流程
- 分步編譯
- 重要編譯選項
- 連結庫處理
- 交叉編譯
- 靜態分析

## 32.9 習題

1. 使用 `-S` 查看不同最佳化等級的組語差異
2. 實現條件編譯的除錯系統
3. 研究 `-flto` 連結時間最佳化
4. 比較靜態連結和動態連結的效能差異
5. 為不同架構交叉編譯同一個程式
