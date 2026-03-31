"""
費波那契數列實作範例 (Fibonacci Implementation)
===============================================
展示費波那契數列的各種實現方式，包括純遞迴、迭代、記憶化等優化方法。
"""

from typing import List, Dict, Callable, Tuple
import functools
import time


def fibonacci_recursive(n: int) -> int:
    """
    純遞迴計算費波那契數
    
    參數:
        n: 索引（從 0 開始）
    
    返回:
        F(n)
    """
    if n < 0:
        raise ValueError("索引不能為負數")
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def fibonacci_iterative(n: int) -> int:
    """
    迭代計算費波那契數
    
    參數:
        n: 索引
    
    返回:
        F(n)
    """
    if n < 0:
        raise ValueError("索引不能為負數")
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def fibonacci_matrix(n: int) -> int:
    """
    使用矩陣乘法計算費波那契數（對數時間）
    
    參數:
        n: 索引
    
    返回:
        F(n)
    """
    if n < 0:
        raise ValueError("索引不能為負數")
    if n <= 1:
        return n
    
    def matrix_multiply(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
        return [
            [A[0][0] * B[0][0] + A[0][1] * B[1][0],
             A[0][0] * B[0][1] + A[0][1] * B[1][1]],
            [A[1][0] * B[0][0] + A[1][1] * B[1][0],
             A[1][0] * B[0][1] + A[1][1] * B[1][1]]
        ]
    
    def matrix_power(M: List[List[int]], power: int) -> List[List[int]]:
        if power == 1:
            return M
        if power % 2 == 0:
            half = matrix_power(M, power // 2)
            return matrix_multiply(half, half)
        else:
            return matrix_multiply(M, matrix_power(M, power - 1))
    
    result_matrix = matrix_power([[1, 1], [1, 0]], n)
    return result_matrix[0][1]


def fibonacci_memoized(n: int, cache: Dict[int, int] = None) -> int:
    """
    帶有記憶化的費波那契數計算
    
    參數:
        n: 索引
        cache: 快取字典
    
    返回:
        F(n)
    """
    if cache is None:
        cache = {}
    
    if n < 0:
        raise ValueError("索引不能為負數")
    if n <= 1:
        return n
    if n in cache:
        return cache[n]
    
    result = fibonacci_memoized(n - 1, cache) + fibonacci_memoized(n - 2, cache)
    cache[n] = result
    return result


def fibonacci_lru_cache(n: int) -> int:
    """
    使用 LRU 快取裝飾器
    
    參數:
        n: 索引
    
    返回:
        F(n)
    """
    @functools.lru_cache(maxsize=None)
    def fib(n: int) -> int:
        if n <= 1:
            return n
        return fib(n - 1) + fib(n - 2)
    
    return fib(n)


def fibonacci_tail_recursive(n: int, a: int = 0, b: int = 1) -> int:
    """
    尾遞迴計算費波那契數
    
    參數:
        n: 剩餘迭代次數
        a: 第一個值
        b: 第二個值
    
    返回:
        F(n)
    """
    if n < 0:
        raise ValueError("索引不能為負數")
    if n == 0:
        return a
    return fibonacci_tail_recursive(n - 1, b, a + b)


def fibonacci_generator(n: int) -> List[int]:
    """
    使用生成器產生費波那契數列
    
    參數:
        n: 要產生的數量
    
    返回:
        前 n 個費波那契數的列表
    """
    def _gen():
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b
    
    gen = _gen()
    return [next(gen) for _ in range(n)]


def fibonacci_two_term_recurrence(n: int, k: int = 2) -> int:
    """
    廣義費波那契數（k 階遞迴關係）
    F(n) = F(n-1) + F(n-2) + ... + F(n-k)
    
    參數:
        n: 索引
        k: 階數
    
    返回:
        F(n)
    """
    if n < 0:
        raise ValueError("索引不能為負數")
    if n < k:
        return 1
    
    dp = [0] * (n + 1)
    dp[0] = 1
    for i in range(1, min(k, n + 1)):
        dp[i] = dp[i - 1] + dp[i - 1]
    
    for i in range(k, n + 1):
        dp[i] = sum(dp[i - j] for j in range(1, k + 1))
    
    return dp[n]


def fibonacci_closed_form(n: int) -> float:
    """
    閉式公式（比內公式）計算費波那契數
    
    參數:
        n: 索引
    
    返回:
        F(n) 的近似值
    """
    import math
    
    if n < 0:
        raise ValueError("索引不能為負數")
    if n <= 1:
        return n
    
    phi = (1 + math.sqrt(5)) / 2
    psi = (1 - math.sqrt(5)) / 2
    
    return int((phi ** n - psi ** n) / math.sqrt(5))


def fibonacci_table(max_n: int) -> List[int]:
    """
    建立費波那契數查詢表
    
    參數:
        max_n: 最大索引
    
    返回:
        查詢表列表
    """
    table = [0] * (max_n + 1)
    
    for i in range(max_n + 1):
        if i <= 1:
            table[i] = i
        else:
            table[i] = table[i - 1] + table[i - 2]
    
    return table


def fibonacci_pisano_period(m: int) -> int:
    """
    計算費波那契數列模 m 的週期（Pisano 週期）
    
    參數:
        m: 模數
    
    返回:
        Pisano 週期長度
    """
    if m < 2:
        return 1
    
    prev, curr = 0, 1
    period = 0
    
    while True:
        prev, curr = curr, (prev + curr) % m
        period += 1
        
        if prev == 0 and curr == 1:
            return period


def fibonacci_reversed(n: int) -> int:
    """
    反向費波那契：給定 F(n)，求 n
    使用 Binet 公式的反函數
    
    參數:
        n: 費波那契數
    
    返回:
        索引
    """
    import math
    
    if n < 0:
        return -1
    if n <= 1:
        return n
    
    phi = (1 + math.sqrt(5)) / 2
    index = int(round(math.log(n * math.sqrt(5) + 0.5) / math.log(phi)))
    
    return index


class FibonacciCalculator:
    """費波那契數計算器"""
    
    def __init__(self, method: str = "iterative"):
        self.method = method
        self.cache: Dict[int, int] = {}
        self.call_count = 0
    
    def calculate(self, n: int) -> int:
        """計算 F(n)"""
        self.call_count += 1
        
        if n in self.cache:
            return self.cache[n]
        
        if self.method == "recursive":
            result = fibonacci_recursive(n)
        elif self.method == "iterative":
            result = fibonacci_iterative(n)
        elif self.method == "matrix":
            result = fibonacci_matrix(n)
        elif self.method == "tail":
            result = fibonacci_tail_recursive(n)
        elif self.method == "closed_form":
            result = int(fibonacci_closed_form(n))
        else:
            result = fibonacci_iterative(n)
        
        self.cache[n] = result
        return result
    
    def calculate_range(self, start: int, end: int) -> List[int]:
        """計算範圍內的費波那契數"""
        return [self.calculate(i) for i in range(start, end + 1)]
    
    def clear_cache(self) -> None:
        """清除快取"""
        self.cache.clear()
    
    def get_stats(self) -> Dict:
        """取得統計"""
        return {
            "cache_size": len(self.cache),
            "call_count": self.call_count
        }


def benchmark_fibonacci(n: int) -> Dict[str, float]:
    """
    基準測試不同方法的效能
    
    參數:
        n: 要計算的索引
    
    返回:
        效能比較結果
    """
    import time
    
    results = {}
    
    methods = [
        ("iterative", lambda: fibonacci_iterative(n)),
        ("matrix", lambda: fibonacci_matrix(n)),
        ("memoized", lambda: fibonacci_memoized(n)),
        ("lru_cache", lambda: fibonacci_lru_cache(n)),
        ("closed_form", lambda: fibonacci_closed_form(n)),
    ]
    
    for name, method in methods:
        start = time.perf_counter()
        result = method()
        elapsed = time.perf_counter() - start
        results[name] = {"result": result, "time": elapsed}
    
    return results


def demo_fibonacci():
    """演示費波那契數"""
    print("=== 費波那契數列實作範例演示 ===")
    print()
    
    print("1. 迭代:")
    print(f"   F(20) = {fibonacci_iterative(20)}")
    print()
    
    print("2. 矩陣乘法:")
    print(f"   F(20) = {fibonacci_matrix(20)}")
    print()
    
    print("3. 記憶化:")
    cache = {}
    print(f"   F(20) = {fibonacci_memoized(20, cache)}")
    print(f"   快取大小: {len(cache)}")
    print()
    
    print("4. 尾遞迴:")
    print(f"   F(20) = {fibonacci_tail_recursive(20)}")
    print()
    
    print("5. 閉式公式:")
    print(f"   F(20) = {int(fibonacci_closed_form(20))}")
    print()
    
    print("6. 產生器:")
    fibs = fibonacci_generator(10)
    print(f"   前10個費波那契數: {fibs}")
    print()
    
    print("7. Pisano 週期:")
    for m in [2, 3, 5, 7, 10]:
        print(f"   模 {m}: 週期 = {fibonacci_pisano_period(m)}")
    print()
    
    print("8. 基準測試:")
    results = benchmark_fibonacci(30)
    for name, data in results.items():
        print(f"   {name}: {data['time']:.6f}秒")


if __name__ == "__main__":
    demo_fibonacci()
