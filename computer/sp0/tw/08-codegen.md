# 8. 程式碼生成——從語法樹到虛擬機指令

## 8.1 程式碼生成的任務

程式碼生成（Code Generation）是編譯器將語法分析結果轉為目標程式碼的階段。在 c4 中，目標是虛擬機的位元組碼。

```
語法分析 → AST/直接生成 → 虛擬機指令 → 虛擬機執行
```

c4 使用「語意制導翻譯」方法：在語法分析的同時直接發射指令，不需要建立顯式的語法樹。

## 8.2 c4 的程式碼發射

c4 使用一個全域指標 `e` 來發射指令：

```c
int *e;  // current position in emitted code

// 發射一條指令
*++e = opcode;    // 先遞增指標，再存入值
```

發射的記憶體布局：
```
記憶體: [opcode][operand][opcode][operand]...
         ↑
         e 指向當前位置
```

## 8.3 即時補丁（Backpatching）

很多指令需要跳轉目標位址，但目標位址在跳轉發射時還不知道。c4 使用「即時補丁」技術：

```c
// 發射條件跳躍
*++e = BNZ;  // Branch if Not Zero
d = ++e;     // 記住補丁位置，d 指向待填入的目標位址

// ... 發射跳轉後的指令 ...

// 補丁：填入目標位址
*d = (int)(e + 1);  // 計算並填入目標
```

## 8.4 表達式程式碼生成

### 8.4.1 即時值

```c
if (tk == Num) { 
    *++e = IMM;    // 載入立即值指令
    *++e = ival;   // 立即值
    next(); 
}
```

生成的指令：
```
IMM 42     ; 載入立即值 42
```

### 8.4.2 變數載入

```c
if (d[Class] == Loc) { 
    *++e = LEA; *++e = loc - d[Val];  // 局部位址
}
else if (d[Class] == Glo) { 
    *++e = IMM; *++e = d[Val];  // 全域位址
}
*++e = (ty = d[Type]) == CHAR ? LC : LI;  // 載入值
```

生成的指令：
```
LEA -8     ; 載入局部變數位址（相對於 bp）
LI         ; 載入整數值
```

### 8.4.3 加法

```c
else if (tk == Add) {
    next(); *++e = PSH;    // 保存左運算元
    expr(Mul);
    *++e = ADD;            // 彈出並相加
}
```

生成的指令（對於 `a + b`）：
```
... a 的程式碼 ...
PSH         ; 推入堆疊
... b 的程式碼 ...
ADD         ; 彈出兩個值相加
```

執行時：
```
初始: [a]           ; a 在累加器
PSH: [] [a]          ; 堆疊: [a]，累加器: a
b: [b]               ; 累加器: b
ADD: [a+b]           ; 堆疊: []，累加器: a+b
```

### 8.4.4 賦值

```c
if (tk == Assign) {
    next();
    if (*e == LC || *e == LI) 
        *e = PSH;  // 保留載入指令，轉為保存指標
    else { printf("bad lvalue\n"); exit(-1); }
    expr(Assign);   // 右側值
    *++e = SC;       // 存入指標
}
```

生成的指令（對於 `x = 5`）：
```
LEA -8     ; x 的位址
PSH        ; 保存位址
IMM 5      ; 載入 5
SC         ; 存入
```

## 8.5 函式呼叫程式碼生成

### 8.5.1 函式呼叫

```c
if (tk == '(') {
    next();
    t = 0;
    while (tk != ')') { 
        expr(Assign); 
        *++e = PSH;  // 參數入棧
        ++t; 
        if (tk == ',') next(); 
    }
    next();
    if (d[Class] == Sys) 
        *++e = d[Val];  // 系統呼叫
    else if (d[Class] == Fun) { 
        *++e = JSR; 
        *++e = d[Val];  // 跳到函式
    }
    if (t) { *++e = ADJ; *++e = t; }  // 清理參數
}
```

生成的指令（對於 `printf("Hello")`）：
```
IMM addr_of_string  ; 字串指標
PSH                 ; 推入參數
PRTF                ; 呼叫 printf
ADJ 1               ; 清理 1 個參數
```

