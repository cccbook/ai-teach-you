# 直譯器 (Interpreter)

## 概述

直譯器是一種直接執行原始程式碼的程式，不預先編譯為機器碼。直譯器讀取原始碼，翻譯並立即執行每條語句。相比編譯器，直譯器更容易實現跨平台，但執行速度通常較慢。

## 歷史

- **1950s**：最早的直譯器用於 LISP
- **1960s**：BASIC 語言使用直譯器
- **1970s**：Pascal 引入 p-code 直譯器
- **1990s**：Python、Ruby 等腳本語言普及
- **現在**：JIT 技術結合兩者優勢

## 直譯器架構

```
原始碼 → [詞法分析] → [語法分析] → [語意分析] → [解釋執行]
```

### 1. 簡單直譯器範例

```python
class SimpleInterpreter:
    def __init__(self):
        self.variables = {}
    
    def eval_expr(self, expr):
        if isinstance(expr, int):
            return expr
        if isinstance(expr, str):
            return self.variables.get(expr, 0)
        
        op, left, right = expr
        left_val = self.eval_expr(left)
        right_val = self.eval_expr(right)
        
        if op == '+':
            return left_val + right_val
        elif op == '-':
            return left_val - right_val
        elif op == '*':
            return left_val * right_val
        elif op == '/':
            return left_val // right_val
    
    def exec_statement(self, stmt):
        if stmt[0] == 'assign':
            _, var, expr = stmt
            self.variables[var] = self.eval_expr(expr)
        elif stmt[0] == 'print':
            _, expr = stmt
            print(self.eval_expr(expr))

# AST: ('assign', 'x', ('+', 5, 3))
# AST: ('print', 'x')
```

### 2. 詞法分析器

```python
import re

class Lexer:
    def __init__(self, source):
        self.source = source
        self.pos = 0
    
    def next_token(self):
        patterns = [
            (r'\d+', 'NUMBER'),
            (r'[a-zA-Z_]\w*', 'IDENT'),
            (r'\+', 'PLUS'),
            (r'-', 'MINUS'),
            (r'\*', 'MULT'),
            (r'/', 'DIV'),
            (r'=', 'EQ'),
            (r'\(', 'LPAREN'),
            (r'\)', 'RPAREN'),
        ]
        
        while self.pos < len(self.source):
            for pattern, token_type in patterns:
                regex = re.compile(pattern)
                match = regex.match(self.source, self.pos)
                if match:
                    value = match.group(0)
                    self.pos = match.end()
                    return (token_type, value)
            raise SyntaxError(f"無法識別: {self.source[self.pos]}")
        return None
```

### 3. 語法分析器

```python
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def parse(self):
        statements = []
        while self.pos < len(self.tokens):
            statements.append(self.statement())
        return statements
    
    def statement(self):
        token = self.peek()
        if token[0] == 'IDENT':
            var = self.consume()[1]
            self.consume()  # '='
            expr = self.expr()
            return ('assign', var, expr)
        elif token[0] == 'PRINT':
            self.consume()
            expr = self.expr()
            return ('print', expr)
    
    def expr(self):
        left = self.term()
        while self.peek()[0] in ('PLUS', 'MINUS'):
            op = self.consume()[1]
            right = self.term()
            left = (op, left, right)
        return left
    
    def term(self):
        left = self.factor()
        while self.peek()[0] in ('MULT', 'DIV'):
            op = self.consume()[1]
            right = self.factor()
            left = (op, left, right)
        return left
    
    def factor(self):
        token = self.consume()
        if token[0] == 'NUMBER':
            return int(token[1])
        elif token[0] == 'IDENT':
            return token[1]
        elif token[0] == 'LPAREN':
            expr = self.expr()
            self.consume()  # ')'
            return expr
```

## 直譯器 vs 編譯器

| 特性 | 直譯器 | 編譯器 |
|------|--------|--------|
| 執行方式 | 逐行翻譯執行 | 預先編譯 |
| 啟動速度 | 快 | 慢 |
| 執行速度 | 慢 | 快 |
| 跨平台 | 易 | 需重新編譯 |
| 錯誤報告 | 即時 | 編譯時 |

## 為什麼學習直譯器？

1. **理解語言執行**：深入了解程式語言運作
2. **實現新語言**：建立DSL或腳本語言
3. **除錯工具**：開發除錯器
4. **JIT基礎**：理解JIT編譯器原理

## 參考資源

- "Programming Language Implementations and Design"
- "Crafting Interpreters"
- Python 原始碼
