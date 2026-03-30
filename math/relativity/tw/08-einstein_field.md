# 第 8 章：愛因斯坦場方程式

## 8.1 愛因斯坦場方程式

$$R_{\mu\nu} - \frac{1}{2}g_{\mu\nu}R + \Lambda g_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu}$$

[程式檔案：08-1-einstein-field.py](../_code/08/08-1-einstein-field.py)

```python
print("""愛因斯坦場方程式 (EFE)：

R_μν - (1/2)g_μν R + Λg_μν = (8πG/c⁴) T_μν
""")
```

## 8.2 方程式各項的物理意義

[程式檔案：08-1-einstein-field.py](../_code/08/08-1-einstein-field.py)

```python
print("""左邊（幾何側）：
- R_μν: 描述時空如何彎曲
- R: 曲率的標量強度
- Λ: 宇宙學常數

右邊（物質側）：
- T_μν: 能量、動量、壓力分佈
- 8πG/c⁴: 耦合常數，非常小 ≈ 2.08 × 10^-43 s²/m·kg
""")
```

## 8.3 真空場方程式

當 $T_{\mu\nu} = 0$ 時：

$$R_{\mu\nu} = \Lambda g_{\mu\nu}$$

若 $\Lambda = 0$：

$$R_{\mu\nu} = 0$$

## 8.4 史瓦西半徑

$$R_s = \frac{2GM}{c^2}$$

[程式檔案：08-1-einstein-field.py](../_code/08/08-1-einstein-field.py)

```python
Rs = 2 * M * G / c**2
M_sun = 1.989e30  # kg
Rs_sun = 2 * G * M_sun / c**2
print(f"太陽的史瓦西半徑：{Rs_sun/1000:.2f} km")
```

## 習題

1. 計算地球的史瓦西半徑。
