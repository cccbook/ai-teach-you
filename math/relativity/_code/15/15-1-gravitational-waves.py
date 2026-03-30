#!/usr/bin/env python3
"""
重力波簡介 - 第15章第1節
"""

import numpy as np
import sympy as sp
from sympy import symbols, sqrt, sin, cos, simplify


def main():
    print("=" * 60)
    print("重力波簡介 - Chapter 15.1")
    print("=" * 60)

    print("\n1. 重力波是什麼？")
    print("-" * 40)
    print("""重力波是時空曲率的波動：
- 由加速質量產生
- 以光速傳播
- 攜帶能量和信息

2015年9月14日，LIGO 首次直接探測到重力波！
來源：兩個黑洞合併""")

    print("\n2. 愛因斯坦預言")
    print("-" * 40)
    print("""1916年，愛因斯坦從廣義相對論預言了重力波的存在。

線性近似下，弱重力波可以視為度規的擾動：
h_μν = 度規偏離平整的值

在 transverse-traceless (TT) 規範：
h_μν = 
| 0   0   0   0 |
| 0  h+  hx  0 |
| 0  hx  -h+ 0 |
| 0   0   0   0 |

兩種偏振：+ (plus) 和 × (cross)""")

    print("\n3. 重力波效應")
    print("-" * 40)
    print("""重力波穿過時，會造成時空畸變：

- 在一個方向拉伸
- 在垂直方向壓縮
- 效果非常微弱！

典型量級：
- 恆星合併：h ≈ 10^-21
- 銀河系內脈衝星：h ≈ 10^-24""")

    print("\n4. 重力波源")
    print("-" * 40)
    print("""
1. 雙星黑洞合併
   - 能量最大
   - LIGO/Virgo 主要探測源

2. 雙星中子星合併
   - 產生可見光對應體
   - 2017年 GW170817

3. 超新星爆發
   - 銀河系內約每數十年一次

4. 早期宇宙漲落
   - 宇宙學重力波背景
""")

    print("\n5. 探測器")
    print("-" * 40)
    print("""
地面探測器 (km 規模)：
- LIGO (美國): 4 km 臂長
- Virgo (義大利): 3 km
- KAGRA (日本): 3 km

太空探測器：
- LISA (計畫中): 250萬公里臂長
- Taiji (中國): 300萬公里

脈衝星計時陣列：
- NANOGrav
- PPTA
""")

    print("\n6. 重力波天文學")
    print("-" * 40)
    print("""重力波的探測開啟了新的天文學時代：

1. 黑洞的直接觀測
2. 雙星系統的精確測量
3. 中子星內部結構
4. 宇宙膨脹歷史

2017年諾貝爾物理學獎：
頒給 LIGO 的三位創始人""")

    print("\n7. 能量攜帶")
    print("-" * 40)
    print("""重力波攜帶的能量：

對於雙星系統：
P = (32/5) G⁴/c⁵ × (m₁² m₂² (m₁+m₂))/r⁵

LIGO 探測的黑洞合併：
- 總能量 ~ 3 M☉c²
- 峰值功率 ~ 10⁵⁶ erg/s""")

    print("\n" + "=" * 60)
    print("重力波簡介完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
