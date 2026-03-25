"""
虛擬機實作：堆疊式 vs 暫存器式
"""

# 基於堆疊的 VM（如 JVM）
class StackVM:
    def __init__(self):
        self.stack = []      # 操作數堆疊
        self.variables = {}  # 區域變數
        self.pc = 0
    
    def run(self, bytecode):
        while self.pc < len(bytecode):
            op = bytecode[self.pc]
            
            if op == 'iconst':
                self.stack.append(bytecode[self.pc + 1])
                self.pc += 2
            
            elif op == 'iload':
                var_idx = bytecode[self.pc + 1]
                self.stack.append(self.variables.get(var_idx, 0))
                self.pc += 2
            
            elif op == 'istore':
                self.variables[bytecode[self.pc + 1]] = self.stack.pop()
                self.pc += 2
            
            elif op == 'iadd':
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)
                self.pc += 1
            
            elif op == 'isub':
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a - b)
                self.pc += 1
            
            elif op == 'imul':
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a * b)
                self.pc += 1
            
            elif op == 'if_icmplt':
                false_target = bytecode[self.pc + 1]
                b = self.stack.pop()
                a = self.stack.pop()
                if a < b:
                    self.pc = false_target
                else:
                    self.pc += 2
            
            elif op == 'goto':
                self.pc = bytecode[self.pc + 1]
            
            elif op == 'print':
                print(self.stack.pop())
                self.pc += 1
            
            elif op == 'halt':
                break

# 基於暫存器的 VM（如 Lua VM）
class RegisterVM:
    def __init__(self):
        self.registers = [0] * 256  # 256 個暫存器
        self.pc = 0
    
    def run(self, bytecode):
        while self.pc < len(bytecode):
            op = bytecode[self.pc]
            
            if op == 'LOADK':  # 載入常數到暫存器
                reg = bytecode[self.pc + 1]
                const = bytecode[self.pc + 2]
                self.registers[reg] = const
                self.pc += 3
            
            elif op == 'MOVE':  # 複製暫存器
                dest = bytecode[self.pc + 1]
                src = bytecode[self.pc + 2]
                self.registers[dest] = self.registers[src]
                self.pc += 3
            
            elif op == 'ADD':  # 暫存器相加
                dest = bytecode[self.pc + 1]
                left = bytecode[self.pc + 2]
                right = bytecode[self.pc + 3]
                self.registers[dest] = self.registers[left] + self.registers[right]
                self.pc += 4
            
            elif op == 'PRINT':
                reg = bytecode[self.pc + 1]
                print(self.registers[reg])
                self.pc += 2
            
            elif op == 'HALT':
                break

# 比較：同一段程式碼的位元組碼差異
print("=== 基於堆疊 VM ===")
# 計算 1 + 2:
stack_bytecode = [
    'iconst', 1,    # 推入 1
    'iconst', 2,    # 推入 2
    'iadd',         # 彈出並相加，結果推回
    'print',        # 輸出
    'halt'
]
StackVM().run(stack_bytecode)

print("\n=== 基於暫存器 VM ===")
# 計算 1 + 2:
register_bytecode = [
    'LOADK', 0, 1,     # R0 = 1
    'LOADK', 1, 2,     # R1 = 2
    'ADD', 2, 0, 1,    # R2 = R0 + R1
    'PRINT', 2,        # 輸出 R2
    'HALT'
]
RegisterVM().run(register_bytecode)