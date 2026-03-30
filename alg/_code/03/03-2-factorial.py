"""
階乘實作範例 (Factorial Implementation)
=======================================
展示階乘（Factorial）的各種實現方式，包括遞迴、迭代和優化版本。
"""

from typing import Callable, List, Dict
import math
import functools


def factorial_recursive(n: int) -> int:
    """
    遞迴計算階乘
    
    參數:
        n: 非負整數
    
    返回:
        n!
    """
    if n < 0:
        raise ValueError("階乘不能為負數")
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)


def factorial_iterative(n: int) -> int:
    """
    迭代計算階乘
    
    參數:
        n: 非負整數
    
    返回:
        n!
    """
    if n < 0:
        raise ValueError("階乘不能為負數")
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def factorial_reduce(n: int) -> int:
    """
    使用 reduce 計算階乘
    
    參數:
        n: 非負整數
    
    返回:
        n!
    """
    if n < 0:
        raise ValueError("階乘不能為負數")
    
    return functools.reduce(lambda a, b: a * b, range(1, n + 1), 1)


def factorial_math(n: int) -> int:
    """
    使用 math 模組計算階乘
    
    參數:
        n: 非負整數
    
    返回:
        n!
    """
    if n < 0:
        raise ValueError("階乘不能為負數")
    return math.factorial(n)


def factorial_memoized(n: int, cache: Dict[int, int] = None) -> int:
    """
    帶有記憶化（Memoization）的階乘計算
    
    參數:
        n: 非負整數
        cache: 快取字典
    
    返回:
        n!
    """
    if cache is None:
        cache = {}
    
    if n < 0:
        raise ValueError("階乘不能為負數")
    if n <= 1:
        return 1
    if n in cache:
        return cache[n]
    
    result = n * factorial_memoized(n - 1, cache)
    cache[n] = result
    return result


def factorial_tail_recursive(n: int, acc: int = 1) -> int:
    """
    尾遞迴計算階乘
    
    參數:
        n: 非負整數
        acc: 累加器
    
    返回:
        n!
    """
    if n < 0:
        raise ValueError("階乘不能為負數")
    if n == 0:
        return acc
    return factorial_tail_recursive(n - 1, n * acc)


def factorial_generator(n: int) -> int:
    """
    使用生成器計算階乘
    
    參數:
        n: 非負整數
    
    返回:
        n!
    """
    def _gen():
        result = 1
        for i in range(1, n + 1):
            result *= i
            yield result
    
    gen = _gen()
    for _ in gen:
        pass
    return gen.send(None)


def factorial_division_conquer(n: int) -> int:
    """
    分治法計算階乘
    
    參數:
        n: 非負整數
    
    返回:
        n!
    """
    if n <= 1:
        return 1
    
    mid = n // 2
    left = factorial_division_conquer(mid)
    right = factorial_division_conquer(n - mid)
    
    return left * right


def factorial_logarithmic(n: int) -> int:
    """
    對數時間複雜度的階乘（利用質因數分解）
    
    參數:
        n: 非負整數
    
    返回:
        n! 的近似值（實際精確值）
    """
    if n <= 1:
        return 1
    
    def prime_factors(n: int) -> Dict[int, int]:
        factors = {}
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors[d] = factors.get(d, 0) + 1
                n //= d
            d += 1
        if n > 1:
            factors[n] = factors.get(n, 0) + 1
        return factors
    
    prime_counts = {}
    for i in range(2, n + 1):
        for prime, count in prime_factors(i).items():
            prime_counts[prime] = prime_counts.get(prime, 0) + count
    
    result = 1
    for prime, count in prime_counts.items():
        result *= prime ** count
    
    return result


def double_factorial(n: int) -> int:
    """
    雙階乘 n!!
    
    參數:
        n: 整數
    
    返回:
        n!!
    """
    if n < 0:
        raise ValueError("雙階乘不能為負數")
    if n <= 1:
        return 1
    
    result = 1
    for i in range(n, 0, -2):
        result *= i
    return result


