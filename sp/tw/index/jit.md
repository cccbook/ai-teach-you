# JIT 編譯器 (Just-In-Time Compiler)

## 概述

JIT 編譯器結合了直譯器和 AOT（Ahead-of-Time）編譯器的優點。JIT 在執行時動態將程式碼編譯為機器碼，常用于 Java、C#、JavaScript 等語言，實現「一次編譯，到處執行」並保持高效能。

## 歷史

- **1970s**：Smalltalk 首先使用 JIT
- **1990s**：Sun 為 Java 實現 JIT
- **2000s**：.NET CLR 使用 JIT
- **2008**：V8 JavaScript 引擎
- **現在**：幾乎所有現代語言都支援 JIT

## JIT 架構

```
原始碼 → [直譯執行] → [熱點偵測] → [JIT編譯] → [優化機器碼] → [快取執行]
```

### 1. 簡單 JIT 範例

```python
import ctypes
import os

class SimpleJIT:
    def __init__(self):
        self.code_cache = {}
    
    def compile(self, source):
        if source in self.code_cache:
            return self.code_cache[source]
        
        # 模擬編譯過程
        code = self.generate_code(source)
        self.code_cache[source] = code
        return code
    
    def generate_code(self, source):
        # 解析錶達式並生成機器碼
        # 這是一個簡化的例子
        parts = source.split()
        if len(parts) == 3 and parts[1] == '+':
            a, op, b = parts
            # 返回計算結果的函數
            return lambda: int(a) + int(b)
        return None
    
    def execute(self, source):
        code = self.compile(source)
        return code()
```

### 2. 使用 LLVM JIT

```python
# 使用 llvmlite (Python LLVM bindings)
from llvmlite import ir, binding

# 初始化 LLVM
binding.initialize()
target = binding.Target.from_triple(binding.get_default_triple())

# 創建模組
module = ir.Module(name="test")
func_type = ir.FunctionType(ir.IntType(32), [])
func = ir.Function(module, func_type, name="add")
block = func.append_basic_block(name="entry")
builder = ir.Builder(block)

# 生成: return a + b
a, b = func.args
result = builder.add(a, b)
builder.ret(result)

# 編譯為機器碼
with binding.create_mcjit_compiler(module, target) as compiler:
    ptr = compiler.get_function_address(func.name)
    add_func = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32, ctypes.c_int32)(ptr)
    result = add_func(3, 4)
    print(result)  # 7
```

### 3. 熱點偵測

```python
class HotSpotDetector:
    def __init__(self, threshold=1000):
        self.call_counts = {}
        self.threshold = threshold
    
    def record_call(self, func_name):
        count = self.call_counts.get(func_name, 0) + 1
        self.call_counts[func_name] = count
        
        if count >= self.threshold:
            return True
        return False
    
    def should_compile(self, func_name):
        return self.call_counts.get(func_name, 0) >= self.threshold

# 使用範例
detector = HotSpotDetector(threshold=5)

for i in range(10):
    if detector.record_call("hot_function"):
        print(f"Compiling hot_function...")
```

### 4. JIT 編譯策略

```python
class JITCompiler:
    def __init__(self):
        self.interpreter_mode = True
        self.compiled_functions = {}
    
    def execute(self, func_name, *args):
        if func_name in self.compiled_functions:
            # 已編譯，直接執行機器碼
            return self.compiled_functions[func_name](*args)
        
        # 直譯模式執行
        result = self.interpret(func_name, *args)
        
        # 檢查是否應該編譯
        if self.should_jit_compile(func_name):
            self.compile_function(func_name)
        
        return result
    
    def should_jit_compile(self, func_name):
        # 根據執行次數決定是否 JIT
        return self.call_count.get(func_name, 0) > 100
```

## JIT 優化技術

### 1. 內聯快取（Inline Cache）

```python
class InlineCache:
    def __init__(self):
        self.cache = {}
    
    def lookup(self, key):
        return self.cache.get(key)
    
    def update(self, key, value):
        self.cache[key] = value
```

### 2. 方法內联（Method Inlining）

```python
# 將小函數內聯到調用點
def inline_small_functions(code):
    # 識別小函數並內聯
    return optimized_code
```

### 3. 型別特化

```python
# 根據實際型別生成專門化代碼
def specialize(type_signature, code):
    return generate_specialized_code(type_signature)
```

## 為什麼使用 JIT？

1. **效能**：接近原生程式碼
2. **平台適應**：自動適應目標平台
3. **熱點優化**：只優化常用程式碼
4. **動態特性**：支援 eval、動態類型

## 參考資源

- "Java HotSpot Virtual Machine"
- V8 引擎文檔
- LLVM JIT 文件
