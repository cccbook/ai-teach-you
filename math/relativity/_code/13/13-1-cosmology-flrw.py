#!/usr/bin/env python3
"""
宇宙學模型：FLRW 度規 - 第13章第1節
"""

import sympy as sp
from sympy import symbols, sqrt, simplify, sin, Function


def main():
    print("=" * 60)
    print("宇宙學模型：FLRW 度規 - Chapter 13.1")
    print("=" * 60)

    print("\n1. FLRW 度規")
    print("-" * 40)
    print("""FLRW (Friedmann-Lemaître-Robertson-Walker) 度規
描述均勻各向同性膨脹/收縮的宇宙：

ds² = -c²dt² + a(t)² [dr²/(1-kr²) + r²dΩ²]

其中：
- a(t): 宇宙尺度因子
- k: 空間曲率 (-1, 0, +1)
""")

    print("\n2. 宇宙學常數")
    print("-" * 40)
    H0 = 67.4  # km/s/Mpc (Planck 2018)
    c = 3e5  # km/s
    
    H0_inv = c / H0  # Hubble distance
    print(f"哈伯常數: H₀ = {H0} km/s/Mpc")
    print(f"哈伯距離: c/H₀ = {H0_inv:.1f} Mpc")
    print(f"           = {H0_inv * 3.26e6:.1f} 光年")

    print("\n3. 宇宙年齡")
    print("-" * 40)
    age = 1 / H0  # in Gyr roughly
    print(f"哈伯時間: t_H = 1/H₀ ≈ {1/H0:.1f} Gyr")
    print("（宇宙年齡 ≈ 13.8 Gyr）")

    print("\n4. 宇宙學紅移")
    print("-" * 40)
    a = symbols('a')
    z = 1/a - 1
    print("紅移與尺度因子的關係：")
    print("z = 1/a - 1")
    print("\n常見紅移：")
    for a_val in [1.0, 0.5, 0.2, 0.1, 0.01]:
        z_val = float(z.subs(a, a_val))
        print(f"a = {a_val} → z = {z_val:.2f}")

    print("\n5. 弗里德曼方程式")
    print("-" * 40)
    print("""弗里德曼方程式（宇宙動力學）：

(ä/a) = -(4πG/3)(ρ + 3P/c²) + Λc²/3

(ẋ/a)² = (8πG/3)ρ - kc²/a² + Λc²/3

其中：
- ρ: 能量密度
- P: 壓力
- Λ: 宇宙學常數""")

    print("\n6. 臨界密度")
    print("-" * 40)
    G = 4.3e-6  # kpc M☉⁻¹ (km/s)²
    H0_val = 67.4
    
    rho_crit = 3 * H0_val**2 / (8 * 3.14 * G)
    print(f"臨界密度: ρ_c = 3H₀²/(8πG)")
    print(f"         = {rho_crit:.2f} M☉/kpc³")
    print(f"         ≈ {rho_crit * 2.8e77:.2e} 粒子/立方米")

    print("\n7. 宇宙組成")
    print("-" * 40)
    print("""
根據 Planck 2018 數據：

- 暗能量 (Λ): Ω_Λ ≈ 0.685
- 暗物質: Ω_dm ≈ 0.315  
- 普通物質: Ω_b ≈ 0.049
- 中微子: Ω_ν ≈ 0.003
- 光子: Ω_γ ≈ 0.00005
""")

    print("\n" + "=" * 60)
    print("FLRW 宇宙學完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
