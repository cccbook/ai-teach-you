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