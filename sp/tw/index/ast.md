# 抽象語法樹 (Abstract Syntax Tree)

## 概述

抽象語法樹（AST）是程式碼的樹狀表示，代表程式的語法結構。與具體語法樹不同，AST 只保留語意上重要的部分，忽略語法細節（如括號）。AST 是編譯器中重要的中間表示，用於語意分析和程式碼生成。

## AST 範例

### 1. 運算式 AST

```python
# 原始程式: 2 + 3 * 4

# AST 結構:
#       (+)
#       / \
#      2   (*)
#          / \
#         3   4
```

### 2. AST 節點定義

```python
from abc import ABC, abstractmethod

class ASTNode(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value
    
    def accept(self, visitor):
        return visitor.visit_number(self)

class BinaryOpNode(ASTNode):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right
    
    def accept(self, visitor):
        return visitor.visit_binary_op(self)

class VariableNode(ASTNode):
    def __init__(self, name):
        self.name = name
    
    def accept(self, visitor):
        return visitor.visit_variable(self)

class IfNode(ASTNode):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch
    
    def accept(self, visitor):
        return visitor.visit_if(self)
```

### 3. 解析器生成 AST

```python
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def parse(self):
        return self.statement()
    
    def statement(self):
        token = self.peek()
        
        if token[0] == 'IF':
            return self.if_statement()
        elif token[0] == 'IDENT':
            return self.assignment()
        else:
            return self.expression()
    
    def if_statement(self):
        self.consume()  # 'if'
        condition = self.expression()
        self.consume()  # 'then'
        then_branch = self.statement()
        
        else_branch = None
        if self.peek()[0] == 'ELSE':
            self.consume()
            else_branch = self.statement()
        
        self.consume()  # 'end'
        return IfNode(condition, then_branch, else_branch)
    
    def expression(self):
        result = self.term()
        while self.peek()[0] in ('PLUS', 'MINUS'):
            op = self.consume()[1]
            right = self.term()
            result = BinaryOpNode(op, result, right)
        return result
    
    def term(self):
        result = self.factor()
        while self.peek()[0] in ('MULT', 'DIV'):
            op = self.consume()[1]
            right = self.factor()
            result = BinaryOpNode(op, result, right)
        return result
    
    def factor(self):
        token = self.peek()
        
        if token[0] == 'NUMBER':
            self.consume()
            return NumberNode(int(token[1]))
        
        elif token[0] == 'IDENT':
            self.consume()
            return VariableNode(token[1])
        
        elif token[0] == 'LPAREN':
            self.consume()
            result = self.expression()
            self.consume()  # ')'
            return result
        
        raise SyntaxError("Unexpected token")
    
    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    
    def consume(self):
        token = self.tokens[self.pos]
        self.pos += 1
        return token
```

### 4. AST 走訪器（Visitor）

```python
class ASTVisitor:
    def visit(self, node):
        return node.accept(self)
    
    def visit_number(self, node):
        return node.value
    
    def visit_binary_op(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        if node.op == '+':
            return left + right
        elif node.op == '-':
            return left - right
        elif node.op == '*':
            return left * right
        elif node.op == '/':
            return left / right
    
    def visit_variable(self, node):
        return self.get_variable(node.name)
    
    def visit_if(self, node):
        condition = self.visit(node.condition)
        if condition:
            return self.visit(node.then_branch)
        elif node.else_branch:
            return self.visit(node.else_branch)
        return None

# 使用
parser = Parser(tokens)
ast = parser.parse()
visitor = ASTVisitor()
result = visitor.visit(ast)
```

### 5. AST 視覺化

```python
def ast_to_string(node, indent=0):
    prefix = "  " * indent
    
    if isinstance(node, NumberNode):
        return f"{prefix}Number({node.value})"
    elif isinstance(node, VariableNode):
        return f"{prefix}Variable({node.name})"
    elif isinstance(node, BinaryOpNode):
        lines = [f"{prefix}BinaryOp({node.op})"]
        lines.append(ast_to_string(node.left, indent + 1))
        lines.append(ast_to_string(node.right, indent + 1))
        return "\n".join(lines)
    elif isinstance(node, IfNode):
        lines = [f"{prefix}If"]
        lines.append(f"{prefix}  Condition:")
        lines.append(ast_to_string(node.condition, indent + 2))
        lines.append(f"{prefix}  Then:")
        lines.append(ast_to_string(node.then_branch, indent + 2))
        if node.else_branch:
            lines.append(f"{prefix}  Else:")
            lines.append(ast_to_string(node.else_branch, indent + 2))
        return "\n".join(lines)

print(ast_to_string(ast))
```

## AST 在編譯器中的角色

```
原始碼 → 詞法分析 → Token
                  ↓
              語法分析 → AST
                  ↓
              語意分析 → 裝飾的 AST
                  ↓
              中間碼生成 → IR
                  ↓
              優化
                  ↓
              目的碼生成 → 機器碼
```

## 為什麼學習 AST？

1. **編譯器核心**：理解編譯過程
2. **靜態分析**：程式碼分析工具基礎
3. **程式碼轉換**：重構和程式碼生成
4. **IDE 功能**：語法高亮、智慧提示

## 參考資源

- "Compilers: Principles, Techniques, and Tools"
- ANTLR AST 處理
- "Language Implementation Patterns"
