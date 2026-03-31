"""
基於堆疊的虛擬機（Stack-based VM）
"""

class VirtualMachine:
    def __init__(self):
        self.stack = []      # 運算堆疊
        self.variables = {}  # 變數表
    
    def run(self, bytecode):
        """執行位元組碼指令"""
        pc = 0  # 程式計數器
        while pc < len(bytecode):
            op = bytecode[pc]
            
            if op == 'LOAD_CONST':  # 載入常數
                self.stack.append(bytecode[pc + 1])
                pc += 2
            
            elif op == 'LOAD_VAR':  # 載入變數
                var_name = bytecode[pc + 1]
                self.stack.append(self.variables.get(var_name, 0))
                pc += 2
            
            elif op == 'STORE_VAR':  # 儲存變數
                var_name = bytecode[pc + 1]
                value = self.stack.pop()
                self.variables[var_name] = value
                pc += 2
            
            elif op == 'ADD':        # 加法
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)
                pc += 1
            
            elif op == 'SUB':        # 減法
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a - b)
                pc += 1
            
            elif op == 'MUL':        # 乘法
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a * b)
                pc += 1
            
            elif op == 'DIV':        # 除法
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a // b)
                pc += 1
            
            elif op == 'PRINT':       # 輸出
                value = self.stack.pop()
                print(value)
                pc += 1
            
            elif op == 'HALT':        # 結束
                break

# 範例：將高階程式編譯為位元組碼
# let a = 10;
# 等同於：
LOAD_CONST, 10
STORE_VAR, 'a'

# print(a + 5);
# 等同於：
LOAD_VAR, 'a'
LOAD_CONST, 5
ADD
PRINT

# 測試 VM
vm = VirtualMachine()
bytecode = [
    'LOAD_CONST', 10,
    'STORE_VAR', 'a',
    'LOAD_CONST', 20,
    'STORE_VAR', 'b',
    'LOAD_VAR', 'a',
    'LOAD_VAR', 'b',
    'ADD',
    'PRINT'
]
vm.run(bytecode)
# 輸出：30
