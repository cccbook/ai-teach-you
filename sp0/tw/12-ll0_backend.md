# 12. ll0 後端——LLVM IR 到 RISC-V 組語

## 12.1 什麼是編譯器後端？

編譯器後端負責將中間表示（IR）轉換為目標機器的程式碼。

```
前端 (Clang)     後端 (llc/ll0c)
   ↓                ↓
C → IR ──────→ 組語/機器碼
```

## 12.2 ll0c 是什麼？

ll0c 是 cpy0 專案中的 LLVM IR 到 RISC-V 組語的轉換工具。

位置：[_code/cpy0/ll0/](../_code/cpy0/ll0/)

## 12.3 使用 ll0c

```bash
# 基本用法
./ll0/ll0c/ll0c input.ll -o output.s

# 或使用 LLVM 的 LLC
llc fact.ll -o fact.s --mtriple=riscv64-unknown-elf
```

## 12.4 RISC-V 指令集基礎

RISC-V 是精簡指令集計算機，特點：
- 指令長度固定（32 位元）
- 暫存器數量多（32 個）
- 負載/儲存架構（記憶體只能透過 load/store 存取）

### 12.4.1 RISC-V 暫存器

| 暫存器 | 別名 | 用途 |
|--------|------|------|
| x0 | zero | 常數 0 |
| x1 | ra | 返回位址 |
| x2 | sp | 堆疊指標 |
| x3 | gp | 全域指標 |
| x4 | tp | 執行緒指標 |
| x5-x7 | t0-t2 | 暫存暫存器 |
| x8 | s0/fp | 保存暫存器 / 框架指標 |
| x9 | s1 | 保存暫存器 |
| x10-x17 | a0-a7 | 函式引數/返回值 |
| x18-x27 | s2-s11 | 保存暫存器 |
| x28-x31 | t3-t6 | 暫存暫存器 |

### 12.4.2 基本指令格式

```
R 類型: rd = rs1 op rs2
+-------+-------+-------+-------+-------+-------+
| 31-25 | 24-20 | 19-15 | 14-12 |  11-7 |  6-0 |
| funct7| rs2   | rs1   | funct3| rd    | opcode|
+-------+-------+-------+-------+-------+-------+

I 類型: rd = rs1 op imm
+-------+-------+-------+-------+-------+-------+
|  11-10|  9-5  | 4-0   |  12   |  11-7 |  6-0 |
|       | rs2   | rs1   | imm11 | rd    | opcode|
+-------+-------+-------+-------+-------+-------+

S 類型: mem[rs1+imm] = rs2
+-------+-------+-------+-------+-------+-------+
| 31-25 | 24-20 | 19-15 | 11-7  |  12   |  6-0 |
| imm11 | rs2   | rs1   | imm11 | imm4  | opcode|
+-------+-------+-------+-------+-------+-------+
```

## 12.5 常見 RISC-V 指令

### 12.5.1 算術指令

```asm
# 加法 (R 型)
add  a0, a0, a1    ; a0 = a0 + a1

# 減法
sub  a0, a0, a1    ; a0 = a0 - a1

# 立即數加法 (I 型)
addi sp, sp, -16   ; sp = sp - 16

# 乘法 (需要 M 擴展)
mul  a0, a0, a1    ; a0 = a0 * a1

# 除法 (需要 M 擴展)
div  a0, a0, a1    ; a0 = a0 / a1
```

### 12.5.2 邏輯指令

```asm
# AND
and  a0, a0, a1    ; a0 = a0 & a1
andi a0, a0, 0xFF  ; a0 = a0 & 0xFF

# OR
or   a0, a0, a1    ; a0 = a0 | a1

# XOR
xor  a0, a0, a1    ; a0 = a0 ^ a1
```

### 12.5.3 移位指令

```asm
# 左移
sll  a0, a0, a1    ; a0 = a0 << a1
slli a0, a0, 2     ; a0 = a0 << 2

# 邏輯右移
srl  a0, a0, a1    ; a0 = a0 >> a1
srli a0, a0, 2     ; a0 = a0 >> 2

# 算術右移（保留符號）
sra  a0, a0, a1
srai a0, a0, 2
```

### 12.5.4 比較指令

```asm
# 設定小於 (Set on Less Than)
slt  a0, a0, a1    ; a0 = (a0 < a1) ? 1 : 0
slti a0, a0, 10    ; a0 = (a0 < 10) ? 1 : 0

# 無號比較
sltu a0, a0, a1
sltiu a0, a0, 10
```

### 12.5.5 負載/儲存指令

```asm
# 載入 (I 型)
lw   a0, 0(sp)     ; a0 = *((int*)(sp + 0))
lui  a0, 0x10000    ; a0 = 0x10000 << 12

# 儲存 (S 型)
sw   a0, 0(sp)     ; *((int*)(sp + 0)) = a0
```

### 12.5.6 分支指令 (B 型)

```asm
# 分支相等
beq  a0, a1, .L1   ; if (a0 == a1) goto .L1

# 分支不等
bne  a0, a1, .L1

# 分支小於 (signed)
blt  a0, a1, .L1   ; if (a0 < a1) goto .L1
bge  a0, a1, .L1   ; if (a0 >= a1) goto .L1

# 分支小於 (unsigned)
bltu a0, a1, .L1
bgeu a0, a1, .L1
```

