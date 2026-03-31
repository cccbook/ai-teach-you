"""
爬山演算法範例 (Hill Climbing Algorithm)
=========================================
展示爬山法（Hill Climbing）的各種實作方式。
爬山法是一種局部搜尋最佳化演算法，透過持續向目標函數值增加的方向移動來找到解答。
"""

from typing import Callable, List, Tuple, Any, Dict, Optional
import random
import math


def hill_climbing_basic(
    objective: Callable[[float], float],
    x0: float,
    step_size: float = 0.01,
    max_iterations: int = 1000,
    tolerance: float = 1e-8
) -> Tuple[float, float, int]:
    """
    基本爬山法
    
    參數:
        objective: 目標函數
        x0: 初始點
        step_size: 步長
        max_iterations: 最大迭代次數
        tolerance: 容差
    
    返回:
        (最佳點, 最佳值, 迭代次數)
    """
    x = x0
    best_x = x
    best_value = objective(x)
    
    for i in range(max_iterations):
        found_better = False
        
        for direction in [1, -1]:
            candidate = x + direction * step_size
            value = objective(candidate)
            
            if value > best_value:
                best_value = value
                best_x = candidate
                found_better = True
        
        if found_better:
            x = best_x
            if step_size < tolerance:
                break
        else:
            step_size *= 0.5
    
    return best_x, best_value, min(i + 1, max_iterations)


def hill_climbing_stochastic(
    objective: Callable[[List[float]], float],
    initial: List[float],
    step_sizes: List[float],
    max_iterations: int = 1000,
    temperature: float = 100.0
) -> Tuple[List[float], float, int]:
    """
    隨機爬山法
    
    參數:
        objective: 目標函數
        initial: 初始點
        step_sizes: 各維度的步長
        max_iterations: 最大迭代次數
        temperature: 溫度參數
    
    返回:
        (最佳點, 最佳值, 迭代次數)
    """
    current = initial[:]
    current_value = objective(current)
    best = current[:]
    best_value = current_value
    
    for i in range(max_iterations):
        candidate = current[:]
        
        for j in range(len(candidate)):
            delta = random.uniform(-step_sizes[j], step_sizes[j])
            candidate[j] += delta
        
        candidate_value = objective(candidate)
        delta = candidate_value - current_value
        
        if delta > 0:
            current = candidate
            current_value = candidate_value
            
            if current_value > best_value:
                best = current[:]
                best_value = current_value
        else:
            prob = math.exp(delta / temperature)
            if random.random() < prob:
                current = candidate
                current_value = candidate_value
    
    return best, best_value, max_iterations


def hill_climbing_with_restarts(
    objective: Callable[[List[float]], float],
    dimensions: int,
    bounds: List[Tuple[float, float]],
    num_restarts: int = 10,
    max_iterations: int = 1000
) -> Tuple[List[float], float]:
    """
    帶有隨機重啟的爬山法
    
    參數:
        objective: 目標函數
        dimensions: 維度
        bounds: 邊界 [(min, max), ...]
        num_restarts: 重啟次數
        max_iterations: 每次最大迭代次數
    
    返回:
        (最佳點, 最佳值)
    """
    best_solution = None
    best_value = float('-inf')
    
    for _ in range(num_restarts):
        initial = [random.uniform(bounds[i][0], bounds[i][1]) for i in range(dimensions)]
        
        solution, value, _ = hill_climbing_stochastic(
            objective, initial, [0.1] * dimensions, max_iterations
        )
        
        if value > best_value:
            best_value = value
            best_solution = solution
    
    return best_solution, best_value


def hill_climbing_adaptive(
    objective: Callable[[float], float],
    x0: float,
    initial_step: float = 0.1,
    max_iterations: int = 1000,
    shrink_factor: float = 0.5,
    expand_factor: float = 2.0
) -> Tuple[float, float, int]:
    """
    自適應步長爬山法
    
    參數:
        objective: 目標函數
        x0: 初始點
        initial_step: 初始步長
        max_iterations: 最大迭代次數
        shrink_factor: 收縮因子
        expand_factor: 擴展因子
    
    返回:
        (最佳點, 最佳值, 迭代次數)
    """
    x = x0
    step = initial_step
    best_x = x
    best_value = objective(x)
    prev_value = best_value
    
    for i in range(max_iterations):
        improved = False
        
        for direction in [1, -1]:
            candidate = x + direction * step
            value = objective(candidate)
            
            if value > best_value:
                best_value = value
                best_x = candidate
                improved = True
        
        if improved:
            x = best_x
            step *= expand_factor
        else:
            step *= shrink_factor
        
        if step < 1e-10:
            break
        
        prev_value = best_value
    
    return best_x, best_value, i + 1


