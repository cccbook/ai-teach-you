"""
二分搜尋範例 (Binary Search)
===========================
展示二分搜尋（Binary Search）的各種實作方式。
二分搜尋是一種高效的搜尋演算法，適用於已排序的資料，時間複雜度為 O(log n)。
"""

from typing import List, Any, Tuple, Callable
import bisect


def binary_search(arr: List[Any], target: Any) -> int:
    """
    基本二分搜尋
    
    參數:
        arr: 已排序陣列
        target: 目標值
    
    返回:
        目標的索引，若不存在則返回 -1
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1


def binary_search_leftmost(arr: List[Any], target: Any) -> int:
    """
    找最左邊的第一個匹配
    
    參數:
        arr: 已排序陣列
        target: 目標值
    
    返回:
        最左邊匹配的索引
    """
    left, right = 0, len(arr) - 1
    result = -1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            result = mid
            right = mid - 1
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return result


def binary_search_rightmost(arr: List[Any], target: Any) -> int:
    """
    找最右邊的最後一個匹配
    
    參數:
        arr: 已排序陣列
        target: 目標值
    
    返回:
        最右邊匹配的索引
    """
    left, right = 0, len(arr) - 1
    result = -1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            result = mid
            left = mid + 1
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return result


def binary_search_insert_position(arr: List[Any], target: Any) -> int:
    """
    找出插入位置
    
    參數:
        arr: 已排序陣列
        target: 目標值
    
    返回:
        應該插入的位置
    """
    left, right = 0, len(arr)
    
    while left < right:
        mid = (left + right) // 2
        
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    
    return left


def binary_search_recursive(arr: List[Any], target: Any, left: int = 0, right: int = None) -> int:
    """
    遞迴二分搜尋
    
    參數:
        arr: 已排序陣列
        target: 目標值
        left, right: 搜尋範圍
    
    返回:
        索引或 -1
    """
    if right is None:
        right = len(arr) - 1
    
    if left > right:
        return -1
    
    mid = (left + right) // 2
    
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)


def binary_search_count_occurrences(arr: List[Any], target: Any) -> int:
    """
    計算目標出現次數
    
    參數:
        arr: 已排序陣列
        target: 目標值
    
    返回:
        出現次數
    """
    left = binary_search_leftmost(arr, target)
    
    if left == -1:
        return 0
    
    right = binary_search_rightmost(arr, target)
    
    return right - left + 1


def binary_search_lower_bound(arr: List[Any], target: Any) -> int:
    """
    下界（第一個 >= target 的位置）
    
    參數:
        arr: 已排序陣列
        target: 目標值
    
    返回:
        下界索引
    """
    return bisect.bisect_left(arr, target)


def binary_search_upper_bound(arr: List[Any], target: Any) -> int:
    """
    上界（第一個 > target 的位置）
    
    參數:
        arr: 已排序陣列
        target: 目標值
    
    返回:
        上界索引
    """
    return bisect.bisect_right(arr, target)


def binary_search_range(arr: List[Any], target: Any) -> Tuple[int, int]:
    """
    找出目標的範圍
    
    參數:
        arr: 已排序陣列
        target: 目標值
    
    返回:
        (起始索引, 結束索引)
    """
    start = bisect.bisect_left(arr, target)
    end = bisect.bisect_right(arr, target)
    
    if start >= len(arr) or arr[start] != target:
        return (-1, -1)
    
    return (start, end - 1)


def binary_search_rotated(arr: List[Any], target: Any) -> int:
    """
    搜尋旋轉排序陣列
    
    參數:
        arr: 旋轉排序陣列
        target: 目標值
    
    返回:
        索引或 -1
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        
        if arr[left] <= arr[mid]:
            if arr[left] <= target < arr[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            if arr[mid] < target <= arr[right]:
                left = mid + 1
            else:
                right = mid - 1
    
    return -1


def binary_search_find_minimum(arr: List[Any]) -> int:
    """
    找出旋轉排序陣列中的最小值
    
    參數:
        arr: 旋轉排序陣列
    
    返回:
        最小值的索引
    """
    left, right = 0, len(arr) - 1
    
    while left < right:
        mid = (left + right) // 2
        
        if arr[mid] > arr[right]:
            left = mid + 1
        else:
            right = mid
    
    return left


def binary_search_2d(matrix: List[List[Any]], target: Any) -> Tuple[int, int]:
    """
    2D 已排序矩陣搜尋
    
    參數:
        matrix: 已排序 2D 矩陣
        target: 目標值
    
    返回:
        (row, col) 或 (-1, -1)
    """
    if not matrix or not matrix[0]:
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


def binary_search_floor(arr: List[Any], target: Any) -> Any:
    """
    找下界（最大 <= target）
    
    參數:
        arr: 已排序陣列
        target: 目標值
    
    返回:
        下界值，若不存在則返回 None
    """
    idx = bisect.bisect_right(arr, target) - 1
    
    return arr[idx] if idx >= 0 else None


def binary_search_ceiling(arr: List[Any], target: Any) -> Any:
    """
    找上界（最小 >= target）
    
    參數:
        arr: 已排序陣列
        target: 目標值
    
    返回:
        上界值，若不存在則返回 None
    """
    idx = bisect.bisect_left(arr, target)
    
    return arr[idx] if idx < len(arr) else None


def binary_search_exponential_search(arr: List[Any], target: Any) -> int:
    """
    指數搜尋
    
    參數:
        arr: 已排序陣列
        target: 目標值
    
    返回:
        索引或 -1
    """
    n = len(arr)
    
    if n == 0:
        return -1
    
    bound = 1
    while bound < n and arr[bound] < target:
        bound *= 2
    
    left = bound // 2
    right = min(bound, n - 1)
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1


def binary_search_interpolation(arr: List[Any], target: Any) -> int:
    """
    插值搜尋
    
    參數:
        arr: 已排序且均勻分布的陣列
        target: 目標值
    
    返回:
        索引或 -1
    """
    left, right = 0, len(arr) - 1
    
    while left <= right and target >= arr[left] and target <= arr[right]:
        if left == right:
            if arr[left] == target:
                return left
            return -1
        
        pos = left + ((target - arr[left]) * (right - left) // (arr[right] - arr[left]))
        
        if arr[pos] == target:
            return pos
        elif arr[pos] < target:
            left = pos + 1
        else:
            right = pos - 1
    
    return -1


def demo_binary_search():
    """演示二分搜尋"""
    print("=== 二分搜尋範例演示 ===")
    print()
    
    print("1. 基本二分搜尋:")
    arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    idx = binary_search(arr, 7)
    print(f"   在 {arr} 中搜尋 7: 索引 {idx}")
    print()
    
    print("2. 最左/右匹配:")
    arr = [1, 2, 2, 2, 3, 4, 5]
    left = binary_search_leftmost(arr, 2)
    right = binary_search_rightmost(arr, 2)
    print(f"   在 {arr} 中搜尋 2")
    print(f"   最左: {left}, 最右: {right}")
    print()
    
    print("3. 插入位置:")
    arr = [1, 3, 5, 7]
    pos = binary_search_insert_position(arr, 4)
    print(f"   在 {arr} 中插入 4 的位置: {pos}")
    print()
    
    print("4. 範圍搜尋:")
    arr = [1, 2, 3, 3, 3, 4, 5]
    start, end = binary_search_range(arr, 3)
    print(f"   在 {arr} 中 3 的範圍: {start} 到 {end}")
    print()
    
    print("5. 旋轉陣列搜尋:")
    arr = [4, 5, 6, 7, 0, 1, 2]
    idx = binary_search_rotated(arr, 0)
    print(f"   在旋轉陣列 {arr} 中搜尋 0: 索引 {idx}")
    print()
    
    print("6. 指數搜尋:")
    arr = list(range(100))
    idx = binary_search_exponential_search(arr, 73)
    print(f"   在 0-99 中搜尋 73: 索引 {idx}")


if __name__ == "__main__":
    demo_binary_search()
