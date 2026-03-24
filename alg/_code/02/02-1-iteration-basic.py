"""
基本迭代範例 (Basic Iteration)
===============================
展示各種基本迭代技術和模式。
迭代是重複執行某個操作的過程，是程式設計中最基本的控制結構之一。
"""

from typing import List, Any, Callable, Iterator, Iterable
import itertools
import math


def iterate_for(arr: List[Any]) -> None:
    """
    使用 for 迴圈迭代
    
    參數:
        arr: 要迭代的列表
    """
    for i, item in enumerate(arr):
        print(f"索引 {i}: {item}")


def iterate_while(condition: Callable[[], bool], action: Callable[[], None]) -> None:
    """
    使用 while 迴圈迭代
    
    參數:
        condition: 條件函數
        action: 要執行的動作
    """
    count = 0
    while condition() and count < 100:
        action()
        count += 1


def iterate_range(start: int, stop: int, step: int = 1) -> List[int]:
    """
    使用 range 迭代
    
    參數:
        start: 起始值
        stop: 結束值
        step: 步長
    
    返回:
        產生的數字列表
    """
    return list(range(start, stop, step))


def iterate_n_times(n: int, action: Callable[[int], Any]) -> List[Any]:
    """
    執行 n 次迭代
    
    參數:
        n: 迭代次數
        action: 每次執行的動作
    
    返回:
        結果列表
    """
    return [action(i) for i in range(n)]


def iterate_nested(rows: int, cols: int) -> List[List[int]]:
    """
    巢狀迭代
    
    參數:
        rows: 行數
        cols: 列數
    
    返回:
        2D 矩陣
    """
    return [[i * cols + j for j in range(cols)] for i in range(rows)]


def iterate_index_based(arr: List[Any], indices: List[int]) -> List[Any]:
    """
    基於索引的迭代
    
    參數:
        arr: 陣列
        indices: 索引列表
    
    返回:
        對應的元素列表
    """
    return [arr[i] for i in indices if 0 <= i < len(arr)]


def iterate_with_condition(arr: List[Any], predicate: Callable[[Any], bool]) -> List[Any]:
    """
    带條件的迭代
    
    參數:
        arr: 陣列
        predicate: 條件函數
    
    返回:
        滿足條件的元素列表
    """
    return [item for item in arr if predicate(item)]


def iterate_accumulate(arr: List[float], init: float = 0, op: str = "add") -> List[float]:
    """
    累加迭代
    
    參數:
        arr: 陣列
        init: 初始值
        op: 操作類型 ("add", "mul", "max", "min")
    
    返回:
        累加結果列表
    """
    result = [init]
    
    if op == "add":
        for item in arr:
            result.append(result[-1] + item)
    elif op == "mul":
        for item in arr:
            result.append(result[-1] * item)
    elif op == "max":
        for item in arr:
            result.append(max(result[-1], item))
    elif op == "min":
        for item in arr:
            result.append(min(result[-1], item))
    
    return result[1:]


def iterate_pairwise(arr: List[Any]) -> Iterator[Tuple[Any, Any]]:
    """
    成對迭代
    
    參數:
        arr: 陣列
    
    返回:
        相鄰元素對的迭代器
    """
    for i in range(len(arr) - 1):
        yield (arr[i], arr[i + 1])


def iterate_window(arr: List[Any], window_size: int) -> Iterator[List[Any]]:
    """
    滑動視窗迭代
    
    參數:
        arr: 陣列
        window_size: 視窗大小
    
    返回:
        每個視窗的迭代器
    """
    for i in range(len(arr) - window_size + 1):
        yield arr[i:i + window_size]


def iterate_cyclic(arr: List[Any], n: int) -> Iterator[Any]:
    """
    循環迭代
    
    參數:
        arr: 陣列
        n: 迭代次數
    
    返回:
        循環元素的迭代器
    """
    for i in range(n):
        yield arr[i % len(arr)]


def iterate_combine(arr1: List[Any], arr2: List[Any]) -> Iterator[Tuple[Any, Any]]:
    """
    合併兩個列表迭代
    
    參數:
        arr1: 第一個列表
        arr2: 第二個列表
    
    返回:
        合併後的元素對迭代器
    """
    for a, b in zip(arr1, arr2):
        yield (a, b)


