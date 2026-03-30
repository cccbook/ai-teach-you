# 第 2 章：黎曼幾何與曲率

## 2.1 克里斯多費符號

克里斯多費符號（Christoffel Symbols）是描述時空彎曲的關鍵數學對象。它們不是張量，但在協變微分中起重要作用。

### 2.1.1 克里斯多費符號的定義

克里斯多費符號（又稱 Levi-Civita 連接係數）定義為：

$$\Gamma^k_{ij} = \frac{1}{2} g^{kl} \left( \frac{\partial g_{jl}}{\partial x^i} + \frac{\partial g_{il}}{\partial x^j} - \frac{\partial g_{ij}}{\partial x^l} \right)$$

[程式檔案：02-1-christoffel-symbols.py](../_code/02/02-1-christoffel-symbols.py)

```python
import sympy as sp
from sympy import symbols, sin, cos, simplify

def christoffel_symbols(metric, coords):
    """計算克里斯多費符號"""
    n = len(coords)
    g = sp.Matrix(metric)
    g_inv = g.inv()
    
    Gamma = [[[0]*n for _ in range(n)] for _ in range(n)]
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                sum_term = 0
                for l in range(n):
                    dg_i = sp.diff(metric[l][j], coords[i])
                    dg_j = sp.diff(metric[i][l], coords[j])
                    dg_l = sp.diff(metric[i][j], coords[l])
                    sum_term += (dg_i + dg_j - dg_l) * g_inv[k, l]
                Gamma[k][i][j] = simplify(sum_term / 2)
    
    return Gamma
```

### 2.1.2 二維球面度規的克里斯多費符號

球座標是廣義相對論中常用的座標系之一。

[程式檔案：02-1-christoffel-symbols.py](../_code/02/02-1-christoffel-symbols.py)

```python
theta, phi = symbols('theta phi')
coords = [theta, phi]

# 二維球面度規
g = [[1, 0], [0, sin(theta)**2]]

Gamma = christoffel_symbols(g, coords)
print(f"Γ^θ_{{φφ}} = {Gamma[0][1][1]}")  # -sin(θ)cos(θ)
print(f"Γ^φ_{{θφ}} = {Gamma[1][0][1]}")  # cot(θ)
```

### 2.1.3 Minkowski 時空的克里斯多費符號

平坦時空（Minkowski 時空）的克里斯多費符號全部為零！

[程式檔案：02-1-christoffel-symbols.py](../_code/02/02-1-christoffel-symbols.py)

```python
ct, x, y, z = symbols('ct x y z')
coords_mink = [ct, x, y, z]

# Minkowski 度規
eta = [[-1, 0, 0, 0],
       [0, 1, 0, 0],
       [0, 0, 1, 0],
       [0, 0, 0, 1]]

Gamma_mink = christoffel_symbols(eta, coords_mink)

# 驗證所有克里斯多費符號為零
all_zero = all(Gamma_mink[k][i][j] == 0 
               for k in range(4) for i in range(4) for j in range(4))
print(f"所有 Γ 為零: {all_zero}")
```

### 2.1.4 柱座標度規

[程式檔案：02-1-christoffel-symbols.py](../_code/02/02-1-christoffel-symbols.py)

```python
r, phi, z = symbols('r phi z')
coords_cyl = [r, phi, z]

g_cyl = [[1, 0, 0],
         [0, r**2, 0],
         [0, 0, 1]]

Gamma_cyl = christoffel_symbols(g_cyl, coords_cyl)
print(f"Γ^r_{{φφ}} = {Gamma_cyl[0][1][1]}")  # -r
print(f"Γ^φ_{{rφ}} = {Gamma_cyl[1][0][1]}")  # 1/r
```

## 2.2 黎曼曲率張量

黎曼曲率張量是描述時空彎曲的基本量。它告訴我們平行移動一個向量後，結果與原向量有多少差異。

### 2.2.1 黎曼曲率張量的定義

$$R^i_{jkl} = \frac{\partial \Gamma^i_{jl}}{\partial x^k} - \frac{\partial \Gamma^i_{jk}}{\partial x^l} + \Gamma^i_{mk}\Gamma^m_{jl} - \Gamma^i_{ml}\Gamma^m_{jk}$$

