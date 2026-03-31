"""
合併排序範例 (Merge Sort)
========================
展示合併排序（Merge Sort）的各種實作方式。
合併排序是一種穩定且時間複雜度為 O(n log n) 的分治排序演算法。
"""

from typing import List, Any, Callable
import math


def merge_sort_basic(arr: List[Any]) -> List[Any]:
    """
    基本合併排序
    
    參數:
        arr: 待排序陣列
    
    返回:
        排序後的陣列
    """
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort_basic(arr[:mid])
    right = merge_sort_basic(arr[mid:])
    
    return merge(left, right)


def merge(left: List[Any], right: List[Any]) -> List[Any]:
    """
    合併兩個已排序陣列
    
    參數:
        left, right: 已排序陣列
    
    返回:
        合併後的已排序陣列
    """
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result


def merge_sort_inplace(arr: List[Any], left: int = None, right: int = None) -> None:
    """
    原地合併排序
    
    參數:
        arr: 待排序陣列
        left, right: 排序範圍
    """
    if left is None:
        left = 0
    if right is None:
        right = len(arr)
    
    if right - left <= 1:
        return
    
    mid = (left + right) // 2
    
    merge_sort_inplace(arr, left, mid)
    merge_sort_inplace(arr, mid, right)
    merge_inplace(arr, left, mid, right)


def merge_inplace(arr: List[Any], left: int, mid: int, right: int) -> None:
    """
    原地合併
    
    參數:
        arr: 陣列
        left, mid, right: 範圍
    """
    left_arr = arr[left:mid]
    right_arr = arr[mid:right]
    
    i = j = 0
    k = left
    
    while i < len(left_arr) and j < len(right_arr):
        if left_arr[i] <= right_arr[j]:
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1
        k += 1
    
    while i < len(left_arr):
        arr[k] = left_arr[i]
        i += 1
        k += 1
    
    while j < len(right_arr):
        arr[k] = right_arr[j]
        j += 1
        k += 1


def merge_sort_bottom_up(arr: List[Any]) -> List[Any]:
    """
    自底向上的合併排序
    
    參數:
        arr: 待排序陣列
    
    返回:
        排序後的陣列
    """
    n = len(arr)
    result = arr[:]
    
    size = 1
    
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(left + size, n)
            right = min(left + 2 * size, n)
            
            left_arr = result[left:mid]
            right_arr = result[mid:right]
            
            i = j = 0
            k = left
            
            while i < len(left_arr) and j < len(right_arr):
                if left_arr[i] <= right_arr[j]:
                    result[k] = left_arr[i]
                    i += 1
                else:
                    result[k] = right_arr[j]
                    j += 1
                k += 1
            
            while i < len(left_arr):
                result[k] = left_arr[i]
                i += 1
                k += 1
            
            while j < len(right_arr):
                result[k] = right_arr[j]
                j += 1
                k += 1
        
        size *= 2
    
    return result


def merge_sort_count_inversions(arr: List[Any]) -> tuple:
    """
    合併排序計算反轉數
    
    參數:
        arr: 待排序陣列
    
    返回:
        (排序後的陣列, 反轉數)
    """
    if len(arr) <= 1:
        return arr, 0
    
    mid = len(arr) // 2
    left, left_inv = merge_sort_count_inversions(arr[:mid])
    right, right_inv = merge_sort_count_inversions(arr[mid:])
    merged, split_inv = merge_and_count(left, right)
    
    return merged, left_inv + right_inv + split_inv


def merge_and_count(left: List[Any], right: List[Any]) -> tuple:
    """合併並計算跨區間反轉"""
    result = []
    inversions = 0
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            inversions += len(left) - i
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result, inversions


def merge_sort_stable(arr: List[Any], key: Callable[[Any], Any] = None) -> List[Any]:
    """
    穩定合併排序
    
    參數:
        arr: 待排序陣列
        key: 排序鍵函數
    
    返回:
        排序後的陣列
    """
    if key is None:
        key = lambda x: x
    
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort_stable(arr[:mid], key)
    right = merge_sort_stable(arr[mid:], key)
    
    return merge_stable(left, right, key)


