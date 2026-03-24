"""
函數式程式設計基礎範例 (Functional Programming Basics)
=====================================================
展示函數式程式設計的基本概念與技巧。
函數式程式設計是一種強調使用函數和不可變資料結構的程式設計範式。
"""

from typing import Callable, List, Any, Dict, Tuple, Optional
import functools
import itertools


def map_example(arr: List[int]) -> List[int]:
    """
    map - 對每個元素應用函數
    
    參數:
        arr: 輸入列表
    
    返回:
        轉換後的列表
    """
    return list(map(lambda x: x * 2, arr))


def filter_example(arr: List[int]) -> List[int]:
    """
    filter - 篩選滿足條件的元素
    
    參數:
        arr: 輸入列表
    
    返回:
        篩選後的列表
    """
    return list(filter(lambda x: x % 2 == 0, arr))


def reduce_example(arr: List[int]) -> int:
    """
    reduce - 將元素依序合併為單一值
    
    參數:
        arr: 輸入列表
    
    返回:
        合併後的結果
    """
    return functools.reduce(lambda a, b: a + b, arr, 0)


def compose_functions(f: Callable, g: Callable) -> Callable:
    """
    組合兩個函數：f ∘ g
    
    參數:
        f, g: 要組合的函數
    
    返回:
        組合後的函數
    """
    return lambda x: f(g(x))


def pipe_functions(*functions: Callable) -> Callable:
    """
    管道函數：將函數串接在一起
    
    參數:
        functions: 要串接的函數
    
    返回:
        組合後的函數
    """
    def pipeline(x):
        result = x
        for func in functions:
            result = func(result)
        return result
    return pipeline


def curry_function(f: Callable) -> Callable:
    """
    柯里化函數
    
    參數:
        f: 要柯里化的函數
    
    返回:
        柯里化後的函數
    """
    @functools.wraps(f)
    def curried(*args):
        if len(args) == f.__code__.co_argcount:
            return f(*args)
        return lambda *more: curried(*(args + more))
    return curried


def partial_function(f: Callable, *args, **kwargs) -> Callable:
    """
    部分應用函數
    
    參數:
        f: 要應用的函數
        args, kwargs: 預設參數
    
    返回:
        部分應用後的函數
    """
    return functools.partial(f, *args, **kwargs)


def higher_order_function_example() -> Dict[str, Callable]:
    """
    高階函數範例
    
    返回:
        包含高階函數的字典
    """
    
    def apply_twice(f: Callable, x: Any) -> Any:
        return f(f(x))
    
    def add_five(x: int) -> int:
        return x + 5
    
    def multiply_three(x: int) -> int:
        return x * 3
    
    return {
        "apply_twice_add": lambda x: apply_twice(add_five, x),
        "apply_twice_mult": lambda x: apply_twice(multiply_three, x),
    }


def functional_list_operations(arr: List[int]) -> Dict[str, List[int]]:
    """
    函數式列表操作
    
    參數:
        arr: 輸入列表
    
    返回:
        操作結果字典
    """
    return {
        "doubled": list(map(lambda x: x * 2, arr)),
        "evens": list(filter(lambda x: x % 2 == 0, arr)),
        "sorted": sorted(arr),
        "sorted_desc": sorted(arr, reverse=True),
        "sum": functools.reduce(lambda a, b: a + b, arr, 0),
        "product": functools.reduce(lambda a, b: a * b, arr, 1),
        "max": max(arr) if arr else None,
        "min": min(arr) if arr else None,
    }


def lazy_evaluation() -> Callable:
    """
    延遲評估範例
    
    返回:
        延遲評估的生成器
    """
    def lazy_map(func: Callable, iterable):
        for item in iterable:
            yield func(item)
    
    def lazy_filter(predicate: Callable, iterable):
        for item in iterable:
            if predicate(item):
                yield item
    
    return {
        "lazy_map": lazy_map,
        "lazy_filter": lazy_filter,
    }


def list_comprehension_with_conditions(arr: List[int]) -> Dict[str, List[int]]:
    """
    列表推導式（包含條件）
    
    參數:
        arr: 輸入列表
    
    返回:
        結果字典
    """
    return {
        "squares": [x ** 2 for x in arr],
        "even_squares": [x ** 2 for x in arr if x % 2 == 0],
        "add_ten": [x + 10 for x in arr],
        "nested": [[x * y for y in arr] for x in arr],
    }


def generator_expression(arr: List[int]) -> Any:
    """
    生成器表達式
    
    參數:
        arr: 輸入列表
    
    返回:
        生成器對象
    """
    return (x ** 2 for x in arr)


