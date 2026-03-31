"""
巴貝奇分析機的簡化模擬
展示早期機械計算的概念
"""

class AnalyticalEngine:
    """巴貝奇分析機的簡化模擬"""
    
    def __init__(self):
        self.store = [0] * 1000  # 儲存裝置：1000個暫存器
        self.mill = 0            # 運算裝置：類似累加器
        self.program = []         # 程式：操作序列
    
    def load(self, register: int, value: int):
        """將值載入指定暫存器"""
        self.store[register] = value
    
    def add(self, target: int, source: int):
        """將 source 暫存器的值加到 target"""
        self.store[target] += self.store[source]
    
    def sub(self, target: int, source: int):
        """從 target 減去 source"""
        self.store[target] -= self.store[source]
    
    def print_register(self, register: int):
        """輸出暫存器內容"""
        print(f"寄存器[{register}] = {self.store[register]}")


def demo_sum():
    """範例：計算 1 + 2 + 3 + ... + 10"""
    print("=== 巴貝奇分析機模擬 ===\n")
    
    engine = AnalyticalEngine()
    n = 10
    
    # 初始化
    engine.load(0, n)        # R0 = 10
    engine.load(1, 1)        # R1 = 1 (計數器)
    engine.load(2, 0)        # R2 = 0 (結果)
    engine.load(3, 1)        # R3 = 1 (遞增常數)
    
    # 計算 sum = 1 + 2 + ... + 10
    print("計算 1 + 2 + 3 + ... + 10:")
    for i in range(1, 11):
        engine.store[0] = i      # R0 = i
        engine.add(2, 0)         # R2 = R2 + R0
        engine.add(0, 3)         # R0 = R0 + 1 (準備下一個 i)
    
    print(f"\n結果：")
    engine.print_register(2)  # 輸出結果：55


if __name__ == "__main__":
    demo_sum()
