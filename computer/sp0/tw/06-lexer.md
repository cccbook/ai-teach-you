# 6. 詞彙分析——如何將原始碼轉為 Token

## 6.1 詞彙分析的任務

詞彙分析（Lexical Analysis / Scanning）是編譯器的第一階段。它的任務是：
- 讀取原始碼字元
- 將字元分組為有意義的單元（Token）
- 忽略空白字元和註解
- 報告詞彙錯誤

```
原始碼: "int x = 42;"
         ↓
Token流: [INT] [IDENT:x] [ASSIGN] [NUM:42] [SEMICOLON]
```

## 6.2 Token 的結構

```c
enum TokenType {
    // 終結符 (Terminals)
    NUM = 128,    // 數值常量
    IDENT,        // 識別符
    STRING,       // 字串常量
    
    // 關鍵字
    INT, CHAR, IF, ELSE, WHILE, RETURN, SIZEOF,
    
    // 運算子
    ASSIGN,       // =
    PLUS, MINUS,  // + -
    MUL, DIV,     // * /
    EQ, NE, LT, GT, LE, GE,  // == != < > <= >=
    AND, OR, NOT, // && || !
    // ...
};
```

c4 的 Token 定義：
```c
enum {
  Num = 128, Fun, Sys, Glo, Loc, Id,
  Char, Else, Enum, If, Int, Return, Sizeof, While,
  Assign, Cond, Lor, Lan, Or, Xor, And, Eq, Ne, Lt, Gt, Le, Ge, Shl, Shr, Add, Sub, Mul, Div, Mod, Inc, Dec, Brak
};
```

## 6.3 c4 的 next() 函式結構

```c
void next() {
    char *pp;
    
    while (tk = *p) {  // 讀取下一個字元
        ++p;
        
        if (tk == '\n') {
            // 處理換行
        }
        else if (tk == '#') {
            // 處理預處理器行（跳過）
        }
        else if (isalpha(tk) || tk == '_') {
            // 識別符或關鍵字
        }
        else if (isdigit(tk)) {
            // 數值常量
        }
        else if (tk == '/') {
            // 除號或註解
        }
        else if (tk == '\'' || tk == '"') {
            // 字元常量或字串常量
        }
        else if (tk 是運算子) {
            // 處理運算子
        }
        // ...
    }
}
```

## 6.4 識別符解析

識別符是字母開頭，由字母、數字、底線組成的序列：

```c
else if ((tk >= 'a' && tk <= 'z') || 
         (tk >= 'A' && tk <= 'Z') || 
         tk == '_') {
    pp = p - 1;  // 記住識別符開始位置
    
    // 讀取剩餘字元
    while ((*p >= 'a' && *p <= 'z') || 
           (*p >= 'A' && *p <= 'Z') || 
           (*p >= '0' && *p <= '9') || 
           *p == '_')
        tk = tk * 147 + *p++;
    
    tk = (tk << 6) + (p - pp);  // 雜湊值 = 雜湊 << 6 + 長度
    
    // 查符號表
    id = sym;
    while (id[Tk]) {
        if (tk == id[Hash] && !memcmp((char *)id[Name], pp, p - pp)) {
            tk = id[Tk];  // 找到，是關鍵字或已宣告識別符
            return;
        }
        id = id + Idsz;
    }
    
    // 新識別符
    id[Name] = (int)pp;
    id[Hash] = tk;
    tk = id[Tk] = Id;  // 預設為 Id
    return;
}
```

## 6.5 數值常量解析

c4 支援十進位、十六進位、八進位：

```c
else if (tk >= '0' && tk <= '9') {
    if (ival = tk - '0') { 
        // 十進位
        while (*p >= '0' && *p <= '9') 
            ival = ival * 10 + *p++ - '0';
    }
    else if (*p == 'x' || *p == 'X') {
        // 十六進位
        while ((tk = *++p) && 
               ((tk >= '0' && tk <= '9') || 
                (tk >= 'a' && tk <= 'f') || 
                (tk >= 'A' && tk <= 'F')))
            ival = ival * 16 + (tk & 15) + (tk >= 'A' ? 9 : 0);
    }
    else { 
        // 八進位
        while (*p >= '0' && *p <= '7') 
            ival = ival * 8 + *p++ - '0';
    }
    tk = Num;
    return;
}
```

## 6.6 字元常量和字串常量

