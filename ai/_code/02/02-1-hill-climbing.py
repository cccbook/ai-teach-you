#!/usr/bin/env python3
"""
爬山演算法：f(x) = (x-1)² 找最低點
最優化問題的基本方法
"""

import random
import math

def f(x):
    """目標函數: f(x) = (x-1)^2"""
    return (x - 1) ** 2

def hill_climbing(func, start, step_size=0.1, max_iterations=1000):
    """
    爬山演算法
    
    參數:
        func: 目標函數
        start: 起始點
        step_size: 每次移動的步長
        max_iterations: 最大迭代次數
    
    返回:
        (最佳位置, 最小值, 歷史記錄)
    """
    current = start
    current_value = func(current)
    history = [(current, current_value)]
    
    for i in range(max_iterations):
        neighbors = [
            current + step_size,
            current - step_size
        ]
        
        best_neighbor = current
        best_value = current_value
        
        for neighbor in neighbors:
            value = func(neighbor)
            if value < best_value:
                best_neighbor = neighbor
                best_value = value
        
        if best_value < current_value:
            current = best_neighbor
            current_value = best_value
            history.append((current, current_value))
        else:
            break
    
    return current, current_value, history

def hill_climbing_stochastic(func, start, step_size=0.5, max_iterations=1000):
    """
    隨機爬山演算法 - 加入隨機性避免局部極小值
    """
    current = start
    current_value = func(current)
    history = [(current, current_value)]
    
    for i in range(max_iterations):
        delta = random.uniform(-step_size, step_size)
        neighbor = current + delta
        neighbor_value = func(neighbor)
        
        if neighbor_value < current_value:
            current = neighbor
            current_value = neighbor_value
            history.append((current, current_value))
        
        step_size *= 0.995
    
    return current, current_value, history

def visualize_search(history):
    print("迭代過程:")
    print("-" * 50)
    for i, (x, y) in enumerate(history):
        print(f"迭代 {i:3d}: x = {x:8.4f}, f(x) = {y:8.4f}")

def example_2d():
    """二維例子: f(x,y) = (x-1)^2 + (y-2)^2"""
    def f2d(point):
        x, y = point
        return (x - 1) ** 2 + (y - 2) ** 2
    
    def hill_climb_2d(start, steps=0.1, iterations=1000):
        current = start
        current_value = f2d(current)
        
        for _ in range(iterations):
            best = current
            best_value = current_value
            
            for dx, dy in [(steps, 0), (-steps, 0), (0, steps), (0, -steps)]:
                neighbor = (current[0] + dx, current[1] + dy)
                value = f2d(neighbor)
                if value < best_value:
                    best = neighbor
                    best_value = value
            
            if best_value < current_value:
                current = best
                current_value = best_value
            else:
                break
        
        return current, current_value
    
    print("\n=== 二維爬山演算法 ===")
    print("目標: minimize f(x,y) = (x-1)² + (y-2)²")
    print("理論最優解: (1, 2), f = 0")
    print()
    
    start = (0.0, 0.0)
    result, value = hill_climb_2d(start)
    print(f"起始點: {start}")
    print(f"結果: x = {result[0]:.4f}, y = {result[1]:.4f}")
    print(f"最小值: {value:.4f}")

if __name__ == "__main__":
    print("=== 爬山演算法：f(x) = (x-1)² 找最低點 ===\n")
    print("目標函數: f(x) = (x-1)²")
    print("理論最優解: x = 1, f(x) = 0")
    print()
    
    print("--- 標準爬山演算法 ---")
    start = 0.0
    best_x, min_value, history = hill_climbing(f, start)
    visualize_search(history)
    print(f"\n最終結果: x = {best_x:.4f}, f(x) = {min_value:.4f}")
    
    print("\n" + "=" * 50)
    print("\n--- 隨機爬山演算法 (多次執行) ---")
    results = []
    for _ in range(5):
        start = random.uniform(-5, 5)
        best_x, min_value, _ = hill_climbing_stochastic(f, start, step_size=0.5)
        results.append((best_x, min_value))
        print(f"起始 {start:.2f} -> x = {best_x:.4f}, f(x) = {min_value:.4f}")
    
    best = min(results, key=lambda x: x[1])
    print(f"\n最佳結果: x = {best[0]:.4f}, f(x) = {best[1]:.4f}")
    
    example_2d()
