#!/usr/bin/env python3
"""
愛因斯坦場方程式 - 第8章第1節
"""

import sympy as sp
from sympy import symbols, sqrt, simplify, pi, Rational


def main():
    print("=" * 60)
    print("愛因斯坦場方程式 - Chapter 8.1")
    print("=" * 60)

    print("\n1. 愛因斯坦場方程式")
    print("-" * 40)
    print("""愛因斯坦場方程式 (EFE)：

R_μν - (1/2)g_μν R + Λg_μν = (8πG/c⁴) T_μν

或等價形式：
R_μν = (8πG/c⁴) (T_μν - (1/2)g_μν T) + Λg_μν

其中：
- R_μν: 里奇曲率張量
- R: 里奇標量
- g_μν: 度規張量
- Λ: 宇宙學常數
- T_μν: 能量-動量張量
- G: 萬有引力常數
- c: 光速""")

    print("\n2. 方程式各項的物理意義")
    print("-" * 40)
    print("""左邊（幾何側）：
- R_μν: 描述時空如何彎曲
- R: 曲率的標量強度
- Λ: 宇宙學常數（宇宙膨脹效應）

右邊（物質側）：
- T_μν: 能量、動量、壓力分佈
- 8πG/c⁴: 耦合常數，非常小
  ≈ 2.08 × 10^-43 s^2/m·kg""")

    print("\n3. 愛因斯坦張量")
    print("-" * 40)
    print("""愛因斯坦張量：
G_μν = R_μν - (1/2)g_μν R

特點：
- 是里奇張量的協變微分
- 自動滿足協變守恆 ▽^μ G_μν = 0
- 這保證了能量-動量守恆""")

    print("\n4. 真空場方程式")
    print("-" * 40)
    print("""當 T_μν = 0（真空中）：

R_μν - (1/2)g_μν R + Λg_μν = 0
→ R_μν = Λg_μν

若 Λ = 0：
→ R_μν = 0

真空愛因斯坦方程的解包括：
- 閔考斯基時空 (Minkowski)
- 史瓦西解 (Schwarzschild)
- 克爾解 (Kerr)""")

    print("\n5. 宇宙學常數")
    print("-" * 40)
    G = 6.674e-11  # m³/(kg·s²)
    c = 3e8  # m/s
    rho_crit = 3 * c**2 * 8 * pi * G / (8 * pi * G)**2
    
    print(f"宇宙學常數 Λ 的現代值：")
    print(f"Λ ≈ 1.1 × 10^-52 m^-2")
    print(f"\n宇宙臨界密度：")
    print(f"ρ_crit ≈ 9.5 × 10^-27 kg/m³")
    print(f"≈ 每立方米 5.9 個氫原子")

    print("\n6. 史瓦西半徑")
    print("-" * 40)
    M = symbols('M')
    Rs = 2 * M * G / c**2
    print(f"史瓦西半徑公式：")
    print(f"R_s = 2GM/c²")
    print(f"R_s = {Rs}")
    
    M_sun = 1.989e30  # kg
    Rs_sun = 2 * G * M_sun / c**2
    print(f"\n太陽的史瓦西半徑：{Rs_sun/1000:.2f} km")
    
    M_earth = 5.972e24
    Rs_earth = 2 * G * M_earth / c**2
    print(f"地球的史瓦西半徑：{Rs_earth:.2f} mm")

    print("\n" + "=" * 60)
    print("愛因斯坦場方程式完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
