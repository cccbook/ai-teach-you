"""
不動點迭代範例 (Fixed-Point Iteration)
=====================================
展示不動點迭代（Fixed-Point Iteration）方法的理論與實作。
不動點迭代是一種用於求解方程式的數值方法，透過迭代 x = g(x) 來逼近解答。
"""

from typing import Callable, Tuple, List, Optional
import math


def fixed_point_iteration(
    g: Callable[[float], float],
    x0: float,
    tolerance: float = 1e-10,
    max_iterations: int = 100,
    track_history: bool = True
) -> Tuple[float, int, List[float], bool]:
    """
    不動點迭代法
    
    參數:
        g: 迭代函數 x = g(x)
        x0: 初始猜測值
        tolerance: 容差
        max_iterations: 最大迭代次數
        track_history: 是否記錄歷史
    
    返回:
        (不動點, 迭代次數, 歷史記錄, 是否收斂)
    """
    history = [] if track_history else None
    x = x0
    
    for i in range(max_iterations):
        x_new = g(x)
        
        if track_history:
            history.append(x_new)
        
        if abs(x_new - x) < tolerance:
            return x_new, i + 1, history, True
        
        x = x_new
    
    return x, max_iterations, history, False


def fixed_point_theorem_check(
    g: Callable[[float], float],
    a: float,
    b: float,
    tolerance: float = 1e-8
) -> dict:
    """
    檢查 Banach 不動點定理的條件
    
    參數:
        g: 迭代函數
        a, b: 區間端點
        tolerance: 導數估計的步長
    
    返回:
        檢查結果字典
    """
    result = {
        "interval": (a, b),
        "g_in_interval": True,
        "contraction": False,
        " Lipschitz_constant": None
    }
    
    n_samples = 100
    max_derivative = 0
    
    for i in range(n_samples + 1):
        x = a + (b - a) * i / n_samples
        
        try:
            gx = g(x)
            if not (a <= gx <= b):
                result["g_in_interval"] = False
                continue
            
            derivative_estimate = abs(g(x + tolerance) - g(x)) / tolerance
            max_derivative = max(max_derivative, derivative_estimate)
            
        except:
            result["g_in_interval"] = False
    
    result["Lipschitz_constant"] = max_derivative
    result["contraction"] = max_derivative < 1
    
    return result


def aitken_acceleration(
    g: Callable[[float], float],
    x0: float,
    tolerance: float = 1e-10,
    max_iterations: int = 100
) -> Tuple[float, int, List[float]]:
    """
    Aitken 加速法
    
    參數:
        g: 迭代函數
        x0: 初始猜測值
        tolerance: 容差
        max_iterations: 最大迭代次數
    
    返回:
        (不動點, 迭代次數, 歷史記錄)
    """
    history = []
    x = x0
    
    for i in range(max_iterations):
        x1 = g(x)
        x2 = g(x1)
        
        if abs(x2 - 2 * x1 + x) < 1e-15:
            raise ValueError("分母太小")
        
        x_new = x - (x1 - x) ** 2 / (x2 - 2 * x1 + x)
        history.append(x_new)
        
        if abs(x_new - x) < tolerance:
            return x_new, i + 1, history
        
        x = x_new
    
    return x, max_iterations, history


def steffensen_method(
    f: Callable[[float], float],
    x0: float,
    tolerance: float = 1e-10,
    max_iterations: int = 100
) -> Tuple[float, int, List[float]]:
    """
    Steffensen 方法 - 相當於 Aitken 應用於牛頓法
    
    參數:
        f: 目標函數 f(x) = 0
        x0: 初始猜測值
        tolerance: 容差
        max_iterations: 最大迭代次數
    
    返回:
        (根, 迭代次數, 歷史記錄)
    """
    history = []
    x = x0
    
    def g(x_val):
        return x_val - f(x_val)
    
    for i in range(max_iterations):
        x1 = g(x)
        x2 = g(x1)
        
        if abs(x2 - 2 * x1 + x) < 1e-15:
            raise ValueError("分母太小")
        
        x_new = x - (x1 - x) ** 2 / (x2 - 2 * x1 + x)
        history.append(x_new)
        
        if abs(f(x_new)) < tolerance:
            return x_new, i + 1, history
        
        x = x_new
    
    return x, max_iterations, history