def accumulator_pattern(initial: Any) -> Dict[str, Callable]:
    """
    累加器模式
    
    參數:
        initial: 初始值
    
    返回:
        累加工具字典
    """
    class Accumulator:
        def __init__(self):
            self.value = initial
        
        def add(self, x):
            self.value += x
            return self
        
        def multiply(self, x):
            self.value *= x
            return self
        
        def get(self):
            return self.value
    
    acc = Accumulator()
    return {
        "add": lambda x: acc.add(x),
        "multiply": lambda x: acc.multiply(x),
        "get": lambda: acc.get(),
    }


def immutable_data_example() -> Dict[str, Any]:
    """
    不可變資料範例
    
    返回:
        不可變資料結構
    """
    frozen_set = frozenset([1, 2, 3])
    
    tuple_data = (1, 2, 3)
    
    def add_to_tuple(t: Tuple, x: Any) -> Tuple:
        return t + (x,)
    
    return {
        "frozen_set": frozen_set,
        "tuple": tuple_data,
        "tuple_extended": add_to_tuple(tuple_data, 4),
    }


def monad_example() -> Dict[str, Any]:
    """
    單子（Monad）模式範例
    
    返回:
        單子操作結果
    """
    
    class Maybe:
        def __init__(self, value: Any):
            self.value = value
        
        def bind(self, func: Callable) -> 'Maybe':
            if self.value is None:
                return Maybe(None)
            return Maybe(func(self.value))
        
        def __repr__(self):
            return f"Maybe({self.value})"
    
    def safe_divide(x: float, y: float) -> Maybe:
        if y == 0:
            return Maybe(None)
        return Maybe(x / y)
    
    result = Maybe(10).bind(lambda x: Maybe(x + 5)).bind(lambda x: safe_divide(x, 2))
    
    return {"result": result}


def recursion_as_functional() -> Dict[str, Any]:
    """
    函數式遞迴範例
    
    返回:
        遞迴函數結果
    """
    def factorial(n: int, acc: int = 1) -> int:
        if n <= 1:
            return acc
        return factorial(n - 1, n * acc)
    
    def fibonacci(n: int, a: int = 0, b: int = 1) -> int:
        if n == 0:
            return a
        return fibonacci(n - 1, b, a + b)
    
    return {
        "factorial_5": factorial(5),
        "fibonacci_10": fibonacci(10),
    }


def closure_example() -> Callable:
    """
    閉包範例
    
    返回:
        閉包函數
    """
    def make_adder(n: int) -> Callable:
        return lambda x: x + n
    
    add_five = make_adder(5)
    add_ten = make_adder(10)
    
    return add_five


def memoization_example() -> Callable:
    """
    記憶化範例
    
    返回:
        記憶化裝飾器
    """
    def memoize(f: Callable) -> Callable:
        cache = {}
        
        @functools.wraps(f)
        def wrapper(*args):
            if args not in cache:
                cache[args] = f(*args)
            return cache[args]
        
        wrapper.cache = cache
        return wrapper
    
    @memoize
    def fib(n: int) -> int:
        if n < 2:
            return n
        return fib(n - 1) + fib(n - 2)
    
    return fib


def demo_functional():
    """演示函數式程式設計"""
    print("=== 函數式程式設計基礎範例演示 ===")
    print()
    
    print("1. map/filter/reduce:")
    arr = [1, 2, 3, 4, 5]
    print(f"   原陣列: {arr}")
    print(f"   map (*2): {map_example(arr)}")
    print(f"   filter (偶數): {filter_example(arr)}")
    print(f"   reduce (加總): {reduce_example(arr)}")
    print()
    
    print("2. 函數組合:")
    f = lambda x: x + 1
    g = lambda x: x * 2
    composed = compose_functions(f, g)
    print(f"   f(x) = x+1, g(x) = x*2")
    print(f"   (f ∘ g)(5) = {composed(5)}")
    print()
    
    print("3. 柯里化:")
    def add(a, b, c):
        return a + b + c
    curried_add = curry_function(add)
    print(f"   add(1, 2, 3) = {add(1, 2, 3)}")
    print(f"   add(1)(2)(3) = {curried_add(1)(2)(3)}")
    print()
    
    print("4. 列表推導式:")
    arr = [1, 2, 3, 4, 5]
    result = list_comprehension_with_conditions(arr)
    print(f"   平方: {result['squares']}")
    print(f"   偶數平方: {result['even_squares']}")
    print()
    
    print("5. 閉包:")
    add_five = closure_example()
    print(f"   add_five(10) = {add_five(10)}")
    print()
    
    print("6. 記憶化:")
    fib = memoization_example()
    for i in range(10):
        fib(i)
    print(f"   fib(10) = {fib(10)}")
    print(f"   快取大小: {len(fib.cache)}")


if __name__ == "__main__":
    demo_functional()
