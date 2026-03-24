# 6. 編譯與解譯器的優化與加速技巧

## 6.1 最佳化分類

[程式檔案：06-1-optimization.py](../_code/06/06-1-optimization.py)
```python
"""
編譯器最佳化分類與實作
"""

# 1. 本地最佳化 - 僅看單一基本區塊
def local_optimization(ir):
    """本地最佳化"""
    optimized = []
    
    for i, instr in enumerate(ir):
        # 常數折疊：compile-time 計算
        if 't0 = 2 + 3' in instr:
            optimized.append('t0 = 5')
        
        # 冗餘消除：消除重複計算
        # 範例：如果 t0 已計算過，不再重複
        
        # 代數簡化
        if 't0 = x * 1' in instr:
            optimized.append('t0 = x')
        if 't0 = x + 0' in instr:
            optimized.append('t0 = x')
        
        else:
            optimized.append(instr)
    
    return optimized

# 2. 全域最佳化 - 跨基本區塊
def global_optimization(ir_blocks):
    """全域最佳化"""
    
    # 活躍性分析
    def liveness_analysis(block):
        """計算變數的活躍區間"""
        live = set()
        for instr in reversed(block):
            if '=' in instr:
                var = instr.split('=')[0].strip()
                live.add(var)
            if 'return' in instr:
                live.discard('result')
        return live
    
    # 公共子表達式消除 (CSE)
    def cse(ir):
        seen = {}
        result = []
        for instr in ir:
            if '=' in instr:
                expr = instr.split('=')[1].strip()
                if expr in seen:
                    result.append(f"{instr.split('=')[0].strip()} = {seen[expr]}")
                else:
                    result.append(instr)
                    seen[expr] = instr.split('=')[0].strip()
            else:
                result.append(instr)
        return result
    
    return [cse(block) for block in ir_blocks]

# 3. 跨程序最佳化
def interprocedural_optimization(functions):
    """跨程序最佳化"""
    
    # 內聯展開（Inline Expansion）
    def inline(function_call, functions):
        """將函數呼叫展開為主體"""
        func = functions.get(function_call['name'])
        if not func:
            return function_call
        
        # 簡單的內聯：直接替換
        body = func['body'].copy()
        return body
    
    # 常數傳播
    def const_propagation(ir):
        constants = {}
        result = []
        
        for instr in ir:
            if 'const' in instr:
                var = instr.split('=')[0].strip()
                val = instr.split('=')[1].strip()
                constants[var] = val
            
            # 用常數替換變數
            new_instr = instr
            for var, val in constants.items():
                new_instr = new_instr.replace(var, val)
            result.append(new_instr)
        
        return result
    
    return {'inlined': [], 'propagated': []}

# 測試最佳化
ir = [
    "t0 = 2 + 3",      # 常數折疊
    "t1 = t0 * 1",     # 代數簡化
    "t2 = x + 0",      # 代數簡化
    "t3 = t0",         # 冗餘複製
]

print("原始 IR:", ir)
print("最佳化後:", local_optimization(ir))
```

## 6.2 資料流分析

[程式檔案：06-2-dataflow.py](../_code/06/06-2-dataflow.py)
```python
"""
資料流分析（Data Flow Analysis）
"""

class DataFlowAnalyzer:
    def __init__(self, cfg):
        self.cfg = cfg  # 控制流程圖
    
    def reaching_definitions(self):
        """可達定義分析"""
        # 初始化：所有定義為 OUT = ∅
        out = {block: set() for block in self.cfg}
        
        changed = True
        while changed:
            changed = False
            for block in self.cfg:
                # IN = ∪ OUT(predecessors)
                in_set = set()
                for pred in block.get('preds', []):
                    in_set.update(out.get(pred, set()))
                
                # OUT = GEN ∪ (IN - KILL)
                new_out = block.get('gen', set()) | (in_set - block.get('kill', set()))
                
                if new_out != out.get(block, set()):
                    out[block] = new_out
                    changed = True
        
        return out
    
    def available_expressions(self):
        """可用表達式分析"""
        # 初始化：所有表達式為不可用
        out = {block: set() for block in self.cfg}
        
        changed = True
        while changed:
            changed = False
            for block in self.cfg:
                # IN = ∩ OUT(predecessors)
                if not block.get('preds'):
                    in_set = {'+', '-', '*', '/'}  # 假設所有運算可用
                else:
                    in_set = None
                    for pred in block.get('preds', []):
                        pred_out = out.get(pred, set())
                        if in_set is None:
                            in_set = pred_out.copy()
                        else:
                            in_set &= pred_out
                
                # OUT = GEN ∪ (IN - KILL)
                new_out = block.get('gen_ex', set()) | (in_set - block.get('kill_ex', set()))
                
                if new_out != out.get(block, set()):
                    out[block] = new_out
                    changed = True
        
        return out
    
    def liveness_analysis(self):
        """活躍性分析"""
        # 初始化：所有變數為不活躍
        in_vars = {block: set() for block in self.cfg}
        out_vars = {block: set() for block in self.cfg}
        
        changed = True
        while changed:
            changed = False
            for block in reversed(self.cfg):
                # OUT = ∪ IN(successors)
                out_new = set()
                for succ in block.get('succs', []):
                    out_new |= in_vars.get(succ, set())
                
                # IN = USE ∪ (OUT - DEF)
                in_new = block.get('use', set()) | (out_new - block.get('def', set()))
                
                if in_new != in_vars.get(block, set()):
                    in_vars[block] = in_new
                    changed = True
                if out_new != out_vars.get(block, set()):
                    out_vars[block] = out_new
                    changed = True
        
        return in_vars, out_vars

# 建立簡單的控制流程圖
cfg = [
    {'id': 'B1', 'preds': [], 'succs': ['B2'],
     'gen': {'x = 5'}, 'kill': {'x'}, 'use': set(), 'def': {'x'}},
    {'id': 'B2', 'preds': ['B1'], 'succs': ['B3'],
     'gen': {'y = x + 1'}, 'kill': {'y'}, 'use': {'x'}, 'def': {'y'}},
    {'id': 'B3', 'preds': ['B2'], 'succs': [],
     'gen': set(), 'kill': set(), 'use': {'y'}, 'def': set()},
]

analyzer = DataFlowAnalyzer(cfg)
print("可達定義:", analyzer.reaching_definitions())
```

