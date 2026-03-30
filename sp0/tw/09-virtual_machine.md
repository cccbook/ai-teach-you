# 9. 虛擬機——堆疊式指令集架構

## 9.1 虛擬機簡介

虛擬機是一種軟體模擬的電腦系統。它有自己的指令集、暫存器和記憶體模型，可以在沒有實際硬體的情況下執行程式。

c4 內建一個**堆疊式虛擬機**，這意味著：
- 運算元隱式地從堆疊取得（無需指定暫存器）
- 結果隱式地放回堆疊
- 適合實現簡單的語言

## 9.2 c4 虛擬機架構

### 9.2.1 暫存器

```c
int *pc, *sp, *bp, a, cycle;
// pc: 程式計數器 (Program Counter)
// sp: 堆疊指標 (Stack Pointer)
// bp: 基底指標 (Base Pointer)
// a:  累加器 (Accumulator)
// cycle: 執行週期計數
```

### 9.2.2 記憶體佈局

```c
char *data;   // 資料段：字串常量等
int *e;       // 程式碼段發射指標
int *le;      // 程式碼段當前指標
int *sym;     // 符號表
int *sp;      // 堆疊段指標
```

### 9.2.3 堆疊使用

```
低位址 ← [ 資料段 ] → [ 程式碼段 ] → [ 符號表 ] → [ 堆疊段 ] → 高位址
                   ↑
                   e, le 指向這裡

sp 指向堆疊頂端，向低地址生長
```

## 9.3 虛擬機初始化

```c
poolsz = 256*1024;  // 256KB

sym  = malloc(poolsz);  // 符號表
e    = malloc(poolsz);  // 程式碼
data = malloc(poolsz);  // 資料
sp   = malloc(poolsz);  // 堆疊

memset(sym,  0, poolsz);
memset(e,    0, poolsz);
memset(data, 0, poolsz);

lp = p = malloc(poolsz);  // 原始碼緩衝區
```

## 9.4 指令解釋器

```c
cycle = 0;
while (1) {
    i = *pc++;           // 取指令，pc 前進
    ++cycle;
    
    // 執行指令...
    
    if (i == EXIT) { 
        printf("exit(%d) cycle = %d\n", *sp, cycle); 
        return *sp; 
    }
}
```

## 9.5 載入和儲存指令

### 9.5.1 LEA - 載入有效位址

```c
else if (i == LEA) 
    a = (int)(bp + *pc++);  // a = bp + offset
```

用途：取得本地變數的位址（相對於基底指標）

### 9.5.2 IMM - 載入立即值

```c
else if (i == IMM) 
    a = *pc++;  // a = *pc; pc++
```

### 9.5.3 LI/LC - 載入整數/字元

```c
else if (i == LI) 
    a = *(int *)a;        // a = *((int *)a)
else if (i == LC) 
    a = *(char *)a;       // a = *((char *)a)
```

### 9.5.4 SI/SC - 儲存整數/字元

```c
else if (i == SI) 
    *(int *)*sp++ = a;    // *sp = a; sp++
else if (i == SC) 
    a = *(char *)*sp++ = a;  // *sp = (char)a; sp++
```

## 9.6 堆疊指令

### 9.6.1 PSH - 推入堆疊

```c
else if (i == PSH) 
    *--sp = a;  // sp--; *sp = a
```

```
執行前:     執行後:
  sp → [xxx]      sp → [a   ]
            [yyy]           [xxx]
            [zzz]           [yyy]
                          [zzz]
```

## 9.7 算術指令

所有二元運算都遵循同樣模式：彈出兩個值，計算，結果放入累加器。

```c
else if (i == ADD) 
    a = *sp++ + a;     // a = *sp + a; sp++

else if (i == SUB) 
    a = *sp++ - a;     // a = *sp - a; sp++

else if (i == MUL) 
    a = *sp++ * a;     // a = *sp * a; sp++

else if (i == DIV) 
    a = *sp++ / a;     // a = *sp / a; sp++
```

範例（計算 `3 + 4`）：
```
IMM 3      ; a = 3
PSH        ; sp--; *sp = 3
IMM 4      ; a = 4
ADD        ; a = *sp + a = 3 + 4 = 7; sp++
結果: a = 7
```

## 9.8 比較指令

```c
else if (i == LT)  a = *sp++ <  a;
else if (i == GT)  a = *sp++ >  a;
else if (i == LE)  a = *sp++ <= a;
else if (i == GE)  a = *sp++ >= a;
else if (i == EQ)  a = *sp++ == a;
else if (i == NE)  a = *sp++ != a;
```

結果是 0（false）或 1（true）。

## 9.9 位元指令

