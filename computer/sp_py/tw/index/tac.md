# 三地址碼 (Three-Address Code)

## 概述

三地址碼（TAC）是編譯器中常用的低階中間表示，每條指令最多包含三個運算元（一個目標和兩個來源）。TAC 簡單且易於生成和最佳化，是從高階語言到機器碼的理想橋樑。

## TAC 指令類型

### 1. 基本指令格式

```
result = op1 op op2
result = op operand
result = label
result = jump target
```

### 2. TAC 生成器

```python
class TACGenerator:
    def __init__(self):
        self.code = []
        self.temp_counter = 0
        self.label_counter = 0
    
    def new_temp(self):
        self.temp_counter += 1
        return f"t{self.temp_counter}"
    
    def new_label(self):
        self.label_counter += 1
        return f"L{self.label_counter}"
    
    def emit(self, instr):
        self.code.append(instr)
    
    def generate(self, node):
        if isinstance(node, NumberNode):
            t = self.new_temp()
            self.emit(f"{t} = {node.value}")
            return t
        
        elif isinstance(node, VariableNode):
            return node.name
        
        elif isinstance(node, BinaryOpNode):
            left = self.generate(node.left)
            right = self.generate(node.right)
            t = self.new_temp()
            self.emit(f"{t} = {left} {node.op} {right}")
            return t
        
        elif isinstance(node, AssignmentNode):
            value = self.generate(node.value)
            self.emit(f"{node.name} = {value}")
        
        elif isinstance(node, IfNode):
            condition = self.generate(node.condition)
            else_label = self.new_label()
            end_label = self.new_label()
            self.emit(f"if {condition} == 0 goto {else_label}")
            self.generate(node.then_branch)
            self.emit(f"goto {end_label}")
            self.emit(f"{else_label}:")
            if node.else_branch:
                self.generate(node.else_branch)
            self.emit(f"{end_label}:")
        
        elif isinstance(node, WhileNode):
            start_label = self.new_label()
            end_label = self.new_label()
            self.emit(f"{start_label}:")
            condition = self.generate(node.condition)
            self.emit(f"if {condition} == 0 goto {end_label}")
            self.generate(node.body)
            self.emit(f"goto {start_label}")
            self.emit(f"{end_label}:")
        
        elif isinstance(node, ReturnNode):
            value = self.generate(node.value)
            self.emit(f"return {value}")
```

### 3. 運算表達式

```python
# 原始: 2 + 3 * 4 - 5

# 生成的 TAC:
t1 = 3
t2 = 4
t3 = t1 * t2    # 3 * 4
t4 = 2
t5 = t4 + t3    # 2 + 12
t6 = 5
t7 = t5 - t6    # 14 - 5
```

### 4. 函數呼叫

```python
# 原始: result = add(x, y)

# 生成的 TAC:
t1 = x
t2 = y
param t1
param t2
t3 = call add, 2
result = t3
```

### 5. 控制流

```python
# 原始:
# if x > 0:
#     y = 1
# else:
#     y = 0

# 生成的 TAC:
t1 = x
if t1 <= 0 goto L1
y = 1
goto L2
L1:
y = 0
L2:
```

### 6. 完整範例

```python
class ASTNode:
    pass

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

class BinaryOpNode(ASTNode):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class AssignmentNode(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

# 編譯: x = 2 + 3 * 4
ast = AssignmentNode(
    'x',
    BinaryOpNode('+',
        NumberNode(2),
        BinaryOpNode('*',
            NumberNode(3),
            NumberNode(4)
        )
    )
)

gen = TACGenerator()
gen.generate(ast)
print("\n".join(gen.code))

# 輸出:
# t1 = 3
# t2 = 4
# t3 = t1 * t2
# t4 = 2
# t5 = t4 + t3
# x = t5
```

## TAC 到機器碼

```python
class TACToAssembly:
    def __init__(self):
        self.code = []
        self.temp_offset = 0
    
    def translate(self, tac):
        for instr in tac:
            if '=' in instr:
                parts = instr.split('=')
                dest = parts[0].strip()
                expr = parts[1].strip()
                
                if 'call' in expr:
                    # 函數呼叫
                    self.code.append(f"call {expr.split()[1]}")
                    self.code.append(f"mov {dest}, eax")
                elif '*' in expr or '+' in expr or '-' in expr:
                    # 算術運算
                    self.generate_arithmetic(dest, expr)
                else:
                    # 簡單賦值
                    self.code.append(f"mov {dest}, {expr}")
        
        return self.code
    
    def generate_arithmetic(self, dest, expr):
        self.code.append(f"; {dest} = {expr}")
        self.code.append(f"mov eax, {dest}")
```

## TAC 最佳化

### 1. 常數折疊

```python
def constant_fold(tac):
    result = []
    for instr in tac:
        if '=' in instr:
            parts = instr.split('=')
            if parts[1].strip().isdigit():
                continue  # 可在編譯時計算
        result.append(instr)
    return result
```

### 2. 複製傳播

```python
def copy_propagation(tac):
    # 用實際值替換簡單複製
    return tac
```

## 為什麼學習 TAC？

1. **編譯器基礎**：理解編譯器中間表示
2. **易於優化**：簡單結構易於最佳化
3. **程式碼生成**：易於轉換為機器碼
4. **教學價值**：理解編譯原理

## 參考資源

- "Compilers: Principles, Techniques, and Tools"
- "Engineering a Compiler"
