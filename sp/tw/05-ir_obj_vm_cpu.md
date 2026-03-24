# 5. 執行環境：中間碼與目的檔，虛擬機與真實處理器

## 5.1 中間表示（IR）形式

中間表示是編譯器前端和後端之間的橋樑。讓我們實作一個完整的 IR 系統：

[程式檔案：05-1-tac_generator.py](../_code/05/05-1-tac_generator.py)
```python
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
```

## 5.2 目的檔格式

讓我們用 Python 解析 ELF 格式：

[程式檔案：05-2-elf_parser.py](../_code/05/05-2-elf_parser.py)
```python
"""
ELF（Executable and Linkable Format）解析器
"""

import struct

class ELFParser:
    def __init__(self, data):
        self.data = data
    
    def parse_header(self):
        """解析 ELF 檔頭"""
        # ELF 魔數
        magic = self.data[:4]
        if magic != b'\x7fELF':
            raise ValueError("不是有效的 ELF 檔")
        
        # 檔頭結構
        e_type = struct.unpack('<H', self.data[16:18])[0]
        e_machine = struct.unpack('<H', self.data[18:20])[0]
        e_entry = struct.unpack('<Q', self.data[24:32])[0]
        e_phoff = struct.unpack('<Q', self.data[32:40])[0]
        e_shoff = struct.unpack('<Q', self.data[40:48])[0]
        
        print(f"ELF 類型: {e_type}")
        print(f"目標架構: {e_machine}")
        print(f"入口點: 0x{e_entry:x}")
        print(f"程式頭偏移: {e_phoff}")
        print(f"區段頭偏移: {e_shoff}")
        
        return {'type': e_type, 'entry': e_entry}
    
    def parse_program_headers(self, count, entsize, offset):
        """解析程式頭"""
        headers = []
        for i in range(count):
            base = offset + i * entsize
            p_type = struct.unpack('<I', self.data[base:base+4])[0]
            p_offset = struct.unpack('<Q', self.data[base+8:base+16])[0]
            p_vaddr = struct.unpack('<Q', self.data[base+16:base+24])[0]
            p_filesz = struct.unpack('<Q', self.data[base+32:base+40])[0]
            headers.append({'type': p_type, 'offset': p_offset, 'vaddr': p_vaddr, 'filesz': p_filesz})
        return headers

# 練習：檢視自己的 ELF 檔
# $ readelf -h /bin/ls

# 不同平台的執行檔格式
# Linux: ELF (Executable and Linkable Format)
# Windows: PE (Portable Executable)
# macOS: Mach-O

# PE 格式範例結構
class PEParser:
    """PE (Portable Executable) 解析器"""
    
    DOS_HEADER_SIGNATURE = b'MZ'
    PE_SIGNATURE = b'PE\x00\x00'
    
    def parse(self, data):
        # DOS Header
        if data[:2] != self.DOS_HEADER_SIGNATURE:
            raise ValueError("不是有效的 PE 檔")
        
        # PE 簽名位置
        e_lfanew = struct.unpack('<I', data[60:64])[0]
        
        # PE 簽名
        if data[e_lfanew:e_lfanew+4] != self.PE_SIGNATURE:
            raise ValueError("PE 簽名無效")
        
        print(f"有效的 PE 檔，PE 頭位於: {e_lfanew}")

# Mach-O 格式
class MachOParser:
    """Apple Mach-O 解析器"""
    
    FAT_MAGIC = 0xcafebabe
    MH_MAGIC = 0xfeedface
    
    def parse(self, data):
        magic = struct.unpack('>I', data[:4])[0]
        
        if magic == self.FAT_MAGIC:
            print("Fat Binary (通用二進制)")
        elif magic == self.MH_MAGIC:
            print("32-bit Mach-O")
        else:
            print("64-bit Mach-O")
```

## 5.3 虛擬機架構

[程式檔案：05-3-stack_vm.py](../_code/05/05-3-stack_vm.py)
```python
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
```

## 5.4 x86/x64、ARM、RISC-V 架構介紹