def hill_climbing_2d(
    objective: Callable[[float, float], float],
    x0: float,
    y0: float,
    step_size: float = 0.01,
    max_iterations: int = 1000
) -> Tuple[float, float, float, int]:
    """
    2D 爬山法
    
    參數:
        objective: 目標函數 f(x, y)
        x0, y0: 初始點
        step_size: 步長
        max_iterations: 最大迭代次數
    
    返回:
        (best_x, best_y, best_value, iterations)
    """
    x, y = x0, y0
    best_x, best_y = x, y
    best_value = objective(x, y)
    
    for i in range(max_iterations):
        found_better = False
        
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            candidate_x = x + dx * step_size
            candidate_y = y + dy * step_size
            value = objective(candidate_x, candidate_y)
            
            if value > best_value:
                best_value = value
                best_x = candidate_x
                best_y = candidate_y
                found_better = True
        
        if found_better:
            x, y = best_x, best_y
        else:
            step_size *= 0.5
            if step_size < 1e-10:
                break
    
    return best_x, best_y, best_value, min(i + 1, max_iterations)


class HillClimbingSolver:
    """爬山法求解器類別"""
    
    def __init__(self, objective: Callable, bounds: List[Tuple[float, float]]):
        self.objective = objective
        self.bounds = bounds
        self.dimensions = len(bounds)
    
    def solve(
        self,
        initial: List[float] = None,
        method: str = "basic",
        max_iterations: int = 1000
    ) -> Dict[str, Any]:
        """
        求解最佳化問題
        
        參數:
            initial: 初始點
            method: 方法 ("basic", "stochastic", "adaptive")
            max_iterations: 最大迭代次數
        
        返回:
            結果字典
        """
        if initial is None:
            initial = [random.uniform(self.bounds[i][0], self.bounds[i][1]) 
                      for i in range(self.dimensions)]
        
        if method == "basic":
            step_sizes = [0.1] * self.dimensions
            return hill_climbing_stochastic(
                self.objective, initial, step_sizes, max_iterations
            )
        elif method == "adaptive":
            return self._adaptive_search(initial, max_iterations)
        
        return hill_climbing_stochastic(
            self.objective, initial, [0.1] * self.dimensions, max_iterations
        )
    
    def _adaptive_search(self, initial: List[float], max_iterations: int):
        """自適應搜尋"""
        current = initial[:]
        current_value = self.objective(current)
        best = current[:]
        best_value = current_value
        step_sizes = [0.1] * self.dimensions
        
        for i in range(max_iterations):
            improved = False
            
            for j in range(self.dimensions):
                for direction in [-1, 1]:
                    candidate = current[:]
                    candidate[j] += direction * step_sizes[j]
                    candidate_value = self.objective(candidate)
                    
                    if candidate_value > current_value:
                        current = candidate
                        current_value = candidate_value
                        step_sizes[j] *= 1.5
                        improved = True
                        
                        if current_value > best_value:
                            best = current[:]
                            best_value = current_value
            
            if not improved:
                for j in range(self.dimensions):
                    step_sizes[j] *= 0.5
            
            if all(s < 1e-10 for s in step_sizes):
                break
        
        return {
            "solution": best,
            "value": best_value,
            "iterations": i + 1
        }


def test_function(x: List[float]) -> float:
    """測試函數：Rastrigin 函數"""
    n = len(x)
    return 10 * n - sum([xi ** 2 - 10 * math.cos(2 * math.pi * xi) for xi in x])


def demo_hill_climbing():
    """演示爬山法"""
    print("=== 爬山演算法範例演示 ===")
    print()
    
    print("1. 基本爬山法:")
    obj = lambda x: -x ** 2 + 4 * x
    x, value, iterations = hill_climbing_basic(obj, x0=0.1)
    print(f"   最大化 -x^2 + 4x")
    print(f"   最佳點: x = {x:.4f}, 值 = {value:.4f}")
    print(f"   迭代次數: {iterations}")
    print()
    
    print("2. 隨機爬山法:")
    obj_2d = lambda xy: -(xy[0] - 1) ** 2 - (xy[1] - 2) ** 2
    solution, value, iterations = hill_climbing_stochastic(
        obj_2d, [0, 0], [0.1, 0.1], 1000
    )
    print(f"   最小化 (x-1)^2 + (y-2)^2")
    print(f"   最佳解: {solution}, 值: {value:.4f}")
    print()
    
    print("3. 2D 爬山法:")
    obj_2d_max = lambda x, y: math.sin(x) * math.cos(y)
    x, y, value, iterations = hill_climbing_2d(obj_2d_max, 1.0, 1.0)
    print(f"   最大化 sin(x)cos(y)")
    print(f"   最佳點: ({x:.4f}, {y:.4f}), 值: {value:.4f}")
    print()
    
    print("4. 自適應步長:")
    obj_sharp = lambda x: -(x - 3) ** 4 + (x - 3) ** 2 + x
    x, value, iterations = hill_climbing_adaptive(obj_sharp, 0.0)
    print(f"   最佳化函數")
    print(f"   最佳點: x = {x:.4f}, 值 = {value:.4f}")


if __name__ == "__main__":
    demo_hill_climbing()
