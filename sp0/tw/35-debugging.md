# 35. 除錯工具——GDB 與 LLDB

## 35.1 除錯的必要性

編譯後的程式碼缺少：
- 變數名稱
- 原始碼位置
- 函式結構

除錯器幫助我們：
- 設定斷點
- 逐步執行
- 檢查變數
- 分析崩潰

## 35.2 GDB 基本用法

### 35.2.1 編譯除錯程式

```bash
gcc -g hello.c -o hello
```

### 35.2.2 啟動

```bash
gdb ./hello
```

### 35.2.3 常用命令

```bash
(gdb) run              # 執行
(gdb) break main       # 在 main 設定斷點
(gdb) break hello.c:10 # 在行號設定斷點
(gdb) continue          # 繼續執行
(gdb) next             # 下一行（不進入函式）
(gdb) step             # 下一行（進入函式）
(gdb) print x          # 印出變數
(gdb) info locals      # 印出所有本地變數
(gdb) info registers    # 印出暫存器
(gdb) backtrace        # 顯示呼叫堆疊
(gdb) quit             # 離開
```

## 35.3 斷點

### 35.3.1 設定斷點

```bash
(gdb) break foo        # 函式名
(gdb) break *0x400544  # 位址
(gdb) break hello.c:10 # 行號
```

### 35.3.2 條件斷點

```bash
(gdb) break foo if x > 10
```

### 35.3.3 監控點

```bash
(gdb) watch global_var      # 監控寫入
(gdb) rwatch global_var    # 監控讀取
(gdb) awatch global_var    # 監控讀寫
```

## 35.4 檢視資料

### 35.4.1 印出變數

```bash
(gdb) print x         # 十進位
(gdb) print /x x      # 十六進位
(gdb) print /d x      # 十進位
(gdb) print /t x      # 二進位
```

### 35.4.2 指標和陣列

```bash
(gdb) print *ptr      # 解引用
(gdb) print ptr[0]    # 陣列元素
(gdb) print *ptr@len  # C 風格陣列
```

### 35.4.3 結構體

```bash
(gdb) print struct_var.member
(gdb) print *struct_ptr->member
```

## 35.5 呼叫堆疊

### 35.5.1 backtrace

```bash
(gdb) backtrace
#0  foo () at hello.c:5
#1  0x0000555555555149 in bar () at hello.c:10
#2  0x0000555555555156 in main () at hello.c:15
```

### 35.5.2 切換框架

```bash
(gdb) frame 1
(gdb) print x  # 查看該框架的變數
```

## 35.6 LLDB

### 35.6.1 基本命令對照

| GDB | LLDB |
|-----|------|
| run | process launch |
| break | breakpoint set |
| next | thread step-inst-over |
| step | thread step-inst |
| print | frame variable |
| bt | thread backtrace |
| info registers | register read |
| x | memory read |

### 35.6.2 LLDB 範例

```bash
lldb ./hello
(lldb) breakpoint set --name main
(lldb) process launch
(lldb) frame variable
(lldb) thread step-over
(lldb) thread backtrace
```

## 35.7 核心轉儲

### 35.7.1 產生核心轉儲

```bash
# Linux
ulimit -c unlimited
./hello  # 崩潰
ls -l core*

# macOS
./hello  # 崩潰
# 核心轉儲在 /cores/
```

### 35.7.2 分析核心轉儲

```bash
gdb ./hello core
(gdb) bt  # 顯示崩潰時的堆疊
```

## 35.8 小結

本章節我們學習了：
- GDB 基本用法
- 斷點和監控點
- 檢視資料
- 呼叫堆疊
- LLDB 命令
- 核心轉儲分析

## 35.9 習題

1. 使用 GDB 除錯一個有 bug 的程式
2. 實現條件斷點
3. 研究 GDB 的 Python 介面
4. 比較 GDB 和 LLDB
5. 分析一個真實的 core dump
