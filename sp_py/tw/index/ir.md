# 中間表示 (Intermediate Representation)

## 概述

中間表示（IR）是編譯器中介於原始碼和目的碼之間的程式表示。IR 應該與原始語言和目標機器無關，以便進行平台無關的優化。LLVM IR 是最著名的 IR 格式之一。

## IR 類型

### 1. 高階 IR（接近原始語言）

```python
# 接近原始語言的中間表示
IR = """
function add(a, b):
    return a + b

function main():
    x = 5
    y = add(x, 10)
    return y
"""
```

### 2. 低階 IR（接近機器語言）

```python
# 三地址碼（TAC）
IR = """
t1 = 5
t2 = 10
t3 = call add(t1, t2)
return t3
"""
```

### 3. LLVM IR

```llvm
; 簡單的 LLVM IR 範例
define i32 @add(i32 %a, i32 %b) {
  %result = add i32 %a, %b
  ret i32 %result
}

define i32 @main() {
  %x = alloca i32
  store i32 5, i32* %x
  %y = load i32, i32* %x
  %z = call i32 @add(i32 %y, i32 10)
  ret i32 %z
}
```

### 4. 三地址碼（Three-Address Code）

```python
class TACGenerator:
    def __init__(self):
        self.instructions = []
        self.temp_count = 0
    
    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"
    
    def generate(self, node):
        if isinstance(node, NumberNode):
            temp = self.new_temp()
            self.instructions.append(f"{temp} = {node.value}")
            return temp
        
        elif isinstance(node, BinaryOpNode):
            left = self.generate(node.left)
            right = self.generate(node.right)
            temp = self.new_temp()
            self.instructions.append(f"{temp} = {left} {node.op} {right}")
            return temp
        
        elif isinstance(node, AssignmentNode):
            value = self.generate(node.value)
            self.instructions.append(f"{node.name} = {value}")
        
        elif isinstance(node, ReturnNode):
            value = self.generate(node.value)
            self.instructions.append(f"return {value}")
    
    def get_code(self):
        return "\n".join(self.instructions)

# TAC 範例輸出:
# t1 = 2
# t2 = 3
# t3 = t1 * t2
# t4 = 4
# t5 = t3 + t4
# return t5
```

### 5. 控制流圖（CFG）

```python
# 基本塊（Basic Block）
class BasicBlock:
    def __init__(self, label):
        self.label = label
        self.instructions = []
        self.successors = []
        self.predecessors = []
    
    def add_instruction(self, instr):
        self.instructions.append(instr)

# CFG 範例
# BB1: x = 5
#      if x > 10 goto BB2 else BB3
#
# BB2: y = x + 1
#      goto BB4
#
# BB3: y = x - 1
# BB4: return y
```

### 6. SSA（靜態單一指定形式）

```python
# SSA: 每個變數只被指定一次
SSA = """
x1 = 5
if x1 > 10:
    y1 = x1 + 1
else:
    y2 = x1 - 1
y3 = phi(y1, y2)
return y3
"""
```

## IR 最佳化

### 1. 常數折疊

```python
# 編譯時計算常數表達式
def constant_folding(instructions):
    for i, instr in enumerate(instructions):
        if '=' in instr:
            parts = instr.split('=')
            rhs = parts[1].strip()
            # 嘗試計算
            try:
                result = eval(rhs)
                instructions[i] = f"{parts[0].strip()} = {result}"
            except:
                pass
    return instructions
```

### 2. 代數簡化

```python
def algebraic_simplification(instructions):
    rules = [
        ("x + 0", "x"),
        ("0 + x", "x"),
        ("x * 1", "x"),
        ("1 * x", "x"),
        ("x * 0", "0"),
    ]
    # 應用簡化規則
    return instructions
```

### 3. 公共子表達式消除

```python
def cse(instructions):
    # 識別重複計算
    seen = {}
    result = []
    
    for instr in instructions:
        if instr in seen:
            result.append(f"t = {instr}")
        else:
            seen[instr] = True
            result.append(instr)
    
    return result
```

## 為什麼學習 IR？

1. **編譯器設計**：理解編譯器核心
2. **最佳化**：進行程式碼優化
3. **多語言支援**：同一 IR 支援多種語言
4. **工具開發**：靜態分析工具

## 參考資源

- "Engineering a Compiler"
- LLVM Language Reference
- "Optimizing Compilers for Modern Architectures"
