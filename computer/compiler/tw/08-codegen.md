# 8. 目標碼生成

## 8.1 什麼是目標碼生成

目標碼生成（Code Generation）是編譯器的最後一個階段，負責將中間表示（IR）轉換為特定硬體平台的機器碼或組合語言。

## 8.2 LLVM 的目標碼生成

LLVM 的後端負責將 LLVM IR 轉換為目標機器的指令：

```
LLVM IR
   │
   ▼
┌────────────┐
│ 選擇指令    │  (Instruction Selection)
└────────────┘
   │
   ▼
┌────────────┐
│ 暫存器配置  │  (Register Allocation)
└────────────┘
   │
   ▼
┌────────────┐
│ 指令排程   │  (Instruction Scheduling)
└────────────┘
   │
   ▼
  機器碼
```

## 8.3 函數呼叫

[程式檔案：08-1-call.c](../_code/08/08-1-call.c)
```c
int add(int a, int b) {
    return a + b;
}

int main() {
    int result = add(10, 20);
    printf("Result: %d\n", result);
    return 0;
}
```

產生的 LLVM IR：

[程式檔案：08-1-call.ll](../_code/08/08-1-call.ll)
```llvm
define i32 @add(i32, i32) #0 {
  %3 = add nsw i32 %0, %1
  ret i32 %3
}

define i32 @main() #0 {
  %result = alloca i32, align 4
  %1 = call i32 @add(i32 10, i32 20)
  store i32 %1, i32* %result, align 4
  ret i32 0
}
```

## 8.4 指令選擇

指令選擇將 IR 指令轉換為目標機器的指令。以 x86-64 為例：

| LLVM IR | x86-64 組合語言 |
|---------|----------------|
| `add i32 %a, %b` | `addl %ebx, %eax` |
| `mul i32 %a, %b` | `imull %ebx, %eax` |
| `icmp slt i32 %a, %b` | `cmpl %ebx, %eax; setl %cl` |
| `br i1 %cond` | `jne .Llabel` |

## 8.5 暫存器配置

LLVM 使用圖著色演算法進行暫存器配置：

```bash
# 產生物理暫存器
llc -O2 -march=x86-64 example.ll -o example.s
```

產生的 x86-64 組合語言：

```asm
add:
    leal    (%rdi,%rsi), %eax
    ret

main:
    pushq   %rbp
    movq    %rsp, %rbp
    subq    $16, %rsp
    movl    $10, -4(%rbp)
    movl    $20, -8(%rbp)
    movl    -8(%rbp), %esi
    movl    -4(%rbp), %edi
    callq   add
    movl    %eax, -12(%rbp)
    addq    $16, %rsp
    popq    %rbp
    retq
```

## 8.6 使用 clang 生成目標碼

```bash
# 產生目的檔（.o）
clang -c example.c -o example.o

# 產生組合語言
clang -S example.c -o example.s

# 產生執行檔
clang example.c -o example

# 指定目標平台
clang -target x86_64-pc-linux-gnu example.c -o example
```

## 8.7 常見目標平台

LLVM 支援多種目標平台：

| Triple | 描述 |
|--------|------|
| x86_64-apple-darwin | macOS x86-64 |
| aarch64-apple-darwin | macOS ARM64 |
| x86_64-pc-linux-gnu | Linux x86-64 |
| aarch64-unknown-linux-gnu | Linux ARM64 |
| riscv64-unknown-elf | RISC-V 64-bit |

## 8.8 本章小結

本章介紹了目標碼生成的核心概念：
- LLVM 後端架構
- 指令選擇
- 暫存器配置
- 指令排程
- 使用 clang 生成目標碼

## 練習題

1. 比較不同目標平台產生的機器碼差異。
2. 分析暫存器配置演算法。
3. 為新的目標平台實作後端支援。
4. 研究指令排程對效能的影響。