```c
// C 程式碼
int add(int a, int b) {
    return a + b;
}

int main() {
    return add(1, 2);
}
```

x86-64 組語（AT&T 語法）：

[程式檔案：05-5-x86_64.s](../_code/05/05-5-x86_64.s)
```asm
# add 函數
add:
    lea    (%rdi,%rsi,1), %rax   # rax = rdi + rsi
    ret

# main 函數
main:
    push   %rbp
    mov    %rsp, %rbp
    mov    $2, %esi               # 第二個參數
    mov    $1, %edi               # 第一個參數
    call   add
    pop    %rbp
    ret
```

ARM64（AArch64）組語：

[程式檔案：05-6-arm64.s](../_code/05/05-6-arm64.s)
```asm
# add 函數
add:
    add    w0, w0, w1            # w0 = w0 + w1
    ret

# main 函數
main:
    stp    x29, x30, [sp, -16]!  # 保存 frame pointer
    mov    w1, 2                 # 第二個參數
    mov    w0, 1                 # 第一個參數
    bl     add                   # 呼叫 add
    ldp    x29, x30, [sp], 16    # 恢復
    ret
```

RISC-V 組語：

[程式檔案：05-7-riscv.s](../_code/05/05-7-riscv.s)
```asm
# add 函數
add:
    add    a0, a0, a1            # a0 = a0 + a1
    ret

# main 函數
    addi   a1, zero, 2           # a1 = 2
    addi   a0, zero, 1           # a0 = 1
    jal    ra, add               # 呼叫 add
    # a0 現在是結果
```

讓我用 Python 來模擬這些指令：

[程式檔案：05-8-cpu_simulator.py](../_code/05/05-8-cpu_simulator.py)
```python
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
```

## 5.5 系統呼叫與 ABI

[程式檔案：05-9-syscall.c](../_code/05/05-9-syscall.c)
```c
/* Linux 系統呼叫範例 */
#include <unistd.h>
#include <sys/syscall.h>

int main() {
    // write(1, "Hello\n", 6)
    // 系統呼叫號: 1 (write)
    // fd=1, buf="Hello\n", count=6
    char msg[] = "Hello, World!\n";
    syscall(SYS_write, 1, msg, 14);
    
    // exit(0)
    syscall(SYS_exit, 0);
    return 0;
}
```

用 Python 模擬系統呼叫：

[程式檔案：05-10-simple_os.py](../_code/05/05-10-simple_os.py)
```python
"""簡化的系統呼叫模擬"""

class SimpleOS:
    def __init__(self):
        self.registers = {}
        self.files = {0: 'stdin', 1: 'stdout', 2: 'stderr'}
    
    def syscall(self, number, args):
        """模擬系統呼叫"""
        
        # SYS_read (0)
        if number == 0:
            fd = args[0]
            return 0
        
        # SYS_write (1)
        elif number == 1:
            fd = args[0]
            buf = args[1]
            count = args[2]
            if fd == 1:  # stdout
                print(buf[:count], end='')
                return count
        
        # SYS_open (2)
        elif number == 2:
            return 3  # 假分配檔案描述符
        
        # SYS_exit (60)
        elif number == 60:
            print(f"\n程式以退出碼 {args[0]} 結束")
            exit()
        
        return -1

# 測試
os = SimpleOS()
os.syscall(1, [1, "Hello from system call!\n", 24])
os.syscall(60, [0])
```

ABI（Application Binary Interface）定義了函式呼叫約定：

[程式檔案：05-11-abi.c](../_code/05/05-11-abi.c)
```c
// x86-64 System V ABI
// 參數傳遞: rdi, rsi, rdx, rcx, r8, r9
// 返回值: rax
// 被呼叫者保存: rbx, rbp, r12, r13, r14, r15
// 呼叫者保存: rax, rcx, rdx, rsi, rdi, r8, r9, r10, r11

// 棧框架
void function(int a, int b) {
    // a -> rdi, b -> rsi
    int local = a + b;  // local 在棧上
    // 返回值在 rax
}
```