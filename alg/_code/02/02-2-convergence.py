"""
收斂分析範例 (Convergence Analysis)
===================================
展示各種迭代過程的收斂分析方法。
收斂分析是分析數值方法是否能趨近於正確解答的學問。
"""

from typing import List, Callable, Tuple, Dict
import math


class ConvergenceAnalyzer:
    """收斂分析器"""
    
    def __init__(self, tolerance: float = 1e-10, max_iterations: int = 1000):
        self.tolerance = tolerance
        self.max_iterations = max_iterations
        self.history: List[float] = []
    
    def add_value(self, value: float) -> None:
        """記錄每次迭代的值"""
        self.history.append(value)
    
    def check_convergence(self) -> bool:
        """檢查是否收斂"""
        if len(self.history) < 2:
            return False
        
        last = self.history[-1]
        second_last = self.history[-2]
        
        return abs(last - second_last) < self.tolerance
    
    def get_convergence_rate(self) -> float:
        """
        計算收斂速率
        
        返回:
            收斂速率階數
            - 線性收斂: 速率 ≈ 1
            - 超線性收斂: 速率 ≈ 2
            - 二階收斂: 速率 ≈ 3
        """
        if len(self.history) < 3:
            return 0.0
        
        rates = []
        for i in range(2, len(self.history)):
            if self.history[i-1] != 0 and self.history[i-2] != 0:
                ratio = abs(self.history[i] - self.history[i-1]) / abs(self.history[i-1] - self.history[i-2])
                if ratio > 0 and ratio < 1:
                    rates.append(ratio)
        
        return rates[-1] if rates else 0.0
    
    def order_of_convergence(self) -> float:
        """
        計算收斂階數
        
        使用: |e_{n+1}| ≈ C * |e_n|^p
        
        返回:
            收斂階數 p
        """
        if len(self.history) < 4:
            return 0.0
        
        errors = []
        for i in range(1, len(self.history)):
            if self.history[i] != 0:
                errors.append(abs(self.history[i]))
        
        if len(errors) < 3:
            return 0.0
        
        ratios = []
        for i in range(2, len(errors)):
            if errors[i-1] > 0 and errors[i-2] > 0:
                ratio = math.log(errors[i] / errors[i-1]) / math.log(errors[i-1] / errors[i-2])
                if not math.isnan(ratio) and not math.isinf(ratio):
                    ratios.append(ratio)
        
        return ratios[-1] if ratios else 0.0


def newton_raphson(
    func: Callable[[float], float],
    deriv: Callable[[float], float],
    x0: float,
    tolerance: float = 1e-10,
    max_iterations: int = 100
) -> Tuple[float, int, List[float]]:
    """
    牛頓-拉夫森法（Newton-Raphson Method）
    
    參數:
        func: 函數 f(x)
        deriv: 導函數 f'(x)
        x0: 初始猜測
        tolerance: 容差
        max_iterations: 最大迭代次數
    
    返回:
        (根, 迭代次數, 歷史記錄)
    """
    history = []
    x = x0
    
    for i in range(max_iterations):
        fx = func(x)
        dfx = deriv(x)
        
        if abs(dfx) < 1e-15:
            raise ValueError("導數值太小")
        
        x_new = x - fx / dfx
        history.append(x_new)
        
        if abs(x_new - x) < tolerance:
            return x_new, i + 1, history
        
        x = x_new
    
    return x, max_iterations, history


def bisection_method(
    func: Callable[[float], float],
    a: float,
    b: float,
    tolerance: float = 1e-10,
    max_iterations: int = 100
) -> Tuple[float, int, List[float]]:
    """
    二分法（Bisection Method）
    
    參數:
        func: 函數 f(x)
        a: 左端點
        b: 右端點
        tolerance: 容差
        max_iterations: 最大迭代次數
    
    返回:
        (根, 迭代次數, 歷史記錄)
    """
    history = []
    fa, fb = func(a), func(b)
    
    if fa * fb > 0:
        raise ValueError("端點函數值需異號")
    
    for i in range(max_iterations):
        c = (a + b) / 2
        fc = func(c)
        history.append(c)
        
        if abs(b - a) < tolerance or abs(fc) < tolerance:
            return c, i + 1, history
        
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
    
    return (a + b) / 2, max_iterations, history


def secant_method(
    func: Callable[[float], float],
    x0: float,
    x1: float,
    tolerance: float = 1e-10,
    max_iterations: int = 100
) -> Tuple[float, int, List[float]]:
    """
    割線法（Secant Method）
    
    參數:
        func: 函數 f(x)
        x0: 第一個初始猜測
        x1: 第二個初始猜測
        tolerance: 容差
        max_iterations: 最大迭代次數
    
    返回:
        (根, 迭代次數, 歷史記錄)
    """
    history = []
    x_prev, x = x0, x1
    
    for i in range(max_iterations):
        fx = func(x)
        fx_prev = func(x_prev)
        
        if abs(fx - fx_prev) < 1e-15:
            raise ValueError("函數值差異太小")
        
        x_new = x - fx * (x - x_prev) / (fx - fx_prev)
        history.append(x_new)
        
        if abs(x_new - x) < tolerance:
            return x_new, i + 1, history
        
        x_prev, x = x, x_new
    
    return x, max_iterations, history


