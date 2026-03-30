#!/usr/bin/env python3
"""
測地線與光子路徑 - 第10章第1節
"""

import sympy as sp
from sympy import symbols, sqrt, simplify, diff, Function


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
    print("測地線與光子路徑 - Chapter 10.1")
    print("=" * 60)

    print("\n1. 測地線方程式")
    print("-" * 40)
    print("""測地線是時空中「直線」的一般化：

d²x^μ/dτ² + Γ^μ_αβ(dx^α/dτ)(dx^β/dτ) = 0

這是自由粒子（或光子）的運動方程式：
- 在無重力時：直線運動
- 在重力場中：沿時空曲率運動

「物質告訴時空如何彎曲，時空告訴物質如何運動」""")

    print("\n2. 測地線方程式的推導")
    print("-" * 40)
    print("""測地線方程式可以從變分原理推導：

δ∫ ds = 0

其中 ds² = g_μν dx^μ dx^ν

這相當於最小化粒子在時空中行進的「距離」""")

    print("\n3. 光子在重力場中的偏折")
    print("-" * 40)
    print("""光子在重力場中的偏折是廣義相對論的重要預言：

1919年愛丁頓觀測日食，驗證了光線經過太陽時會偏折
偏折角：α = 4GM/(rc²)

對於太陽：α ≈ 1.75 角秒""")

    M = 1.989e30  # 太陽質量 kg
    G = 6.674e-11
    c = 3e8
    r_sun = 6.96e8  # 太陽半徑
    
    alpha = 4 * G * M / (r_sun * c**2)
    alpha_arcsec = alpha * 206265  # 轉換為角秒
    print(f"\n計算：α = 4GM/(rc²)")
    print(f"     = {alpha:.4e} rad")
    print(f"     = {alpha_arcsec:.2f} 角秒")

    print("\n4. 光線的零測地線")
    print("-" * 40)
    print("""對於光子，ds² = 0：

光子世界線滿足：
g_μν dx^μ dx^ν = 0

這稱為「零測地線」(null geodesic)""")

    print("\n5. 事件視界與光子")
    print("-" * 40)
    print("""在史瓦西時空中：

光子軌道：
- r < 3GM/c²：光子無法穩定軌道
- r = 3GM/c²：光子球 (photon sphere)
- r > 3GM/c²：光子可以逃逸

對於史瓦西黑洞，光子球位於 1.5 倍史瓦西半徑處""")

    print("\n6. 引力透鏡效應")
    print("-" * 40)
    print("""引力透鏡效應的應用：

1. 宇宙學：測量暗物質分佈
2. 類星體：觀測遙遠星系的放大影像
3. 恆星：尋找系外行星

愛因斯坦環：當光源、透鏡、觀測者完全對齊時""")

    print("\n7. Shapiro 延遲")
    print("-" * 40)
    print("""Shapiro 延遲（1964）：

當雷達信號近距離掠過大質量物體時，
傳播時間會比平坦時空更長。

延遲公式：
Δt = (4GM/c³) ln(4r_e r_s / b²)

其中 b 是撞擊參數""")

    print("\n" + "=" * 60)
    print("測地線完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