## 6.3 指令排程與管線化

[程式檔案：06-3-pipeline.py](../_code/06/06-3-pipeline.py)
```python
"""
指令排程與管線化最佳化
"""

# 指令延遲槽
def pipeline_scheduling(instructions):
    """指令排程"""
    # 假設每個指令有不同的延遲
    latency = {
        'load': 1,
        'store': 1,
        'add': 1,
        'mul': 3,
        'div': 20,
        'branch': 2
    }
    
    scheduled = []
    pending = []
    
    for instr in instructions:
        instr_type = instr['type']
        delay = latency.get(instr_type, 1)
        
        # 檢查依賴
        if pending:
            # 等待之前指令完成
            for p in pending[:]:
                p['remaining'] -= 1
                if p['remaining'] <= 0:
                    pending.remove(p)
        
        # 排程當前指令
        scheduled.append(instr)
        pending.append({'instr': instr, 'remaining': delay})
    
    return scheduled

# 練習：找出指令級並行性
def find_ilp(instructions):
    """找出指令級並行性"""
    # 依賴圖
    dependencies = {
        'add': ['load'],
        'mul': ['add'],
        'store': ['mul']
    }
    
    # 簡單的排程
    ready = [i for i, instr in enumerate(instructions) 
             if instr not in dependencies or 
             all(dep in instructions[:i] for dep in dependencies[instr])]
    
    return ready

# 練習：迴圈展開
def loop_unrolling(code, unroll_factor=4):
    """迴圈展開"""
    if 'while' in code:
        # 展開多個副本
        lines = code.split('\n')
        result = []
        for i in range(unroll_factor):
            for line in lines:
                if 'while' not in line and 'end' not in line:
                    result.append(line.replace('i', f'i+{i}'))
        return '\n'.join(result)
    return code
```

## 6.4 JIT 編譯與 AOT 編譯

[程式檔案：06-4-jit-aot.py](../_code/06/06-4-jit-aot.py)
```python
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
```

## 6.5 SIMD 與向量化的應用

[程式檔案：06-5-simd.c](../_code/06/06-5-simd.c)
```c
// C 程式：無 SIMD
void add_arrays(float* a, float* b, float* c, int n) {
    for (int i = 0; i < n; i++) {
        c[i] = a[i] + b[i];
    }
}

// 使用 SIMD (SSE/AVX)
void add_arrays_simd(float* a, float* b, float* c, int n) {
    // 每次處理 4 個 float (SSE) 或 8 個 float (AVX)
    int i = 0;
    
    // AVX: 一次處理 8 個 float
    for (; i + 7 < n; i += 8) {
        __m256 va = _mm256_load_ps(&a[i]);
        __m256 vb = _mm256_load_ps(&b[i]);
        __m256 vc = _mm256_add_ps(va, vb);
        _mm256_store_ps(&c[i], vc);
    }
    
    // 處理剩餘元素
    for (; i < n; i++) {
        c[i] = a[i] + b[i];
    }
}

// 使用編譯器向量化
// gcc -O3 -march=native -ftree-vectorize
```

Python 使用 NumPy 向量化：

[程式檔案：06-6-vectorize.py](../_code/06/06-6-vectorize.py)
```python
import numpy as np

# 純 Python（慢）
def add_arrays_python(a, b):
    c = []
    for i in range(len(a)):
        c.append(a[i] + b[i])
    return c

# NumPy 向量化（快）
def add_arrays_numpy(a, b):
    return a + b

# 效能測試
import time

n = 10000000
a = np.random.rand(n)
b = np.random.rand(n)

start = time.time()
for _ in range(10):
    c = a + b
numpy_time = time.time() - start

print(f"NumPy 時間: {numpy_time:.3f}s")
print(f"處理 {n} 個元素，吞吐量: {n * 10 / numpy_time:.0f} ops/s")

# 自動向量化範例
# 使用 Numba JIT
from numba import jit

@jit(nopython=True)
def add_arrays_numba(a, b):
    n = len(a)
    c = np.empty(n)
    for i in range(n):
        c[i] = a[i] + b[i]
    return c

# 第一次呼叫會編譯，後續呼叫會使用編譯後的程式碼
result = add_arrays_numba(a, b)
```

實際應用：影像處理
```python
import numpy as np

def grayscale_naive(image):
    """逐像素處理（慢）"""
    h, w, c = image.shape
    result = np.zeros((h, w))
    for i in range(h):
        for j in range(w):
            result[i, j] = 0.299 * image[i, j, 0] + 0.587 * image[i, j, 1] + 0.114 * image[i, j, 2]
    return result

def grayscale_vectorized(image):
    """向量化處理（快）"""
    # 使用 NumPy 廣播
    return np.dot(image, [0.299, 0.587, 0.114])

# 測試
image = np.random.randint(0, 255, (1000, 1000, 3), dtype=np.uint8)

start = time.time()
g1 = grayscale_naive(image)
t1 = time.time() - start

start = time.time()
g2 = grayscale_vectorized(image)
t2 = time.time() - start

print(f"逐像素: {t1:.3f}s")
print(f"向量化: {t2:.3f}s")
print(f"加速比: {t1/t2:.1f}x")
```