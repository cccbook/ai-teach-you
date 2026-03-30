#!/usr/bin/env python3
"""
SymPy 基礎教學 - 第1章第1節
介紹 SymPy 的基本用法，包括符號、運算、矩陣等
"""

import sympy as sp
from sympy import symbols, sqrt, sin, cos, exp, diff, integrate, Matrix
from sympy.abc import x, y, z, t


def main():
    print("=" * 60)
    print("SymPy 基礎教學 - Chapter 1")
    print("=" * 60)

    print("\n1. 符號定義")
    print("-" * 40)
    a, b, c = symbols('a b c')
    print(f"a = {a}, b = {b}, c = {c}")

    alpha, beta, gamma = symbols('alpha beta gamma')
    print(f"alpha = {alpha}, beta = {beta}")

    print("\n2. 代數運算")
    print("-" * 40)
    expr1 = (a + b)**2
    expr2 = (a - b)**2
    print(f"(a + b)^2 = {sp.expand(expr1)}")
    print(f"(a - b)^2 = {sp.expand(expr2)}")
    print(f"(a + b)^2 - (a - b)^2 = {sp.simplify(expr1 - expr2)}")

    print("\n3. 求解方程式")
    print("-" * 40)
    solutions = sp.solve(a**2 - 4, a)
    print(f"a^2 - 4 = 0 的解: {solutions}")

    solutions2 = sp.solve([a + b - 1, a - b - 3], (a, b))
    print(f"a + b = 1, a - b = 3 的解: {solutions2}")

    print("\n4. 微積分運算")
    print("-" * 40)
    f = x**3 + 2*x**2 - 5*x + 1
    print(f"f(x) = {f}")
    print(f"f'(x) = {diff(f, x)}")
    print(f"f''(x) = {diff(f, x, 2)}")
    print(f"∫ f(x) dx = {integrate(f, x)}")

    g = sin(x) * exp(x)
    print(f"g(x) = sin(x) * e^x")
    print(f"∫ g(x) dx = {integrate(g, x)}")

    print("\n5. 矩陣運算")
    print("-" * 40)
    M = Matrix([[a, b], [c, a]])
    print(f"M = \n{M}")
    print(f"det(M) = {M.det()}")
    print(f"M^(-1) = ")
    print(M.inv())
    print(f"特徵值: {M.eigenvals()}")
    print(f"特徵向量: {M.eigenvects()}")

    print("\n6. 化簡與展開")
    print("-" * 40)
    expr = (sin(x)**2 + cos(x)**2) * (a + b)
    print(f"sin^2(x) + cos^2(x) = {sp.simplify(sin(x)**2 + cos(x)**2)}")

    expr2 = (a + b)*(a - b + c)
    print(f"(a + b)(a - b + c) = {sp.expand(expr2)}")
    print(f"因式分解: {sp.factor(expr2)}")

    print("\n7. 代入值計算")
    print("-" * 40)
    f = x**2 + y**2
    print(f"f = x^2 + y^2")
    print(f"f | x=1, y=2 = {f.subs({x: 1, y: 2})}")
    print(f"f | x=a, y=b = {f.subs({x: a, y: b})}")

    print("\n8. 洛倫茲因子範例")
    print("-" * 40)
    v, c = symbols('v c', positive=True)
    gamma = 1 / sqrt(1 - v**2 / c**2)
    print(f"洛倫茲因子 γ = {gamma}")
    v_val = 0.8 * c
    gamma_val = gamma.subs(v, v_val)
    print(f"當 v = 0.8c 時，γ = {gamma_val.simplify()} = {float(gamma_val.simplify()):.4f}")

    print("\n" + "=" * 60)
    print("教學完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
