"""
線性搜尋範例 (Linear Search)
===========================
展示線性搜尋（Linear Search）的基本實作方式。
線性搜尋是最簡單的搜尋演算法，逐一檢查每個元素直到找到目標。
"""

from typing import List, Any, Tuple, Callable
import time


def linear_search(arr: List[Any], target: Any) -> int:
    """
    基本線性搜尋
    
    參數:
        arr: 待搜尋陣列
        target: 目標值
    
    返回:
        目標的索引，若不存在則返回 -1
    """
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1


def linear_search_sorted(arr: List[Any], target: Any) -> int:
    """
    對已排序陣列的線性搜尋（可提前終止）
    
    參數:
        arr: 已排序陣列
        target: 目標值
    
    返回:
        目標的索引，若不存在則返回 -1
    """
    for i in range(len(arr)):
        if arr[i] == target:
            return i
        if arr[i] > target:
            break
    return -1


def linear_search_count_comparisons(arr: List[Any], target: Any) -> Tuple[int, int]:
    """
    線性搜尋並計算比較次數
    
    參數:
        arr: 待搜尋陣列
        target: 目標值
    
    返回:
        (索引, 比較次數)
    """
    comparisons = 0
    
    for i in range(len(arr)):
        comparisons += 1
        if arr[i] == target:
            return i, comparisons
    
    return -1, comparisons


def linear_search_recursive(arr: List[Any], target: Any, index: int = 0) -> int:
    """
    遞迴線性搜尋
    
    參數:
        arr: 待搜尋陣列
        target: 目標值
        index: 目前索引
    
    返回:
        索引或 -1
    """
    if index >= len(arr):
        return -1
    
    if arr[index] == target:
        return index
    
    return linear_search_recursive(arr, target, index + 1)


def linear_search_sentinel(arr: List[Any], target: Any) -> int:
    """
    哨兵線性搜尋
    
    參數:
        arr: 待搜尋陣列
        target: 目標值
    
    返回:
        索引或 -1
    """
    last = arr[-1]
    arr[-1] = target
    
    i = 0
    while arr[i] != target:
        i += 1
    
    arr[-1] = last
    
    if i < len(arr) - 1 or last == target:
        return i
    
    return -1


def linear_search_with_predicate(
    arr: List[Any],
    predicate: Callable[[Any], bool]
) -> int:
    """
    使用述詞的線性搜尋
    
    參數:
        arr: 待搜尋陣列
        predicate: 條件函數
    
    返回:
        滿足條件的第一個元素的索引
    """
    for i, item in enumerate(arr):
        if predicate(item):
            return i
    return -1


def linear_search_find_all(arr: List[Any], target: Any) -> List[int]:
    """
    找出所有匹配的元素
    
    參數:
        arr: 待搜尋陣列
        target: 目標值
    
    返回:
        所有匹配元素的索引列表
    """
    indices = []
    for i, item in enumerate(arr):
        if item == target:
            indices.append(i)
    return indices


def linear_search_binary_search_hybrid(arr: List[Any], target: Any) -> int:
    """
    混合搜尋：小陣列用線性搜尋，大陣列用二分搜尋
    
    參數:
        arr: 待搜尋陣列
        target: 目標值
    
    返回:
        索引或 -1
    """
    threshold = 10
    
    if len(arr) < threshold:
        return linear_search(arr, target)
    
    left, right = 0, len(arr) - 1
    
    if target < arr[left] or target > arr[right]:
        return -1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
        
        if right - left + 1 < threshold:
            return linear_search(arr[left:right + 1], target)
    
    return -1


def linear_search_indexed(
    arr: List[Any],
    target: Any,
    index: Callable[[Any], int]
) -> int:
    """
    索引輔助的線性搜尋
    
    參數:
        arr: 待搜尋陣列
        target: 目標值
        index: 索引函數
    
    返回:
        索引或 -1
    """
    for i, item in enumerate(arr):
        if index(item) == index(target):
            return i
    return -1


