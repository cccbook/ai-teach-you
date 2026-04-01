# 2. 詞法分析

## 2.1 什麼是詞法分析

詞法分析（Lexical Analysis）是編譯器的第一個階段，負責將原始程式的字元序列轉換為 Token 序列。Token 是具有語義的最小單位，例如關鍵字、識別字、運算子、數值常數等。

```
原始程式碼:  int x = 10;
                
                │
                ▼
         ┌────────────┐
         │  詞法分析   │
         └────────────┘
                │
                ▼
Tokens: [INT] [IDENT x] [ASSIGN] [NUMBER 10] [SEMICOLON]
```

## 2.2 Token 定義

以下是 C 語言的 Token 類型：

[程式檔案：02-1-token.h](../_code/02/02-1-token.h)
```c
typedef enum {
    TOKEN_INT,
    TOKEN_RETURN,
    TOKEN_IF,
    TOKEN_ELSE,
    TOKEN_FOR,
    TOKEN_WHILE,
    TOKEN_IDENT,
    TOKEN_NUMBER,
    TOKEN_PLUS,
    TOKEN_MINUS,
    TOKEN_MUL,
    TOKEN_DIV,
    TOKEN_LPAREN,
    TOKEN_RPAREN,
    TOKEN_LBRACE,
    TOKEN_RBRACE,
    TOKEN_SEMICOLON,
    TOKEN_ASSIGN,
    TOKEN_LT,
    TOKEN_GT,
    TOKEN_EQ,
    TOKEN_EOF,
    TOKEN_ERROR
} TokenType;
```

## 2.3 詞法分析器實作

詞法分析器的核心是有限狀態機（Finite State Machine）。以下是一個簡單的 C 語言詞法分析器：

[程式檔案：02-1-lexer.c](../_code/02/02-1-lexer.c)
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "02-1-token.h"

typedef struct {
    const char* source;
    size_t position;
    size_t length;
    int line;
} Lexer;

static void initLexer(Lexer* lexer, const char* source) {
    lexer->source = source;
    lexer->position = 0;
    lexer->length = strlen(source);
    lexer->line = 1;
}

static char peek(Lexer* lexer) {
    if (lexer->position >= lexer->length) {
        return '\0';
    }
    return lexer->source[lexer->position];
}

static char advance(Lexer* lexer) {
    char c = peek(lexer);
    lexer->position++;
    return c;
}

static void skipWhitespace(Lexer* lexer) {
    while (peek(lexer) == ' ' || peek(lexer) == '\t' || 
           peek(lexer) == '\n' || peek(lexer) == '\r') {
        if (peek(lexer) == '\n') {
            lexer->line++;
        }
        advance(lexer);
    }
}

Token scanToken(Lexer* lexer) {
    skipWhitespace(lexer);
    
    if (peek(lexer) == '\0') {
        return makeToken(lexer, TOKEN_EOF, NULL);
    }
    
    char c = advance(lexer);
    
    if (isdigit(c)) {
        lexer->position--;
        return scanNumber(lexer);
    }
    
    if (isalpha(c) || c == '_') {
        lexer->position--;
        return scanIdentifier(lexer);
    }
    
    switch (c) {
        case '(': return makeToken(lexer, TOKEN_LPAREN, "(");
        case ')': return makeToken(lexer, TOKEN_RPAREN, ")");
        case '{': return makeToken(lexer, TOKEN_LBRACE, "{");
        case '}': return makeToken(lexer, TOKEN_RBRACE, "}");
        case ';': return makeToken(lexer, TOKEN_SEMICOLON, ";");
        case '+': return makeToken(lexer, TOKEN_PLUS, "+");
        case '-': return makeToken(lexer, TOKEN_MINUS, "-");
        case '*': return makeToken(lexer, TOKEN_MUL, "*");
        case '/': return makeToken(lexer, TOKEN_DIV, "/");
        case '<': return makeToken(lexer, TOKEN_LT, "<");
        case '>': return makeToken(lexer, TOKEN_GT, ">");
        case '=': return makeToken(lexer, TOKEN_ASSIGN, "=");
    }
    
    return makeToken(lexer, TOKEN_ERROR, "Unknown token");
}
```

## 2.4 正規表達式

詞法規則通常用正規表達式（Regular Expression）描述：

| Token 類型 | 正規表達式 |
|-----------|-----------|
| 識別字 | `[a-zA-Z_][a-zA-Z0-9_]*` |
| 整數 | `[0-9]+` |
| 關鍵字 | `int\|return\|if\|else\|for\|while` |
| 運算子 | `+\|-\|*\|/\|<\|>\|=` |
| 分隔符 | `\(\|\)\{\}\|\;` |

## 2.5 詞法分析的輸出

讓我們對一個簡單的 C 程式進行詞法分析：

[程式檔案：02-2-sample.c](../_code/02/02-2-sample.c)
```c
int add(int a, int b) {
    return a + b;
}

int main() {
    int x = 10;
    int y = 20;
    int z = add(x, y);
    if (z > 5) {
        return z;
    }
    return 0;
}
```

經過詞法分析後，產生的 Token 序列：

```
INT (int) at line 1
IDENT (add) at line 1
LPAREN (() at line 1
INT (int) at line 1
IDENT (a) at line 1
COMMA (,) at line 1
INT (int) at line 1
IDENT (b) at line 1
RPAREN ()) at line 1
LBRACE ({) at line 2
RETURN (return) at line 3
IDENT (a) at line 3
PLUS (+) at line 3
IDENT (b) at line 3
SEMICOLON (;) at line 3
RBRACE (}) at line 4
INT (int) at line 6
IDENT (main) at line 6
LPAREN (() at line 6
RPAREN ()) at line 6
LBRACE ({) at line 6
INT (int) at line 7
IDENT (x) at line 7
ASSIGN (=) at line 7
NUMBER (10) value=10 at line 7
SEMICOLON (;) at line 7
...
```

## 2.6 使用 clang 生成 Token

clang 提供了 `-E` 選項可以查看詞法分析的結果：

```bash
# 查看预处理后的词法分析结果
clang -E -Xclang -dump-tokens sample.c

# 查看更详细的 token 信息
clang -Xclang -ast-dump -fsyntax-only sample.c
```

## 2.7 本章小結

本章介紹了編譯器的第一個階段：詞法分析。詞法分析器的職責是：
- 識別 Token 類型
- 記錄 Token 的語義值（lexeme）
- 處理空白字元和註解
- 報告詞法錯誤

詞法分析器通常使用有限狀態機或正規表達式來實現。

## 練習題

1. 擴充詞法分析器以支援浮點數。
2. 為詞法分析器加入位置追蹤功能。
3. 處理字串常量和字元常量。
4. 支援多字元運算子（如 `==`, `!=`, `<=`, `>=`, `++`, `--`）。
