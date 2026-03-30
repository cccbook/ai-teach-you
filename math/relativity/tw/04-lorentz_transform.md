# 第 4 章：洛倫茲轉換與時空圖

## 4.1 洛倫茲轉換

洛倫茲轉換是連接不同慣性參考系的數學工具。

### 4.1.1 洛倫茲轉換矩陣

對於沿 x 方向以速度 v 運動的參考系：

[程式檔案：04-1-lorentz-transform.py](../_code/04/04-1-lorentz-transform.py)

```python
import sympy as sp
from sympy import symbols, sqrt, Matrix

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
```

### 4.1.2 洛倫茲因子

$$\gamma = \frac{1}{\sqrt{1 - v^2/c^2}}$$

[程式檔案：04-1-lorentz-transform.py](../_code/04/04-1-lorentz-transform.py)

```python
print(f"γ = {gamma}")

for v_ratio in [0.0, 0.5, 0.8, 0.9, 0.99]:
    gamma_val = gamma.subs(v, v_ratio*c)
    print(f"v = {v_ratio}c → γ = {float(gamma_val):.4f}")
```

## 4.2 時空座標轉換

### 4.2.1 座標轉換公式

$$ct' = \gamma(ct - \beta x)$$
$$x' = \gamma(x - \beta ct)$$

[程式檔案：04-1-lorentz-transform.py](../_code/04/04-1-lorentz-transform.py)

```python
ct, x, y, z = symbols('ct x y z')
X = Matrix([ct, x, y, z])

v_val = 0.8 * c
Lambda_val = Lambda.subs(v, v_val)

X_prime = Lambda_val * X
print(f"ct' = {X_prime[0]}")
print(f"x' = {X_prime[1]}")
```

### 4.2.2 數值範例

[程式檔案：04-1-lorentz-transform.py](../_code/04/04-1-lorentz-transform.py)

```python
ct, x = 10, 4
v = 0.6 * 3e8
c = 3e8
gamma = 1 / sqrt(1 - (v/c)**2)

ct_prime = gamma * (ct - v*x/c)
x_prime = gamma * (x - v*ct/c)

print(f"原始事件: (ct, x) = ({ct}, {x})")
print(f"γ = {gamma:.4f}")
print(f"轉換後: (ct', x') = ({ct_prime:.4f}, {x_prime:.4f})")
```

## 4.3 速度加成公式

相對論中的速度不能簡單相加！

### 4.3.1 公式

$$u' = \frac{u - v}{1 - uv/c^2}$$

[程式檔案：04-1-lorentz-transform.py](../_code/04/04-1-lorentz-transform.py)

```python
u, v, c = symbols('u v c', positive=True)
u_prime = (u - v) / (1 - u*v/c**2)
print(f"u' = (u - v) / (1 - uv/c²)")

# 範例
u_prime_val = u_prime.subs({u: 0.9*c, v: 0.9*c})
print(f"當 u = 0.9c, v = 0.9c 時: u' = {float(u_prime_val):.4f}c")
```

## 4.4 時空圖 (Minkowski Diagram)

時空圖是理解相對論的有力工具。

### 4.4.1 圖的結構

- **垂直軸**: ct (時間)
- **水平軸**: x (空間)

### 4.4.2 特殊線

[程式檔案：04-1-lorentz-transform.py](../_code/04/04-1-lorentz-transform.py)

```python
print("""
時空圖說明：
- 垂直軸：ct (時間)
- 水平軸：x (空間)

特殊線：
- 光Worldline: ct = ±x (45度線)
- 同時線: ct' = 常數 (相對於運動觀察者)
- 固有長度線: x' = 常數
""")
```

### 4.4.3 光錐

光錐結構是相對論因果性的關鍵：
- **未來光錐**: 光可以到達的區域
- **過去光錐**: 光可以來自的區域
- **類空間**: 因果無關的區域

## 4.5 四維向量

### 4.5.1 四維位置

$$x^\mu = (ct, x, y, z)$$

### 4.5.2 四維速度

$$U^\mu = \frac{dx^\mu}{d\tau} = \gamma(c, \vec{v})$$

### 4.5.3 四維動量

$$p^\mu = mU^\mu = (\gamma mc, \gamma m\vec{v})$$

## 4.6 時空的幾何性質

### 4.6.1 不變量

在洛倫茲轉換下不改變的量：
- 時空間隔 $ds^2$
- 固有時間 $d\tau$
- 粒子質量 $m$

### 4.6.2 因果結構

時空圖清楚地顯示了因果關係和光錐結構。

## 習題

1. 證明兩個洛倫茲轉換的乘積仍是洛倫茲轉換。
2. 計算兩個物體各以 0.9c 速度相向而行時的相對速度。
3. 畫出一個時空圖，顯示兩個事件的因果關係。
