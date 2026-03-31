"""
梯度下降法範例 (Gradient Descent)
=================================
展示梯度下降法（Gradient Descent）的各種實作方式。
梯度下降法是一種用於求解最佳化問題的一階最佳化演算法。
"""

from typing import Callable, List, Tuple, Any, Dict, Optional
import numpy as np


def gradient_descent_basic(
    func: Callable[[float], float],
    deriv: Callable[[float], float],
    x0: float,
    learning_rate: float = 0.01,
    tolerance: float = 1e-8,
    max_iterations: int = 1000
) -> Tuple[float, float, int]:
    """
    基本梯度下降法
    
    參數:
        func: 目標函數
        deriv: 導函數
        x0: 初始點
        learning_rate: 學習率
        tolerance: 容差
        max_iterations: 最大迭代次數
    
    返回:
        (最佳點, 最小值, 迭代次數)
    """
    x = x0
    
    for i in range(max_iterations):
        gradient = deriv(x)
        
        if abs(gradient) < tolerance:
            break
        
        x = x - learning_rate * gradient
    
    return x, func(x), i + 1


def gradient_descent_momentum(
    func: Callable[[float], float],
    deriv: Callable[[float], float],
    x0: float,
    learning_rate: float = 0.01,
    momentum: float = 0.9,
    tolerance: float = 1e-8,
    max_iterations: int = 1000
) -> Tuple[float, float, int]:
    """
    帶有動量的梯度下降法
    
    參數:
        func: 目標函數
        deriv: 導函數
        x0: 初始點
        learning_rate: 學習率
        momentum: 動量因子
        tolerance: 容差
        max_iterations: 最大迭代次數
    
    返回:
        (最佳點, 最小值, 迭代次數)
    """
    x = x0
    velocity = 0.0
    
    for i in range(max_iterations):
        gradient = deriv(x)
        
        if abs(gradient) < tolerance:
            break
        
        velocity = momentum * velocity - learning_rate * gradient
        x = x + velocity
    
    return x, func(x), i + 1


def gradient_descent_adagrad(
    func: Callable[[float], float],
    deriv: Callable[[float], float],
    x0: float,
    learning_rate: float = 1.0,
    epsilon: float = 1e-8,
    max_iterations: int = 1000
) -> Tuple[float, float, int]:
    """
    AdaGrad 方法
    
    參數:
        func: 目標函數
        deriv: 導函數
        x0: 初始點
        learning_rate: 學習率
        epsilon: 防止除零的小數
        max_iterations: 最大迭代次數
    
    返回:
        (最佳點, 最小值, 迭代次數)
    """
    x = x0
    sum_squared_gradients = 0.0
    
    for i in range(max_iterations):
        gradient = deriv(x)
        sum_squared_gradients += gradient ** 2
        
        adjusted_lr = learning_rate / (epsilon + np.sqrt(sum_squared_gradients))
        x = x - adjusted_lr * gradient
    
    return x, func(x), i + 1


def gradient_descent_rmsprop(
    func: Callable[[float], float],
    deriv: Callable[[float], float],
    x0: float,
    learning_rate: float = 0.01,
    decay_rate: float = 0.99,
    epsilon: float = 1e-8,
    max_iterations: int = 1000
) -> Tuple[float, float, int]:
    """
    RMSProp 方法
    
    參數:
        func: 目標函數
        deriv: 導函數
        x0: 初始點
        learning_rate: 學習率
        decay_rate: 衰減率
        epsilon: 防止除零的小數
        max_iterations: 最大迭代次數
    
    返回:
        (最佳點, 最小值, 迭代次數)
    """
    x = x0
    sum_squared_gradients = 0.0
    
    for i in range(max_iterations):
        gradient = deriv(x)
        sum_squared_gradients = decay_rate * sum_squared_gradients + (1 - decay_rate) * gradient ** 2
        
        adjusted_lr = learning_rate / (epsilon + np.sqrt(sum_squared_gradients))
        x = x - adjusted_lr * gradient
    
    return x, func(x), i + 1


def gradient_descent_adam(
    func: Callable[[float], float],
    deriv: Callable[[float], float],
    x0: float,
    learning_rate: float = 0.01,
    beta1: float = 0.9,
    beta2: float = 0.999,
    epsilon: float = 1e-8,
    max_iterations: int = 1000
) -> Tuple[float, float, int]:
    """
    Adam 方法
    
    參數:
        func: 目標函數
        deriv: 導函數
        x0: 初始點
        learning_rate: 學習率
        beta1: 第一矩估計的衰減率
        beta2: 第二矩估計的衰減率
        epsilon: 防止除零的小數
        max_iterations: 最大迭代次數
    
    返回:
        (最佳點, 最小值, 迭代次數)
    """
    x = x0
    m = 0.0
    v = 0.0
    
    for i in range(max_iterations):
        gradient = deriv(x)
        
        m = beta1 * m + (1 - beta1) * gradient
        v = beta2 * v + (1 - beta2) * gradient ** 2
        
        m_hat = m / (1 - beta1 ** (i + 1))
        v_hat = v / (1 - beta2 ** (i + 1))
        
        x = x - learning_rate * m_hat / (epsilon + np.sqrt(v_hat))
    
    return x, func(x), i + 1


