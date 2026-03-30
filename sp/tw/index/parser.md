# 解析器 (Parser)

## 概述

解析器（Parser）是編譯器的組成部分，負責將 Token 序列轉換為抽象語法樹（AST）。解析器驗證程式碼的語法結構，確保 Token 序列符合語言的文法規則。

## 歷史

- **1950s**：早期編譯器使用遞迴下降
- **1970s**：LR 解析器發展
- **1980s**：Yacc/Bison 工具普及
- **現在**：ANTLR 等 LL(*) 解析器

## 解析器類型

### 1. 遞迴下降解析器

```python
class RecursiveDescentParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def parse(self):
        return self.program()
    
    def program(self):
        return self.statement_list()
    
    def statement_list(self):
        statements = []
        while self.peek() is not None:
            statements.append(self.statement())
        return statements
    
    def statement(self):
        token = self.peek()
        
        if token[0] == 'IF':
            return self.if_statement()
        elif token[0] == 'WHILE':
            return self.while_statement()
        elif token[0] == 'RETURN':
            return self.return_statement()
        elif token[0] == 'IDENT':
            return self.assignment()
        
        raise SyntaxError(f"Unexpected token: {token}")
    
    def if_statement(self):
        self.consume()  # if
        condition = self.expression()
        self.consume()  # then
        then_branch = self.statement()
        
        else_branch = None
        if self.peek()[0] == 'ELSE':
            self.consume()
            else_branch = self.statement()
        
        self.consume()  # end
        return ('if', condition, then_branch, else_branch)
    
    def expression(self):
        left = self.term()
        
        while self.peek()[0] in ('PLUS', 'MINUS'):
            op = self.consume()[1]
            right = self.term()
            left = ('binary', op, left, right)
        
        return left
    
    def term(self):
        left = self.factor()
        
        while self.peek()[0] in ('MULT', 'DIV'):
            op = self.consume()[1]
            right = self.factor()
            left = ('binary', op, left, right)
        
        return left
    
    def factor(self):
        token = self.peek()
        
        if token[0] == 'NUMBER':
            self.consume()
            return ('number', token[1])
        
        elif token[0] == 'IDENT':
            self.consume()
            return ('identifier', token[1])
        
        elif token[0] == 'LPAREN':
            self.consume()
            result = self.expression()
            self.consume()  # RPAREN
            return result
        
        raise SyntaxError("Invalid factor")
    
    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    
    def consume(self):
        token = self.tokens[self.pos]
        self.pos += 1
        return token
```

### 2. LL(1) 解析器

```python
# LL(1) 分析表驅動解析器

# 預測分析表
table = {
    ('E', 'id'): ['T', "E'"],
    ('E', '('): ['T', "E'"],
    ("E'", '+'): ['+', 'T', "E'"],
    ("E'", ')'): ['epsilon'],
    ("E'", '$'): ['epsilon'],
    ('T', 'id'): ['F', "T'"],
    ('T', '('): ['F', "T'"],
    ("T'", '*'): ['*', 'F', "T'"],
    ("T'", '+'): ['epsilon'],
    ("T"', ')'): ['epsilon'],
    ("T'", '$'): ['epsilon'],
    ('F', 'id'): ['id'],
    ('F', '('): ['(', 'E', ')'],
}

def ll1_parse(tokens):
    stack = ['$', 'E']
    pos = 0
    input_buffer = tokens + ['$']
    
    while stack:
        top = stack.pop()
        current = input_buffer[pos]
        
        if top == current:
            pos += 1
        elif top in table:
            production = table.get((top, current[0]))
            if production:
                for symbol in reversed(production):
                    if symbol != 'epsilon':
                        stack.append(symbol)
            else:
                raise SyntaxError(f"Error at {current}")
        else:
            raise SyntaxError(f"Unexpected {top}")
```

### 3. LR 解析器

```python
# LR 解析器使用狀態機

class LRParser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.action = {}  # action 表
        self.goto = {}    # goto 表
    
    def parse(self, tokens):
        stack = [(0, None)]  # 狀態棧
        pos = 0
        
        while True:
            state = stack[-1][0]
            token = tokens[pos]
            
            action = self.action.get((state, token[0]))
            
            if action is None:
                raise SyntaxError(f"Error at token {token}")
            
            if action[0] == 'shift':
                stack.append((action[1], token))
                pos += 1
            
            elif action[0] == 'reduce':
                rule = action[1]
                for _ in range(rule[1]):
                    stack.pop()
                
                state = stack[-1][0]
                stack.append((self.goto[(state, rule[0])], None))
            
            elif action[0] == 'accept':
                break
```

### 4. 使用 ANTLR

```antlr
// ANTLR 語法
grammar Expr;

prog: stat+ ;

stat: expr NEWLINE           # printExpr
    | ID '=' expr NEWLINE    # assign
    | NEWLINE               # blank
    ;

expr: expr op=('*'|'/') expr # op
    | expr op=('+'|'-') expr # op
    | INT                   # int
    | '(' expr ')'          # parens
    | ID                    # id
    ;

ID  : [a-zA-Z]+ ;
INT : [0-9]+ ;
NEWLINE : '\r'? '\n' ;
WS  : [ \t]+ -> skip ;
```

## 語法錯誤處理

```python
class ErrorRecoveryParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.errors = []
    
    def sync(self):
        """同步到安全點"""
        while self.peek() not in [';', 'END', '$']:
            self.consume()
        
        if self.peek():
            self.consume()  # 吃掉終結符
    
    def statement(self):
        try:
            return self.parse_statement()
        except SyntaxError as e:
            self.errors.append(e)
            self.sync()
            return None
```

## 為什麼學習解析器？

1. **編譯器基礎**：理解語法分析
2. **語言設計**：實現 DSL
3. **工具使用**：ANTLR
4. **除錯**：語法錯誤處理

## 參考資源

- "Compilers: Principles, Techniques, and Tools"
- ANTLR 官方文檔
- "Parsing Techniques"
