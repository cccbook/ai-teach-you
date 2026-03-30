# 10. cpy0 工具鏈總覽——從原始碼到 RISC-V 執行檔

## 10.1 cpy0 是什麼？

cpy0（讀作 "C-P-Y-Zero"）是陳鍾誠老師的自製編譯器工具鏈專案，展示如何從零打造一個完整的編譯器系統。

專案位置：[_code/cpy0/](../_code/cpy0/)

## 10.2 工具鏈架構

cpy0 包含多個工具，形成一個完整的編譯流程：

```
C 語言流程：
  C 原始碼 (.c)
       ↓  [c0c / clang]
  LLVM IR (.ll)
       ↓  [ll0c]
  RISC-V 組語 (.s)
       ↓  [rv0as]
  RISC-V 目的檔 (.o)
       ↓  [ld / rv0vm]
  可執行檔

Python 語言流程：
  Python 原始碼 (.py)
       ↓  [py0c]
  qd0 位元組碼 (.qd)
       ↓  [qd0c]
  LLVM IR (.ll)
       ↓  [clang]
  可執行檔
       ↓  或 [ll0c] → [rv0as] → [rv0vm]
  RISC-V 可執行檔
```

## 10.3 各工具簡介

| 工具 | 功能 | 輸入 | 輸出 |
|------|------|------|------|
| c0c | C 編譯器（自製） | .c | .ll (LLVM IR) |
| ll0c | LLVM IR → RISC-V | .ll | .s (RISC-V 組語) |
| rv0as | RISC-V 組譯器 | .s | .o (目的檔) |
| rv0vm | RISC-V 虛擬機 | .o | 執行結果 |
| py0c | Python 編譯器（自製） | .py | .qd (位元組碼) |
| qd0c | qd0 → LLVM IR | .qd | .ll |

## 10.4 目錄結構

```
cpy0/
├── c0/           # C 編譯器相關
│   ├── _doc/     # 文件
│   └── c0c/      # C 編譯器實作
├── py0/          # Python 編譯器相關
│   ├── _doc/     # 文件
│   ├── py0c/     # Python 編譯器實作
│   └── py0i/     # Python 解释器 (可選)
├── ll0/          # LLVM IR → RISC-V 後端
│   ├── ll0c/     # 後端實作
│   └── ll0i/     # 反向工具 (可選)
├── qd0/          # qd0 位元組碼相關
│   ├── _doc/     # 文件
│   └── qd0c/     # qd0 → LLVM IR 轉換器
├── rv0/          # RISC-V 虛擬機
│   ├── rv0as     # RISC-V 組譯器
│   ├── rv0vm     # RISC-V 虛擬機
│   └── rv0objdump # 反組譯工具
├── _data/        # 測試範例
│   ├── fact.c    # 階乘 (C)
│   └── test.py   # Python 測試
└── Makefile      # 建置腳本
```

## 10.5 快速開始

### 10.5.1 建置工具鏈

```bash
cd _code/cpy0
make
```

這會編譯所有工具並執行測試。

### 10.5.2 編譯 C 程式到 RISC-V

```bash
# 使用 clang 編譯到 LLVM IR
clang --target=riscv64 -march=rv64g -mabi=lp64d -S fact.c -o fact.s

# 使用 rv0as 組譯
./rv0/rv0as fact.s -o fact.o

# 使用 rv0vm 執行
./rv0/rv0vm -e 0x6c fact.o
```

### 10.5.3 編譯 Python 程式

```bash
# Python → qd0 位元組碼
./py0/py0c/py0c test.py -o test.qd

# qd0 → LLVM IR
./qd0/qd0c/qd0c test.qd -o test.ll

# LLVM IR → 主機執行檔
cc test.ll qd0/qd0c/qd0lib.c -o test.host -lm
./test.host
```

## 10.6 完整流程圖

```
                    ┌─────────────────────────────────────────┐
                    │              cpy0 工具鏈                  │
                    └─────────────────────────────────────────┘

  ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
  │   .c    │ ──▶ │ c0c 或  │ ──▶ │  LLVM   │ ──▶ │   .ll   │
  │ (原始碼) │     │ clang   │     │   IR    │     │         │
  └─────────┘     └─────────┘     └─────────┘     └─────────┘
                                                        
                         ┌───────────────────────────────────┐
                         │           C 語言分支               │
                         │  ll0c ──▶ .s ──▶ rv0as ──▶ .o   │
                         │                 ──▶ rv0vm 執行    │
                         └───────────────────────────────────┘

                         ┌───────────────────────────────────┐
                         │         Python 分支               │
                         │  py0c ──▶ .qd ──▶ qd0c ──▶ .ll  │
                         │       位元組碼       LLVM IR      │
                         │  ──▶ clang ──▶ host 可執行檔     │
                         │  ──▶ ll0c ──▶ rv0vm 執行         │
                         └───────────────────────────────────┘
```

## 10.7 為什麼要學習這個工具鏈？

### 10.7.1 理解編譯器工作原理

cpy0 展示了一個真實可用的編譯器系統：
- **前端**：詞彙分析、語法分析、語意分析
- **中端**：中間表示（LLVM IR、qd0 位元組碼）
- **後端**：指令選擇、寄存器分配、程式碼發射

### 10.7.2 理解不同語言的編譯過程

- C 語言：較傳統的編譯流程
- Python：需要先轉換為位元組碼，再編譯

### 10.7.3 理解 RISC-V 架構

最終目標是生成 RISC-V 機器碼，這需要：
- 理解 RISC-V 指令格式
- 理解函式呼叫約定
- 理解記憶體佈局

## 10.8 測試範例

### 10.8.1 fact.c - 階乘計算

```c
// fact.c
long long fact(long long n) {
    if (n <= 1) return 1;
    return n * fact(n - 1);
}

long long main() {
    return fact(10);
}
```

### 10.8.2 test.py - Python 測試

```python
# test.py
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

print(fib(10))
```

## 10.9 Makefile 使用

```bash
# 全部測試
make test

# 只測試 C 程式
make test_c

# 只測試 Python 程式
make test_py

# 編譯特定檔案
make fact
make test

# 清除生成的檔案
make clean

# 執行特定程式
make run name=fact
```

## 10.10 小結

本章節我們學習了：
- cpy0 工具鏈的整體架構
- C 語言和 Python 語言的編譯流程
- 各工具的功能和輸入輸出
- 如何建置和使用工具鏈
- 工具鏈學習的價值

## 10.11 習題

1. 閱讀 Makefile，了解每個目標的作用
2. 嘗試修改一個 C 程式並重新編譯執行
3. 嘗試修改一個 Python 程式並重新編譯執行
4. 研究 c0c 和 clang 的輸出有何不同
5. 追蹤一個完整程式的編譯過程
