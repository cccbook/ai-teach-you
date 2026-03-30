# 文法 (Grammar)

## 概述

文法（Grammar）是描述程式語言語法的形式化工具。乔姆斯基（Noam Chomsky）將文法分為四種類型：正則文法、上下文無關文法、上下文相關文法和無限制文法。編譯器使用文法來定義語言語法並構建解析器。

## 歷史

- **1956**：Noam Chomsky 發明文法層次
- **1957**：Backus-Naur Form (BNF) 發明
- **1960s**：上下文無關文法廣泛用於程式語言
- **現在**：ANTLR 等工具自動生成解析器

## 文法類型

### 1. BNF（Backus-Naur Form）

```bnf
<program>        ::= <statement_list>
<statement_list> ::= <statement> | <statement> <statement_list>
<statement>      ::= <assignment> | <if_statement> | <while_statement>
<assignment>     ::= <identifier> '=' <expression>
<if_statement>    ::= 'if' <expression> 'then' <statement_list> 'end'
<expression>     ::= <term> | <expression> '+' <term>
<term>           ::= <factor> | <term> '*' <factor>
<factor>         ::= <identifier> | <number> | '(' <expression> ')'
<identifier>     ::= <letter> | <identifier> <letter> | <identifier> <digit>
<number>         ::= <digit> | <number> <digit>
<letter>         ::= 'a' | 'b' | ... | 'z'
<digit>          ::= '0' | '1' | ... | '9'
```

### 2. EBNF（擴展 BNF）

```ebnf
program        = statement_list ;
statement_list = statement { statement } ;
statement      = assignment | if_statement | while_statement ;
assignment     = identifier "=" expression ;
if_statement   = "if" expression "then" statement_list "end" ;
expression     = term { "+" term } ;
term           = factor { "*" factor } ;
factor         = identifier | number | "(" expression ")" ;
identifier      = letter { letter | digit } ;
number          = digit { digit } ;
```

### 3. 文法術語

```python
# 簡化運算式文法
grammar = {
    # 非終結符
    'nonterminals': ['E', 'T', 'F'],
    # 終結符
    'terminals': ['+', '*', '(', ')', 'id', 'num'],
    # 起始符號
    'start': 'E',
    # 產生式
    'productions': [
        ('E', 'E', '+', 'T'),   # E -> E + T
        ('E', 'T'),             # E -> T
        ('T', 'T', '*', 'F'),   # T -> T * F
        ('T', 'F'),             # T -> F
        ('F', '(', 'E', ')'),   # F -> ( E )
        ('F', 'id'),            # F -> id
        ('F', 'num'),           # F -> num
    ]
}
```

## 遞迴下降解析器

```python
class RecursiveDescentParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def parse(self):
        return self.expr()
    
    def expr(self):
        result = self.term()
        while self.peek() == '+':
            self.consume()
            right = self.term()
            result = ('add', result, right)
        return result
    
    def term(self):
        result = self.factor()
        while self.peek() == '*':
            self.consume()
            right = self.factor()
            result = ('mul', result, right)
        return result
    
    def factor(self):
        if self.peek() == 'id':
            return ('id', self.consume()[1])
        elif self.peek() == 'num':
            return ('num', self.consume()[1])
        elif self.peek() == '(':
            self.consume()
            result = self.expr()
            self.consume()  # ')'
            return result
        raise SyntaxError("Unexpected token")
    
    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos][0]
        return None
    
    def consume(self):
        token = self.tokens[self.pos]
        self.pos += 1
        return token
```

## LL(1) 文法

```python
# LL(1) 分析表範例
ll1_table = {
    ('E', 'id'):   ['T', 'E''],
    ('E', 'num'):  ['T', 'E''],
    ('E', '('):    ['T', 'E''],
    ('E'', '+'):   ['+', 'T', 'E''],
    ('E'', ')'):   ['epsilon'],
    ('E'', '$'):   ['epsilon'],
    ('T', 'id'):   ['F', 'T''],
    ('T', 'num'):  ['F', 'T''],
    ('T', '('):    ['F', 'T''],
    ('T'', '*'):   ['*', 'F', 'T''],
    ('T'', '+'):   ['epsilon'],
    ('T'', ')'):   ['epsilon'],
    ('T'', '$'):   ['epsilon'],
    ('F', 'id'):   ['id'],
    ('F', 'num'):  ['num'],
    ('F', '('):    ['(', 'E', ')'],
}
```

## LR 解析器

```python
# LR 分析動作
lr_action = {
    0:  {'id': 's5', 'num': 's6', '(': 's4'},
    1:  {'+': 's7', '*': 's8', ')': 'acc', '$': 'acc'},
    2:  {'+': 'r2', '*': 'r2', ')': 'r2', '$': 'r2'},
    # ... 更多狀態
}

# LR 移入/規約
lr_goto = {
    0:  {'E': 1, 'T': 2, 'F': 3},
    1:  {'E': 1, 'T': 2, 'F': 3},
    # ... 更多狀態
}
```

## 為什麼學習文法？

1. **語言設計**：定義自己的程式語言
2. **編譯器**：理解解析器原理
3. **語法分析**：識別語法結構
4. **工具使用**： ANTLR、Yacc、Bison

## 參考資源

- "Compilers: Principles, Techniques, and Tools"
- "Parsing Techniques"
- ANTLR 官方文檔
