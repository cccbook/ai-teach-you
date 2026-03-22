# 19. 函式呼叫約定——堆疊框架與暫存器使用

## 19.1 為什麼需要呼叫約定？

呼叫約定（Calling Convention）定義了：
- 參數如何傳遞
- 返回值如何傳回
- 哪些暫存器需要保存
- 堆疊如何維護

統一的呼叫約定確保不同編譯器、不同模組可以相互呼叫。

## 19.2 RISC-V 呼叫約定（ELF psABI）

### 19.2.1 參數傳遞

整數/指標參數（前 8 個）：
```
a0 = 第一個參數
a1 = 第二個參數
...
a7 = 第八個參數
```

超過 8 個的參數：透過堆疊傳遞（由呼叫者 push）

浮點參數：
- 如果函式有 "double" 或 "float" 參數，使用 fa0-fa7
- 否則使用 a0-a7

### 19.2.2 返回值

```
a0 = 第一個返回值
a1 = 第二個返回值（如果需要）
```

### 19.2.3 暫存器分類

| 類別 | 暫存器 | 說明 |
|------|--------|------|
| 保存者 (callee-saved) | s0-s11, sp, gp, tp | **被呼叫者**負責保存 |
| 呼叫者 (caller-saved) | t0-t6, a0-a7, ra | **呼叫者**自行處理 |

### 19.2.4 堆疊指標對齊

- 入口時：`sp mod 16 = 0`（16 位元組對齊）
- 呼叫 `call/jal` 前：`sp mod 16 = 0`

## 19.3 完整範例

### 19.3.1 C 程式

```c
long long sum3(long long a, long long b, long long c) {
    return a + b + c;
}

long long main() {
    return sum3(10, 20, 30);
}
```

### 19.3.2 組語分析

```asm
sum3:
    # 函式進入
    addi    sp, sp, -16      ; 分配棧框架 (16 位元組對齊)
    sd      ra, 8(sp)         ; 保存返回位址
    sd      s0, 0(sp)         ; 保存 frame pointer (可選)
    
    # 函式主體
    # a = a0, b = a1, c = a2
    add     a0, a0, a1        ; a = a + b
    add     a0, a0, a2        ; a = a + c
    # 返回值已在 a0
    
    # 函式離開
    ld      ra, 8(sp)         ; 恢復返回位址
    ld      s0, 0(sp)         ; 恢復 s0
    addi    sp, sp, 16        ; 釋放棧框架
    
    jalr    x0, 0(ra)         ; 返回 (ret 偽指令)

main:
    addi    sp, sp, -16      ; 分配棧框架
    sd      ra, 8(sp)         ; 保存 main 的返回位址
    
    # 設定參數
    li      a0, 10            ; 第一個參數
    li      a1, 20            ; 第二個參數
    li      a2, 30            ; 第三個參數
    
    jal     ra, sum3          ; 呼叫 sum3
    
    # 這裡 a0 = sum3 的返回值 (60)
    
    ld      ra, 8(sp)         ; 恢復返回位址
    addi    sp, sp, 16        ; 釋放棧框架
    li      a0, 0             ; main 返回值
    jalr    x0, 0(ra)         ; 返回
```

## 19.4 棧框架結構

### 19.4.1 典型棧框架

```
高位址
+------------------+
|  參數 8          |  ← 呼叫者 push (如果需要)
+------------------+
|  參數 7          |
+------------------+
|  ...             |
+------------------+
|  參數 N          |
+------------------+ <- sp' (呼叫後新的 sp)
|  保存的 ra       |  ← jal 之後自動 push (軟體約定)
+------------------+
|  保存的 s0 (fp)  |  ← 被呼叫者保存
+------------------+ ← fp (frame pointer)
|  本地變數 1      |
+------------------+
|  本地變數 2      |
+------------------+
|  ...             |
+------------------+ <- sp (當前)
低位址
```

### 19.4.2 Frame Pointer 省略

現代編譯器經常省略 frame pointer（`fno-omit-frame-pointer` vs `-fomit-frame-pointer`）：

```asm
# 有 frame pointer
sum3:
    addi    sp, sp, -8
    sd      ra, 0(sp)
    addi    fp, sp, 8      ; fp = sp + 8
    # ... 使用 fp 存取本地變數
    ld      ra, 0(sp)
    addi    sp, sp, 8
    ret

# 沒有 frame pointer (更節省空間)
sum3:
    addi    sp, sp, -8
    sd      ra, 0(sp)
    # ... 使用 sp + offset 存取本地變數
    ld      ra, 0(sp)
    addi    sp, sp, 8
    ret
```

## 19.5 複雜參數傳遞

### 19.5.1 結構成員

```c
struct Point {
    long long x;
    long long y;
};

long long dist(struct Point p) {
    return p.x * p.x + p.y * p.y;
}
```

因為 `Point` 佔 16 位元組 (2 個 int64)，會用 a0 和 a1 傳遞：

```asm
dist:
    # a0 = p.x ( caller loaded )
    # a1 = p.y ( caller loaded )
    mul     a0, a0, a0
    mul     a1, a1, a1
    add     a0, a0, a1
    ret
```

### 19.5.2 大結構體

