#!/usr/bin/env python3
"""
時空度規與克里斯多費符號 - 第12章第1節
"""

import sympy as sp
from sympy import symbols, sqrt, simplify, sin, cos, diff


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


def main():
    print("=" * 60)
    print("時空度規與克里斯多費符號 - Chapter 12.1")
    print("=" * 60)

    print("\n1. 常見時空度規")
    print("-" * 40)
    print("""
1. 閔考斯基度規 (平坦時空)
   ds² = -c²dt² + dx² + dy² + dz²

2. 史瓦西度規 (球對稱靜止黑洞)
   ds² = -(1-2GM/rc²)c²dt² + (1-2GM/rc²)^-1dr² + r²dΩ²

3. Rindler 度規 (加速觀察者)
   ds² = -(ξ²/c²)dξ² + dξ⊥² + c²dτ²

4. FLRW 度規 (宇宙學)
   ds² = -c²dt² + a(t)² [dr²/(1-kr²) + r²dΩ²]
""")

    print("\n2. 史瓦西度規")
    print("-" * 40)
    t, r, theta, phi = symbols('t r theta phi')
    M, G, c = symbols('M G c', positive=True)
    
    Rs = 2 * M * G / c**2
    g_tt = -(1 - Rs/r)
    g_rr = 1 / (1 - Rs/r)
    g_thth = r**2
    g_phiph = r**2 * sin(theta)**2
    
    metric = [
        [g_tt*c**2, 0, 0, 0],
        [0, g_rr, 0, 0],
        [0, 0, g_thth, 0],
        [0, 0, 0, g_phiph]
    ]
    
    print("史瓦西度規分量:")
    print(f"g_tt = {g_tt*c**2}")
    print(f"g_rr = {g_rr}")
    print(f"g_θθ = {g_thth}")
    print(f"g_φφ = {g_phiph}")

    print("\n3. 克里斯多費符號")
    print("-" * 40)
    coords = [t, r, theta, phi]
    Gamma = christoffel_symbols(metric, coords)
    
    print("史瓦西時空的克里斯多費符號:")
    print(f"Γ^t_{{tr}} = {Gamma[0][1][0]}")
    print(f"Γ^r_{{tt}} = {Gamma[1][0][0]}")
    print(f"Γ^r_{{rr}} = {Gamma[1][1][1]}")
    print(f"Γ^r_{{θθ}} = {Gamma[1][2][2]}")
    print(f"Γ^r_{{φφ}} = {Gamma[1][3][3]}")

    print("\n4. 坐標系選擇")
    print("-" * 40)
    print("""
不同坐標系適合不同物理情況：

1. 史瓦西坐標 (t, r, θ, φ)
   - 最簡單
   - 在 r = Rs 有坐標奇點

2. Eddington-Finkelstein 坐標
   - 穿過事件視界不會有奇異

3. Kruskal-Szekeres 坐標
   - 整個時空可以用單一坐標覆蓋
   - 光錐結構清晰

4. Gullstrand-Painlevé 座標
   - 落體觀察者的視角
   - 空間像是在塌縮
""")

    print("\n5. 固有距離與固有時間")
    print("-" * 40)
    print("固有距離: dl = √(g_ij dx^i dx^j)")
    print("固有時間: dτ = √(-g_00) dt")
    print("\n在靜止觀察者的固有時間:")
    dtau_dt = sqrt(1 - Rs/r)
    print(f"dτ/dt = √(1 - Rs/r) = {dtau_dt}")

    print("\n" + "=" * 60)
    print("時空度規與克里斯多費符號完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
