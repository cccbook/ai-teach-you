# 5. c4：僅用四個函式打造的 C 編譯器

## 5.1 世界上最小的 C 編譯器

Robert Swierczek 寫了一個令人驚嘆的 C 編譯器——c4。整個編譯器只有 528 行 C 程式碼，卻能：
- 編譯 C 語言的一個子集
- **自我編譯**（用 c4 編譯 c4.c）
- 生成自己的虛擬機位元組碼

c4 的原始碼位於：[_code/c4/c4.c](../_code/c4/c4.c)

## 5.2 c4 支援的功能

### 支援的特性：
- **資料類型**：`char`、`int`、指標
- **控制結構**：`if/else`、`while`、`return`
- **運算子**：算術、邏輯、位元、比較
- **函式呼叫**：支援系統函式和自訂函式
- **全域/本地變數**

### 不支援的特性：
- `struct`、`union`
- `float`、`double`
- 陣列（指標代替）
- 預處理器巨集（`#include`、`#define`）
- 標準函式庫（內建部分常用函式）

## 5.3 四個核心函式

c4 的核心由四個函式組成：

```c
void next()       // 詞彙分析器：讀取下一個 token
void expr(int lev) // 表達式解析：處理運算子優先順序
void stmt()        // 語句解析：處理控制結構
int main()         // 主函式：檔案讀取、符號表、虛擬機執行
```

整個編譯-解釋流程：
```
原始碼 → next() (詞彙分析) 
       → stmt() + expr() (語法/語意分析 + 程式碼生成)
       → 虛擬機指令 
       → main() 中的虛擬機執行
```

## 5.4 編譯與執行 c4

```bash
cd _code/c4

# 編譯 c4
gcc -o c4 c4.c

# 查看幫助
./c4

# 編譯 hello.c 並執行
./c4 hello.c

# 查看生成的組語（-s 選項）
./c4 -s hello.c
```

## 5.5 c4 的虛擬機架構

c4 內建一個堆疊式虛擬機，有以下暫存器：

```c
int *pc, *sp, *bp, a, cycle;  // vm registers
```

- `pc`：程式計數器，指向下一條要執行的指令
- `sp`：堆疊指標，指向堆疊頂端
- `bp`：基底指標，用於存取本地變數
- `a`：累加器，儲存運算結果

記憶體區域：
```c
char *data;   // 資料段指標
int *e;       // 程式碼發射指標
int *sym;     // 符號表指標
int *sp;      // 堆疊指標
```

## 5.6 c4 的指令集

c4 有 31 條指令，分為幾類：

### 控制流程：
```c
enum { LEA ,IMM ,JMP ,JSR ,BZ  ,BNZ ,ENT ,ADJ ,LEV ,... };
// LEA: 載入本地位址 (Load Effective Address)
// IMM: 載入立即值 (Immediate)
// JMP: 跳躍 (Jump)
// JSR: 跳躍到子程式 (Jump to SubRoutine)
// BZ:  if zero 跳躍 (Branch if Zero)
// BNZ: if not zero 跳躍
// ENT: 進入函式 (Enter)
// ADJ: 調整堆疊 (Adjust)
// LEV: 離開函式 (Leave)
```

### 記憶體存取：
```c
LI  ,   // 載入整數 (Load Integer)
LC  ,   // 載入字元 (Load Char)
SI  ,   // 儲存整數 (Store Integer)
SC  ,   // 儲存字元 (Store Char)
PSH ,   // 推入堆疊 (Push)
```

### 算術邏輯：
```c
OR  ,XOR ,AND ,EQ  ,NE  ,LT  ,GT  ,LE  ,GE  ,
SHL ,SHR ,ADD ,SUB ,MUL ,DIV ,MOD ,
```

### 系統呼叫：
```c
OPEN,READ,CLOS,PRTF,MALC,FREE,MSET,MCMP,EXIT
// PRTF: printf, MALC: malloc, EXIT: exit
```

## 5.7 自我編譯的奇蹟

最令人驚嘆的是：c4 可以編譯自己！

```bash
# 用 gcc 編譯 c4
gcc -o c4 c4.c

# 用 c4 編譯 c4.c（生成新的虛擬機指令）
./c4 c4.c hello.c

# 現在 hello 是用 c4 自己編譯出來的版本！
./hello
```

這個自我編譯能力展示了小型、自包含編譯器的威力。

## 5.8 程式碼結構分析

### 5.8.1 詞彙分析器 next()

`next()` 函式負責：
1. 跳過空白字元
2. 處理換行（可選地列印原始碼和生成的指令）
3. 解析識別符和關鍵字
4. 解析數值常量和字元/字串常量
5. 處理運算子和符號

詞彙分析的核心是**雜湊識別符**：

```c
tk = tk * 147 + *p++;  // 簡單的雜湊函式
tk = (tk << 6) + (p - pp);  // 加入長度
```

### 5.8.2 表達式解析器 expr()

使用**優先順序 climbing**（或 Pratt parser）方法：

```c
void expr(int lev) {
    // ... 處理一元運算子、前綴、原子表達式 ...
    
    while (tk >= lev) {  // 根據優先順序處理二元運算子
        if (tk == '+') { next(); expr(Mul); *++e = ADD; }
        if (tk == '-') { next(); expr(Mul); *++e = SUB; }
        // ...
    }
}
```

### 5.8.3 語句解析器 stmt()

處理控制結構：

```c
void stmt() {
    if (tk == If) {
        // if (condition) statement [else statement]
        expr(Assign);
        *++e = BZ; b = ++e;  // 發射條件跳躍
        stmt();
        if (tk == Else) {
            *b = (int)(e + 3);
            *++e = JMP; b = ++e;
            next(); stmt();
        }
        *b = (int)(e + 1);
    }
    else if (tk == While) {
        // while (condition) statement
        a = e + 1;
        expr(Assign);
        *++e = BZ; b = ++e;
        stmt();
        *++e = JMP; *++e = (int)a;
        *b = (int)(e + 1);
    }
    // ...
}
```

## 5.9 從 C 到虛擬機指令的轉換

讓我們追蹤一個簡單程式的編譯過程：

```c
int main() {
    return 2 + 3;
}
```

編譯生成的指令：
```
IMM 2        ; 載入立即值 2
PSH          ; 推入堆疊
IMM 3        ; 載入立即值 3
ADD          ; 彈出兩個值相加
LEV          ; 返回
```

執行流程：
```
堆疊: []          ; 初始空堆疊
IMM 2 → 堆疊: [2]
PSH  → 堆疊: []
ADD  → 堆疊: [5]  ; 2+3=5
LEV  → 返回 5
```

## 5.10 小結

本章節我們：
- 認識了世界上最小的 C 編譯器 c4
- 了解了 c4 的四個核心函式
- 學習了 c4 的虛擬機架構和指令集
- 見證了自我編譯的奇蹟

## 5.11 習題

1. 下載並編譯 c4，嘗試執行 hello.c
2. 用 `c4 -s hello.c` 查看生成的指令
3. 嘗試修改 c4.c，增加一個小功能（如 ++、-- 運算子）
4. 研究 c4 如何處理遞迴函式呼叫
5. 追蹤一個複雜表達式的編譯過程
