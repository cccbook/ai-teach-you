# 第 10 章：測地線與光子路徑

## 10.1 測地線方程式

測地線是時空中「直線」的一般化：

$$\frac{d^2x^\mu}{d\tau^2} + \Gamma^\mu_{\alpha\beta}\frac{dx^\alpha}{d\tau}\frac{dx^\beta}{d\tau} = 0$$

[程式檔案：10-1-geodesic.py](../_code/10/10-1-geodesic.py)

```python
print("""測地線方程式：

d²x^μ/dτ² + Γ^μ_αβ(dx^α/dτ)(dx^β/dτ) = 0
""")
```

## 10.2 光子在重力場中的偏折

$$\alpha = \frac{4GM}{rc^2}$$

[程式檔案：10-1-geodesic.py](../_code/10/10-1-geodesic.py)

```python
M = 1.989e30  # 太陽質量 kg
r_sun = 6.96e8  # 太陽半徑
alpha = 4 * G * M / (r_sun * c**2)
alpha_arcsec = alpha * 206265
print(f"光線偏折角: {alpha_arcsec:.2f} 角秒")
```

## 10.3 光子球

光子球位於 $r = 3GM/c^2$

## 10.4 Shapiro 延遲

$$\Delta t = \frac{4GM}{c^3} \ln\frac{4r_e r_s}{b^2}$$

## 習題

1. 計算光線經過太陽時的偏折角。
