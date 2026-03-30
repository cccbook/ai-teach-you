#!/usr/bin/env python3
"""
相對論性動力學模擬 - 第14章第1節
"""

import numpy as np


def lorentz_factor(beta):
    """計算洛倫茲因子 γ"""
    return 1.0 / np.sqrt(1 - beta**2)


def time_dilation(gamma):
    """時間膨脹"""
    return 1.0 / gamma


def length_contraction(gamma):
    """長度收縮"""
    return 1.0 / gamma


def relativistic_momentum(mass, velocity, c=1.0):
    """相對論動量 p = γmv"""
    beta = velocity / c
    gamma = lorentz_factor(beta)
    return gamma * mass * velocity


def relativistic_energy(mass, velocity, c=1.0):
    """相對論總能量 E = γmc²"""
    beta = velocity / c
    gamma = lorentz_factor(beta)
    return gamma * mass * c**2


def kinetic_energy(mass, velocity, c=1.0):
    """相對論動能 K = (γ-1)mc²"""
    beta = velocity / c
    gamma = lorentz_factor(beta)
    return (gamma - 1) * mass * c**2


def main():
    print("=" * 60)
    print("相對論性動力學模擬 - Chapter 14.1")
    print("=" * 60)

    c = 3e8  # m/s

    print("\n1. 洛倫茲因子")
    print("-" * 40)
    print("β = v/c")
    print("γ = 1/√(1-β²)")
    
    velocities = [0.0, 0.5, 0.8, 0.9, 0.95, 0.99, 0.999]
    print("\n速度\t\tγ\t\t時間膨脹\t長度收縮")
    print("-" * 60)
    for v in velocities:
        beta = v
        gamma = lorentz_factor(beta)
        dt = time_dilation(gamma)
        dl = length_contraction(gamma)
        print(f"{v:.3f}c\t\t{gamma:.4f}\t\t{dt:.4f}\t\t{dl:.4f}")

    print("\n2. 粒子加速模擬")
    print("-" * 40)
    mass = 1.0  # 電子質量單位
    
    print("粒子能量 vs 速度:")
    print("速度\t\tγ\t\t動量\t\t能量")
    print("-" * 60)
    for v in velocities:
        beta = v
        gamma = lorentz_factor(beta)
        p = relativistic_momentum(mass, v*c, c)
        E = relativistic_energy(mass, v*c, c)
        print(f"{v:.3f}c\t\t{gamma:.4f}\t\t{p:.4f}\t\t{E:.4f}")

    print("\n3. 能量單位轉換")
    print("-" * 40)
    eV_to_J = 1.602e-19
    
    m_e = 9.11e-31  # kg
    E_e = m_e * c**2 / eV_to_J
    print(f"電子靜止質量: {m_e:.3e} kg")
    print(f"             = {E_e:.2f} keV")
    print(f"             = {E_e/1e6:.4f} MeV")

    print("\n4. 粒子物理中的相對論效應")
    print("-" * 40)
    print("""
在 LHC (大型強子對撞機) 中：
- 質子加速到 0.99999999 c
- γ ≈ 7000
- 能量 ≈ 7 TeV

這遠超過質子靜止質量 (938 MeV)！
""")

    m_p = 1.67e-27  # kg
    gamma_LHC = 7000
    E_LHC = gamma_LHC * m_p * c**2 / eV_to_J / 1e12
    print(f"LHC 質子能量: {E_LHC:.1f} TeV")

    print("\n5. 雙生子悖論")
    print("-" * 40)
    v = 0.8 * c
    gamma = lorentz_factor(v/c)
    
    # 假設太空人旅行 1 年
    tau = 1  # 年
    t = gamma * tau
    
    print(f"速度: {v/c:.2f} c")
    print(f"γ: {gamma:.4f}")
    print(f"太空人時間 (τ): {tau:.1f} 年")
    print(f"地球時間 (t): {t:.4f} 年")
    print(f"太空人回到地球時，地球已過 {t-tau:.2f} 年！")

    print("\n" + "=" * 60)
    print("相對論性動力學模擬完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
