"""
模擬退火演算法範例 (Simulated Annealing)
========================================
展示模擬退火（Simulated Annealing）演算法的實作。
模擬退火是一種機率性的最佳化演算法，靈感來自金屬退火過程，可在全域中搜尋最佳解。
"""

from typing import Callable, List, Tuple, Any, Dict, Optional
import random
import math
import time


def simulated_annealing(
    objective: Callable[[List[float]], float],
    initial: List[float],
    bounds: List[Tuple[float, float]],
    initial_temp: float = 1000.0,
    final_temp: float = 0.01,
    cooling_rate: float = 0.995,
    max_iterations: int = 10000,
    step_size: float = 0.1
) -> Tuple[List[float], float, int]:
    """
    標準模擬退火演算法
    
    參數:
        objective: 目標函數
        initial: 初始解
        bounds: 變數邊界 [(min, max), ...]
        initial_temp: 初始溫度
        final_temp: 最終溫度
        cooling_rate: 冷卻率
        max_iterations: 最大迭代次數
        step_size: 鄰域搜尋步長
    
    返回:
        (最佳解, 最佳值, 迭代次數)
    """
    current = initial[:]
    current_value = objective(current)
    
    best = current[:]
    best_value = current_value
    
    temp = initial_temp
    iterations = 0
    
    while temp > final_temp and iterations < max_iterations:
        iterations += 1
        
        candidate = current[:]
        idx = random.randint(0, len(candidate) - 1)
        
        delta = random.uniform(-step_size, step_size)
        candidate[idx] += delta
        
        candidate[idx] = max(bounds[idx][0], min(bounds[idx][1], candidate[idx]))
        
        candidate_value = objective(candidate)
        
        delta_e = candidate_value - current_value
        
        if delta_e > 0:
            current = candidate
            current_value = candidate_value
            
            if current_value > best_value:
                best = current[:]
                best_value = current_value
        else:
            probability = math.exp(delta_e / temp)
            if random.random() < probability:
                current = candidate
                current_value = candidate_value
        
        temp *= cooling_rate
    
    return best, best_value, iterations


def simulated_annealing_adaptive(
    objective: Callable[[List[float]], float],
    initial: List[float],
    bounds: List[Tuple[float, float]],
    max_iterations: int = 10000
) -> Tuple[List[float], float, int]:
    """
    自適應模擬退火
    
    參數:
        objective: 目標函數
        initial: 初始解
        bounds: 變數邊界
        max_iterations: 最大迭代次數
    
    返回:
        (最佳解, 最佳值, 迭代次數)
    """
    current = initial[:]
    current_value = objective(current)
    
    best = current[:]
    best_value = current_value
    
    temp = 1000.0
    step_size = 0.5
    
    for i in range(max_iterations):
        temp = 1000 * (1 - i / max_iterations) ** 2
        step_size = 0.5 * (1 - i / max_iterations)
        
        candidate = current[:]
        idx = random.randint(0, len(candidate) - 1)
        
        delta = random.uniform(-step_size, step_size)
        candidate[idx] += delta
        candidate[idx] = max(bounds[idx][0], min(bounds[idx][1], candidate[idx]))
        
        candidate_value = objective(candidate)
        delta_e = candidate_value - current_value
        
        if delta_e > 0 or random.random() < math.exp(delta_e / temp):
            current = candidate
            current_value = candidate_value
            
            if current_value > best_value:
                best = current[:]
                best_value = current_value
    
    return best, best_value, max_iterations


def simulated_annealing_with_restarts(
    objective: Callable[[List[float]], float],
    dimensions: int,
    bounds: List[Tuple[float, float]],
    num_restarts: int = 5,
    max_iterations: int = 5000
) -> Tuple[List[float], float]:
    """
    帶有重啟的模擬退火
    
    參數:
        objective: 目標函數
        dimensions: 維度
        bounds: 變數邊界
        num_restarts: 重啟次數
        max_iterations: 每次最大迭代次數
    
    返回:
        (最佳解, 最佳值)
    """
    best_solution = None
    best_value = float('-inf')
    
    for _ in range(num_restarts):
        initial = [random.uniform(bounds[i][0], bounds[i][1]) for i in range(dimensions)]
        
        solution, value, _ = simulated_annealing(
            objective, initial, bounds, max_iterations=max_iterations
        )
        
        if value > best_value:
            best_value = value
            best_solution = solution
    
    return best_solution, best_value


def boltzmann_annealing(
    objective: Callable[[List[float]], float],
    initial: List[float],
    bounds: List[Tuple[float, float]],
    max_iterations: int = 10000
) -> Tuple[List[float], float, int]:
    """
    波茲曼退火
    
    參數:
        objective: 目標函數
        initial: 初始解
        bounds: 變數邊界
        max_iterations: 最大迭代次數
    
    返回:
        (最佳解, 最佳值, 迭代次數)
    """
    current = initial[:]
    current_value = objective(current)
    
    best = current[:]
    best_value = current_value
    
    temp = 1000.0
    
    for i in range(max_iterations):
        temp = 1000 / math.log(2 + i)
        
        candidate = current[:]
        idx = random.randint(0, len(candidate) - 1)
        delta = random.uniform(-0.1, 0.1)
        
        candidate[idx] += delta
        candidate[idx] = max(bounds[idx][0], min(bounds[idx][1], candidate[idx]))
        
        candidate_value = objective(candidate)
        delta_e = candidate_value - current_value
        
        if delta_e > 0 or random.random() < math.exp(delta_e / temp):
            current = candidate
            current_value = candidate_value
            
            if current_value > best_value:
                best = current[:]
                best_value = current_value
    
    return best, best_value, max_iterations