def iterate_zip_longest(arr1: List[Any], arr2: List[Any], fillvalue: Any = None) -> Iterator[Tuple[Any, Any]]:
    """
    使用 fillvalue 合併迭代
    
    參數:
        arr1: 第一個列表
        arr2: 第二個列表
        fillvalue: 填充值
    
    返回:
        合併後的元素對迭代器
    """
    for a, b in itertools.zip_longest(arr1, arr2, fillvalue=fillvalue):
        yield (a, b)


class IteratorExhaust:
    """迭代器耗盡示例"""
    
    @staticmethod
    def take(iterator: Iterator, n: int) -> List[Any]:
        """
        從迭代器中取 n 個元素
        
        參數:
            iterator: 迭代器
            n: 數量
        
        返回:
            元素列表
        """
        return [next(iterator) for _ in range(n)]
    
    @staticmethod
    def skip(iterator: Iterator, n: int) -> None:
        """
        跳過迭代器的前 n 個元素
        
        參數:
            iterator: 迭代器
            n: 數量
        """
        for _ in range(n):
            next(iterator, None)
    
    @staticmethod
    def chain(iterators: List[Iterator]) -> Iterator[Any]:
        """
        鏈結多個迭代器
        
        參數:
            iterators: 迭代器列表
        
        返回:
            鏈結後的迭代器
        """
        return itertools.chain(*iterators)


def iterate_sieve_of_eratosthenes(limit: int) -> List[int]:
    """
    埃拉托斯特尼篩法 - 使用迭代找出質數
    
    參數:
        limit: 上限
    
    返回:
        質數列表
    """
    if limit < 2:
        return []
    
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    
    for i in range(2, int(math.sqrt(limit)) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False
    
    return [i for i in range(2, limit + 1) is_prime[i]]


class FibonacciIterator:
    """費波那契數列迭代器"""
    
    def __init__(self, max_value: int = None):
        self.max_value = max_value
        self.current = 0
        self.next = 1
    
    def __iter__(self):
        return self
    
    def __next__(self) -> int:
        if self.max_value is not None and self.current > self.max_value:
            raise StopIteration
        
        result = self.current
        self.current, self.next = self.next, self.current + self.next
        return result


class PrimeIterator:
    """質數迭代器"""
    
    def __init__(self):
        self.current = 2
    
    def __iter__(self):
        return self
    
    def __next__(self) -> int:
        while True:
            result = self.current
            self.current += 1
            
            if self._is_prime(result):
                return result
    
    def _is_prime(self, n: int) -> bool:
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        
        return True


def iterate_fibonacci_generator(n: int) -> Iterator[int]:
    """
    使用生成器迭代費波那契數列
    
    參數:
        n: 產生數量
    
    返回:
        費波那契數的迭代器
    """
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


def iterate_custom_generator(start: int, stop: int) -> Iterator[int]:
    """
    自定義生成器迭代
    
    參數:
        start: 起始值
        stop: 結束值
    
    返回:
        數字的迭代器
    """
    current = start
    while current < stop:
        yield current
        current += 1


def demo_basic_iteration():
    """演示基本迭代"""
    print("=== 基本迭代範例演示 ===")
    print()
    
    print("1. for 迴圈迭代:")
    iterate_for(["Apple", "Banana", "Orange"])
    print()
    
    print("2. range 迭代:")
    print(f"   range(0, 10, 2): {iterate_range(0, 10, 2)}")
    print()
    
    print("3. 巢狀迭代:")
    matrix = iterate_nested(3, 4)
    print(f"   3x4 矩陣: {matrix}")
    print()
    
    print("4. 成對迭代:")
    arr = [1, 2, 3, 4, 5]
    pairs = list(iterate_pairwise(arr))
    print(f"   {arr} 的相鄰對: {pairs}")
    print()
    
    print("5. 滑動視窗迭代:")
    windows = list(iterate_window(arr, 3))
    print(f"   {arr} 的3元素視窗: {windows}")
    print()
    
    print("6. 累加迭代:")
    print(f"   累加: {iterate_accumulate([1, 2, 3, 4, 5])}")
    print(f"   累乘: {iterate_accumulate([1, 2, 3, 4, 5], init=1, op='mul')}")
    print()
    
    print("7. 費波那契迭代器:")
    fibs = list(FibonacciIterator(max_value=100))
    print(f"   100 以內的費波那契數: {fibs}")
    print()
    
    print("8. 合併迭代:")
    arr1 = [1, 2, 3]
    arr2 = ['a', 'b', 'c']
    combined = list(iterate_combine(arr1, arr2))
    print(f"   合併 {arr1} 和 {arr2}: {combined}")


if __name__ == "__main__":
    demo_basic_iteration()
