#!/usr/bin/env python3
"""
克里斯多費符號計算 - 第2章第1節
使用 SymPy 計算克里斯多費符號（Gamma）
"""

import sympy as sp
from sympy import symbols, simplify, sin, cos, diff, sqrt, Function, simplify
from sympy.tensor.array import Array


def christoffel_symbols(metric, coords):
    """
    計算克里斯多費符號
    Γ^k_ij = (1/2) * g^kl * (∂g_lj/∂x^i + ∂g_il/∂x^j - ∂g_ij/∂x^l)
    """
    n = len(coords)
    g = sp.Matrix(metric)
    g_inv = g.inv()
    
    Gamma = [[[0]*n for _ in range(n)] for _ in range(n)]
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                sum_term = 0
                for l in range(n):
                    dg_i = diff(metric[l][j], coords[i])
                    dg_j = diff(metric[i][l], coords[j])
                    dg_l = diff(metric[i][j], coords[l])
                    sum_term += (dg_i + dg_j - dg_l) * g_inv[k, l]
                Gamma[k][i][j] = simplify(sum_term / 2)
    
    return Gamma


def main():
    print("=" * 60)
    print("克里斯多費符號計算 - Chapter 2.1")
    print("=" * 60)

    print("\n1. 二維球面度規 (球座標)")
    print("-" * 40)
    theta, phi = symbols('theta phi')
    coords = [theta, phi]
    
    g = [[1, 0],
         [0, sin(theta)**2]]
    print(f"度規 g_{{ij}} = {g}")
    
    Gamma = christoffel_symbols(g, coords)
    print(f"\n克里斯多費符號 Γ^k_ij:")
    for k in range(2):
        print(f"\nΓ^{k}:")
        for i in range(2):
            row = [sp.simplify(Gamma[k][i][j]) for j in range(2)]
            print(f"  Γ^{{{k}}}_{{{i}j}} = {row}")

    print("\n\n2. 測地線方程式測試")
    print("-" * 40)
    print("Γ^θ_φφ = -sin(θ)cos(θ)")
    print("這導致球面上自由粒子會繞大圓運動")

    print("\n\n3. Minkowski 時空 (特殊相對論)")
    print("-" * 40)
    ct, x, y, z = symbols('ct x y z')
    coords_mink = [ct, x, y, z]
    
    eta = [[-1, 0, 0, 0],
           [0, 1, 0, 0],
           [0, 0, 1, 0],
           [0, 0, 0, 1]]
    
    Gamma_mink = christoffel_symbols(eta, coords_mink)
    print("Minkowski 度規的克里斯多費符號全部為零！")
    print("這表示平坦時空中沒有重力效應")
    
    all_zero = all(Gamma_mink[k][i][j] == 0 
                   for k in range(4) for i in range(4) for j in range(4))
    print(f"所有 Γ 為零: {all_zero}")

    print("\n\n4. 柱座標度規")
    print("-" * 40)
    r, phi, z_cyl = symbols('r phi z_cyl')
    coords_cyl = [r, phi, z_cyl]
    
    g_cyl = [[1, 0, 0],
             [0, r**2, 0],
             [0, 0, 1]]
    print(f"柱座標度規 g_{{ij}} = ")
    print(sp.Matrix(g_cyl))
    
    Gamma_cyl = christoffel_symbols(g_cyl, coords_cyl)
    print(f"\n非零克里斯多費符號:")
    for k in range(3):
        for i in range(3):
            for j in range(3):
                if Gamma_cyl[k][i][j] != 0:
                    print(f"Γ^{{{k}}}_{{{i}{j}}} = {sp.simplify(Gamma_cyl[k][i][j])}")

    print("\n" + "=" * 60)
    print("克里斯多費符號計算完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