def factorial_table(max_n: int = 20) -> Dict[int, int]:
    """
    建立階乘查詢表
    
    參數:
        max_n: 最大 n 值
    
    返回:
        查詢表字典
    """
    table = {0: 1, 1: 1}
    result = 1
    
    for i in range(2, max_n + 1):
        result *= i
        table[i] = result
    
    return table


def factorial_bigint(n: int) -> int:
    """
    使用大整數計算大數階乘
    
    參數:
        n: 非負整數
    
    返回:
        n! (Python 自動使用大整數)
    """
    if n < 0:
        raise ValueError("階乘不能為負數")
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def factorial_stirling_approximation(n: int) -> float:
    """
    使用斯特林公式近似計算階乘
    
    參數:
        n: 正整數
    
    返回:
        n! 的近似值
    """
    if n <= 0:
        return 1
    
    return math.sqrt(2 * math.pi * n) * (n / math.e) ** n


class FactorialCalculator:
    """階乘計算器類別"""
    
    def __init__(self, method: str = "iterative", use_cache: bool = True):
        self.method = method
        self.use_cache = use_cache
        self.cache: Dict[int, int] = {}
        self.call_count = 0
    
    def calculate(self, n: int) -> int:
        """計算 n!"""
        self.call_count += 1
        
        if self.use_cache and n in self.cache:
            return self.cache[n]
        
        if self.method == "recursive":
            result = factorial_recursive(n)
        elif self.method == "iterative":
            result = factorial_iterative(n)
        elif self.method == "tail":
            result = factorial_tail_recursive(n)
        else:
            result = factorial_iterative(n)
        
        if self.use_cache:
            self.cache[n] = result
        
        return result
    
    def clear_cache(self) -> None:
        """清除快取"""
        self.cache.clear()
    
    def get_stats(self) -> Dict:
        """取得統計資訊"""
        return {
            "cache_size": len(self.cache),
            "call_count": self.call_count
        }


def benchmark_factorial(n: int, methods: List[Callable[[int], int]]) -> Dict[str, float]:
    """
    基準測試不同階乘計算方法
    
    參數:
        n: 要計算的數字
        methods: 方法列表
    
    返回:
        效能比較結果
    """
    import time
    
    results = {}
    
    for method in methods:
        start = time.perf_counter()
        result = method(n)
        elapsed = time.perf_counter() - start
        results[method.__name__] = {
            "result": result,
            "time": elapsed
        }
    
    return results


def demo_factorial():
    """演示階乘計算"""
    print("=== 階乘實作範例演示 ===")
    print()
    
    print("1. 遞迴:")
    print(f"   5! = {factorial_recursive(5)}")
    print()
    
    print("2. 迭代:")
    print(f"   10! = {factorial_iterative(10)}")
    print()
    
    print("3. 記憶化:")
    cache = {}
    print(f"   10! = {factorial_memoized(10, cache)}")
    print(f"   快取大小: {len(cache)}")
    print()
    
    print("4. 尾遞迴:")
    print(f"   10! = {factorial_tail_recursive(10)}")
    print()
    
    print("5. 雙階乘:")
    print(f"   6!! = {double_factorial(6)}")
    print()
    
    print("6. 斯特林近似:")
    print(f"   10! 近似 = {factorial_stirling_approximation(10):.2f}")
    print(f"   10! 精確 = {factorial_iterative(10)}")
    print()
    
    print("7. 查詢表:")
    table = factorial_table(10)
    print(f"   查詢表: {table}")
    print()
    
    print("8. 計算器類別:")
    calc = FactorialCalculator(method="iterative", use_cache=True)
    for i in range(1, 11):
        calc.calculate(i)
    print(f"   統計: {calc.get_stats()}")


if __name__ == "__main__":
    demo_factorial()
