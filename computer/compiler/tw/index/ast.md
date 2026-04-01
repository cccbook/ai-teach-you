# 抽象語法樹 (Abstract Syntax Tree, AST)

## 概述

抽象語法樹是程式碼的樹狀表示，每個節點代表一個語法結構，是編譯器內部表示的核心。

## AST vs 語法樹

| 特性 | 語法樹 | 抽象語法樹 |
|-----|-------|-----------|
| 完整性 | 保留所有語法細節 | 僅保留語義結構 |
| 大小 | 較大 | 較小 |
| 可讀性 | 較差 | 較好 |

## AST 範例

對於以下 C 程式：

```c
int add(int a, int b) {
    return a + b;
}
```

產生的 AST：

```
FUNCTION (add)
├── PARAM_LIST
│   ├── DECL (a)
│   └── DECL (b)
└── BLOCK
    └── RETURN
        └── BINOP (+)
            ├── VAR (a)
            └── VAR (b)
```

## AST 節點類型

```c
typedef enum {
    AST_PROGRAM,
    AST_FUNCTION,
    AST_CALL,
    AST_RETURN,
    AST_IF,
    AST_WHILE,
    AST_ASSIGN,
    AST_BINARY_OP,
    AST_VARIABLE,
    AST_NUMBER,
    AST_DECL
} ASTNodeType;
```

## 參考資源

- [第 3 章：語法分析](../03-parser.md)