def gradient_descent_2d(
    func: Callable[[float, float], float],
    grad: Callable[[float, float], Tuple[float, float]],
    x0: float,
    y0: float,
    learning_rate: float = 0.01,
    tolerance: float = 1e-8,
    max_iterations: int = 1000
) -> Tuple[float, float, float, int]:
    """
    2D 梯度下降法
    
    參數:
        func: 目標函數 f(x, y)
        grad: 梯度函數 (∂f/∂x, ∂f/∂y)
        x0, y0: 初始點
        learning_rate: 學習率
        tolerance: 容差
        max_iterations: 最大迭代次數
    
    返回:
        (最佳x, 最佳y, 最小值, 迭代次數)
    """
    x, y = x0, y0
    
    for i in range(max_iterations):
        grad_x, grad_y = grad(x, y)
        
        grad_magnitude = np.sqrt(grad_x ** 2 + grad_y ** 2)
        
        if grad_magnitude < tolerance:
            break
        
        x = x - learning_rate * grad_x
        y = y - learning_rate * grad_y
    
    return x, y, func(x, y), i + 1


def gradient_descent_backtracking(
    func: Callable[[float], float],
    deriv: Callable[[float], float],
    x0: float,
    learning_rate: float = 1.0,
    alpha: float = 0.3,
    beta: float = 0.5,
    max_iterations: int = 1000
) -> Tuple[float, float, int]:
    """
    回溯直線搜尋梯度下降法
    
    參數:
        func: 目標函數
        deriv: 導函數
        x0: 初始點
        learning_rate: 初始學習率
        alpha: 回溯參數
        beta: 衰減因子
        max_iterations: 最大迭代次數
    
    返回:
        (最佳點, 最小值, 迭代次數)
    """
    x = x0
    lr = learning_rate
    
    for i in range(max_iterations):
        gradient = deriv(x)
        
        while func(x - lr * gradient) > func(x) - alpha * lr * gradient ** 2:
            lr *= beta
        
        x = x - lr * gradient
    
    return x, func(x), i + 1


class GradientDescentSolver:
    """梯度下降求解器"""
    
    def __init__(self, objective: Callable, gradient: Callable):
        self.objective = objective
        self.gradient = gradient
    
    def solve(
        self,
        initial: List[float],
        method: str = "basic",
        learning_rate: float = 0.01,
        max_iterations: int = 1000
    ) -> Dict[str, Any]:
        """
        求解
        
        參數:
            initial: 初始點
            method: 方法 ("basic", "momentum", "adam")
            learning_rate: 學習率
            max_iterations: 最大迭代次數
        
        返回:
            結果字典
        """
        x = initial[0]
        
        if method == "basic":
            return gradient_descent_basic(
                self.objective, self.gradient, x, learning_rate, max_iterations=max_iterations
            )
        elif method == "momentum":
            return gradient_descent_momentum(
                self.objective, self.gradient, x, learning_rate, max_iterations=max_iterations
            )
        elif method == "adam":
            return gradient_descent_adam(
                self.objective, self.gradient, x, learning_rate, max_iterations=max_iterations
            )
        
        return gradient_descent_basic(
            self.objective, self.gradient, x, learning_rate, max_iterations=max_iterations
        )


def demo_gradient_descent():
    """演示梯度下降"""
    print("=== 梯度下降法範例演示 ===")
    print()
    
    print("1. 基本梯度下降:")
    f = lambda x: x ** 2 + 2 * x + 1
    df = lambda x: 2 * x + 2
    x, value, iterations = gradient_descent_basic(f, df, x0=10.0, learning_rate=0.1)
    print(f"   最小化 f(x) = x^2 + 2x + 1")
    print(f"   最小點: x = {x:.4f}, 值 = {value:.4f}")
    print(f"   迭代次數: {iterations}")
    print()
    
    print("2. 動量梯度下降:")
    x, value, iterations = gradient_descent_momentum(f, df, x0=10.0, learning_rate=0.1)
    print(f"   最小點: x = {x:.4f}, 值 = {value:.4f}")
    print(f"   迭代次數: {iterations}")
    print()
    
    print("3. Adam 方法:")
    x, value, iterations = gradient_descent_adam(f, df, x0=10.0, learning_rate=0.1)
    print(f"   最小點: x = {x:.4f}, 值 = {value:.4f}")
    print(f"   迭代次數: {iterations}")
    print()
    
    print("4. 2D 梯度下降:")
    f2d = lambda x, y: x ** 2 + y ** 2
    grad2d = lambda x, y: (2 * x, 2 * y)
    x, y, value, iterations = gradient_descent_2d(f2d, grad2d, 5.0, 5.0, learning_rate=0.1)
    print(f"   最小化 f(x,y) = x^2 + y^2")
    print(f"   最小點: ({x:.4f}, {y:.4f}), 值 = {value:.4f}")
    print(f"   迭代次數: {iterations}")
    print()
    
    print("5. 回溯直線搜尋:")
    x, value, iterations = gradient_descent_backtracking(f, df, x0=10.0)
    print(f"   最小點: x = {x:.4f}, 值 = {value:.4f}")


if __name__ == "__main__":
    demo_gradient_descent()
