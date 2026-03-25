# 編譯器 (Compiler)

## 概述

編譯器是一種將原始程式碼翻譯為目標程式碼（機器碼或位元組碼）的程式。它的主要任務是進行語法分析、語意分析，並產生高效的目標碼。編譯器是電腦科學中最重要的工具之一，幾乎所有軟體的開發都離不開編譯器。

## 編譯器架構

現代編譯器通常採用多階段架構：

```
原始碼 → [詞法分析] → [語法分析] → [語意分析] → [中間生成] → [最佳化] → [目的碼生成] → 目的碼
```

### 1. 詞法分析 (Lexical Analysis)

將原始字元流轉換為 Token 序列：

```python
import re

class Lexer:
    TOKEN_PATTERNS = [
        ('NUMBER', r'\d+'),
        ('IDENT', r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ('PLUS', r'\+'),
        ('MINUS', r'-'),
        ('MULT', r'\*'),
        ('DIV', r'/'),
        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
    ]
    
    def __init__(self, source):
        self.source = source
        self.pos = 0
    
    def tokenize(self):
        tokens = []
        while self.pos < len(self.source):
            matched = False
            for token_type, pattern in self.TOKEN_PATTERNS:
                regex = re.compile(pattern)
                match = regex.match(self.source, self.pos)
                if match:
                    value = match.group(0)
                    if token_type not in ('SKIP', 'WHITESPACE'):
                        tokens.append((token_type, value))
                    self.pos = match.end()
                    matched = True
                    break
            if not matched:
                raise SyntaxError(f"無法識別: {self.source[self.pos]}")
        return tokens
```

### 2. 語法分析 (Syntax Analysis)

驗證 Token 序列是否符合語法規則，建立語法樹或 AST：

```python
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def parse(self):
        return self.expr()
    
    def expr(self):
        result = self.term()
        while self.peek() and self.peek()[0] in ('PLUS', 'MINUS'):
            op = self.consume()[1]
            right = self.term()
            result = {'op': op, 'left': result, 'right': right}
        return result
    
    def term(self):
        result = self.factor()
        while self.peek() and self.peek()[0] in ('MULT', 'DIV'):
            op = self.consume()[1]
            right = self.factor()
            result = {'op': op, 'left': result, 'right': right}
        return result
    
    def factor(self):
        token = self.peek()
        if token[0] == 'NUMBER':
            return {'type': 'num', 'value': token[1]}
        elif token[0] == 'LPAREN':
            self.consume()
            result = self.expr()
            self.consume()  # RPAREN
            return result
        raise SyntaxError("語法錯誤")
```

### 3. 語意分析 (Semantic Analysis)

進行類型檢查、作用域分析等：

```python
class TypeChecker:
    def __init__(self):
        self.symbols = {}
        self.errors = []
    
    def check(self, node):
        if node['type'] == 'num':
            return 'int'
        elif node['type'] == 'binary':
            left_type = self.check(node['left'])
            right_type = self.check(node['right'])
            if left_type != right_type:
                self.errors.append(f"類型不匹配: {left_type} vs {right_type}")
            return left_type
        return 'unknown'
```

### 4. 中間碼生成 (IR Generation)

生成與硬體無關的中間表示：

```python
class IRGenerator:
    def __init__(self):
        self.code = []
        self.temp_count = 0
    
    def generate(self, node):
        if node['type'] == 'num':
            temp = self.new_temp()
            self.code.append(f"{temp} = {node['value']}")
            return temp
        elif node['type'] == 'binary':
            left = self.generate(node['left'])
            right = self.generate(node['right'])
            temp = self.new_temp()
            self.code.append(f"{temp} = {left} {node['op']} {right}")
            return temp
    
    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"
```

### 5. 目的碼生成 (Code Generation)

將中間碼轉換為目標機器的機器碼：

```python
class CodeGenerator:
    def __init__(self):
        self.code = []
    
    def generate(self, ir):
        for line in ir:
            if '=' in line:
                parts = line.split('=')
                dest = parts[0].strip()
                expr = parts[1].strip()
                self.code.append(f"MOV eax, {expr}")
                self.code.append(f"MOV {dest}, eax")
        return self.code
```

## 編譯器類型

### 1. AOT 編譯器 (Ahead-of-Time)

在執行前完全編譯：

```bash
# C 編譯器範例
gcc -O2 -o program program.c
```

### 2. JIT 編譯器 (Just-in-Time)

在執行時動態編譯：

```python
class JITCompiler:
    def __init__(self):
        self.code_cache = {}
    
    def compile(self, source):
        if source in self.code_cache:
            return self.code_cache[source]
        
        # 動態編譯
        code = self.do_compile(source)
        self.code_cache[source] = code
        return code
```

## 經典編譯器

- **GCC**: GNU Compiler Collection，支援 C、C++、Fortran 等
- **Clang**: LLVM 的 C/C++ 編譯器
- **LLVM**:  modular compiler infrastructure
- **javac**: Java 編譯器
- **csc**: C# 編譯器

## 參考資源

- "Compilers: Principles, Techniques, and Tools" (龍書)
- "Engineering a Compiler"
- LLVM 官方文檔
