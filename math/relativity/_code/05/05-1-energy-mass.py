#!/usr/bin/env python3
"""
質能方程式與四維向量 - 第5章第1節
"""

import sympy as sp
from sympy import symbols, sqrt, simplify, Matrix


def main():
    print("=" * 60)
    print("質能方程式與四維向量 - Chapter 5.1")
    print("=" * 60)

    print("\n1. 質能等價 (E = mc²)")
    print("-" * 40)
    m, c = symbols('m c', positive=True)
    E = m * c**2
    print(f"E = mc² = {E}")
    
    m_kg = 1  # kg
    c_val = 3e8  # m/s
    E_joules = m_kg * c_val**2
    print(f"1 kg 物質蘊含的能量: {E_joules:.2e} 焦耳")
    print(f"約等於 {E_joules/4.18e9:.2f} 噸 TNT 當量")

    print("\n2. 相對論動量")
    print("-" * 40)
    v = symbols('v', positive=True)
    gamma = 1 / sqrt(1 - v**2/c**2)
    p = gamma * m * v
    print(f"相對論動量: p = γmv")
    print(f"p = {p}")

    print("\n3. 相對論能量")
    print("-" * 40)
    E_total = gamma * m * c**2
    E_kin = (gamma - 1) * m * c**2
    print(f"總能量: E = γmc² = {E_total}")
    print(f"動能: K = (γ-1)mc² = {E_kin}")

    print("\n4. 四維動量向量")
    print("-" * 40)
    p_mu = Matrix([E/c, p, 0, 0])
    print(f"四維動量 p^μ = (E/c, p^x, p^y, p^z) = ")
    print(p_mu)
    
    p_sq = p_mu[0]**2 - p_mu[1]**2 - p_mu[2]**2 - p_mu[3]**2
    p_sq_simplified = simplify(p_sq)
    print(f"\np·p = {p_sq_simplified} = {(m*c)**2}")
    print("不變質量平方: p^μ p_μ = m²c²")

    print("\n5. 四維速度")
    print("-" * 40)
    tau = symbols('tau')
    U_mu = Matrix([gamma*c, gamma*v, 0, 0])
    print(f"四維速度 U^μ = γ(c, v) = ")
    print(U_mu)
    
    U_sq = U_mu[0]**2 - U_mu[1]**2 - U_mu[2]**2 - U_mu[3]**2
    print(f"U^μ U_μ = {simplify(U_sq)} = -c²")
    print("四維速度的大小永遠是 -c²")

    print("\n6. 能量-動量關係")
    print("-" * 40)
    E, p, m, c = symbols('E p m c')
    E_sq = (m*c**2)**2 + (p*c)**2
    print(f"E² = (mc²)² + (pc)²")
    print(f"E² = {E_sq}")
    print("這是相對論中的能量-動量關係式")

    print("\n" + "=" * 60)
    print("質能方程式完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
