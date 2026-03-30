#!/usr/bin/env python3
"""
SymPy 張量基礎 - 第1章第2節
介紹如何使用 SymPy 的張量模組
"""

import sympy as sp
from sympy import symbols, sqrt, simplify, expand, sin, cos, Function
from sympy.tensor.array import Array, derive_by_array


def main():
    print("=" * 60)
    print("SymPy 張量基礎教學 - Chapter 1.2")
    print("=" * 60)

    print("\n1. 使用 Array 創建張量")
    print("-" * 40)
    A = Array([1, 2, 3, 4, 5, 6])
    print(f"1D Array: {A}")
    print(f"Shape: {A.shape}")

    B = Array([[1, 2, 3], [4, 5, 6]])
    print(f"2D Array:\n{B}")
    print(f"Shape: {B.shape}")

    print("\n2. 使用符號創建張量")
    print("-" * 40)
    a, b, c, d = symbols('a b c d')
    C = Array([[a, b], [c, d]])
    print(f"符號矩陣 C:\n{C}")

    print("\n3. 張量加法與乘法")
    print("-" * 40)
    D = Array([[1, 2], [3, 4]])
    E = Array([[5, 6], [7, 8]])
    print(f"D + E =")
    print(D + E)
    print(f"2 * D =")
    print(2 * D)

    print("\n4. 愛因斯坦慣例 - 愛因斯坦求和約定")
    print("-" * 40)
    u = Array([1, 2, 3])
    v = Array([4, 5, 6])
    result = sum(u[i] * v[i] for i in range(3))
    print(f"u = {u}")
    print(f"v = {v}")
    print(f"u^i * v_i (愛因斯坦慣例) = {result}")

    M = Array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print(f"M = \n{M}")
    result2 = sum(M[i, i] for i in range(3))
    print(f"M^i_i (.trace) = {result2}")

    print("\n5. 度規張量 (Minkowski metric)")
    print("-" * 40)
    eta = Array([[-1, 0, 0, 0],
                 [0, 1, 0, 0],
                 [0, 0, 1, 0],
                 [0, 0, 0, 1]])
    print(f"Minkowski 度規 η = \n{eta}")
    print("這是特殊相對論中的時空度規")

    print("\n6. 四維向量")
    print("-" * 40)
    ct, x, y, z = symbols('ct x y z')
    four_position = Array([ct, x, y, z])
    print(f"四維位置: x^μ = {four_position}")

    print("\n7. 克里斯多費符號計算準備")
    print("-" * 40)
    theta = symbols('theta')
    g = Array([[1, 0], [0, sin(theta)**2]])
    print(f"2D 球面度規 g_{{ij}} = ")
    print(g)
    print("這是球座標 (r, θ) 的度規")

    print("\n8. 導數與張量")
    print("-" * 40)
    x, y = symbols('x y')
    f = Function('f')(x, y)
    grad = derive_by_array(f, (x, y))
    print(f"∂f/∂x, ∂f/∂y = {grad}")

    print("\n9. 協變導數範例")
    print("-" * 40)
    t, x = symbols('t x')
    phi = Function('phi')(x, t)
    dphi_dt = sp.diff(phi, t)
    dphi_dx = sp.diff(phi, x)
    print(f"φ(x,t) = φ")
    print(f"∂φ/∂t = {dphi_dt}")
    print(f"∂φ/∂x = {dphi_dx}")

    print("\n10. 度規逆矩陣計算")
    print("-" * 40)
    g = sp.Matrix([[1, 0], [0, sin(theta)**2]])
    g_inv = g.inv()
    print(f"g = \n{g}")
    print(f"g^(-1) = \n{g_inv}")
    print("注意：在球座標中，g^θθ = 1/sin²θ")

    print("\n" + "=" * 60)
    print("張量基礎教學完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
