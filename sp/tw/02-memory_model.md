# 2. 記憶體模型——堆疊、堆積與靜態記憶體

## 2.1 程式執行時的記憶體

當一個 C 程式執行時，作業系統會為它分配一塊虛擬記憶體。這塊記憶體被劃分成不同的區域，每個區域有不同的用途。

```
+------------------+ 高位址
|     核心空間      |  (Kernel space) - 作業系統保留
+------------------+
|       堆疊        |  (Stack) - 向下生長
|       ↓          |
|                  |
|     未使用        |
|                  |
|       ↑          |
|       堆積        |  (Heap) - 向上生長
+------------------+
|      BSS         |  (Block Started by Symbol) - 未初始化全域變數
+------------------+
|      Data        |  (Data) - 已初始化全域變數
+------------------+
|      Text        |  (Text) - 程式碼
+------------------+ 0x400000 (低位址)
```

## 2.2 各記憶體區域詳解

### 2.2.1 Text 段（程式碼區）

儲存程式的執行指令。

特點：
- **唯讀** - 防止程式意外修改自己的程式碼
- **可執行** - CPU 可以執行這段記憶體中的指令
- **共享** - 多個相同程式的執行個體可以共享同一份程式碼

```c
int add(int a, int b) {
    return a + b;
}
// add 函式的機器碼就存在 Text 段
```

### 2.2.2 Data 段（已初始化全域/靜態變數）

儲存已初始化的全域變數和靜態變數。

```c
int initialized_global = 42;      // Data 段
const char *name = "Alice";       // Data 段（指標本身）

static int count = 100;           // Data 段

int main() {
    static int counter = 0;       // Data 段（函式內的靜態）
    return 0;
}
```

### 2.2.3 BSS 段（未初始化全域/靜態變數）

「Block Started by Symbol」的縮寫，儲存未初始化或初始化為零的全域變數。

```c
int uninitialized_global;         // BSS 段（自動設為 0）
int zero_global = 0;               // BSS 段（優化後等同於未初始化）

static int uninitialized_static;   // BSS 段

int main() {
    static int static_local;       // BSS 段
    return 0;
}
```

為什麼分開 Data 和 BSS？**節省磁碟空間**。BSS 段不需要儲存實際資料，只需記錄大小，執行時由作業系統初始化為零。

### 2.2.4 Heap 段（堆積）

動態記憶體配置區域，程式執行時透過 `malloc`/`free` 管理。

```c
#include <stdlib.h>

int main() {
    // 配置 100 個 int 的空間
    int *arr = (int *)malloc(100 * sizeof(int));
    
    if (arr == NULL) {
        return 1;  // 配置失敗
    }
    
    arr[0] = 42;   // 使用配置到的記憶體
    free(arr);     // 釋放記憶體
    
    return 0;
}
```

特點：
- **手動管理** - 程式員負責配置和釋放
- **向上生長** - 配置新記憶體時，堆積頂端向上移動
- **靈活大小** - 可在執行時決定配置大小

### 2.2.5 Stack 段（堆疊）

儲存函式呼叫相關資訊、本地變數。

```c
void function_c() {
    int c = 3;      // 堆疊 Frame C
}

void function_b() {
    int b = 2;      // 堆疊 Frame B
    function_c();
}

void function_a() {
    int a = 1;      // 堆疊 Frame A
    function_b();
}

int main() {
    function_a();
    return 0;
}
```

呼叫順序：`main` → `function_a` → `function_b` → `function_c`

堆疊佈局（由高到低）：
```
+------------------+ 高位址
|   function_c     |  ← 目前在此
+------------------+
|   function_b     |
+------------------+
|   function_a     |
+------------------+
|      main        |
+------------------+ 低位址
```

## 2.3 堆疊 Frame（堆疊框架）

每個函式呼叫都會建立一個「堆疊框架」，包含：
- 返回位址（函式結束後繼續執行的位置）
- 舊的基底指標
- 函式參數
- 本地變數