### 12.5.7 跳躍指令 (J 型)

```asm
# 無條件跳躍 (J 型)
jal  ra, .L1       ; ra = pc + 4; goto .L1

# 跳躍並連結 (函式呼叫)
jal  ra, callee    ; ra = pc + 4; goto callee

# 跳躍註冊 (R 型)
jalr ra, 0(callee) ; ra = pc + 4; goto *callee
ret                 ; jalr x0, 0(ra)
```

## 12.6 LLVM IR 到 RISC-V 的對應

### 12.6.1 加法

LLVM IR:
```llvm
%add = add i64 %a, %b
```

RISC-V:
```asm
add a0, a0, a1    ; 假設 a = a0, b = a1, 結果在 a0
```

### 12.6.2 條件分支

LLVM IR:
```llvm
%cmp = icmp slt i64 %a, %b
br i1 %cmp, label %then, label %else
```

RISC-V:
```asm
    blt a0, a1, .then    ; if (a < b) goto .then
    j .else
.then:
    ; then 區塊
.else:
    ; else 區塊
```

### 12.6.3 函式呼叫

LLVM IR:
```llvm
%ret = call i64 @callee(i64 %arg1, i64 %arg2)
```

RISC-V:
```asm
    mv a0, t0       ; 移動引數到 a0
    mv a1, t1       ; 移動引數到 a1
    jal ra, callee  ; 呼叫函式
    ; 返回值在 a0
```

## 12.7 函式呼叫約定

RISC-V 的函式呼叫約定（Calling Convention）：

### 12.7.1 參數傳遞

- 前 8 個整數參數：a0-a7
- 更多參數：透過堆疊
- 返回值：a0-a1

### 12.7.2 暫存器分類

| 類別 | 暫存器 | 用途 |
|------|--------|------|
| 保存者 (callee-saved) | s0-s11, sp, gp, tp | 函式負責保存 |
| 呼叫者 (caller-saved) | t0-t6, a0-a7, ra | 函式不需保存 |

### 12.7.3 棧框架

```asm
; 函式進入
frame:
    addi sp, sp, -frame_size   ; 分配棧框架
    ; 保存保存者暫存器
    sw ra, -4(sp)              ; 保存返回位址
    sw s0, -8(sp)              ; 保存 s0

; 函式離開
    ; 恢復保存者暫存器
    lw ra, -4(sp)
    lw s0, -8(sp)
    addi sp, sp, frame_size    ; 釋放棧框架
    ret
```

## 12.8 實際範例

完整的 LLVM IR 到 RISC-V 組語：

LLVM IR:
```llvm
define i64 @fact(i64 %n) {
entry:
  %cmp = icmp sle i64 %n, 1
  br i1 %cmp, label %then, label %else

then:
  ret i64 1

else:
  %sub = sub i64 %n, 1
  %call = call i64 @fact(i64 %sub)
  %mul = mul i64 %n, %call
  ret i64 %mul
}
```

RISC-V 組語:
```asm
    .text
    .globl fact
    .align 2
fact:
    # n 在 a0 中
    li t0, 1
    ble a0, t0, .LBB0_1   ; if (n <= 1) goto .LBB0_1
    
    # else 分支
    addi sp, sp, -16      ; 分配棧框架
    sw ra, 12(sp)         ; 保存返回位址
    sw a0, 8(sp)          ; 保存 n
    
    addi a0, a0, -1        ; n - 1
    jal ra, fact           ; 遞迴呼叫
    
    lw t0, 8(sp)           ; 恢復 n
    mul a0, t0, a0          ; n * fact(n-1)
    
    lw ra, 12(sp)          ; 恢復返回位址
    addi sp, sp, 16        ; 釋放棧框架
    ret
    
.LBB0_1:                  ; then 分支
    li a0, 1              ; 返回 1
    ret
```

## 12.9 使用 LLC 工具

LLVM 提供的 `llc` 工具可以用來測試：

```bash
# 使用 LLC 編譯 IR 到 RISC-V
llc -march=riscv64 fact.ll -o fact.s

# 指定 ABI
llc -march=riscv64 -mattr=+m,+f,+c fact.ll -o fact.s

# 顯示最佳化後的組語
llc -march=riscv64 -O2 fact.ll -o fact_O2.s
```

## 12.10 小結

本章節我們學習了：
- 編譯器後端的概念
- RISC-V 指令集基礎
- 各類指令格式（R、I、S、B、J）
- LLVM IR 到 RISC-V 的對應
- RISC-V 函式呼叫約定
- 使用 ll0c 或 LLC 進行轉換

## 12.11 習題

1. 用 `llc` 將 cpy0 中的 LLVM IR 編譯到 RISC-V
2. 比較不同最佳化等級 (-O0, -O2) 生成的組語
3. 手動翻譯一個簡單的 LLVM IR 函式到 RISC-V
4. 研究 RISC-V 的壓縮指令集 (C 擴展)
5. 實現一個簡單的 LLVM IR 到 x86 的後端
