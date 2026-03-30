# 第 1 章：張量計算與 SymPy 基礎

## 1.1 SymPy 簡介與安裝

SymPy 是 Python 的符號數學庫，完全使用 Python 編寫，不需要外部依賴。它提供了符號計算、微積分、矩陣運算等功能，非常適合學習相對論所需的張量計算。

### 1.1.1 安裝 SymPy

```bash
pip install sympy
```

[程式檔案：01-1-sympy-basics.py](../_code/01/01-1-sympy-basics.py)

```python
import sympy as sp
from sympy import symbols, sqrt, sin, cos

# 創建符號變數
x, y, z = symbols('x y z')

# 基本運算
expr = (x + y)**2
print(sp.expand(expr))  # x**2 + 2*x*y + y**2

# 微積分
f = x**3 + 2*x**2 - 5*x + 1
print(sp.diff(f, x))   # 3*x**2 + 4*x - 5
print(sp.integrate(f, x))  # x**4/4 + 2*x**3/3 - 5*x**2/2 + x
```

### 1.1.2 符號與表達式

SymPy 的核心是符號（Symbol）。與 Python 的普通變數不同，SymPy 符號代表精確的數學對象。

[程式檔案：01-1-sympy-basics.py](../_code/01/01-1-sympy-basics.py)

```python
# 符號定義
a, b, c = symbols('a b c')

# 代數運算
expr1 = (a + b)**2
expr2 = (a - b)**2
print(f"(a + b)^2 = {sp.expand(expr1)}")
print(f"(a + b)^2 - (a - b)^2 = {sp.simplify(expr1 - expr2)}")

# 求解方程式
solutions = sp.solve(a**2 - 4, a)  # [-2, 2]
```

### 1.1.3 矩陣運算

在相對論中，我們經常需要處理矩陣形式的度規和張量。SymPy 提供了強大的矩陣運算功能。

[程式檔案：01-1-sympy-basics.py](../_code/01/01-1-sympy-basics.py)

```python
from sympy import Matrix

# 創建矩陣
M = Matrix([[a, b], [c, a]])
print(f"M = \n{M}")
print(f"det(M) = {M.det()}")
print(f"M^(-1) = ")
print(M.inv())
```

## 1.2 張量基礎

張量是相對論的語言。在廣義相對論中，我們使用四維張量來描述時空和物質。

### 1.2.1 使用 Array 創建張量

[程式檔案：01-2-tensor-basics.py](../_code/01/01-2-tensor-basics.py)

```python
from sympy.tensor.array import Array

# 1D Array
A = Array([1, 2, 3, 4, 5, 6])
print(f"1D Array: {A}, Shape: {A.shape}")

# 2D Array
B = Array([[1, 2, 3], [4, 5, 6]])
print(f"2D Array:\n{B}, Shape: {B.shape}")

# 符號張量
a, b, c, d = symbols('a b c d')
C = Array([[a, b], [c, d]])
print(f"符號矩陣 C:\n{C}")
```

### 1.2.2 度規張量

度規張量是時空的基本結構，定義了時空中兩點之間的「距離」。

[程式檔案：01-2-tensor-basics.py](../_code/01/01-2-tensor-basics.py)

```python
# Minkowski 度規 (特殊相對論)
eta = Array([[-1, 0, 0, 0],
             [0, 1, 0, 0],
             [0, 0, 1, 0],
             [0, 0, 0, 1]])
print(f"Minkowski 度規 η = \n{eta}")
```

### 1.2.3 愛因斯坦慣例

愛因斯坦求和約定是張量運算中的簡便寫法：當一個指標重複出現時，表示對該指標求和。

[程式檔案：01-2-tensor-basics.py](../_code/01/01-2-tensor-basics.py)

```python
u = Array([1, 2, 3])
v = Array([4, 5, 6])

# 愛因斯坦慣例：u^i * v_i = Σ u_i * v_i
result = sum(u[i] * v[i] for i in range(3))
print(f"u^i v_i = {result}")  # 32

# 矩陣的跡 (trace)
M = Array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
result2 = sum(M[i, i] for i in range(3))
print(f"Tr(M) = {result2}")  # 15
```

### 1.2.4 球座標度規

[程式檔案：01-2-tensor-basics.py](../_code/01/01-2-tensor-basics.py)

```python
from sympy import sin

theta = symbols('theta')
g = Array([[1, 0], [0, sin(theta)**2]])
print(f"2D 球面度規 g_{{ij}} = \n{g}")

# 度規逆矩陣
g_matrix = sp.Matrix([[1, 0], [0, sin(theta)**2]])
g_inv = g_matrix.inv()
print(f"g^(-1) = \n{g_inv}")
```

## 1.3 SymPy 在相對論中的應用

### 1.3.1 洛倫茲因子

狹義相對論中的洛倫茲因子是理解時間膨脹和長度收縮的關鍵。

[程式檔案：01-1-sympy-basics.py](../_code/01/01-1-sympy-basics.py)

```python
v, c = symbols('v c', positive=True)
gamma = 1 / sqrt(1 - v**2 / c**2)
print(f"洛倫茲因子 γ = {gamma}")

# 數值計算
v_val = 0.8 * c
gamma_val = gamma.subs(v, v_val)
print(f"當 v = 0.8c 時，γ = {float(gamma_val.simplify()):.4f}")
```

### 1.3.2 張量導數

協變導數是處理彎曲時空中的微分運算所必需的。

[程式檔案：01-2-tensor-basics.py](../_code/01/01-2-tensor-basics.py)

```python
from sympy.tensor.array import derive_by_array

x, y = symbols('x y')
f = Function('f')(x, y)
grad = derive_by_array(f, (x, y))
print(f"∂f/∂x, ∂f/∂y = {grad}")
```

## 習題

1. 使用 SymPy 計算矩陣 `[[1, 2], [3, 4]]` 的特徵值和特徵向量。
2. 創建一個 3x3 的度規張量和它的逆矩陣。
3. 計算洛倫茲因子在 v = 0.99c 時的值。
4. 使用愛因斯坦慣例計算兩個向量的內積。
