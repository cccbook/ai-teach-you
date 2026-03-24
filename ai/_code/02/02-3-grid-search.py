#!/usr/bin/env python3
"""
網格搜尋演算法
暴力搜尋找最低點
"""

def grid_search(func, ranges, step=0.1):
    """
    網格搜尋
    
    參數:
        func: 目標函數
        ranges: 每個維度的搜尋範圍 [(min, max), ...]
        step: 搜尋步長
    
    返回:
        (最佳點, 最小值)
    """
    best_x = None
    best_value = float('inf')
    
    grids = []
    for min_val, max_val in ranges:
        grid = []
        x = min_val
        while x <= max_val:
            grid.append(x)
            x += step
        grids.append(grid)
    
    import itertools
    for values in itertools.product(*grids):
        value = func(*values)
        if value < best_value:
            best_value = value
            best_x = values
    
    return best_x, best_value

def f1(x):
    """一維函數"""
    return (x - 3) ** 2

def f2(x, y):
    """二維函數"""
    return (x - 1) ** 2 + (y - 2) ** 2

def f3(x, y):
    """有區域極小的函數"""
    return (x ** 2 - 4) ** 2 + (y ** 2 - 4) ** 2

if __name__ == "__main__":
    print("=== 網格搜尋演算法 ===\n")
    
    print("--- 一維範例: f(x) = (x-3)² ---")
    best_x, best_value = grid_search(f1, [(-5, 10)], step=0.5)
    print(f"網格搜尋: x = {best_x[0]:.1f}, f(x) = {best_value:.1f}")
    print(f"理論最優: x = 3, f(x) = 0")
    
    print("\n--- 二維範例: f(x,y) = (x-1)² + (y-2)² ---")
    best_x, best_value = grid_search(f2, [(-5, 5), (-5, 5)], step=1.0)
    print(f"網格搜尋: x = {best_x[0]}, y = {best_x[1]}, f(x,y) = {best_value}")
    print(f"理論最優: x = 1, y = 2, f(x,y) = 0")
    
    print("\n--- 多區域極小範例 ---")
    best_x, best_value = grid_search(f3, [(-3, 3), (-3, 3)], step=0.5)
    print(f"網格搜尋: x = {best_x[0]:.1f}, y = {best_x[1]:.1f}, f(x,y) = {best_value:.1f}")