x86-64 的堆疊框架：
```
+------------------+  rbp（基底指標）
|   舊的 RBP       |
+------------------+
|   返回位址       |
+------------------+  rsp（堆疊指標）
|   參數 3         |
+------------------+
|   參數 2         |
+------------------+
|   參數 1         |
+------------------+
|   返回位址       |
+------------------+
|   舊的 RBP       |
+------------------+ ← rbp
|   本地變數 1     |
+------------------+
|   本地變數 2     |
+------------------+ ← rsp
```

## 2.4 堆積 vs 堆疊

| 特性 | 堆疊 (Stack) | 堆積 (Heap) |
|------|-------------|-------------|
| 配置方式 | 自動（函式進入時分配） | 手動（malloc/free） |
| 釋放方式 | 自動（函式結束時釋放） | 手動（free） |
| 大小 | 較小（預設 8MB） | 較大（受系統限制） |
| 速度 | 快 | 慢 |
| 碎片化 | 不會 | 可能 |
| 配置失敗 | 通常不會 | 可能（記憶體不足） |
| 生存期 | 函式範圍內 | 直到 free |

## 2.5 常見記憶體錯誤

### 2.5.1 記憶體洩漏（Memory Leak）

配置了記憶體但忘記釋放：

```c
void leak() {
    int *ptr = (int *)malloc(sizeof(int));
    *ptr = 42;
    // 忘記 free(ptr)！
    // 每次呼叫 leak() 都會洩漏 sizeof(int) 位元組
}
```

### 2.5.2 雙重釋放（Double Free）

```c
void double_free() {
    int *ptr = (int *)malloc(sizeof(int));
    free(ptr);
    free(ptr);  // 錯誤！ptr 已經被釋放
}
```

### 2.5.3 使用已釋放記憶體（Use After Free）

```c
void use_after_free() {
    int *ptr = (int *)malloc(sizeof(int));
    *ptr = 42;
    free(ptr);
    int x = *ptr;  // 錯誤！ptr 指向的記憶體已被釋放
}
```

### 2.5.4 緩衝區溢位（Buffer Overflow）

```c
void buffer_overflow() {
    char buffer[10];
    strcpy(buffer, "This is too long!");  // 溢出！
}
```

### 2.5.5 堆疊溢位（Stack Overflow）

```c
void infinite_recursion() {
    int arr[1000000];  // 嘗試在堆疊上配置太大陣列
    infinite_recursion();  // 無限遞迴
}
```

## 2.6 用 GDB 查看記憶體

```bash
# 編譯（帶除錯資訊）
gcc -g -o memory_demo memory_demo.c

# 啟動 GDB
gdb ./memory_demo

# 在 GDB 中
(gdb) break main
(gdb) run
(gdb) info registers
(gdb) x/20x $sp      # 查看堆疊（16進位）
(gdb) x/20x &global_var  # 查看全域變數
(gdb) print &heap_var    # 印出堆積變數位址
```

## 2.7 用 size 查看記憶體佈局

```bash
size ./a.out
```

輸出範例：
```
text    data     bss     dec     hex filename
1672     608       8    2288     8f0 a.out
```

- `text`: 程式碼大小
- `data`: 已初始化全域變數
- `bss`: 未初始化全域變數
- `dec`: 總大小（十進位）
- `hex`: 總大小（十六進位）

## 2.8 小結

本章節我們學習了：
- 程式記憶體分為：Text、Data、BSS、Heap、Stack
- 各區域的用途和特性
- 堆疊用於函式呼叫，堆積用於動態配置
- 常見的記憶體錯誤類型

## 2.9 習題

1. 寫一個程式，用 `printf("%p\n", &var)` 印出幾個不同變數的位址，觀察它們的位置
2. 用 `size` 命令比較不同程式的各段大小
3. 造成一次記憶體洩漏，並用 Valgrind 檢測
4. 研究你系統的預設堆疊大小限制
