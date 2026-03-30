#!/usr/bin/env python3
"""
史瓦西解與黑洞 - 第9章第1節
"""

import sympy as sp
from sympy import symbols, sqrt, simplify, sin, cos


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
    print("史瓦西解與黑洞 - Chapter 9.1")
    print("=" * 60)

    print("\n1. 史瓦西度規")
    print("-" * 40)
    print("""1916年，卡爾·史瓦西求得愛因斯坦場方程式的第一個精確解：

ds² = -(1-2GM/rc²)c²dt² + (1-2GM/rc²)^-1dr² + r²dΩ²

其中 dΩ² = dθ² + sin²θ dφ²

這個度規描述：靜止、球對稱、無旋轉的真空時空""")

    print("\n2. 史瓦西度規的 SymPy 表示")
    print("-" * 40)
    t, r, theta, phi = symbols('t r theta phi')
    M, G, c = symbols('M G c', positive=True)
    
    Rs = 2 * M * G / c**2
    print(f"史瓦西半徑: R_s = 2GM/c² = {Rs}")

    print("\n3. 史瓦西度規的克里斯多費符號")
    print("-" * 40)
    coords = [t, r, theta, phi]
    
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
    
    Gamma = christoffel_symbols(metric, coords)
    
    print("非零克里斯多費符號範例：")
    print(f"Γ^t_{{tr}} = Γ^t_{{rt}} = {Gamma[0][1][0]}")
    print(f"Γ^r_{{tt}} = {Gamma[1][0][0]}")
    print(f"Γ^r_{{rr}} = {Gamma[1][1][1]}")
    print(f"Γ^r_{{θθ}} = {Gamma[1][2][2]}")
    print(f"Γ^r_{{φφ}} = {Gamma[1][3][3]}")

    print("\n4. 事件視界")
    print("-" * 40)
    print("""事件視界（Event Horizon）：
- 半徑 R_s = 2GM/c²
- 任何物質或訊號都無法從內部逃出
- 黑洞的「表面」

對於太陽：R_s ≈ 3 km
對於地球：R_s ≈ 9 mm""")

    print("\n5. 奇點")
    print("-" * 40)
    print("""史瓦西度規的兩個奇點：

1. r = R_s：坐標奇點（可以通過坐標變換消除）
   → 事件視界

2. r = 0：真實的時空奇點
   → 物質被無限量壓縮
   → 廣義相對論在此失效，需要量子重力理論""")

    print("\n6. 黑洞週期表")
    print("-" * 40)
    print("""
| 類型         | 質量     | 旋轉     | 電荷    |
|--------------|----------|----------|---------|
| 史瓦西       | 有       | 無       | 無      |
| 萊斯納-諾德斯特朗 | 有   | 無       | 有      |
| 克爾         | 有       | 有       | 無      |
| 克爾-紐曼    | 有       | 有       | 有      |
""")

    print("\n7. 引力時間膨脹")
    print("-" * 40)
    print("在距離 r 處的時間膨脹：")
    dt_proper = sqrt(1 - Rs/r)
    print(f"dτ/dt = √(1 - R_s/r) = {dt_proper}")
    print("越靠近黑洞，時間越慢！")

    r_val = 10  # 以史瓦西半徑為單位
    print(f"\nr >> R_s 時，dτ/dt ≈ 1")
    print(f"r = 2R_s 時，dτ/dt = √(1-1/2) = 0.707")

    print("\n" + "=" * 60)
    print("史瓦西解完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
