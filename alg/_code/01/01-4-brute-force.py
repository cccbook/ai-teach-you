"""
暴力搜尋演算法 (Brute Force Algorithms)
=======================================
展示各種暴力搜尋（Brute Force）演算法的實作。
暴力搜尋是一種簡單直接的方法，透過逐一檢查所有可能的情況來找到解答。
"""

from typing import List, Tuple, Any, Callable, Optional
import math
import itertools
import time


def brute_force_search_linear(arr: List[Any], target: Any) -> int:
    """
    線性暴力搜尋
    
    參數:
        arr: 待搜尋陣列
        target: 目標值
    
    返回:
        目標值的索引，若不存在則返回 -1
    """
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1


def brute_force_search_2d(matrix: List[List[Any]], target: Any) -> Tuple[int, int]:
    """
    2D 矩陣暴力搜尋
    
    參數:
        matrix: 2D 矩陣
        target: 目標值
    
    返回:
        (row, col) 若存在，否則 (-1, -1)
    """
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == target:
                return (i, j)
    return (-1, -1)


def brute_force_string_match(text: str, pattern: str) -> List[int]:
    """
    暴力字串匹配
    
    參數:
        text: 主文字串
        pattern: 模式字串
    
    返回:
        所有匹配的起始位置列表
    """
    matches = []
    n, m = len(text), len(pattern)
    
    for i in range(n - m + 1):
        j = 0
        while j < m and text[i + j] == pattern[j]:
            j += 1
        if j == m:
            matches.append(i)
    
    return matches


def brute_force_substring(text: str) -> List[str]:
    """
    列舉所有子字串
    
    參數:
        text: 輸入字串
    
    返回:
        所有子字串列表
    """
    substrings = []
    n = len(text)
    
    for i in range(n):
        for j in range(i + 1, n + 1):
            substrings.append(text[i:j])
    
    return substrings


def brute_force_nearest_pair(points: List[Tuple[float, float]]) -> Tuple[Tuple[float, float], Tuple[float, float], float]:
    """
    暴力法找最近點對
    
    參數:
        points: 點座標列表
    
    返回:
        (點1, 點2, 最短距離)
    """
    if len(points) < 2:
        raise ValueError("需要至少兩個點")
    
    min_dist = float('inf')
    closest_pair = (points[0], points[1])
    
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dx = points[i][0] - points[j][0]
            dy = points[i][1] - points[j][1]
            dist = math.sqrt(dx * dx + dy * dy)
            
            if dist < min_dist:
                min_dist = dist
                closest_pair = (points[i], points[j])
    
    return closest_pair[0], closest_pair[1], min_dist


def brute_force_max_subarray(arr: List[float]) -> Tuple[int, int, float]:
    """
    暴力法找最大子陣列
    
    參數:
        arr: 數字陣列
    
    返回:
        (起始索引, 結束索引, 最大和)
    """
    n = len(arr)
    if n == 0:
        return (0, 0, 0)
    
    max_sum = arr[0]
    best_start = 0
    best_end = 0
    
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += arr[j]
            if current_sum > max_sum:
                max_sum = current_sum
                best_start = i
                best_end = j
    
    return (best_start, best_end, max_sum)


def brute_force_closest_string(
    candidates: List[str],
    target: str
) -> Tuple[str, int]:
    """
    暴力法找最接近的字串
    
    參數:
        candidates: 候選字串列表
        target: 目標字串
    
    返回:
        (最接近的字串, 最小編輯距離)
    """
    def edit_distance(s1: str, s2: str) -> int:
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i-1] == s2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
        
        return dp[m][n]
    
    min_dist = float('inf')
    closest = candidates[0]
    
    for candidate in candidates:
        dist = edit_distance(candidate, target)
        if dist < min_dist:
            min_dist = dist
            closest = candidate
    
    return closest, min_dist


def brute_force_traveling_salesman(
    distances: List[List[float]],
    start: int = 0
) -> Tuple[List[int], float]:
    """
    暴力法解決旅行推销员问题（TSP）
    
    參數:
        distances: 距離矩陣
        start: 起始節點
    
    返回:
        (最佳路徑, 總距離)
    """
    n = len(distances)
    cities = [i for i in range(n) if i != start]
    
    min_dist = float('inf')
    best_path = []
    
    for perm in itertools.permutations(cities):
        path = [start] + list(perm) + [start]
        total = sum(distances[path[i]][path[i+1]] for i in range(n))
        
        if total < min_dist:
            min_dist = total
            best_path = path
    
    return best_path, min_dist


