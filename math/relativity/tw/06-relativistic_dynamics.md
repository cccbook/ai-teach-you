# 第 6 章：狹義相對論動力學

## 6.1 洛倫茲力方程式

[程式檔案：06-1-relativistic-dynamics.py](../_code/06/06-1-relativistic-dynamics.py)

```python
print("""
相對論性洛倫茲力：
dp^μ/dτ = q F^μν U_ν
""")
```

## 6.2 電場張量

[程式檔案：06-1-relativistic-dynamics.py](../_code/06/06-1-relativistic-dynamics.py)

```python
print("""電場張量 F^μν:
     |  0   -E_x/c  -E_y/c  -E_z/c |
F^μν=| E_x/c   0    -B_z    B_y  |
     | E_y/c  B_z     0    -B_x  |
     | E_z/c -B_y   B_x     0   |
""")
```

## 6.3 粒子的極限速度

[程式檔案：06-1-relativistic-dynamics.py](../_code/06/06-1-relativistic-dynamics.py)

```python
for v_ratio in [0.5, 0.9, 0.99, 0.999, 0.9999]:
    gamma_val = float(gamma.subs(v, v_ratio*c))
    print(f"v = {v_ratio}c → γ = {gamma_val:.2f}")
```

## 習題

1. 計算在 LHC 中質子的動能（能量 7 TeV）。
