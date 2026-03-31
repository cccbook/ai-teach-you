"""
SKI 組合子邏輯
展示如何用最少的組合子構造一切
"""

from typing import Callable, Any

S = lambda x: lambda y: lambda z: x(z)(y(z))
K = lambda x: lambda y: x
I = S(K)(K)

TRUE = K
FALSE = S(K)(K)

def demo_combinators():
    print("=== SKI 組合子演示 ===\n")
    
    print("基本組合子：")
    print(f"  I x = {I('value')}")
    print(f"  K x y = {K('x')('y')}")
    print()
    
    print("恆等組合子驗證：")
    print(f"  (S K K) x = {S(K)(K)('test')}")
    print(f"  I = S K K")
    print()
    
    print("Church 布爾值用 SKI 表示：")
    print(f"  TRUE = K = λx.λy.x")
    print(f"  FALSE = S K K = λx.λy.y")
    print(f"  IF TRUE a b = {K('a')('b')}")


if __name__ == "__main__":
    demo_combinators()
