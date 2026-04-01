# 連結器 (Linker)

## 概述

連結器是將多個目標檔案合併成一個可執行檔或共享庫的工具。

## 主要任務

### 1. 符號解析

解析符號引用：

```c
// file1.c
int global_var = 10;

// file2.c
extern int global_var;
void foo() {
    global_var = 20;
}
```

### 2. 重定位

調整符號位址：

```
# 重定位前
callq   0x0

# 重定位後
callq   0x401000
```

### 3. 區段合併

合併相同的區段：

```
file1.o: .text, .data
file2.o: .text, .data
        │
        ▼
program: .text (合併), .data (合併)
```

## 連結類型

### 靜態連結

所有程式碼在編譯時連結：

```bash
gcc main.o lib.a -o program
```

### 動態連結

程式碼在執行時連結：

```bash
gcc main.c -l:lib.so -o program
```

## 目標檔案格式

| 作業系統 | 格式 |
|---------|------|
| Linux | ELF |
| macOS | Mach-O |
| Windows | PE |

## 參考資源

- [第 11 章：連結器與載入器](../11-linker.md)
