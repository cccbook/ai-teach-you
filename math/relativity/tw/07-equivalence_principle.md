# 第 7 章：等效原理與重力幾何化

## 7.1 愛因斯坦的等效原理

[程式檔案：07-1-equivalence-principle.py](../_code/07/07-1-equivalence-principle.py)

```python
print("""愛因斯坦的等效原理：

1. 弱等效原理：慣性質量等於引力質量
   → 在均勻重力場中，所有物體以相同加速度下落

2. 強等效原理：在自由落體參考系中，
   所有物理定律都與在慣性系中相同
   → 無法通過局部實驗區分重力與加速參考系
""")
```

## 7.2 局部慣性參考系

[程式檔案：07-1-equivalence-principle.py](../_code/07/07-1-equivalence-principle.py)

```python
print("""在時空的每一點，都可以找到一個局部慣性參考系：
- 度規在該點可化為閔考斯基度規
- 克里斯多費符號在該點為零
- 該點附近沒有重力效應（局部）
""")
```

## 7.3 重力與時空曲率

[程式檔案：07-1-equivalence-principle.py](../_code/07/07-1-equivalence-principle.py)

```python
Phi = symbols('Phi')
c = symbols('c', positive=True)

g_00 = -(1 + 2*Phi/c**2)
g_ij = 1 - 2*Phi/c**2
print(f"弱場近似: g_00 = {g_00}")
print(f"弱場近似: g_ij = {g_ij}")
```

## 7.4 引力紅移

[程式檔案：07-1-equivalence-principle.py](../_code/07/07-1-equivalence-principle.py)

```python
g = 9.8  # m/s²
h = 100  # m
c_val = 3e8

delta_f_over_f = g * h / c_val**2
print(f"引力紅移公式 (近似): Δf/f ≈ gh/c²")
print(f"高度差 h = {h} m")
print(f"Δf/f = {delta_f_over_f:.2e}")
```

## 習題

1. 證明在均勻重力場中，所有物體加速度相同。
