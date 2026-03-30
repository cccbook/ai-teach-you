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