# 1. 從高階語言到機器碼——C 語言的本質

## 1.1 為什麼要學 C 語言？

在這個充斥著 Python、JavaScript、Go、Rust 的年代，為什麼我們還要學習 C 語言？答案很簡單：**C 語言是最接近硬體的高階語言，同時又是理解電腦系統的最佳起點。**

當你寫下這段程式碼：

```c
int main() {
    int a = 10;
    int b = 20;
    int c = a + b;
    return c;
}
```

你以為電腦直接「懂」了這段程式碼嗎？錯。電腦只懂 0 和 1。從你寫的程式碼到實際被執行的機器指令，中間經過了複雜的轉換過程。

## 1.2 編譯流程總覽

```
原始碼 (source.c)
    │
    ▼  [預處理器 cpp]
預處理後程式碼
    │
    ▼  [編譯器 gcc/clang]
組語 (assembly.s)
    │
    ▼  [組譯器 as]
目的檔 (object.o)
    │
    ▼  [連結器 ld]
可執行檔 (executable)
```

讓我們用實際例子來看看這個流程。假設有個 `hello.c`：

```c
#include <stdio.h>

int main() {
    printf("Hello, World!\n");
    return 0;
}
```

使用編譯器查看各階段輸出：

```bash
# 預處理
gcc -E hello.c -o hello.i

# 編譯到組語
gcc -S hello.c -o hello.s

# 組譯到目的檔
gcc -c hello.c -o hello.o

# 連結成執行檔
gcc hello.c -o hello
```

## 1.3 預處理器做了什麼？

預處理器會處理 `#include`、`#define`、巨集展開等。看看 `hello.i` 的開頭，你會看到標準頭文件的展開內容。

關鍵的 `#include` 展開：stdio.h 的內容被插入到你的程式碼中。這些展開後的內容提供了 `printf` 的函式宣告。

## 1.4 編譯器的工作

編譯器將 C 語法轉換成目標平台的組語。不同 CPU 架構（x86、ARM、RISC-V）有不同的組語。

C 語言被稱為「可移植的組語」，因為：
- 沒有隱藏的記憶體管理
- 沒有自動垃圾回收
- 指標讓你可以直接操作記憶體位址
- 手動管理堆疊和堆積

## 1.5 組語長什麼樣子？

x86-64 的 Hello World 組語：

```asm
section .data
    msg db 'Hello, World!', 0
    len equ $ - msg

section .text
global _start
_start:
    mov rax, 1        ; 系統呼叫編號 (write)
    mov rdi, 1        ; 檔案描述符 (stdout)
    mov rsi, msg      ; 訊息指標
    mov rdx, len      ; 訊息長度
    syscall           ; 觸發系統呼叫
    mov rax, 60       ; 系統呼叫編號 (exit)
    xor rdi, rdi      ; 返回值 0
    syscall           ; 離開程式
```

RISC-V 的等價程式：

```asm
.section .data
msg:
    .string "Hello, World!\n"
    len = 14

.section .text
.globl _start
_start:
    li a0, 1          ; 檔案描述符 (stdout)
    la a1, msg        ; 訊息指標
    li a2, len        ; 訊息長度
    li a7, 64         ; 系統呼叫編號 (write)
    ecall
    li a0, 0          ; 返回值
    li a7, 93         ; 系統呼叫編號 (exit)
    ecall
```

## 1.6 C 語言的設計哲學

Brian Kernighan 和 Dennis Ritchie 在《The C Programming Language》中闡述的原則：

1. **信任程式員** - C 假設你知道自己在做什麼，不會阻止你做「危險」的事
2. **機制，而非策略** - 提供基本機制，讓程式員決定如何使用
3. **簡單性** - 用少量但強大的概念建構複雜系統

這種設計哲學讓 C 成為系統程式的首選語言：作業系統、嵌入式系統、編譯器、資料庫、驅動程式。

## 1.7 第一個 C 程式的秘密

讓我們更深入看 `main` 函式：

```c
int main(void) {
    // 你的程式碼
    return 0;
}
```

`main` 的幾種合法簽名：
```c
int main(void);           // 標準 C
int main(int argc, char *argv[]);  // 接受命令列參數
int main(int argc, char **argv);    // 同上，另一種寫法
```

沒有 `return`？在 C99 之後，如果 `main` 沒有显式返回，預設返回 0。

## 1.8 編譯自己的第一個程式

```bash
# 建立目錄和檔案
mkdir -p examples/ch01
cat > examples/ch01/hello.c << 'EOF'
#include <stdio.h>

int main(void) {
    printf("Hello, System Programming!\n");
    return 0;
}
EOF

# 編譯並執行
gcc -Wall -Wextra -o examples/ch01/hello examples/ch01/hello.c
./examples/ch01/hello
```

`-Wall -Wextra` 開啟所有警告，幫助你寫出更好的程式碼。

## 1.9 小結

本章節我們學習了：
- C 語言是接近硬體的高階語言
- 編譯流程：預處理 → 編譯 → 組譯 → 連結
- 組語是 CPU 的原始語言
- C 的設計哲學：信任程式員、簡單性

## 1.10 習題

1. 編譯一個 C 程式，用 `gcc -S` 查看生成的組語
2. 用 `gcc -E` 查看預處理後的輸出
3. 比較 `gcc` 和 `clang` 生成的組語有何不同
4. 查閱你正在使用的平台的呼叫約定（ABI）
