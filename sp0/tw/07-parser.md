# 7. 語法分析——表達式與優先順序

## 7.1 語法分析的任務

語法分析（Syntax Analysis / Parsing）是編譯器的第二階段。它的任務是：
- 接收 Token 流
- 驗證語法結構
- 建立中介表示（語法樹、抽象語法樹 AST）

```
Token流: [INT] [IDENT:x] [ASSIGN] [NUM:42] [SEMICOLON]
                    ↓
語法樹:
    =
   / \
  x   42
```

## 7.2 優先順序 Climbing 解析器

c4 使用「優先順序 climbing」（Precedence Climbing）方法來解析表達式。這種方法適合解析 C 語言的二元運算式。

核心思想：
- 每個運算子有兩個優先順序：進入（enter）和離開（exit）
- 遞迴下降：先解析左側，再根據優先順序決定是否繼續

```c
void expr(int lev) {
    // 1. 處理一元運算子（前綴）
    // 2. 解析原子表達式（數值、識別符、括號）
    // 3. 根據優先順序處理二元運算子
    
    while (tk >= lev) {
        if (tk == '+') { next(); expr(Mul); *++e = ADD; }
        if (tk == '-') { next(); expr(Mul); *++e = SUB; }
        // ...
    }
}
```

## 7.3 運算子優先順序表

C 語言的運算子優先順序（由高到低）：

| 優先順序 | 運算子 | 結合性 |
|---------|--------|--------|
| 15 | () [] -> | 左到右 |
| 14 | ! ~ ++ -- - * & sizeof | 右到左 |
| 13 | * / % | 左到右 |
| 12 | + - | 左到右 |
| 11 | << >> | 左到右 |
| 10 | < <= > >= | 左到右 |
| 9 | == != | 左到右 |
| 8 | & | 左到右 |
| 7 | ^ | 左到右 |
| 6 | \| | 左到右 |
| 5 | && | 左到右 |
| 4 | \|\| | 左到右 |
| 3 | ?: | 右到左 |
| 2 | = += -= 等 | 右到左 |
| 1 | , | 左到右 |

c4 使用的優先順序值：
```c
// Assign 是最低的
// Cond (?:) 
// Lor (||)
// Lan (&&)
// Or (|)
// Xor (^)
// And (&)
// Eq, Ne (=, !=)
// Lt, Gt, Le, Ge (<, >, <=, >=)
// Shl, Shr (<<, >>)
// Add, Sub (+, -)
// Mul, Div, Mod (*, /, %)
// Inc, Dec (++, --)
```

## 7.4 原子表達式

### 7.4.1 數值常量

```c
if (tk == Num) { 
    *++e = IMM;      // 發射 IMM 指令
    *++e = ival;    // 發射立即值
    next(); 
    ty = INT;        // 類型是 int
}
```

### 7.4.2 字串常量

```c
else if (tk == '"') {
    *++e = IMM;
    *++e = ival;      // ival 是字串在資料段的位址
    next();
    while (tk == '"') next();  // 處理連續字串
    data = (char *)((int)data + sizeof(int) & -sizeof(int));
    ty = PTR;         // 類型是指標
}
```

### 7.4.3 sizeof

```c
else if (tk == Sizeof) {
    next(); 
    if (tk == '(') next(); 
    ty = INT; 
    if (tk == Int) next(); 
    else if (tk == Char) { next(); ty = CHAR; }
    while (tk == Mul) { next(); ty = ty + PTR; }  // 指標層次
    if (tk == ')') next();
    *++e = IMM; 
    *++e = (ty == CHAR) ? sizeof(char) : sizeof(int);
    ty = INT;
}
```

### 7.4.4 識別符

識別符可能是：
- 變數引用
- 函式呼叫
- 常量（在符號表中定義）

```c
else if (tk == Id) {
    d = id;  // 記住識別符
    next();
    
    if (tk == '(') {  // 函式呼叫
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
        ty = d[Type];
    }
    else {  // 變數引用
        if (d[Class] == Loc) { 
            *++e = LEA; *++e = loc - d[Val];  // 本地變數位址
        }
        else if (d[Class] == Glo) { 
            *++e = IMM; *++e = d[Val];  // 全域位址
        }
        *++e = (ty = d[Type]) == CHAR ? LC : LI;  // 載入值
    }
}
```

## 7.5 一元運算子

### 7.5.1 取地址 `&`

```c
else if (tk == And) {
    next(); 
    expr(Inc);
    if (*e == LC || *e == LI) --e;  // 移除載入指令
    else { printf("%d: bad address-of\n", line); exit(-1); }
    ty = ty + PTR;  // 類型變為指標
}
```

### 7.5.2 解參考 `*`

