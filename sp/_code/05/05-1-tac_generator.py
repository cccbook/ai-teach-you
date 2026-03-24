"""
三地址碼（Three-Address Code, TAC）IR 系統
"""

class TACGenerator:
    def __init__(self):
        self.instructions = []
        self.temp_counter = 0
        self.label_counter = 0
    
    def new_temp(self):
        """產生新的臨時變數"""
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp
    
    def new_label(self):
        """產生新的標籤"""
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label
    
    # 運算指令
    def emit_add(self, result, left, right):
        self.instructions.append(f"{result} = {left} + {right}")
    
    def emit_sub(self, result, left, right):
        self.instructions.append(f"{result} = {left} - {right}")
    
    def emit_mul(self, result, left, right):
        self.instructions.append(f"{result} = {left} * {right}")
    
    def emit_div(self, result, left, right):
        self.instructions.append(f"{result} = {left} / {right}")
    
    # 記憶體指令
    def emit_load(self, dest, address):
        self.instructions.append(f"{dest} = *{address}")
    
    def emit_store(self, source, address):
        self.instructions.append(f"*{address} = {source}")
    
    # 控制流
    def emit_branch(self, label):
        self.instructions.append(f"goto {label}")
    
    def emit_cond_branch(self, cond, true_label, false_label):
        self.instructions.append(f"if {cond} goto {true_label}")
        self.instructions.append(f"goto {false_label}")
    
    def emit_label(self, label):
        self.instructions.append(f"{label}:")
    
    # 函數指令
    def emit_call(self, func, args):
        self.instructions.append(f"call {func}({', '.join(args)})")
    
    def emit_return(self, value):
        self.instructions.append(f"return {value}")
    
    # 翻譯 AST 為 TAC
    def translate(self, node):
        if node['type'] == 'number':
            return str(node['value'])
        if node['type'] == 'identifier':
            return node['name']
        if node['type'] == 'binary':
            left = self.translate(node['left'])
            right = self.translate(node['right'])
            result = self.new_temp()
            if node['op'] == '+':
                self.emit_add(result, left, right)
            elif node['op'] == '-':
                self.emit_sub(result, left, right)
            elif node['op'] == '*':
                self.emit_mul(result, left, right)
            elif node['op'] == '/':
                self.emit_div(result, left, right)
            return result
        return ""

# 測試 TAC 生成
tac = TACGenerator()
ast = {
    'type': 'binary',
    'op': '+',
    'left': {'type': 'binary', 'op': '*', 'left': {'type': 'number', 'value': 2}, 'right': {'type': 'number', 'value': 3}},
    'right': {'type': 'number', 'value': 4}
}
tac.translate(ast)
print("\n".join(tac.instructions))
# 輸出：
# t0 = 2 * 3
# t1 = t0 + 4

# 控制流翻譯
def translate_if(tac, node):
    """翻譯 if-else 為 TAC"""
    cond = tac.translate(node['condition'])
    then_label = tac.new_label()
    else_label = tac.new_label()
    end_label = tac.new_label()
    
    tac.emit_cond_branch(cond, then_label, else_label)
    tac.emit_label(then_label)
    for stmt in node['then']:
        tac.translate_stmt(stmt)
    tac.emit_branch(end_label)
    
    tac.emit_label(else_label)
    for stmt in node['else']:
        tac.translate_stmt(stmt)
    
    tac.emit_label(end_label)