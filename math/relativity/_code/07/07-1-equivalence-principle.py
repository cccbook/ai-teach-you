#!/usr/bin/env python3
"""
等效原理與重力幾何化 - 第7章第1節
"""

import sympy as sp
from sympy import symbols, sqrt, simplify, diff


def main():
    print("=" * 60)
    print("等效原理與重力幾何化 - Chapter 7.1")
    print("=" * 60)

    print("\n1. 等效原理")
    print("-" * 40)
    print("""愛因斯坦的等效原理：
    
1. 弱等效原理：慣性質量等於引力質量
   → 在均勻重力場中，所有物體以相同加速度下落

2. 強等效原理：在自由落體參考系中，
   所有物理定律都與在慣性系中相同
   → 無法通過局部實驗區分重力與加速參考系

這是廣義相對論的核心！""")

    print("\n2. 局部慣性參考系")
    print("-" * 40)
    print("""在時空的每一點，都可以找到一個局部慣性參考系：
- 度規在該點可化為閔考斯基度規
- 克里斯多費符號在該點為零
- 該點附近沒有重力效應（局部）

但在不同點之間，度規會有所不同，這就是重力！""")

    print("\n3. 重力與時空曲率")
    print("-" * 40)
    print("""愛因斯坦的革命性想法：

牛頓：重力是一種「力」
愛因斯坦：重力是時空的幾何性質

「物質告訴時空如何彎曲，時空告訴物質如何運動」

R_μν - (1/2)g_μν R = (8πG/c⁴) T_μν
（愛因斯坦場方程式）""")

    print("\n4. 度規與重力勢")
    print("-" * 40)
    Phi = symbols('Phi')
    c = symbols('c', positive=True)
    
    print("弱場近似下，度規與牛頓重力勢的關係：")
    print("g_00 ≈ -(1 + 2Φ/c²)")
    print("g_ij ≈ δ_ij(1 - 2Φ/c²)")
    
    g_00 = -(1 + 2*Phi/c**2)
    g_ij = 1 - 2*Phi/c**2
    print(f"\ng_00 = {g_00}")
    print(f"g_ij = {g_ij}")

    print("\n5. 潮汐力與曲率")
    print("-" * 40)
    print("""潮汐力的物理來源：
- 在不同位置，重力場的強度不同
- 這反映了時空的曲率

在廣義相對論中：
- 自由落體粒子沿測地線運動
- 測地線偏離來自時空曲率
- 這就是潮汐力的起源！""")

    print("\n6. 引力紅移")
    print("-" * 40)
    g = 9.8  # m/s²
    h = 100  # m (height difference)
    c_val = 3e8
    
    delta_f_over_f = g * h / c_val**2
    print(f"引力紅移公式 (近似): Δf/f ≈ gh/c²")
    print(f"高度差 h = {h} m")
    print(f"Δf/f = {delta_f_over_f:.2e}")
    print("頻率在較高處較高（藍移），較低處較低（紅移）")

    print("\n" + "=" * 60)
    print("等效原理完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
