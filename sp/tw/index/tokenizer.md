# 詞法分析器 (Tokenizer/Lexer)

## 概述

詞法分析器（Tokenizer 或 Lexer）是編譯器的第一階段，負責將原始字元流轉換為 Token 序列。Token 是程式的最小語法單位，包括識別字、關鍵字、運算符、字面常量等。

## 歷史

- **1975**：Lex 工具出現
- **1987**：GNU Flex 發布
- **1998**： ANTLR 引入
- **現在**：多種 lexer 工具

## 詞法分析流程

```
原始程式碼
    ↓
[字元流] → [詞法分析器] → [Token 流] → [語法分析器]
```

### 1. 基本 Token 定義

```python
import re

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type}, {self.value})"

# Token 類型
TOKEN_TYPES = [
    ('KEYWORD', r'\b(if|else|while|for|return|int|float|void)\b'),
    ('IDENT', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('NUMBER', r'\d+(\.\d+)?'),
    ('STRING', r'"([^"\\]|\\.)*"'),
    ('OPERATOR', r'[+\-*/%=<>!&|^~]+'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('SEMICOLON', r';'),
    ('COMMA', r','),
    ('WHITESPACE', r'\s+'),  # 跳過
]
```

### 2. 簡單 Lexer 實現

```python
class Lexer:
    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []
    
    def tokenize(self):
        while self.pos < len(self.source):
            matched = False
            
            for token_type, pattern in TOKEN_TYPES:
                regex = re.compile(pattern)
                match = regex.match(self.source, self.pos)
                
                if match:
                    value = match.group(0)
                    
                    if token_type not in ('WHITESPACE', 'SKIP'):
                        token = Token(
                            token_type, value,
                            self.line, self.column
                        )
                        self.tokens.append(token)
                    
                    self.pos = match.end()
                    self.column += len(value)
                    
                    if '\n' in value:
                        self.line += value.count('\n')
                        self.column = len(value.split('\n')[-1]) + 1
                    
                    matched = True
                    break
            
            if not matched:
                raise SyntaxError(
                    f"無法識別的字元: {self.source[self.pos]} "
                    f"at line {self.line}, column {self.column}"
                )
        
        return self.tokens

# 使用
lexer = Lexer("int x = 42;")
tokens = lexer.tokenize()
for token in tokens:
    print(token)
```

### 3. Flex 風格定義

```flex
/* 簡單計算器 lexer */
%{
#include "y.tab.h"
%}

/* 規則 */
%%
[0-9]+              { yylval = atoi(yytext); return NUMBER; }
[0-9]+\.[0-9]+     { yylval = atof(yytext); return FLOAT; }
[+\-*\/]           { return yytext[0]; }
[=\(\)\{\}]        { return yytext[0]; }
[\n\t ]+            /* 忽略空白 */
[a-zA-Z_][a-zA-Z0-9_]* { return IDENTIFIER; }
%%
```

### 4. 關鍵字表

```python
class LexerWithKeywords:
    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        self.keywords = {
            'if', 'else', 'while', 'for', 'return',
            'int', 'float', 'double', 'char', 'void',
            'class', 'public', 'private', 'def', 'True', 'False'
        }
    
    def tokenize(self):
        while self.pos < len(self.source):
            # 嘗試匹配識別字
            match = re.match(r'[a-zA-Z_][a-zA-Z0-9_]*', self.source, self.pos)
            if match:
                value = match.group(0)
                
                if value in self.keywords:
                    token_type = 'KEYWORD'
                else:
                    token_type = 'IDENT'
                
                self.tokens.append(Token(token_type, value, self.line, self.column))
                self.pos = match.end()
                continue
            
            # 匹配數字
            match = re.match(r'\d+(\.\d+)?', self.source, self.pos)
            if match:
                value = match.group(0)
                token_type = 'NUMBER'
                self.tokens.append(Token(token_type, value, self.line, self.column))
                self.pos = match.end()
                continue
            
            # ... 其他模式
            
            self.pos += 1
        
        return self.tokens
```

### 5. 使用 ANTLR

```antlr
lexer grammar CalculatorLexer;

NUMBER  : [0-9]+ ('.' [0-9]+)? ;
PLUS    : '+' ;
MINUS   : '-' ;
MULT    : '*' ;
DIV     : '/' ;
LPAREN  : '(' ;
RPAREN  : ')' ;
WS      : [ \t\r\n]+ -> skip ;
```

## 為什麼學習詞法分析？

1. **編譯器基礎**：理解編譯器第一階段
2. **DSL 設計**：建立領域特定語言
3. **文字處理**：分割和分析文字
4. **工具使用**： Flex、ANTLR

## 參考資源

- "Compilers: Principles, Techniques, and Tools"
- Flex 官方文檔
- ANTLR 官方文檔
