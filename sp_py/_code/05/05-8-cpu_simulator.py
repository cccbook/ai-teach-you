"""簡化的 CPU 模擬器"""

class CPUSimulator:
    def __init__(self):
        self.registers = [0] * 8  # 簡化的 8 個暫存器
        self.memory = [0] * 1024   # 簡化的 1KB 記憶體
        self.flags = {}
    
    def execute(self, instructions):
        pc = 0
        while pc < len(instructions):
            instr = instructions[pc]
            
            if instr['op'] == 'mov_imm':
                self.registers[instr['dest']] = instr['imm']
            
            elif instr['op'] == 'add':
                self.registers[instr['dest']] = (
                    self.registers[instr['src1']] + self.registers[instr['src2']]
                )
            
            elif instr['op'] == 'load':
                addr = self.registers[instr['addr_reg']]
                self.registers[instr['dest']] = self.memory[addr]
            
            elif instr == 'halt':
                break
            
            pc += 1
        
        return self.registers[0]

# 模擬 x86 風格的 add
cpu = CPUSimulator()
instructions = [
    {'op': 'mov_imm', 'dest': 0, 'imm': 1},  # eax = 1
    {'op': 'mov_imm', 'dest': 1, 'imm': 2},  # ebx = 2
    {'op': 'add', 'dest': 0, 'src1': 0, 'src2': 1},  # eax = eax + ebx
    'halt'
]
result = cpu.execute(instructions)
print(f"結果: {result}")  # 3