大於 16 位元組的結構體：
- 呼叫者配置記憶體
- 將指標傳入 a0（作為隱含第一個參數）
- 剩餘空間用 a1, a2...

```c
struct Big {
    long long a, b, c, d;
};

void init(struct Big *p) {
    p->a = 1;
    p->b = 2;
    // ...
}
```

### 19.5.3 可變參數函式

```c
int sum(int count, ...) {
    va_list args;
    va_start(args, count);
    int total = 0;
    for (int i = 0; i < count; i++) {
        total += va_arg(args, int);
    }
    va_end(args);
    return total;
}
```

va_list 通常實作為棧指標陣列。

## 19.6 遞迴函式

### 19.6.1 費波那契數列

```c
long long fib(long long n) {
    if (n <= 1) return n;
    return fib(n-1) + fib(n-2);
}
```

```asm
fib:
    # 棧框架分配
    addi    sp, sp, -24     ; 24 位元組
    sd      ra, 16(sp)       ; 保存返回位址
    sd      s0, 8(sp)        ; 保存 s0
    addi    s0, sp, 24       ; 設定 frame pointer
    
    # 保存參數到棧（可選，用於巢狀呼叫需要）
    sd      a0, -16(s0)      ; 保存 n
    
    # if (n <= 1)
    li      t0, 1
    ble     a0, t0, .Lbase   ; if (n <= 1) goto .Lbase
    
    # fib(n-1)
    ld      a0, -16(s0)
    addi    a0, a0, -1
    jal     ra, fib          ; 呼叫 fib(n-1)
    # 返回值在 a0 (result1)
    sd      a0, -24(s0)      ; 保存 result1
    
    # fib(n-2)
    ld      a0, -16(s0)
    addi    a0, a0, -2
    jal     ra, fib          ; 呼叫 fib(n-2)
    # 返回值在 a0 (result2)
    
    # 加上 result1
    ld      t0, -24(s0)
    add     a0, a0, t0       ; a0 = result2 + result1
    
    j       .Lreturn

.Lbase:
    # return n
    ld      a0, -16(s0)      ; a0 = n

.Lreturn:
    # 棧框架釋放
    ld      ra, 16(sp)       ; 恢復 ra
    ld      s0, 8(sp)        ; 恢復 s0
    addi    sp, sp, 24        ; 釋放棧框架
    ret
```

## 19.7 Leaf vs Non-Leaf 函式

### 19.7.1 Leaf 函式

Leaf 函式是不呼叫其他函式的函式：

```asm
# 優化版本（假設 t0, t1 是 caller-saved）
leaf_func:
    # 可以在這裡使用 t0-t6，不需保存
    add     a0, a0, a1
    # 如果不使用棧，可以直接返回
    ret
```

### 19.7.2 Non-Leaf 函式

Non-leaf 函式呼叫其他函式：

```asm
non_leaf:
    addi    sp, sp, -8       ; 必須保存 ra
    sd      ra, 0(sp)
    jal     other_func
    ld      ra, 0(sp)
    addi    sp, sp, 8
    ret
```

## 19.8 暫存器保存責任

### 19.8.1 Caller-Saved 暫存器

使用前不需要保存，呼叫其他函式後可能已經改變：
```
t0-t6 (7 個)
a0-a7 (8 個)
ra (返回位址)
```

### 19.8.2 Callee-Saved 暫存器

使用前需要保存，返回前需要恢復：
```
s0-s11 (12 個)
sp (堆疊指標)
gp, tp (根據abi)
```

```asm
example:
    addi    sp, sp, -16      ; 分配空間
    sd      s0, 8(sp)        ; 保存 s0
    sd      s1, 0(sp)        ; 保存 s1
    
    # 使用 s0, s1...
    
    ld      s0, 8(sp)        ; 恢復 s0
    ld      s1, 0(sp)        ; 恢復 s1
    addi    sp, sp, 16        ; 恢復 sp
    ret
```

## 19.9 棧溢位檢測

### 19.9.1 手動檢測

```c
void *get_sp() {
    long long dummy;
    return &dummy;
}

void safe_function() {
    void *sp_start = get_sp();
    // ... 使用堆疊 ...
    void *sp_end = get_sp();
    if (sp_end > sp_start + STACK_LIMIT) {
        // 棧溢位！
    }
}
```

### 19.9.2 GCC 棧保護

```bash
gcc -fstack-protector -S foo.c
```

會插入棧金絲雀（canary）檢測。

## 19.10 小結

本章節我們學習了：
- RISC-V 呼叫約定的基本規則
- 參數傳遞（前 8 個用 a0-a7）
- 返回值傳遞（a0-a1）
- 暫存器保存責任（callee vs caller saved）
- 棧框架的結構和對齊
- Leaf 和 Non-Leaf 函式
- 遞迴函式的實現

## 19.11 習題

1. 手寫一個遞迴函式並分析產生的組語
2. 實現一個使用 10 個參數的函式呼叫
3. 比較有/無 frame pointer 的組語差異
4. 研究可變參數函式 (`va_start`) 的實現
5. 為 mini-riscv-os 或 xv6 追蹤一個系統呼叫的堆疊
