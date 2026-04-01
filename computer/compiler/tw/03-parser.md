# 3. 語法分析

## 3.1 什麼是語法分析

語法分析（Syntax Analysis）是編譯器的第二個階段，負責檢查 Token 序列是否符合語法規則，並將其轉換為抽象語法樹（Abstract Syntax Tree, AST）。

```
Token 序列: [INT] [IDENT] [LPAREN] ...
                │
                ▼
         ┌────────────┐
         │  語法分析   │
         └────────────┘
                │
                ▼
    抽象語法樹 (AST)
```

## 3.2 上下文無關文法

語法分析通常使用上下文無關文法（Context-Free Grammar, CFG）來描述語言的語法。以下是簡單算術表達式的文法：

```
expression → term (('+' | '-') term)*
term       → factor (('*' | '/') factor)*
factor     → NUMBER | IDENT | '(' expression ')'
```

## 3.3 抽象語法樹

抽象語法樹是程式碼的樹狀表示，每個節點代表一個語法結構：

[程式檔案：03-1-ast.h](../_code/03/03-1-ast.h)
```c
typedef enum {
    AST_PROGRAM,
    AST_FUNCTION,
    AST_CALL,
    AST_RETURN,
    AST_IF,
    AST_WHILE,
    AST_FOR,
    AST_ASSIGN,
    AST_BINARY_OP,
    AST_UNARY_OP,
    AST_VARIABLE,
    AST_NUMBER,
    AST_DECL,
    AST_PARAM_LIST,
    AST_ARG_LIST,
    AST_BLOCK,
    AST_BINOP_ADD,
    AST_BINOP_SUB,
    AST_BINOP_MUL,
    AST_BINOP_DIV,
    AST_BINOP_LT,
    AST_BINOP_GT,
    AST_BINOP_EQ
} ASTNodeType;

typedef struct ASTNode {
    ASTNodeType type;
    char* name;
    int value;
    struct ASTNode* left;
    struct ASTNode* right;
    struct ASTNode* third;
    struct ASTNode* next;
} ASTNode;
```

## 3.4 遞迴下降語法分析器

遞迴下降語法分析器（Recursive Descent Parser）是一種簡單的語法分析方法，每個文法規則對應一個函數：

[程式檔案：03-2-parser.c](../_code/03/03-2-parser.c)
```c
ASTNode* expression(Parser* parser);
ASTNode* term(Parser* parser);
ASTNode* factor(Parser* parser);

ASTNode* factor(Parser* parser) {
    Token* token = peek(parser);
    
    if (token->type == TOKEN_NUMBER) {
        advance(parser);
        ASTNode* node = createNode(AST_NUMBER);
        node->value = token->value;
        return node;
    }
    
    if (token->type == TOKEN_IDENT) {
        advance(parser);
        ASTNode* node = createNode(AST_VARIABLE);
        node->name = strdup(token->lexeme);
        return node;
    }
    
    if (token->type == TOKEN_LPAREN) {
        advance(parser);
        ASTNode* node = expression(parser);
        match(parser, TOKEN_RPAREN);
        return node;
    }
    
    return NULL;
}

ASTNode* term(Parser* parser) {
    ASTNode* node = factor(parser);
    
    while (check(parser, TOKEN_MUL) || check(parser, TOKEN_DIV)) {
        Token* op = advance(parser);
        ASTNode* right = factor(parser);
        ASTNode* newNode = createNode(AST_BINARY_OP);
        newNode->name = strdup(op->lexeme);
        newNode->left = node;
        newNode->right = right;
        node = newNode;
    }
    
    return node;
}

ASTNode* expression(Parser* parser) {
    ASTNode* node = term(parser);
    
    while (check(parser, TOKEN_PLUS) || check(parser, TOKEN_MINUS)) {
        Token* op = advance(parser);
        ASTNode* right = term(parser);
        ASTNode* newNode = createNode(AST_BINARY_OP);
        newNode->name = strdup(op->lexeme);
        newNode->left = node;
        newNode->right = right;
        node = newNode;
    }
    
    return node;
}
```

## 3.5 文法舉例

對於以下 C 語言語法：

```
function → type ident '(' params ')' block
block   → '{' statement* '}'
statement → return expr ';'
         | if '(' expr ')' statement
         | while '(' expr ')' statement
         | type ident '=' expr ';'
```

產生的 AST 結構：

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

## 3.6 使用 clang 查看 AST

clang 可以產生 AST 的文字表示：

```bash
# 查看 AST
clang -Xclang -ast-dump -fsyntax-only example.c

# 產生更易讀的 AST
clang -cc1 -ast-dump example.c
```

## 3.7 LL(1) 與 LR 分析

常見的語法分析方法：

| 方法 | 描述 | 優點 | 缺點 |
|-----|------|------|------|
| LL(1) | 由上而下，從左到右 | 簡單易實作 | 需要消除左遞迴 |
| LR | 由下而上，從左到右 | 能力更強 | 複雜難實作 |
| LALR | LR 的簡化版本 | 效率高 | 狀態數較多 |

## 3.8 本章小結

本章介紹了語法分析的基本概念：
- 語法分析將 Token 序列轉換為 AST
- 使用上下文無關文法描述語法
- 遞迴下降語法分析器是最常見的實作方法
- AST 是編譯器內部表示的核心

## 練習題

1. 擴充語法分析器支援 if-else 語句。
2. 實作 while 迴圈的語法分析。
3. 為語法分析器加入錯誤恢復機制。
4. 比較 LL(1) 和 LR 語法分析器的差異。