```c
else if (i == AND) a = *sp++ &  a;
else if (i == OR)  a = *sp++ |  a;
else if (i == XOR) a = *sp++ ^  a;
else if (i == SHL) a = *sp++ << a;
else if (i == SHR) a = *sp++ >> a;
else if (i == MOD) a = *sp++ %  a;
```

## 9.10 控制流程指令

### 9.10.1 JMP - 無條件跳躍

```c
else if (i == JMP) 
    pc = (int *)*pc;  // pc = *pc
```

### 9.10.2 BZ/BNZ - 條件跳躍

```c
else if (i == BZ)  
    pc = a ? pc + 1 : (int *)*pc;  // if (a == 0) pc = *pc

else if (i == BNZ) 
    pc = a ? (int *)*pc : pc + 1;  // if (a != 0) pc = *pc
```

### 9.10.3 JSR - 跳躍到子程式

```c
else if (i == JSR) { 
    *--sp = (int)(pc + 1);  // 保存返回位址
    pc = (int *)*pc;        // 跳轉
}
```

## 9.11 函式呼叫指令

### 9.11.1 ENT - 進入函式

```c
else if (i == ENT) { 
    *--sp = (int)bp;   // 保存舊基底指標
    bp = sp;           // 設定新基底指標
    sp = sp - *pc++;   // 分配本地空間
}
```

相當於 x86-64 的：
```asm
push rbp
mov rbp, rsp
sub rsp, frame_size
```

### 9.11.2 LEV - 離開函式

```c
else if (i == LEV) { 
    sp = bp;           // 恢復堆疊
    bp = (int *)*sp++; // 恢復基底指標
    pc = (int *)*sp++; // 返回
}
```

相當於：
```asm
mov rsp, rbp
pop rbp
ret
```

### 9.11.3 ADJ - 調整堆疊

```c
else if (i == ADJ) 
    sp = sp + *pc++;  // 清理呼叫者棧框中的參數
```

## 9.12 函式呼叫範例

呼叫 `printf("Hello")`：

```
初始堆疊: [未使用空間...]
           [返回位址]  ← 呼叫前由 JSR 推入
           [舊 bp]     ← 由 ENT 推入
           [本地空間]
sp →

執行 ENT frame_size:
sp → [本地空間...]

執行 printf:
PRTF

執行 ADJ 1:
sp = sp + 1  ; 清理參數

執行 LEV:
返回呼叫者
```

## 9.13 系統呼叫

### 9.13.1 PRTF - printf

```c
else if (i == PRTF) { 
    t = sp + pc[1];    // 取得參數指標
    a = printf((char *)t[-1], t[-2], t[-3], t[-4], t[-5], t[-6]); 
}
```

最多支援 6 個參數，格式化字串在 `t[-1]`。

### 9.13.2 MALC - malloc

```c
else if (i == MALC) 
    a = (int)malloc(*sp);  // 配置記憶體
```

### 9.13.3 EXIT

```c
else if (i == EXIT) { 
    printf("exit(%d) cycle = %d\n", *sp, cycle); 
    return *sp; 
}
```

## 9.14 完整執行範例

原始碼：
```c
int main() {
    return 2 + 3;
}
```

執行追蹤：

| 步驟 | 指令 | pc | a | sp | 堆疊 |
|------|------|-----|---|-----|------|
| 1 | ENT 0 | +1 | - | - | ... |
| 2 | IMM 2 | +2 | 2 | - | ... |
| 3 | PSH | - | 2 | -1 | [2] |
| 4 | IMM 3 | +1 | 3 | -1 | [2] |
| 5 | ADD | - | 5 | 0 | [] |
| 6 | LEV | - | 5 | - | 返回 |

## 9.15 除錯模式

使用 `-d` 選項可以追蹤執行：

```bash
./c4 -d hello.c
```

輸出：
```
1> ENT
2> IMM 10
3> PSH
4> IMM 5
5> GT
6> BZ
...
```

## 9.16 小結

本章節我們學習了：
- c4 堆疊式虛擬機的架構
- 暫存器角色：pc, sp, bp, a
- 載入/儲存指令：LEA, IMM, LI, LC, SI, SC
- 算術指令：ADD, SUB, MUL, DIV, MOD
- 比較和位元指令
- 控制流程：JMP, BZ, BNZ, JSR
- 函式呼叫：ENT, LEV, ADJ
- 系統呼叫：PRTF, MALC, EXIT

## 9.17 習題

1. 使用 `-d` 選項追蹤 hello.c 的執行
2. 手動執行一個簡單程式（計算 10!）
3. 研究為什麼二元運算要先 PSH 再計算
4. 實現一個簡單的堆疊式虛擬機（如 WebAssembly 的簡化版本）
5. 比較堆疊式架構和暫存器架構的優缺點
