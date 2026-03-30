# 第 13 章：宇宙學模型：FLRW 度規

## 13.1 FLRW 度規

FLRW (Friedmann-Lemaître-Robertson-Walker) 度規描述均勻各向同性膨脹/收縮的宇宙：

$$ds^2 = -c^2dt^2 + a(t)^2 \left[\frac{dr^2}{1-kr^2} + r^2d\Omega^2\right]$$

[程式檔案：13-1-cosmology-flrw.py](../_code/13/13-1-cosmology-flrw.py)

```python
print("""FLRW 度規：

ds² = -c²dt² + a(t)² [dr²/(1-kr²) + r²dΩ²]

其中：
- a(t): 宇宙尺度因子
- k: 空間曲率 (-1, 0, +1)
""")
```

## 13.2 宇宙學常數

[程式檔案：13-1-cosmology-flrw.py](../_code/13/13-1-cosmology-flrw.py)

```python
H0 = 67.4  # km/s/Mpc
print(f"哈伯常數: H₀ = {H0} km/s/Mpc")
```

## 13.3 宇宙學紅移

$$z = \frac{1}{a} - 1$$

## 13.4 弗里德曼方程式

$$\left(\frac{\ddot{a}}{a}\right) = -\frac{4\pi G}{3}(\rho + \frac{3P}{c^2}) + \frac{\Lambda c^2}{3}$$

$$\left(\frac{\dot{a}}{a}\right)^2 = \frac{8\pi G}{3}\rho - \frac{kc^2}{a^2} + \frac{\Lambda c^2}{3}$$

## 13.5 宇宙組成 (Planck 2018)

[程式檔案：13-1-cosmology-flrw.py](../_code/13/13-1-cosmology-flrw.py)

```python
print("""
- 暗能量 (Λ): Ω_Λ ≈ 0.685
- 暗物質: Ω_dm ≈ 0.315  
- 普通物質: Ω_b ≈ 0.049
""")
```