### 8.5.2 函式進入和離開

函式進入（ENT）：
```c
*++e = ENT; 
*++e = i - loc;  // 棧框大小
```

相當於：
```
push bp
bp = sp
sp = sp - frame_size
```

函式離開（LEV）：
```c
*++e = LEV;
```

相當於：
```
sp = bp
pop bp
pc = *sp; sp++
```

## 8.6 控制結構程式碼生成

### 8.6.1 if-else

```c
if (tk == If) {
    next();
    expr(Assign);          // 條件
    *++e = BZ; b = ++e;     // 發射條件跳躍，記住補丁位置
    stmt();                // then 語句
    
    if (tk == Else) {
        *b = (int)(e + 3);  // 補丁：跳過 else 區塊
        *++e = JMP; b = ++e;
        next();
        stmt();            // else 語句
    }
    *b = (int)(e + 1);     // 補丁：跳過 then 或 else 區塊
}
```

生成的指令：
```
... 條件程式碼 ...
BZ .L1           ; 條件為假，跳到 else
... then 區塊 ...
JMP .L2          ; 跳過 else 區塊
.L1:
... else 區塊 ...
.L2:
```

### 8.6.2 while

```c
if (tk == While) {
    next();
    a = e + 1;             ; 記住迴圈開始位置
    expr(Assign);          // 條件
    *++e = BZ; b = ++e;    // 發射跳出跳躍
    stmt();                ; 迴圈體
    *++e = JMP; *++e = (int)a;  ; 跳回迴圈開始
    *b = (int)(e + 1);     ; 補丁：跳出目標
}
```

生成的指令：
```
.L0:              ; 迴圈開始
... 條件程式碼 ...
BZ .L1            ; 條件為假，跳出
... 迴圈體 ...
JMP .L0           ; 跳回迴圈開始
.L1:              ; 迴圈結束
```

### 8.6.3 return

```c
if (tk == Return) {
    next();
    if (tk != ';') expr(Assign);
    *++e = LEV;            // 發射離開指令
    if (tk == ';') next();
}
```

## 8.7 完整範例

原始碼：
```c
int main() {
    int a;
    a = 10;
    if (a > 5) {
        return a - 3;
    }
    return 0;
}
```

生成的虛擬機指令：
```
ENT  3            ; 進入 main，3 個本地空間
LEA  -4            ; a 的位址
PSH  
IMM  10            ; 載入 10
SC               ; a = 10
IMM  -4           ; a 的位址
LI               ; 載入 a
PSH  
IMM  5            ; 載入 5
GT               ; a > 5
BZ  .L1           ; 條件為假，跳到 .L1
IMM  -4           ; a 的位址
LI               ; 載入 a
PSH  
IMM  3            ; 載入 3
SUB               ; a - 3
LEV               ; return
JMP  .L2          ; 跳到函式結束
.L1:
IMM  0            ; 載入 0
LEV               ; return 0
.L2:
```

## 8.8 程式碼生成策略比較

### 8.8.1 c4 的策略：語意制導翻譯

優點：
- 簡單直接
- 不需要建立語法樹
- 記憶體效率高

缺點：
- 難以優化
- 錯誤處理複雜

### 8.8.2 現代編譯器的策略

1. **語法樹 → 中間表示 (IR)**
2. **最佳化**
3. **目標程式碼生成**

```
原始碼 → Token → AST → IR → 優化後 IR → 目標碼
              ↑                      ↑
           語法分析               程式碼生成
```

## 8.9 小結

本章節我們學習了：
- 程式碼生成的基本概念
- c4 的指令發射機制
- 即時補丁技術
- 表達式、賦值、函式呼叫的程式碼生成
- if-else、while、return 的程式碼生成
- 完整範例的指令序列

## 8.10 習題

1. 手動追蹤 `a = (b + c) * d` 的程式碼生成過程
2. 為 c4 添加 `for` 迴圈支援
3. 為 c4 添加 `do-while` 迴圈支援
4. 研究現代編譯器如何實現死碼消除（Dead Code Elimination）
5. 實現一個簡單的常量摺疊（Constant Folding）優化