def merge_stable(left: List[Any], right: List[Any], key: Callable) -> List[Any]:
    """穩定合併"""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result


def merge_sort_parallel(arr: List[Any], num_threads: int = 4) -> List[Any]:
    """
    並行合併排序
    
    參數:
        arr: 待排序陣列
        num_threads: 執行緒數
    
    返回:
        排序後的陣列
    """
    from concurrent.futures import ThreadPoolExecutor
    
    n = len(arr)
    chunk_size = max(1, n // num_threads)
    chunks = [arr[i:i + chunk_size] for i in range(0, n, chunk_size)]
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        sorted_chunks = list(executor.map(merge_sort_basic, chunks))
    
    while len(sorted_chunks) > 1:
        new_chunks = []
        
        for i in range(0, len(sorted_chunks), 2):
            if i + 1 < len(sorted_chunks):
                new_chunks.append(merge(sorted_chunks[i], sorted_chunks[i + 1]))
            else:
                new_chunks.append(sorted_chunks[i])
        
        sorted_chunks = new_chunks
    
    return sorted_chunks[0] if sorted_chunks else []


def merge_sort_three_way(arr: List[Any]) -> List[Any]:
    """
    三路合併排序（適用於有大量重複元素）
    
    參數:
        arr: 待排序陣列
    
    返回:
        排序後的陣列
    """
    if len(arr) <= 1:
        return arr
    
    mid1 = len(arr) // 3
    mid2 = 2 * len(arr) // 3
    
    left = merge_sort_three_way(arr[:mid1])
    middle = merge_sort_three_way(arr[mid1:mid2])
    right = merge_sort_three_way(arr[mid2:])
    
    return merge_three_way(left, middle, right)


def merge_three_way(left: List[Any], middle: List[Any], right: List[Any]) -> List[Any]:
    """三路合併"""
    result = []
    i = j = k = 0
    
    while i < len(left) or j < len(middle) or k < len(right):
        candidates = []
        
        if i < len(left):
            candidates.append(left[i])
        if j < len(middle):
            candidates.append(middle[j])
        if k < len(right):
            candidates.append(right[k])
        
        if not candidates:
            break
        
        min_val = min(candidates)
        result.append(min_val)
        
        if i < len(left) and left[i] == min_val:
            i += 1
        elif j < len(middle) and middle[j] == min_val:
            j += 1
        else:
            k += 1
    
    return result


def demo_merge_sort():
    """演示合併排序"""
    print("=== 合併排序範例演示 ===")
    print()
    
    print("1. 基本合併排序:")
    arr = [5, 2, 8, 1, 9, 3, 7, 4, 6]
    sorted_arr = merge_sort_basic(arr.copy())
    print(f"   排序前: {arr}")
    print(f"   排序後: {sorted_arr}")
    print()
    
    print("2. 原地合併排序:")
    arr = [5, 2, 8, 1, 9, 3, 7, 4, 6]
    merge_sort_inplace(arr)
    print(f"   原地排序: {arr}")
    print()
    
    print("3. 自底向上排序:")
    arr = [5, 2, 8, 1, 9, 3, 7, 4, 6]
    sorted_arr = merge_sort_bottom_up(arr.copy())
    print(f"   排序後: {sorted_arr}")
    print()
    
    print("4. 反轉數計算:")
    arr = [2, 4, 1, 3]
    sorted_arr, inversions = merge_sort_count_inversions(arr.copy())
    print(f"   陣列: {arr}")
    print(f"   反轉數: {inversions}")
    print()
    
    print("5. 穩定排序:")
    arr = [(1, 'a'), (3, 'b'), (1, 'c'), (2, 'd')]
    sorted_arr = merge_sort_stable(arr.copy(), key=lambda x: x[0])
    print(f"   排序前: {arr}")
    print(f"   排序後: {sorted_arr}")
    print()
    
    print("6. 三路合併排序:")
    arr = [1, 2, 1, 2, 1, 2, 1]
    sorted_arr = merge_sort_three_way(arr.copy())
    print(f"   有重複元素的排序: {sorted_arr}")


if __name__ == "__main__":
    demo_merge_sort()
