"""
量子計算基礎模擬
"""

from typing import Tuple
import math
import random

class Qubit:
    def __init__(self, alpha: complex = 1, beta: complex = 0):
        norm = math.sqrt(abs(alpha)**2 + abs(beta)**2)
        self.alpha = alpha / norm
        self.beta = beta / norm
    
    def measure(self) -> int:
        prob_zero = abs(self.alpha)**2
        return 0 if random.random() < prob_zero else 1
    
    def __repr__(self):
        return f"Qubit(α={self.alpha:.3f}, β={self.beta:.3f})"


class QuantumGate:
    @staticmethod
    def hadamard(qubit: Qubit) -> Qubit:
        alpha_new = (qubit.alpha + qubit.beta) / math.sqrt(2)
        beta_new = (qubit.alpha - qubit.beta) / math.sqrt(2)
        return Qubit(alpha_new, beta_new)
    
    @staticmethod
    def pauli_x(qubit: Qubit) -> Qubit:
        return Qubit(qubit.beta, qubit.alpha)


def demonstrate_quantum_principles():
    print("=== 量子計算基礎演示 ===\n")
    
    print("1. 創建初始量子位 |0⟩：")
    q0 = Qubit(1, 0)
    print(f"   {q0}")
    print(f"   測量結果：{'0' if q0.measure() == 0 else '1'} (100% 為0)")
    
    print("\n2. 應用Hadamard門，創建疊加態：")
    q = Qubit(1, 0)
    q_h = QuantumGate.hadamard(q)
    print(f"   {q_h}")
    
    # 多次測量展示機率
    counts = {0: 0, 1: 0}
    for _ in range(100):
        q_test = Qubit(1, 0)
        q_test = QuantumGate.hadamard(q_test)
        counts[q_test.measure()] += 1
    print(f"   100次測量：0出現{counts[0]}次，1出現{counts[1]}次")
    
    print("\n3. Grover搜索算法概念：")
    print("   經典搜索：O(N)")
    print("   Grover搜索：O(√N)")
    print("   原理：將目標狀態的振幅放大")
    
    print("\n4. Shor算法概念：")
    print("   用於整數分解")
    print("   經典：亞指數時間")
    print("   量子：多項式時間")
    print("   這對RSA加密有重大影響")


if __name__ == "__main__":
    demonstrate_quantum_principles()
