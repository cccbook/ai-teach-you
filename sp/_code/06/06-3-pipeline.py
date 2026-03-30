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