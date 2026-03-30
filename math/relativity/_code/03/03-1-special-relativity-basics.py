#!/usr/bin/env python3
"""
狹義相對論基礎 - 第3章第1節
介紹狹義相對論的兩個基本假設
"""

import sympy as sp
from sympy import symbols, sqrt, simplify, Rational


def main():
    print("=" * 60)
    print("狹義相對論基礎 - Chapter 3.1")
    print("=" * 60)

    print("\n1. 兩個基本假設")
    print("-" * 40)
    print("""狹義相對論的兩條基本假設：
    
1. 相對性原理：所有慣性參考系中，物理定律的形式都相同
2. 光速不變原理：真空中光速對所有觀察者都是常數 c

這兩條看似簡單的假設，徹底改變了我們對時空的理解！""")

    print("\n2. 光速數值")
    print("-" * 40)
    c = 299792458  # m/s
    print(f"光速 c = {c} m/s")
    print(f"通常近似為 c ≈ 3 × 10^8 m/s")

    print("\n3. 時間膨脹")
    print("-" * 40)
    v, t0, c = symbols('v t0 c', positive=True)
    gamma = 1 / sqrt(1 - v**2 / c**2)
    
    print(f"相對論時間膨脹公式：")
    print(f"Δt = γ Δτ")
    print(f"其中 γ = 1/√(1 - v²/c²)")
    print(f"\nγ = {gamma}")
    
    v_val = 0.9 * c
    gamma_val = gamma.subs(v, v_val)
    print(f"\n當 v = 0.9c 時，γ = {simplify(gamma_val)} ≈ {float(gamma_val):.4f}")
    print(f"這表示運動中的觀察者，時間慢了 {float(gamma_val):.2f} 倍！")

    print("\n4. 長度收縮")
    print("-" * 40)
    L0 = symbols('L0')
    L = L0 / gamma
    print(f"相對論長度收縮公式：")
    print(f"L = L₀/γ")
    print(f"當 v = 0.9c 時，L = L₀/{float(gamma_val):.4f}")
    print(f"物體在運動方向上的長度收縮為原本的 {float(1/gamma_val):.4f} 倍")

    print("\n5. 閔考斯基時空")
    print("-" * 40)
    print("""閔考斯基時空的度規：
    
η = diag(-1, 1, 1, 1)

時空間隔：
ds² = -c²dt² + dx² + dy² + dz²

分為三種類型：
- 類時間隔 (ds² < 0)：可達的因果事件
- 類空間隔 (ds² > 0)：不可達的因果事件  
- 類光間隔 (ds² = 0)：光的世界線""")

    print("\n6. 固有時間")
    print("-" * 40)
    t, x, y, z, ct = symbols('t x y z ct')
    ds2 = -c**2 * t**2 + x**2 + y**2 + z**2
    print(f"ds² = {ds2}")
    print(f"固有時間 τ = ∫ ds/c")

    print("\n" + "=" * 60)
    print("狹義相對論基礎完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