```c
else if (tk == Mul) {
    next(); 
    expr(Inc);
    if (ty > INT) ty = ty - PTR;  // 移除一層指標
    else { printf("%d: bad dereference\n", line); exit(-1); }
    *++e = (ty == CHAR) ? LC : LI;
}
```

### 7.5.3 邏輯非 `!` 和 位元反 `~`

```c
else if (tk == '!') { 
    next(); 
    expr(Inc); 
    *++e = PSH; 
    *++e = IMM; 
    *++e = 0; 
    *++e = EQ; 
    ty = INT; 
}

else if (tk == '~') { 
    next(); 
    expr(Inc); 
    *++e = PSH; 
    *++e = IMM; 
    *++e = -1; 
    *++e = XOR; 
    ty = INT; 
}
```

### 7.5.4 正負號

```c
else if (tk == Sub) {
    next(); 
    *++e = IMM;
    if (tk == Num) { 
        *++e = -ival;  // 負立即數優化
        next(); 
    } else { 
        *++e = -1; 
        *++e = PSH; 
        expr(Inc); 
        *++e = MUL; 
    }
    ty = INT;
}
```

## 7.6 二元運算子

二元運算子的解析在迴圈中處理：

```c
while (tk >= lev) {
    if (tk == Assign) {
        next();
        if (*e == LC || *e == LI) *e = PSH;  // 保留指標
        else { printf("%d: bad lvalue in assignment\n", line); exit(-1); }
        expr(Assign); 
        *++e = (ty = t) == CHAR ? SC : SI;
    }
    else if (tk == Lor) { 
        next(); *++e = BNZ; d = ++e; 
        expr(Lan); *d = (int)(e + 1); ty = INT; 
    }
    else if (tk == Lan) { 
        next(); *++e = BZ; d = ++e; 
        expr(Or); *d = (int)(e + 1); ty = INT; 
    }
    else if (tk == Or) { 
        next(); *++e = PSH; expr(Xor); *++e = OR; ty = INT; 
    }
    // ... 其他運算子
}
```

## 7.7 優先順序解析示例

解析 `2 + 3 * 4`：

```
expr(Assign)
  tk = '+', lev = Assign
  tk != Assign, 進入 while
  tk = '+', 繼續
  tk = Num (2), 處理
  離開 while (tk < '+')

回到上層
  tk = '+'
  while (tk >= Add)
    next()
    expr(Mul)
      tk = Num (3), 處理
      tk = '*', 繼續
      next()
      expr(Inc)
        tk = Num (4), 處理
        結束
      發射 MUL
    結束
    發射 ADD
```

生成的指令：
```
IMM 2
IMM 3
IMM 4
MUL
ADD
```

## 7.8 指標算術

指標的 `+` 和 `-` 需要特別處理：

```c
else if (tk == Add) {
    next(); *++e = PSH; expr(Mul);
    if ((ty = t) > PTR) { 
        *++e = PSH; *++e = IMM; *++e = sizeof(int); 
        *++e = MUL;  // 指標 + n = 指標 + n * sizeof(type)
    }
    *++e = ADD;
}

else if (tk == Sub) {
    next(); *++e = PSH; expr(Mul);
    if (t > PTR && t == ty) { 
        *++e = SUB; 
        *++e = PSH; *++e = IMM; *++e = sizeof(int); 
        *++e = DIV; 
        ty = INT;  // ptr - ptr = element count
    }
    else if ((ty = t) > PTR) { 
        *++e = PSH; *++e = IMM; *++e = sizeof(int); 
        *++e = MUL; *++e = SUB; 
    }
    else *++e = SUB;
}
```

## 7.9 括號表達式

括號改變優先順序，同時也是類型轉換的語法：

```c
else if (tk == '(') {
    next();
    if (tk == Int || tk == Char) {  // 類型轉換
        t = (tk == Int) ? INT : CHAR; 
        next();
        while (tk == Mul) { next(); t = t + PTR; }
        if (tk == ')') next();
        expr(Inc);
        ty = t;  // 新的類型
    }
    else {
        expr(Assign);  // 括號內是表達式
        if (tk == ')') next();
    }
}
```

## 7.10 小結

本章節我們學習了：
- 優先順序 climbing 解析方法
- 原子表達式處理（數值、字串、sizeof、識別符）
- 一元運算器（&、*、!、~、+、-）
- 二元運算子解析迴圈
- 指標算術的特別處理
- 括號和類型轉換

## 7.11 習題

1. 追蹤 `a = b = 5` 的解析過程
2. 追蹤 `*p++` 的解析過程（注意優先順序）
3. 為 c4 添加三元運算子 `?:` 的支援
4. 研究如何實現 `&&` 和 `||` 的短路求值
5. 比較優先順序 climbing 和遞迴下降 parser 的優缺點
