#!/usr/bin/env python3
"""
愛因斯坦張量計算 - 第11章第1節
"""

import sympy as sp
from sympy import symbols, sqrt, simplify, sin, diff


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
                    dg_i = sp.diff(metric[l][j], coords[i])
                    dg_j = sp.diff(metric[i][l], coords[j])
                    dg_l = sp.diff(metric[i][j], coords[l])
                    sum_term += (dg_i + dg_j - dg_l) * g_inv[k, l]
                Gamma[k][i][j] = sp.simplify(sum_term / 2)
    
    return Gamma


def riemann_tensor(Gamma, coords):
    """計算黎曼曲率張量"""
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
    """計算里奇張量"""
    Ricci = [[0]*n for _ in range(n)]
    for j in range(n):
        for k in range(n):
            Ricci[j][k] = simplify(sum(R[i][j][k][i] for i in range(n)))
    return Ricci


def ricci_scalar(Ricci, metric, coords):
    """計算里奇標量"""
    g_inv = sp.Matrix(metric).inv()
    n = len(coords)
    R = 0
    for j in range(n):
        for k in range(n):
            R += g_inv[j, k] * Ricci[j][k]
    return simplify(R)


def einstein_tensor(Ricci, R_scalar, metric, coords):
    """計算愛因斯坦張量"""
    n = len(coords)
    g = sp.Matrix(metric)
    
    G = [[0]*n for _ in range(n)]
    for mu in range(n):
        for nu in range(n):
            g_elem = metric[mu][nu]
            G[mu][nu] = simplify(Ricci[mu][nu] - R_scalar * g_elem / 2)
    
    return G


def main():
    print("=" * 60)
    print("愛因斯坦張量計算 - Chapter 11.1")
    print("=" * 60)

    print("\n1. 愛因斯坦張量定義")
    print("-" * 40)
    print("""愛因斯坦張量：

G_μν = R_μν - (1/2) g_μν R

這是廣義相對論中最重要的張量之一！
它自動滿足協變守恆 ▽^μ G_μν = 0""")

    print("\n2. Minkowski 時空 (真空)")
    print("-" * 40)
    ct, x, y, z = symbols('ct x y z')
    coords = [ct, x, y, z]
    
    eta = [[-1, 0, 0, 0],
           [0, 1, 0, 0],
           [0, 0, 1, 0],
           [0, 0, 0, 1]]
    
    Gamma = christoffel_symbols(eta, coords)
    R_tensor = riemann_tensor(Gamma, coords)
    Ricci = ricci_tensor(R_tensor, 4)
    R_scalar = ricci_scalar(Ricci, eta, coords)
    G = einstein_tensor(Ricci, R_scalar, eta, coords)
    
    print("Minkowski 時空的愛因斯坦張量:")
    print("所有分量都為零！")
    all_zero = all(G[i][j] == 0 for i in range(4) for j in range(4))
    print(f"G_μν = 0: {all_zero}")

    print("\n3. 二維球面")
    print("-" * 40)
    theta, phi = symbols('theta phi')
    coords_sph = [theta, phi]
    
    g_sph = [[1, 0],
             [0, sin(theta)**2]]
    
    Gamma_sph = christoffel_symbols(g_sph, coords_sph)
    R_sph_tensor = riemann_tensor(Gamma_sph, coords_sph)
    Ricci_sph = ricci_tensor(R_sph_tensor, 2)
    R_sph_scalar = ricci_scalar(Ricci_sph, g_sph, coords_sph)
    G_sph = einstein_tensor(Ricci_sph, R_sph_scalar, g_sph, coords_sph)
    
    print(f"二維球面的里奇標量: R = {R_sph_scalar}")
    print(f"愛因斯坦張量:")
    print(sp.Matrix(G_sph))

    print("\n4. 真空場方程式驗證")
    print("-" * 40)
    print("在真空中，T_μν = 0，")
    print("愛因斯坦方程式化為 G_μν = 0")
    print("即 R_μν = 0")
    print("\n史瓦西解就是真空方程式的解！")

    print("\n5. 宇宙學常數項")
    print("-" * 40)
    Lambda = symbols('Lambda')
    print("含宇宙學常數的方程式：")
    print("G_μν + Λg_μν = (8πG/c⁴) T_μν")
    print(f"\n對於真空：G_μν = -Λg_μν")

    print("\n" + "=" * 60)
    print("愛因斯坦張量計算完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
