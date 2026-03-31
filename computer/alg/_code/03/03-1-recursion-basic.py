"""
基本遞迴範例 (Basic Recursion)
===============================
展示遞迴（Recursion）的基本概念與實作方式。
遞迴是一種函數直接或間接呼叫自己的程式設計技術。
"""

from typing import List, Any, Callable
import sys


sys.setrecursionlimit(10000)


def recursive_countdown(n: int) -> None:
    """
    倒數遞迴
    
    參數:
        n: 起始數字
    """
    if n < 0:
        return
    
    print(n)
    recursive_countdown(n - 1)


def recursive_sum(arr: List[Any], index: int = 0) -> Any:
    """
    遞迴求和
    
    參數:
        arr: 陣列
        index: 目前索引
    
    返回:
        總和
    """
    if index >= len(arr):
        return 0
    
    return arr[index] + recursive_sum(arr, index + 1)


def recursive_factorial(n: int) -> int:
    """
    遞迴計算階乘
    
    參數:
        n: 非負整數
    
    返回:
        n!
    """
    if n <= 1:
        return 1
    
    return n * recursive_factorial(n - 1)


def recursive_power(base: float, exp: int) -> float:
    """
    遞迴計算次方
    
    參數:
        base: 底數
        exp: 指數
    
    返回:
        base^exp
    """
    if exp == 0:
        return 1
    
    if exp < 0:
        return 1 / recursive_power(base, -exp)
    
    if exp % 2 == 0:
        half = recursive_power(base, exp // 2)
        return half * half
    else:
        return base * recursive_power(base, exp - 1)


def recursive_fibonacci(n: int) -> int:
    """
    遞迴計算費波那契數
    
    參數:
        n: 索引（從 0 開始）
    
    返回:
        F(n)
    """
    if n <= 1:
        return n
    
    return recursive_fibonacci(n - 1) + recursive_fibonacci(n - 2)


def recursive_reverse(arr: List[Any], left: int = 0, right: int = None) -> List[Any]:
    """
    遞迴反轉陣列
    
    參數:
        arr: 陣列
        left: 左指標
        right: 右指標
    
    返回:
        反轉後的陣列
    """
    if right is None:
        right = len(arr) - 1
    
    if left >= right:
        return arr
    
    arr[left], arr[right] = arr[right], arr[left]
    return recursive_reverse(arr, left + 1, right - 1)


def recursive_binary_search(
    arr: List[Any],
    target: Any,
    left: int = 0,
    right: int = None
) -> int:
    """
    遞迴二分搜尋
    
    參數:
        arr: 已排序陣列
        target: 目標值
        left: 左指標
        right: 右指標
    
    返回:
        目標的索引，若不存在則返回 -1
    """
    if right is None:
        right = len(arr) - 1
    
    if left > right:
        return -1
    
    mid = (left + right) // 2
    
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return recursive_binary_search(arr, target, mid + 1, right)
    else:
        return recursive_binary_search(arr, target, left, mid - 1)


def recursive_sum_of_digits(n: int) -> int:
    """
    遞迴計算數字各位和
    
    參數:
        n: 非負整數
    
    返回:
        各位數之和
    """
    if n < 10:
        return n
    
    return recursive_sum_of_digits(n // 10) + n % 10


def recursive_palindrome(s: str, left: int = 0, right: int = None) -> bool:
    """
    遞迴檢查回文
    
    參數:
        s: 字串
        left: 左指標
        right: 右指標
    
    返回:
        是否為回文
    """
    if right is None:
        right = len(s) - 1
    
    if left >= right:
        return True
    
    if s[left] != s[right]:
        return False
    
    return recursive_palindrome(s, left + 1, right - 1)


def recursive_gcd(a: int, b: int) -> int:
    """
    遞迴計算最大公因數（歐幾里得算法）
    
    參數:
        a, b: 兩個整數
    
    返回:
        gcd(a, b)
    """
    if b == 0:
        return abs(a)
    
    return recursive_gcd(b, a % b)


def recursive_lcm(a: int, b: int) -> int:
    """
    遞迴計算最小公倍數
    
    參數:
        a, b: 兩個整數
    
    返回:
        lcm(a, b)
    """
    if a == 0 or b == 0:
        return 0
    
    return abs(a * b) // recursive_gcd(a, b)


def recursive_sum_array(arr: List[Any]) -> Any:
    """
    遞迴加總陣列
    
    參數:
        arr: 陣列
    
    返回:
        總和
    """
    if len(arr) == 0:
        return 0
    
    if len(arr) == 1:
        return arr[0]
    
    mid = len(arr) // 2
    left_sum = recursive_sum_array(arr[:mid])
    right_sum = recursive_sum_array(arr[mid:])
    
    return left_sum + right_sum


def recursive_count(arr: List[Any], target: Any) -> int:
    """
    遞迴計算目標出現次數
    
    參數:
        arr: 陣列
        target: 目標值
    
    返回:
        出現次數
    """
    if len(arr) == 0:
        return 0
    
    count = 1 if arr[0] == target else 0
    return count + recursive_count(arr[1:], target) if len(arr) > 1 else count


def recursive_range_sum(start: int, end: int) -> int:
    """
    遞迴計算範圍內整數和
    
    參數:
        start: 起始值
        end: 結束值
    
    返回:
        總和
    """
    if start > end:
        return 0
    
    return start + recursive_range_sum(start + 1, end)


def recursive_tower_of_hanoi(
    n: int,
    source: str = "A",
    target: str = "C",
    auxiliary: str = "B"
) -> List[tuple]:
    """
    遞迴解決河內塔問題
    
    參數:
        n: 圓盤數量
        source: 來源柱
        target: 目標柱
        auxiliary: 輔助柱
    
    返回:
        移動步驟列表
    """
    moves = []
    
    if n == 1:
        moves.append((source, target))
    else:
        moves.extend(recursive_tower_of_hanoi(n - 1, source, auxiliary, target))
        moves.append((source, target))
        moves.extend(recursive_tower_of_hanoi(n - 1, auxiliary, target, source))
    
    return moves


class RecursiveBinaryTree:
    """遞迴二元樹"""
    
    def __init__(self, value: Any, left: 'RecursiveBinaryTree' = None, right: 'RecursiveBinaryTree' = None):
        self.value = value
        self.left = left
        self.right = right
    
    def inorder(self) -> List[Any]:
        """中序遍歷"""
        result = []
        
        if self.left:
            result.extend(self.left.inorder())
        
        result.append(self.value)
        
        if self.right:
            result.extend(self.right.inorder())
        
        return result
    
    def preorder(self) -> List[Any]:
        """前序遍歷"""
        result = [self.value]
        
        if self.left:
            result.extend(self.left.preorder())
        
        if self.right:
            result.extend(self.right.preorder())
        
        return result
    
    def postorder(self) -> List[Any]:
        """後序遍歷"""
        result = []
        
        if self.left:
            result.extend(self.left.postorder())
        
        if self.right:
            result.extend(self.right.postorder())
        
        result.append(self.value)
        
        return result
    
    def height(self) -> int:
        """計算樹高"""
        left_height = self.left.height() if self.left else 0
        right_height = self.right.height() if self.right else 0
        
        return 1 + max(left_height, right_height)


def demo_recursion():
    """演示基本遞迴"""
    print("=== 基本遙迴範例演示 ===")
    print()
    
    print("1. 倒數:")
    recursive_countdown(5)
    print()
    
    print("2. 階乘:")
    print(f"   5! = {recursive_factorial(5)}")
    print()
    
    print("3. 費波那契數列:")
    fibs = [recursive_fibonacci(i) for i in range(10)]
    print(f"   前10個費波那契數: {fibs}")
    print()
    
    print("4. 二分搜尋:")
    arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    idx = recursive_binary_search(arr, 5)
    print(f"   在 {arr} 中搜尋 5: 索引 {idx}")
    print()
    
    print("5. 回文檢查:")
    print(f"   'radar' 是回文: {recursive_palindrome('radar')}")
    print(f"   'hello' 是回文: {recursive_palindrome('hello')}")
    print()
    
    print("6. 最大公因數:")
    print(f"   gcd(48, 18) = {recursive_gcd(48, 18)}")
    print()
    
    print("7. 河內塔:")
    moves = recursive_tower_of_hanoi(3)
    print(f"   3層河內塔移動步驟: {len(moves)} 步")
    print(f"   步驟: {moves}")
    print()
    
    print("8. 二元樹遍歷:")
    tree = RecursiveBinaryTree(
        1,
        RecursiveBinaryTree(2, RecursiveBinaryTree(4), RecursiveBinaryTree(5)),
        RecursiveBinaryTree(3, RecursiveBinaryTree(6), RecursiveBinaryTree(7))
    )
    print(f"   中序: {tree.inorder()}")
    print(f"   前序: {tree.preorder()}")
    print(f"   後序: {tree.postorder()}")


if __name__ == "__main__":
    demo_recursion()