def fixed_point_iteration(
    g: Callable[[float], float],
    x0: float,
    tolerance: float = 1e-10,
    max_iterations: int = 100
) -> Tuple[float, int, List[float], bool]:
    """
    不動點迭代（Fixed-Point Iteration）
    
    參數:
        g: 迭代函數 x = g(x)
        x0: 初始猜測
        tolerance: 容差
        max_iterations: 最大迭代次數
    
    返回:
        (根, 迭代次數, 歷史記錄, 是否收斂)
    """
    history = []
    x = x0
    
    for i in range(max_iterations):
        x_new = g(x)
        history.append(x_new)
        
        if abs(x_new - x) < tolerance:
            return x_new, i + 1, history, True
        
        x = x_new
    
    return x, max_iterations, history, False


def steffensen_acceleration(
    g: Callable[[float], float],
    x0: float,
    tolerance: float = 1e-10,
    max_iterations: int = 100
) -> Tuple[float, int, List[float]]:
    """
    Steffensen 加速法
    
    參數:
        g: 迭代函數
        x0: 初始猜測
        tolerance: 容差
        max_iterations: 最大迭代次數
    
    返回:
        (根, 迭代次數, 歷史記錄)
    """
    history = []
    x = x0
    
    for i in range(max_iterations):
        gx = g(x)
        ggx = g(gx)
        
        if abs(ggx - 2 * gx + x) < 1e-15:
            raise ValueError("分母太小")
        
        x_new = x - (gx - x) ** 2 / (ggx - 2 * gx + x)
        history.append(x_new)
        
        if abs(x_new - x) < tolerance:
            return x_new, i + 1, history
        
        x = x_new
    
    return x, max_iterations, history


def analyze_convergence(
    history: List[float],
    exact_solution: float = None
) -> Dict[str, float]:
    """
    分析迭代序列的收斂性質
    
    參數:
        history: 迭代歷史
        exact_solution: 精確解（若已知）
    
    返回:
        分析結果字典
    """
    if len(history) < 2:
        return {"error": "歷史記錄太短"}
    
    result = {
        "num_iterations": len(history),
        "final_value": history[-1],
        "final_error": abs(history[-1] - history[-2]) if exact_solution is None else abs(history[-1] - exact_solution)
    }
    
    if exact_solution is not None:
        errors = [abs(x - exact_solution) for x in history]
        
        if len(errors) >= 3:
            order = 0
            for i in range(2, len(errors)):
                if errors[i-1] > 0 and errors[i-2] > 0:
                    ratio = math.log(errors[i] / errors[i-1]) / math.log(errors[i-1] / errors[i-2])
                    if not math.isnan(ratio):
                        order = ratio
                        break
            
            result["convergence_order"] = order
            result["errors"] = errors
    
    return result


def compare_methods(
    func: Callable[[float], float],
    deriv: Callable[[float], float],
    x0: float,
    a: float = None,
    b: float = None
) -> Dict[str, Dict]:
    """
    比較不同數值方法的收斂速度
    
    參數:
        func: 目標函數
        deriv: 導函數
        x0: 初始點
        a, b: 二分法的區間端點
    """
    results = {}
    
    try:
        root, iterations, history = newton_raphson(func, deriv, x0)
        results["newton_raphson"] = {
            "root": root,
            "iterations": iterations,
            "converged": True
        }
    except Exception as e:
        results["newton_raphson"] = {"error": str(e)}
    
    if a is not None and b is not None:
        try:
            root, iterations, history = bisection_method(func, a, b)
            results["bisection"] = {
                "root": root,
                "iterations": iterations,
                "converged": True
            }
        except Exception as e:
            results["bisection"] = {"error": str(e)}
    
    return results


def demo_convergence():
    """演示收斂分析"""
    print("=== 收斂分析範例演示 ===")
    print()
    
    print("1. 牛頓-拉夫森法:")
    func = lambda x: x ** 2 - 2
    deriv = lambda x: 2 * x
    root, iterations, history = newton_raphson(func, deriv, 1.0)
    print(f"   求 sqrt(2): 根 = {root:.10f}")
    print(f"   迭代次數: {iterations}")
    print()
    
    print("2. 二分法:")
    root, iterations, history = bisection_method(func, 0, 2)
    print(f"   求 sqrt(2): 根 = {root:.10f}")
    print(f"   迭代次數: {iterations}")
    print()
    
    print("3. 割線法:")
    root, iterations, history = secant_method(func, 0, 2)
    print(f"   求 sqrt(2): 根 = {root:.10f}")
    print(f"   迭代次數: {iterations}")
    print()
    
    print("4. 不動點迭代:")
    g = lambda x: 2 / x
    root, iterations, history, converged = fixed_point_iteration(g, 1.0)
    print(f"   求 sqrt(2): 根 = {root:.10f}")
    print(f"   收斂: {converged}, 迭代次數: {iterations}")
    print()
    
    print("5. 收斂分析:")
    analyzer = ConvergenceAnalyzer()
    for val in history:
        analyzer.add_value(val)
    print(f"   收斂速率: {analyzer.get_convergence_rate():.4f}")
    print(f"   收斂階數: {analyzer.order_of_convergence():.4f}")


if __name__ == "__main__":
    demo_convergence()
