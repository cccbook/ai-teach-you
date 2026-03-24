"""
枚舉方法範例 (Enumeration Methods)
==================================
展示各種類型的枚舉（Enumeration）演算法。
枚舉是一種透過逐一檢查所有可能解來找到最佳解的方法。
"""

from typing import List, Dict, Tuple, Any, Callable
import itertools
import math


def enumerate_factors(n: int) -> List[int]:
    """
    枚舉所有因數
    
    參數:
        n: 正整數
    
    返回:
        所有因數的列表
    """
    factors = []
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            factors.append(i)
            if i != n // i:
                factors.append(n // i)
    return sorted(factors)


def enumerate_primes(limit: int) -> List[int]:
    """
    枚舉小於 limit 的所有質數
    
    參數:
        limit: 上限（不含）
    
    返回:
        質數列表
    """
    if limit < 2:
        return []
    
    is_prime = [True] * limit
    is_prime[0] = is_prime[1] = False
    
    for i in range(2, int(math.sqrt(limit)) + 1):
        if is_prime[i]:
            for j in range(i * i, limit, i):
                is_prime[j] = False
    
    return [i for i in range(limit) if is_prime[i]]


def enumerate_subsets(items: List[Any]) -> List[List[Any]]:
    """
    枚舉所有子集
    
    參數:
        items: 項目列表
    
    返回:
        所有可能的子集列表
    """
    subsets = []
    n = len(items)
    
    for mask in range(1 << n):
        subset = []
        for i in range(n):
            if mask & (1 << i):
                subset.append(items[i])
        subsets.append(subset)
    
    return subsets


def enumerate_permutations(items: List[Any]) -> List[List[Any]]:
    """
    枚舉所有排列
    
    參數:
        items: 項目列表
    
    返回:
        所有可能的排列列表
    """
    return [list(p) for p in itertools.permutations(items)]


def enumerate_combinations(items: List[Any], r: int) -> List[List[Any]]:
    """
    枚舉所有組合
    
    參數:
        items: 項目列表
        r: 選擇的數量
    
    返回:
        所有可能的組合列表
    """
    return [list(c) for c in itertools.combinations(items, r)]


def enumerate_partitions(n: int) -> List[List[int]]:
    """
    枚舉整數的所有分拆（Partition）
    
    參數:
        n: 正整數
    
    返回:
        所有分拆的列表
    """
    def helper(remaining: int, max_part: int) -> List[List[int]]:
        if remaining == 0:
            return [[]]
        
        partitions = []
        for part in range(min(max_part, remaining), 0, -1):
            for sub in helper(remaining - part, part):
                partitions.append([part] + sub)
        
        return partitions
    
    return helper(n, n)


def enumerate_all_solutions(
    variables: List[str],
    domains: Dict[str, List[Any]],
    constraints: Callable[[Dict[str, Any]], bool] = None
) -> List[Dict[str, Any]]:
    """
    枚舉所有滿足約束條件的解答
    
    參數:
        variables: 變數列表
        domains: 每個變數的可能值域
        constraints: 約束函數
    
    返回:
        所有滿足約束的解答列表
    """
    solutions = []
    
    def backtrack(assignment: Dict[str, Any], var_idx: int):
        if var_idx == len(variables):
            if constraints is None or constraints(assignment):
                solutions.append(assignment.copy())
            return
        
        var = variables[var_idx]
        for value in domains[var]:
            assignment[var] = value
            backtrack(assignment, var_idx + 1)
            del assignment[var]
    
    backtrack({}, 0)
    return solutions


def enumerate_gray_code(n: int) -> List[str]:
    """
    枚舉 n 位元的葛雷碼（Gray Code）
    
    參數:
        n: 位元數
    
    返回:
        葛雷碼序列
    """
    codes = []
    
    for i in range(1 << n):
        gray = i ^ (i >> 1)
        codes.append(format(gray, f'0{n}b'))
    
    return codes


def brute_force_password(
    length: int,
    charset: str,
    target_hash: str,
    hash_func: Callable[[str], str]
) -> Tuple[str, int]:
    """
    暴力破解密碼（僅用於教育目的）
    
    參數:
        length: 密碼長度
        charset: 字元集
        target_hash: 目標雜湊值
        hash_func: 雜湊函數
    
    返回:
        (找到的密碼, 嘗試次數)
    """
    attempts = 0
    
    for chars in itertools.product(charset, repeat=length):
        password = ''.join(chars)
        attempts += 1
        
        if hash_func(password) == target_hash:
            return password, attempts
    
    return None, attempts


def enumerate_dice_combinations(num_dice: int, target_sum: int) -> List[Tuple[int, ...]]:
    """
    枚舉擲硬幣組合，使總和等於目標值
    
    參數:
        num_dice: 硬幣數量
        target_sum: 目標總和
    
    返回:
        所有可能組合的列表
    """
    min_sum = num_dice
    max_sum = num_dice * 6
    
    if target_sum < min_sum or target_sum > max_sum:
        return []
    
    results = []
    
    def helper(index: int, remaining: int, current: Tuple[int, ...]):
        if index == num_dice:
            if remaining == 0:
                results.append(current)
            return
        
        min_val = max(1, remaining - (num_dice - index - 1) * 6)
        max_val = min(6, remaining - (num_dice - index - 1))
        
        for value in range(min_val, max_val + 1):
            helper(index + 1, remaining - value, current + (value,))
    
    helper(0, target_sum, ())
    return results


class BacktrackingEnumerator:
    """回溯枚舉器"""
    
    def __init__(self, variables: List[str], domains: Dict[str, List[Any]]):
        self.variables = variables
        self.domains = domains
        self.solutions = []
        self.attempts = 0
    
    def enumerate(self, constraints: Callable[[Dict[str, Any]], bool] = None) -> List[Dict[str, Any]]:
        """執行枚舉"""
        self.solutions = []
        self.attempts = 0
        self._backtrack({}, 0, constraints)
        return self.solutions
    
    def _backtrack(self, assignment: Dict[str, Any], index: int, constraints):
        self.attempts += 1
        
        if index == len(self.variables):
            if constraints is None or constraints(assignment):
                self.solutions.append(assignment.copy())
            return
        
        var = self.variables[index]
        for value in self.domains[var]:
            assignment[var] = value
            
            if self._is_consistent(assignment, constraints, index):
                self._backtrack(assignment, index + 1, constraints)
            
            del assignment[var]
    
    def _is_consistent(self, assignment: Dict[str, Any], constraints, index: int) -> bool:
        if constraints is None:
            return True
        return constraints(assignment)


def demo_enumeration():
    """演示枚舉方法"""
    print("=== 枚舉方法範例演示 ===")
    print()
    
    print("1. 枚舉因數:")
    factors = enumerate_factors(36)
    print(f"   36 的因數: {factors}")
    print()
    
    print("2. 枚舉質數:")
    primes = enumerate_primes(30)
    print(f"   30 以內的質數: {primes}")
    print()
    
    print("3. 枚舉子集:")
    items = ['a', 'b', 'c']
    subsets = enumerate_subsets(items)
    print(f"   {{a,b,c}} 的子集數量: {len(subsets)}")
    print()
    
    print("4. 枚舉排列:")
    perms = enumerate_permutations([1, 2, 3])
    print(f"   [1,2,3] 的排列: {perms}")
    print()
    
    print("5. 枚舉組合:")
    combs = enumerate_combinations([1, 2, 3, 4], 2)
    print(f"   [1,2,3,4] 取 2 的組合: {combs}")
    print()
    
    print("6. 枚舉整數分拆:")
    partitions = enumerate_partitions(5)
    print(f"   5 的分拆: {partitions}")
    print()
    
    print("7. 枚舉葛雷碼:")
    gray_codes = enumerate_gray_code(3)
    print(f"   3位元葛雷碼: {gray_codes}")


if __name__ == "__main__":
    demo_enumeration()
