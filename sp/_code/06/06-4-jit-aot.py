"""
JIT（即時編譯）與 AOT（提前編譯）
"""

# 簡化的 JIT 編譯器
class JITCompiler:
    def __init__(self):
        self.traces = {}  # 追蹤熱點程式碼
        self.threshold = 1000  # 觸發 JIT 的閾值
    
    def interpret(self, code):
        """直譯執行"""
        return self.run_bytecode(code)
    
    def run_bytecode(self, bytecode):
        """執行位元組碼"""
        # 模擬直譯
        return "bytecode result"
    
    def compile_tracing(self, code, context):
        """追蹤 JIT 編譯"""
        # 記錄執行次數
        key = hash(code)
        self.traces[key] = self.traces.get(key, 0) + 1
        
        if self.traces[key] > self.threshold:
            # 生成最佳化程式碼
            return self.generate_optimized_code(code, context)
        
        return self.interpret(code)
    
    def generate_optimized_code(self, code, context):
        """生成最佳化機器碼"""
        # 使用 inline cache
        # 逃逸分析
        # 型別特定最佳化
        
        # 模擬生成的機器碼
        return f"optimized machine code for {code}"

# AOT 編譯範例
def aot_compile(source):
    """提前編譯為機器碼"""
    # 1. 詞法分析
    tokens = lex(source)
    # 2. 語法分析
    ast = parse(tokens)
    # 3. 語意分析
    analyze(ast)
    # 4. IR 生成
    ir = generate_ir(ast)
    # 5. 最佳化
    optimized_ir = optimize(ir)
    # 6. 目的碼生成
    machine_code = generate_code(optimized_ir)
    
    return machine_code

# 混合策略：Java HotSpot
class HotSpotVM:
    """模拟 Java HotSpot VM"""
    
    def __init__(self):
        self.interpreter = True
        self.jit_enabled = True
        self.method_counter = {}
    
    def execute(self, method):
        key = hash(method)
        
        # 層級編譯
        # Level 0: 直譯器
        # Level 1: C1 編譯器（快速）
        # Level 2: C2 編譯器（最佳化）
        
        # 檢查是否需要 JIT
        self.method_counter[key] = self.method_counter.get(key, 0) + 1
        
        if self.method_counter[key] < 1000:
            return self.run_interpreter(method)
        elif self.method_counter[key] < 10000:
            return self.run_c1_compiler(method)
        else:
            return self.run_c2_compiler(method)
    
    def run_interpreter(self, method):
        return "interpreted"
    
    def run_c1_compiler(self, method):
        return "C1 compiled"
    
    def run_c2_compiler(self, method):
        return "C2 optimized"