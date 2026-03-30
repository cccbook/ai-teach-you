#!/usr/bin/env python3
"""
洛倫茲轉換 - 第4章第1節
使用 SymPy 計算洛倫茲轉換矩陣
"""

import sympy as sp
from sympy import symbols, sqrt, simplify, Matrix


def lorentz_boost(vx, vy=0, vz=0):
    """
    創建沿 x 方向的洛倫茲 boost 矩陣
    """
    c = symbols('c', positive=True)
    beta = vx / c
    gamma = 1 / sqrt(1 - beta**2)
    
    Lambda = Matrix([
        [gamma, -gamma*beta, 0, 0],
        [-gamma*beta, gamma, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    return Lambda, gamma, beta


def main():
    print("=" * 60)
    print("洛倫茲轉換 - Chapter 4.1")
    print("=" * 60)

    print("\n1. 洛倫茲轉換矩陣")
    print("-" * 40)
    v, c = symbols('v c', positive=True)
    beta = v / c
    gamma = 1 / sqrt(1 - beta**2)
    
    Lambda = Matrix([
        [gamma, -gamma*beta, 0, 0],
        [-gamma*beta, gamma, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    
    print("洛倫茲 boost (沿 x 方向):")
    print(f"Λ = \n{Lambda}")

    print("\n2. 洛倫茲因子")
    print("-" * 40)
    print(f"γ = {gamma}")
    print(f"β = v/c")
    
    for v_ratio in [0.0, 0.5, 0.8, 0.9, 0.99]:
        gamma_val = gamma.subs(v, v_ratio*c)
        print(f"v = {v_ratio}c → γ = {float(simplify(gamma_val)):.4f}")

    print("\n3. 時空座標轉換")
    print("-" * 40)
    ct, x, y, z = symbols('ct x y z')
    X = Matrix([ct, x, y, z])
    
    v_val = 0.8 * c
    Lambda_val = Lambda.subs(v, v_val)
    
    X_prime = Lambda_val * X
    print(f"原座標: (ct, x, y, z) = ({ct}, {x}, {y}, {z})")
    print(f"轉換後:")
    print(f"ct' = {X_prime[0]}")
    print(f"x' = {X_prime[1]}")

    print("\n4. 速度加成公式")
    print("-" * 40)
    u, v, c = symbols('u v c', positive=True)
    u_prime = (u - v) / (1 - u*v/c**2)
    print(f"相對論速度加成公式:")
    print(f"u' = (u - v) / (1 - uv/c²)")
    print(f"當 u = 0.9c, v = 0.9c 時:")
    print(f"u' = {simplify(u_prime.subs({u: 0.9*c, v: 0.9*c}))} ≈ {float(simplify(u_prime.subs({u: 0.9*c, v: 0.9*c}))):.4f}c")

    print("\n5. 時空圖 (Minkowski Diagram)")
    print("-" * 40)
    print("""
時空圖說明：
- 垂直軸：ct (時間)
- 水平軸：x (空間)

特殊線：
- 光Worldline: ct = ±x (45度線)
- 同時線: ct' = 常數 (相對於運動觀察者)
- 固有長度線: x' = 常數
""")

    print("\n6. 轉換範例")
    print("-" * 40)
    ct, x = 10, 4
    v = 0.6 * 3e8
    c = 3e8
    gamma = 1 / sqrt(1 - (v/c)**2)
    
    ct_prime = gamma * (ct - v*x/c)
    x_prime = gamma * (x - v*ct/c)
    
    print(f"原始事件: (ct, x) = ({ct}, {x})")
    print(f"觀察者速度: v = {v:.2e} m/s (β = {v/c:.1f})")
    print(f"γ = {gamma:.4f}")
    print(f"轉換後: (ct', x') = ({ct_prime:.4f}, {x_prime:.4f})")

    print("\n" + "=" * 60)
    print("洛倫茲轉換完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
