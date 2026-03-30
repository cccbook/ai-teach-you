#!/usr/bin/env python3
"""
黎曼曲率張量計算 - 第2章第2節
使用 SymPy 計算黎曼曲率張量 R^i_jkl
"""

import sympy as sp
from sympy import symbols, simplify, sin, cos, diff, sqrt, expand
from sympy.tensor.array import Array


def christoffel_symbols(metric, coords):
    """計算克里斯多費符號"""
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


def riemann_tensor(Gamma, coords):
    """
    計算黎曼曲率張量
    R^i_jkl = ∂Γ^i_jl/∂x^k - ∂Γ^i_jk/∂x^l + Γ^i_mk*Γ^m_jl - Γ^i_ml*Γ^m_jk
    """
    n = len(coords)
    R = [[[[0]*n for _ in range(n)] for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):
                    term1 = diff(Gamma[i][j][l], coords[k])
                    term2 = diff(Gamma[i][j][k], coords[l])
                    
                    sum_term = 0
                    for m in range(n):
                        sum_term += Gamma[i][m][k] * Gamma[m][j][l] - \
                                     Gamma[i][m][l] * Gamma[m][j][k]
                    
                    R[i][j][k][l] = simplify(term1 - term2 + sum_term)
    
    return R


def ricci_tensor(R, n):
    """計算里奇張量 R_jk = R^i_jik"""
    Ricci = [[0]*n for _ in range(n)]
    for j in range(n):
        for k in range(n):
            Ricci[j][k] = simplify(sum(R[i][j][k][i] for i in range(n)))
    return Ricci


def ricci_scalar(Ricci, metric, coords):
    """計算里奇標量 R = g^jk * R_jk"""
    g_inv = sp.Matrix(metric).inv()
    n = len(coords)
    R = 0
    for j in range(n):
        for k in range(n):
            R += g_inv[j, k] * Ricci[j][k]
    return simplify(R)


def main():
    print("=" * 60)
    print("黎曼曲率張量計算 - Chapter 2.2")
    print("=" * 60)

    print("\n1. Minkowski 時空 (平坦)")
    print("-" * 40)
    ct, x, y, z = symbols('ct x y z')
    coords = [ct, x, y, z]
    
    eta = [[-1, 0, 0, 0],
           [0, 1, 0, 0],
           [0, 0, 1, 0],
           [0, 0, 0, 1]]
    
    Gamma = christoffel_symbols(eta, coords)
    R = riemann_tensor(Gamma, coords)
    
    all_zero = all(R[i][j][k][l] == 0 
                   for i in range(4) for j in range(4) 
                   for k in range(4) for l in range(4))
    print(f"Minkowski 時空的黎曼張量全為零: {all_zero}")
    print("確認：平坦時空的曲率為零")

    print("\n\n2. 二維球面度規")
    print("-" * 40)
    theta, phi = symbols('theta phi')
    coords_sph = [theta, phi]
    
    g_sph = [[1, 0],
             [0, sin(theta)**2]]
    
    Gamma_sph = christoffel_symbols(g_sph, coords_sph)
    R_sph = riemann_tensor(Gamma_sph, coords_sph)
    
    print("二維球面的黎曼張量分量:")
    print(f"R^θ_θθθ = {R_sph[0][0][0][0]}")
    print(f"R^θ_θφφ = {R_sph[0][0][1][1]}")
    print(f"R^φ_θθφ = {R_sph[1][0][0][1]}")
    print(f"R^φ_θφθ = {R_sph[1][0][1][0]}")
    
    Ricci_sph = ricci_tensor(R_sph, 2)
    print(f"\n里奇張量 R_jk:")
    for j in range(2):
        print(f"  [{Ricci_sph[j][0]}, {Ricci_sph[j][1]}]")
    
    R_scalar = ricci_scalar(Ricci_sph, g_sph, coords_sph)
    print(f"\n里奇標量 R = {R_scalar}")
    print("對於單位球面，R = 2")

    print("\n\n3. 里奇張量與里奇標量")
    print("-" * 40)
    print("里奇張量：R_ij = R^k_ikj")
    print("里奇標量：R = g^ij * R_ij")
    print("這些量描述了時空的局部曲率")

    print("\n" + "=" * 60)
    print("黎曼曲率張量計算完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