def solve_equation_fixed_point(
    f: Callable[[float], float],
    x0: float,
    method: str = "simple",
    tolerance: float = 1e-10,
    max_iterations: int = 100
) -> Tuple[float, int, List[float]]:
    """
    使用不動點迭代求解方程式
    
    參數:
        f: 目標函數 f(x) = 0
        x0: 初始猜測值
        method: 轉換方法 ("simple", "aitken", "steffensen")
        tolerance: 容差
        max_iterations: 最大迭代次數
    
    返回:
        (根, 迭代次數, 歷史記錄)
    """
    if method == "simple":
        def g(x_val):
            return x_val + f(x_val)
        return fixed_point_iteration(g, x0, tolerance, max_iterations, True)
    
    elif method == "aitken":
        def g(x_val):
            return x_val + f(x_val)
        return aitken_acceleration(g, x0, tolerance, max_iterations)
    
    elif method == "steffensen":
        return steffensen_method(f, x0, tolerance, max_iterations)
    
    else:
        raise ValueError(f"未知方法: {method}")


class FixedPointIterator:
    """不動點迭代器類別"""
    
    def __init__(self, g: Callable[[float], float], x0: float):
        self.g = g
        self.current = x0
    
    def __iter__(self):
        return self
    
    def __next__(self) -> float:
        result = self.current
        self.current = self.g(self.current)
        return result
    
    def __call__(self, n: int, tolerance: float = 1e-10) -> Tuple[float, int]:
        """
        迭代直到收斂
        
        參數:
            n: 最大迭代次數
            tolerance: 容差
        
        返回:
            (收斂值, 迭代次數)
        """
        x = self.current
        
        for i in range(n):
            x_new = self.g(x)
            if abs(x_new - x) < tolerance:
                return x_new, i + 1
            x = x_new
        
        return x, n


def multiple_fixed_points(
    g: Callable[[float], float],
    search_range: Tuple[float, float],
    num_points: int = 100
) -> List[float]:
    """
    搜尋區間內的多個不動點
    
    參數:
        g: 迭代函數
        search_range: 搜尋區間
        num_points: 搜尋點數
    
    返回:
        不動點列表
    """
    fixed_points = []
    a, b = search_range
    
    for i in range(num_points + 1):
        x = a + (b - a) * i / num_points
        
        if abs(g(x) - x) < 1e-6:
            is_new = True
            for fp in fixed_points:
                if abs(fp - x) < 1e-4:
                    is_new = False
                    break
            
            if is_new:
                fixed_points.append(x)
    
    return fixed_points


def convergence_analysis(
    history: List[float],
    exact_solution: float = None
) -> dict:
    """
    收斂性分析
    
    參數:
        history: 迭代歷史
        exact_solution: 精確解（可選）
    
    返回:
        分析結果
    """
    if len(history) < 3:
        return {"error": "歷史記錄不足"}
    
    errors = []
    if exact_solution is not None:
        errors = [abs(x - exact_solution) for x in history]
    else:
        for i in range(1, len(history)):
            errors.append(abs(history[i] - history[i-1]))
    
    result = {
        "num_iterations": len(history),
        "final_value": history[-1],
        "errors": errors
    }
    
    if len(errors) >= 3:
        ratios = []
        for i in range(2, len(errors)):
            if errors[i-1] > 0 and errors[i-2] > 0:
                ratio = errors[i] / errors[i-1]
                ratios.append(ratio)
        
        if ratios:
            result["avg_convergence_ratio"] = sum(ratios) / len(ratios)
            result["converged"] = ratios[-1] < 0.1
    
    return result


def demo_fixed_point():
    """演示不動點迭代"""
    print("=== 不動點迭代範例演示 ===")
    print()
    
    print("1. 簡單不動點迭代:")
    g = lambda x: (x + 2) / x
    root, iterations, history, converged = fixed_point_iteration(g, 1.0)
    print(f"   求 x = (x + 2)/x 的不動點")
    print(f"   不動點: {root:.10f}")
    print(f"   收斂: {converged}, 迭代次數: {iterations}")
    print()
    
    print("2. Aitken 加速:")
    g_simple = lambda x: x + (x ** 2 - 2) / 2
    root, iterations, history = aitken_acceleration(g_simple, 1.0)
    print(f"   求 sqrt(2): {root:.10f}")
    print(f"   迭代次數: {iterations}")
    print()
    
    print("3. Steffensen 方法:")
    f = lambda x: x ** 2 - 2
    root, iterations, history = steffensen_method(f, 1.0)
    print(f"   求 sqrt(2): {root:.10f}")
    print(f"   迭代次數: {iterations}")
    print()
    
    print("4. 收斂分析:")
    analysis = convergence_analysis(history, exact_solution=math.sqrt(2))
    print(f"   平均收斂比率: {analysis.get('avg_convergence_ratio', 'N/A'):.4f}")


if __name__ == "__main__":
    demo_fixed_point()