def brute_force_exhaustive_search(
    objective_func: Callable[[List[int]], float],
    n_variables: int,
    domain: Tuple[int, int],
    maximize: bool = True
) -> Tuple[List[int], float]:
    """
    暴力枚舉法求解最佳化問題
    
    參數:
        objective_func: 目標函數
        n_variables: 變數數量
        domain: (最小值, 最大值)
        maximize: 是否最大化
    
    返回:
        (最佳解, 最佳值)
    """
    min_val, max_val = domain
    best_solution = None
    best_value = float('-inf') if maximize else float('inf')
    
    for values in itertools.product(range(min_val, max_val + 1), repeat=n_variables):
        value = objective_func(list(values))
        
        if maximize and value > best_value:
            best_value = value
            best_solution = list(values)
        elif not maximize and value < best_value:
            best_value = value
            best_solution = list(values)
    
    return best_solution, best_value


def brute_force_password_cracker(
    charset: str,
    max_length: int,
    target_hash: Callable[[str], str],
    hash_func: Callable[[str], str]
) -> Optional[Tuple[str, int]]:
    """
    暴力密碼破解（僅供教育用途）
    
    參數:
        charset: 字元集
        max_length: 最大長度
        target_hash: 目標雜湊值
        hash_func: 雜湊函數
    
    返回:
        (破解的密碼, 嘗試次數)
    """
    attempts = 0
    
    for length in range(1, max_length + 1):
        for attempt in itertools.product(charset, repeat=length):
            password = ''.join(attempt)
            attempts += 1
            
            if hash_func(password) == target_hash:
                return password, attempts
    
    return None


def brute_force_convex_hull(points: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    """
    暴力法計算凸包
    
    參數:
        points: 點座標列表
    
    返回:
        凸包上的點（按順時針順序）
    """
    n = len(points)
    if n < 3:
        return points
    
    hull = []
    
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            
            left = []
            right = []
            
            for k in range(n):
                if k == i or k == j:
                    continue
                
                cross = (points[j][0] - points[i][0]) * (points[k][1] - points[i][1]) - \
                        (points[j][1] - points[i][1]) * (points[k][0] - points[i][0])
                
                if cross > 0:
                    left.append(k)
                elif cross < 0:
                    right.append(k)
            
            if len(left) == 0 or len(right) == 0:
                if points[i] not in hull:
                    hull.append(points[i])
                if points[j] not in hull:
                    hull.append(points[j])
    
    return sorted(hull)


class BruteForceSolver:
    """通用暴力求解器"""
    
    def __init__(self):
        self.operations = 0
    
    def solve(self, problem: Callable, check: Callable[[Any], bool]) -> Optional[Any]:
        """
        通用暴力求解
        
        參數:
            problem: 生成候選解答的函數
            check: 檢查是否為有效解答的函數
        
        返回:
            第一個找到的解答，否則 None
        """
        self.operations = 0
        
        for candidate in problem():
            self.operations += 1
            if check(candidate):
                return candidate
        
        return None
    
    def solve_all(self, problem: Callable, check: Callable[[Any], bool]) -> List[Any]:
        """找出所有解答"""
        self.operations = 0
        solutions = []
        
        for candidate in problem():
            self.operations += 1
            if check(candidate):
                solutions.append(candidate)
        
        return solutions


def demo_brute_force():
    """演示暴力搜尋演算法"""
    print("=== 暴力搜尋演算法範例演示 ===")
    print()
    
    print("1. 線性搜尋:")
    arr = [5, 2, 8, 1, 9, 3, 7, 4, 6]
    idx = brute_force_search_linear(arr, 7)
    print(f"   在 {arr} 中搜尋 7: 索引 {idx}")
    print()
    
    print("2. 2D 矩陣搜尋:")
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    pos = brute_force_search_2d(matrix, 5)
    print(f"   在矩陣中搜尋 5: 位置 {pos}")
    print()
    
    print("3. 字串匹配:")
    text = "ABABDABACDABABCABAB"
    pattern = "ABABCABAB"
    matches = brute_force_string_match(text, pattern)
    print(f"   在 '{text}' 中搜尋 '{pattern}': 位置 {matches}")
    print()
    
    print("4. 最大子陣列:")
    arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    start, end, max_sum = brute_force_max_subarray(arr)
    print(f"   陣列: {arr}")
    print(f"   最大子陣列: 索引 {start} 到 {end}, 和為 {max_sum}")
    print()
    
    print("5. 最近點對:")
    points = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    p1, p2, dist = brute_force_nearest_pair(points)
    print(f"   點: {points}")
    print(f"   最近點對: {p1} 和 {p2}, 距離 {dist:.4f}")


if __name__ == "__main__":
    demo_brute_force()