def linear_search_best_worst(arr: List[Any], target: Any) -> dict:
    """
    分析最好和最差情況
    
    參數:
        arr: 待搜尋陣列
        target: 目標值
    
    返回:
        分析結果
    """
    best_case = 1 if arr[0] == target else None
    worst_case = len(arr) if arr[-1] == target else None
    average_case = (len(arr) + 1) // 2
    
    index = linear_search(arr, target)
    
    return {
        "found": index != -1,
        "index": index,
        "best_case": best_case,
        "worst_case": worst_case,
        "average_case": average_case
    }


def linear_search_2d(matrix: List[List[Any]], target: Any) -> Tuple[int, int]:
    """
    2D 矩陣搜尋（每行已排序）
    
    參數:
        matrix: 2D 矩陣
        target: 目標值
    
    返回:
        (row, col) 或 (-1, -1)
    """
    for i, row in enumerate(matrix):
        for j, item in enumerate(row):
            if item == target:
                return (i, j)
    return (-1, -1)


def linear_search_2d_sorted(matrix: List[List[Any]], target: Any) -> Tuple[int, int]:
    """
    2D 已排序矩陣搜尋
    
    參數:
        matrix: 已排序 2D 矩陣
        target: 目標值
    
    返回:
        (row, col) 或 (-1, -1)
    """
    if not matrix:
        return (-1, -1)
    
    rows = len(matrix)
    cols = len(matrix[0])
    
    row = 0
    col = cols - 1
    
    while row < rows and col >= 0:
        current = matrix[row][col]
        
        if current == target:
            return (row, col)
        elif current > target:
            col -= 1
        else:
            row += 1
    
    return (-1, -1)


class LinearSearchIterator:
    """線性搜尋迭代器"""
    
    def __init__(self, arr: List[Any]):
        self.arr = arr
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self) -> Any:
        if self.index >= len(self.arr):
            raise StopIteration
        
        result = self.arr[self.index]
        self.index += 1
        return result
    
    def find(self, target: Any) -> int:
        """搜尋目標"""
        for i, item in enumerate(self.arr):
            if item == target:
                return i
        return -1


def demo_linear_search():
    """演示線性搜尋"""
    print("=== 線性搜尋範例演示 ===")
    print()
    
    print("1. 基本線性搜尋:")
    arr = [5, 2, 8, 1, 9, 3, 7, 4, 6]
    idx = linear_search(arr, 7)
    print(f"   在 {arr} 中搜尋 7: 索引 {idx}")
    print()
    
    print("2. 已排序陣列搜尋:")
    arr_sorted = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    idx = linear_search_sorted(arr_sorted, 5)
    print(f"   在 {arr_sorted} 中搜尋 5: 索引 {idx}")
    print()
    
    print("3. 計算比較次數:")
    arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    idx, comps = linear_search_count_comparisons(arr, 7)
    print(f"   搜尋 7: 索引 {idx}, 比較次數 {comps}")
    print()
    
    print("4. 找出所有匹配:")
    arr = [1, 2, 3, 2, 4, 2, 5]
    indices = linear_search_find_all(arr, 2)
    print(f"   在 {arr} 中找 2: 索引 {indices}")
    print()
    
    print("5. 哨兵搜尋:")
    arr = [5, 2, 8, 1, 9, 3, 7]
    idx = linear_search_sentinel(arr, 9)
    print(f"   搜尋 9: 索引 {idx}")
    print()
    
    print("6. 2D 已排序矩陣搜尋:")
    matrix = [[1, 4, 7, 11], [2, 5, 8, 12], [3, 6, 9, 16], [10, 13, 14, 17]]
    pos = linear_search_2d_sorted(matrix, 5)
    print(f"   搜尋 5: 位置 {pos}")


if __name__ == "__main__":
    demo_linear_search()