[程式檔案：02-2-riemann-curvature.py](../_code/02/02-2-riemann-curvature.py)

```python
def riemann_tensor(Gamma, coords):
    """計算黎曼曲率張量"""
    n = len(coords)
    R = [[[[0]*n for _ in range(n)] for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):
                    term1 = sp.diff(Gamma[i][j][l], coords[k])
                    term2 = sp.diff(Gamma[i][j][k], coords[l])
                    
                    sum_term = 0
                    for m in range(n):
                        sum_term += Gamma[i][m][k] * Gamma[m][j][l] - \
                                     Gamma[i][m][l] * Gamma[m][j][k]
                    
                    R[i][j][k][l] = sp.simplify(term1 - term2 + sum_term)
    
    return R
```

### 2.2.2 Minkowski 時空的黎曼張量

平坦時空的黎曼張量為零，這是廣義相對論的基本假設的體現。

[程式檔案：02-2-riemann-curvature.py](../_code/02/02-2-riemann-curvature.py)

```python
ct, x, y, z = symbols('ct x y z')
coords = [ct, x, y, z]

eta = [[-1, 0, 0, 0],
       [0, 1, 0, 0],
       [0, 0, 1, 0],
       [0, 0, 0, 1]]

Gamma = christoffel_symbols(eta, coords)
R = riemann_tensor(Gamma, coords)

all_zero = all(R[i][j][k][l] == 0 
               for i in range(4) for j in range(4) 
               for k in range(4) for l in range(4))
print(f"Minkowski 時空的黎曼張量全為零: {all_zero}")
```

### 2.2.3 二維球面的黎曼張量

球面的曲率是非零的，這導致球面上三角形內角和大於 180 度。

[程式檔案：02-2-riemann-curvature.py](../_code/02/02-2-riemann-curvature.py)

```python
theta, phi = symbols('theta phi')
coords_sph = [theta, phi]

g_sph = [[1, 0], [0, sin(theta)**2]]

Gamma_sph = christoffel_symbols(g_sph, coords_sph)
R_sph = riemann_tensor(Gamma_sph, coords_sph)

print(f"R^θ_{{θφφ}} = {R_sph[0][0][1][1]}")
print(f"R^φ_{{θθφ}} = {R_sph[1][0][0][1]}")
```

## 2.3 里奇張量與里奇標量

### 2.3.1 里奇張量

里奇張量是黎曼張量的一種收縮：

$$R_{ij} = R^k_{ikj}$$

[程式檔案：02-2-riemann-curvature.py](../_code/02/02-2-riemann-curvature.py)

```python
def ricci_tensor(R, n):
    """計算里奇張量"""
    Ricci = [[0]*n for _ in range(n)]
    for j in range(n):
        for k in range(n):
            Ricci[j][k] = sp.simplify(sum(R[i][j][k][i] for i in range(n)))
    return Ricci
```

### 2.3.2 里奇標量

里奇標量是里奇張量的又一次收縮：

$$R = g^{ij} R_{ij}$$

[程式檔案：02-2-riemann-curvature.py](../_code/02/02-2-riemann-curvature.py)

```python
def ricci_scalar(Ricci, metric, coords):
    """計算里奇標量"""
    g_inv = sp.Matrix(metric).inv()
    n = len(coords)
    R = 0
    for j in range(n):
        for k in range(n):
            R += g_inv[j, k] * Ricci[j][k]
    return sp.simplify(R)
```

## 2.4 曲率的物理意義

### 2.4.1 時空曲率與重力

在廣義相對論中，「重力」其實是時空曲率的表現。物質的存在使時空彎曲，彎曲的時空告訴物質如何運動。

### 2.4.2 潮汐力

潮汐力是時空曲率的直接表現。兩個相鄰自由落體之間的相對加速正是由時空曲率決定的。

## 習題

1. 計算 FLRW 宇宙學度規的克里斯多費符號。
2. 驗證二維球面的里奇標量 R = 2（對於單位半徑球面）。
3. 證明 Minkowski 時空的里奇張量為零。
