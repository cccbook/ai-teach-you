#!/usr/bin/env python3
"""
狹義相對論動力學 - 第6章第1節
"""

import sympy as sp
from sympy import symbols, sqrt, simplify


def main():
    print("=" * 60)
    print("狹義相對論動力學 - Chapter 6.1")
    print("=" * 60)

    print("\n1. 洛倫茲力方程式")
    print("-" * 40)
    print("""
相對論性洛倫茲力：
dp^μ/dτ = q F^μν U_ν

其中：
- p^μ: 四維動量
- τ: 固有時間
- q: 電荷
- F^μν: 電場張量
- U_ν: 四維速度
""")

    print("\n2. 電場張量")
    print("-" * 40)
    print("""電場張量 F^μν:
     |  0   -E_x/c  -E_y/c  -E_z/c |
F^μν=| E_x/c   0    -B_z    B_y  |
     | E_y/c  B_z     0    -B_x  |
     | E_z/c -B_y   B_x     0   |
""")

    print("\n3. 質能關係與粒子加速")
    print("-" * 40)
    m, c = symbols('m c', positive=True)
    v = symbols('v', positive=True)
    gamma = 1 / sqrt(1 - v**2/c**2)
    
    p = gamma * m * v
    E = gamma * m * c**2
    
    print(f"動量: p = {p}")
    print(f"能量: E = {E}")

    print("\n4. 粒子的極限速度")
    print("-" * 40)
    print("根據相對論，任何有質量粒子的速度都不能達到光速！")
    print("當 v → c 時，γ → ∞，所需的能量也趨近無窮大")
    
    for v_ratio in [0.5, 0.9, 0.99, 0.999, 0.9999]:
        gamma_val = float(gamma.subs(v, v_ratio*c))
        print(f"v = {v_ratio}c → γ = {gamma_val:.2f}")

    print("\n5. 輕子型粒子")
    print("-" * 40)
    m_e = 9.11e-31  # kg
    m_p = 1.67e-27  # kg
    c_val = 3e8
    
    E_e = m_e * c_val**2 / 1.6e-19  # MeV
    E_p = m_p * c_val**2 / 1.6e-19  # MeV
    
    print(f"電子質量: {m_e:.3e} kg = {E_e:.3f} MeV/c²")
    print(f"質子質量: {m_p:.3e} kg = {E_p:.3f} MeV/c²")

    print("\n6. 能量單位轉換")
    print("-" * 40)
    print("1 eV = 1.602 × 10^-19 焦耳")
    print("1 GeV = 10^9 eV")
    
    E_GeV = 1
    E_joules = E_GeV * 1e9 * 1.602e-19
    print(f"1 GeV = {E_joules:.2e} 焦耳")

    print("\n" + "=" * 60)
    print("狹義相對論動力學完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
