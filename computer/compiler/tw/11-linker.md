# 11. 連結器與載入器

## 11.1 連結器概述

連結器（Linker）負責將多個目標檔案合併成一個可執行檔或共享庫。主要任務包括：
- 符號解析
- 重定位
- 區段合併

## 11.2 目標檔案格式

### ELF 格式（Linux）

```
+------------------+
| ELF Header       |
+------------------+
| Program Headers  |
+------------------+
| .text            |  (程式碼)
+------------------+
| .data            |  (已初始化資料)
+------------------+
| .bss             |  (未初始化資料)
+------------------+
| .symtab          |  (符號表)
+------------------+
| .rel/.rela       |  (重定位資訊)
+------------------+
| Section Headers  |
+------------------+
```

### Mach-O 格式（macOS）

```
+------------------+
| Mach Header      |
+------------------+
| Load Commands    |
+------------------+
| .text            |
+------------------+
| .data            |
+------------------+
| .bss             |
+------------------+
```

## 11.3 符號解析

### 定義與引用

[程式檔案：11-1-lib.c](../_code/11/11-1-lib.c)
```c
int square(int x) {
    return x * x;
}
```

編譯為目的檔：
```bash
clang -c 11-1-lib.c -o lib.o
```

### 符號表

```bash
# 查看符號表
nm lib.o

# 結果：
0000000000000000 T _square
0000000000000000 T _cube
```

## 11.4 靜態連結

```bash
# 編譯多個檔案
clang -c main.c -o main.o
clang -c lib.c -o lib.o

# 靜態連結
clang main.o lib.o -o program
```

## 11.5 動態連結

### 共享庫

```bash
# 建立共享庫
clang -fPIC -shared lib.c -o lib.so

# 動態連結
clang main.c -L. -l:lib.so -o program

# 執行時指定庫路徑
LD_LIBRARY_PATH=. ./program
```

### 延遲載入

函數在第一次呼叫時才會被載入：

```c
void (*func)(void);
func = dlsym(handle, "my_function");
func();  // 第一次呼叫時解析
```

## 11.6 重定位

重定位（Relocation）將符號位址調整為實際記憶體位址：

```
# 重定位前
callq   0x0  ; 目標位址未知

# 重定位後
callq   0x401000  ; 目標位址已知
```

## 11.7 載入器

載入器（Loader）將可執行檔載入記憶體並執行：

```c
int execve(const char *filename, char *const argv[], char *const envp[]);
```

### 載入過程

1. 讀取 ELF Header
2. 讀取 Program Headers
3. 建立虛擬記憶體映射
4. 載入需要的區段
5. 設定堆疊
6. 跳轉到入口點

## 11.8 本章小結

本章介紹了連結器與載入器的核心概念：
- 目標檔案格式（ELF、Mach-O）
- 符號解析
- 靜態連結與動態連結
- 重定位機制
- 載入器的運作原理

## 練習題

1. 使用 nm 和 objdump 分析目標檔案。
2. 比較靜態連結和動態連結的優缺點。
3. 實作一個簡單的連結器。
4. 研究 PLT 和 GOT 的運作機制。