```c
else if (tk == '\'' || tk == '"') {
    pp = data;  // 記住資料段位置
    while (*p != 0 && *p != tk) {  // 讀取直到結尾
        if ((ival = *p++) == '\\') {  // 處理轉義
            if ((ival = *p++) == 'n') ival = '\n';
        }
        if (tk == '"') *data++ = ival;  // 字串存到資料段
    }
    ++p;  // 跳過結尾引號
    if (tk == '"') 
        ival = (int)pp;  // 字串：ival 是指標
    else 
        tk = Num;  // 字元：ival 是 ASCII 值
    return;
}
```

## 6.7 運算子處理

### 單一字元運算子：
```c
else if (tk == '*') { tk = Mul; return; }
else if (tk == '+') { tk = Add; return; }
else if (tk == '-') { tk = Sub; return; }
else if (tk == '/') { tk = Div; return; }
```

### 多字元運算子：
```c
else if (tk == '=') { 
    if (*p == '=') { ++p; tk = Eq; }  // ==
    else tk = Assign;                  // =
    return; 
}

else if (tk == '!') { 
    if (*p == '=') { ++p; tk = Ne; }  // !=
    return; 
}

else if (tk == '<') { 
    if (*p == '=') { ++p; tk = Le; }      // <=
    else if (*p == '<') { ++p; tk = Shl; }  // <<
    else tk = Lt;                          // <
    return; 
}

else if (tk == '>') { 
    if (*p == '=') { ++p; tk = Ge; }      // >=
    else if (*p == '>') { ++p; tk = Shr; }  // >>
    else tk = Gt;                          // >
    return; 
}
```

## 6.8 跳過註解

C99 之後支援 `//` 單行註解：
```c
else if (tk == '/') {
    if (*p == '/') {
        ++p;
        while (*p != 0 && *p != '\n') ++p;  // 跳到行尾
    }
    else {
        tk = Div;  // 是除號
        return;
    }
}
```

## 6.9 跳過空白

c4 的設計很巧妙：空白字元會落入迴圈開頭，`continue` 隱含在迴圈邏輯中：

```c
while (tk = *p) {  // 如果是空白，tk = ' '，迴圈體會進入
    ++p;
    if (tk == '\n') { ... }
    // ... 其他處理
    // 空白字元不會觸發任何 if，直接進入下一輪迴圈
}
```

## 6.10 詞彙分析範例

輸入：`int x = 42;`
Token 流：

| 位置 | 詞素 | Token |
|------|------|-------|
| 1-3 | int | INT |
| 4 | (blank) | (skip) |
| 5 | x | IDENT (hash) |
| 6 | (blank) | (skip) |
| 7 | = | Assign |
| 8 | (blank) | (skip) |
| 9-10 | 42 | Num (val=42) |
| 11 | ; | ; |

## 6.11 符號表結構

c4 的符號表是一個簡單的靜態陣列：

```c
int *sym;  // symbol table

enum { Tk, Hash, Name, Class, Type, Val, HClass, HType, HVal, Idsz };
// Idsz = 10，每個識別符佔用 10 個 int
```

每個識別符的結構：
```c
id[Tk]     // Token 類型（關鍵字或 Id）
id[Hash]   // 雜湊值
id[Name]   // 名稱字串指標
id[Class]  // 類別（Glo, Loc, Fun, Sys）
id[Type]   // 類型（INT, CHAR, PTR+n）
id[Val]    // 值（變數位址或函式偏移）
id[HClass] // 保存的類別（用於巢狀作用域）
id[HType]  // 保存的類型
id[HVal]   // 保存的值
```

## 6.12 關鍵字初始化

在解析開始前，先把關鍵字加入符號表：

```c
p = "char else enum if int return sizeof while ";
i = Char; 
while (i <= While) { 
    next(); 
    id[Tk] = i++;  // "char" -> Tk=Char, "else" -> Tk=Else, ...
}

// 內建函式
i = OPEN; 
while (i <= EXIT) { 
    next(); 
    id[Class] = Sys; 
    id[Type] = INT; 
    id[Val] = i++; 
}
```

## 6.13 小結

本章節我們學習了：
- 詞彙分析的任務：將字元流轉為 Token 流
- c4 的 Token 類型和表示
- 識別符解析（雜湊表查詢）
- 數值常量解析（十/十六/八進位）
- 字串和字元常量處理
- 運算子識別（單字元、雙字元）
- c4 的符號表結構

## 6.14 習題

1. 用 c4 -s 編譯 hello.c，觀察生成的 Token 流
2. 為 c4 添加 `break` 關鍵字支援
3. 研究如何添加 `float` 類型支援
4. 實現一個簡單的詞彙分析器（可用 flex 或手寫）
5. 比較手寫詞彙分析器和使用 lex/flex 的優缺點