def fast_annealing(
    objective: Callable[[List[float]], float],
    initial: List[float],
    bounds: List[Tuple[float, float]],
    max_iterations: int = 10000
) -> Tuple[List[float], float, int]:
    """
    快速退火
    
    參數:
        objective: 目標函數
        initial: 初始解
        bounds: 變數邊界
        max_iterations: 最大迭代次數
    
    返回:
        (最佳解, 最佳值, 迭代次數)
    """
    current = initial[:]
    current_value = objective(current)
    
    best = current[:]
    best_value = current_value
    
    temp = 1000.0
    
    for i in range(max_iterations):
        temp = 1000 / (1 + i)
        
        candidate = current[:]
        idx = random.randint(0, len(candidate) - 1)
        
        u = random.random()
        delta = (1 / temp) * ((1 + 1/temp) ** abs(u) - 1) * (1 if random.random() < 0.5 else -1)
        
        candidate[idx] += delta
        candidate[idx] = max(bounds[idx][0], min(bounds[idx][1], candidate[idx]))
        
        candidate_value = objective(candidate)
        delta_e = candidate_value - current_value
        
        if delta_e > 0 or random.random() < math.exp(delta_e / temp):
            current = candidate
            current_value = candidate_value
            
            if current_value > best_value:
                best = current[:]
                best_value = current_value
    
    return best, best_value, max_iterations


class SimulatedAnnealingSolver:
    """模擬退火求解器"""
    
    def __init__(self, objective: Callable, bounds: List[Tuple[float, float]]):
        self.objective = objective
        self.bounds = bounds
        self.dimensions = len(bounds)
        self.history = []
    
    def solve(
        self,
        initial: List[float] = None,
        method: str = "standard",
        max_iterations: int = 10000
    ) -> Dict[str, Any]:
        """
        求解
        
        參數:
            initial: 初始解
            method: 方法 ("standard", "adaptive", "boltzmann", "fast")
            max_iterations: 最大迭代次數
        
        返回:
            結果字典
        """
        if initial is None:
            initial = [random.uniform(self.bounds[i][0], self.bounds[i][1])
                      for i in range(self.dimensions)]
        
        if method == "standard":
            solution, value, iterations = simulated_annealing(
                self.objective, initial, self.bounds, max_iterations=max_iterations
            )
        elif method == "adaptive":
            solution, value, iterations = simulated_annealing_adaptive(
                self.objective, initial, self.bounds, max_iterations=max_iterations
            )
        elif method == "boltzmann":
            solution, value, iterations = boltzmann_annealing(
                self.objective, initial, self.bounds, max_iterations=max_iterations
            )
        elif method == "fast":
            solution, value, iterations = fast_annealing(
                self.objective, initial, self.bounds, max_iterations=max_iterations
            )
        else:
            solution, value, iterations = simulated_annealing(
                self.objective, initial, self.bounds, max_iterations=max_iterations
            )
        
        return {
            "solution": solution,
            "value": value,
            "iterations": iterations,
            "history": self.history
        }


def rastrigin(x: List[float]) -> float:
    """Rastrigin 函數（測試函數）"""
    n = len(x)
    return 10 * n - sum([xi ** 2 - 10 * math.cos(2 * math.pi * xi) for xi in x])


def ackley(x: List[float]) -> float:
    """Ackley 函數（測試函數）"""
    n = len(x)
    sum1 = sum([xi ** 2 for xi in x])
    sum2 = sum([math.cos(2 * math.pi * xi) for xi in x])
    return -20 * math.exp(-0.2 * math.sqrt(sum1 / n)) - math.exp(sum2 / n) + 20 + math.e


def demo_simulated_annealing():
    """演示模擬退火"""
    print("=== 模擬退火演算法範例演示 ===")
    print()
    
    print("1. 標準模擬退火:")
    bounds = [(-5, 5), (-5, 5)]
    initial = [random.uniform(-5, 5), random.uniform(-5, 5)]
    solution, value, iterations = simulated_annealing(
        lambda x: -((x[0] - 1) ** 2 + (x[1] - 2) ** 2),
        initial, bounds
    )
    print(f"   最佳解: {solution}")
    print(f"   最佳值: {value:.4f}")
    print(f"   迭代次數: {iterations}")
    print()
    
    print("2. 自適應模擬退火:")
    initial = [random.uniform(-5, 5), random.uniform(-5, 5)]
    solution, value, iterations = simulated_annealing_adaptive(
        rastrigin, initial, bounds, max_iterations=5000
    )
    print(f"   最佳解: {[round(x, 4) for x in solution]}")
    print(f"   最佳值: {value:.4f}")
    print()
    
    print("3. 波茲曼退火:")
    initial = [random.uniform(-5, 5), random.uniform(-5, 5)]
    solution, value, iterations = boltzmann_annealing(
        ackley, initial, bounds, max_iterations=5000
    )
    print(f"   最佳解: {[round(x, 4) for x in solution]}")
    print(f"   最佳值: {value:.4f}")
    print()
    
    print("4. 快速退火:")
    initial = [random.uniform(-5, 5), random.uniform(-5, 5)]
    solution, value, iterations = fast_annealing(
        rastrigin, initial, bounds, max_iterations=5000
    )
    print(f"   最佳解: {[round(x, 4) for x in solution]}")
    print(f"   最佳值: {value:.4f}")


if __name__ == "__main__":
    demo_simulated_annealing()
