"""
丢番圖方程（Diophantine Equation）
形如：a*x + b*y = c 的整數方程

第10問題問的是：是否存在通用演算法，
判斷任意丢番圖方程是否有整數解？
"""

def gcd(a: int, b: int) -> int:
    """計算最大公約數"""
    while b:
        a, b = b, a % b
    return abs(a)

def extended_gcd(a: int, b: int) -> tuple:
    """擴展歐幾里得算法：返回 (gcd, x, y) 使得 ax + by = gcd"""
    if b == 0:
        return (abs(a), 1 if a > 0 else -1, 0)
    else:
        gcd_val, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return (gcd_val, x, y)

def has_integer_solution(a: int, b: int, c: int) -> tuple:
    """
    判斷方程 ax + by = c 是否有整數解
    返回：(是否有解, 其中一組解或None)
    
    定理：ax + by = c 有整數解 當且僅當 gcd(a,b) 整除 c
    """
    if a == 0 and b == 0:
        if c == 0:
            return (True, (0, 0))  # 任意解
        else:
            return (False, None)
    
    g = gcd(a, b)
    
    if c % g != 0:
        return (False, None)
    
    a_reduced, b_reduced = a // g, b // g
    c_reduced = c // g
    
    _, x0, y0 = extended_gcd(a_reduced, b_reduced)
    
    x0 *= c_reduced
    y0 *= c_reduced
    
    return (True, (x0, y0))

def general_solution(a: int, b: int, c: int) -> str:
    """給出通解公式"""
    has_sol, sol = has_integer_solution(a, b, c)
    
    if not has_sol:
        return f"方程 {a}x + {b}y = {c} 沒有整數解"
    
    if sol is None:
        return f"方程 {a}x + {b}y = {c} 的解：任意值"
    
    x0, y0 = sol
    g = gcd(a, b)
    
    if b == 0:
        return f"x = {x0}"
    elif a == 0:
        return f"y = {y0}"
    else:
        return (f"方程 {a}x + {b}y = {c} 的通解為：\n"
                f"  x = {x0} + {b//g}t\n"
                f"  y = {y0} - {a//g}t\n"
                f"  其中 t 是任意整數")


def find_nonnegative_solutions(a: int, b: int, c: int, max_t: int = 1000) -> list:
    """找出所有非負整數解 (x >= 0, y >= 0)"""
    has_sol, sol = has_integer_solution(a, b, c)
    
    if not has_sol:
        return []
    
    x0, y0 = sol
    g = gcd(a, b)
    
    solutions = []
    for t in range(-max_t, max_t + 1):
        x = x0 + (b // g) * t
        y = y0 - (a // g) * t
        if x >= 0 and y >= 0:
            solutions.append((x, y))
    
    return solutions


def main():
    print("=== 丢番圖方程求解器 ===\n")
    
    test_cases = [
        (2, 3, 7),    # 2x + 3y = 7
        (4, 2, 6),    # 4x + 2y = 6
        (6, 4, 5),    # 6x + 4y = 5 (無解)
        (0, 5, 15),   # 0x + 5y = 15
        (3, 0, 9),    # 3x + 0y = 9
        (0, 0, 0),    # 0x + 0y = 0
        (0, 0, 5),    # 0x + 0y = 5 (無解)
    ]
    
    for a, b, c in test_cases:
        print(general_solution(a, b, c))
        print()
    
    print("=" * 50)
    print("\n非負整數解示例 (2x + 3y = 7):")
    solutions = find_nonnegative_solutions(2, 3, 7)
    for x, y in solutions[:10]:
        print(f"  x = {x}, y = {y}")


if __name__ == "__main__":
    main()
