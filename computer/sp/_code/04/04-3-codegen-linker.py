"""
目的碼生成與連結概念
"""

# x86-64 呼叫約定
# 參數順序: rdi, rsi, rdx, rcx, r8, r9
# 返回值: rax

# 組合語言範例
asm_template = """
    .global _main
_main:
    # 參數傳遞
    movq $10, %rdi      # 第一個參數
    call _factorial
    
    # 列印結果（系統呼叫）
    movq %rax, %rsi     # 要輸出的數字
    leq format(%rip), %rdi
    movq $0, %rax
    syscall
    
    ret

factorial:
    cmpq $1, %rdi
    jle .Lbase
    
    pushq %rbp
    movq %rsp, %rbp
    
    #遞迴呼叫
    decq %rdi
    call factorial
    
    popq %rbp
    ret

.Lbase:
    movq $1, %rax
    ret

format:
    .asciz "%d\\n"
"""

# 連結器概念：合併多個目標檔
class Linker:
    def __init__(self):
        self.object_files = []
        self.symbols = {}
    
    def add_object(self, obj):
        """加入目標檔"""
        self.object_files.append(obj)
        for sym in obj['symbols']:
            self.symbols[sym['name']] = sym
    
    def resolve_references(self):
        """解析符號引用"""
        for obj in self.object_files:
            for ref in obj['references']:
                if ref not in self.symbols:
                    raise LinkError(f"未定義的符號: {ref}")
    
    def link(self):
        """產生執行檔"""
        # 合併段、重定位符號
        return {'type': 'executable', 'sections': []}

# 載入器概念
class Loader:
    def __init__(self, program):
        self.program = program
    
    def load(self):
        """將程式載入記憶體並執行"""
        # 1. 讀取執行檔頭部
        # 2. 映射段到記憶體
        # 3. 設定程式計數器
        # 4. 跳轉到入口點
        pass
