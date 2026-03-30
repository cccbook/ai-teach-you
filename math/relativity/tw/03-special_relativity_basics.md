# 第 3 章：狹義相對論基本假設

## 3.1 狹義相對論的兩個基本假設

1905 年，愛因斯坦發表了狹義相對論，徹底改變了我們對時間和空間的理解。這一理論基於兩個基本假設：

### 3.1.1 相對性原理

> 所有慣性參考系中，物理定律的形式都相同。

這意味著不存在「絕對靜止」的參考系。任何以恆定速度運動的觀察者都認為自己是靜止的，而物理定律對他們來說是一樣的。

### 3.1.2 光速不變原理

> 真空中光速對所有觀察者都是常數 c ≈ 3×10⁸ m/s。

無論觀察者如何運動，他們測量到的光速都是相同的。這與經典力學的直覺相矛盾，卻被無數實驗驗證。

[程式檔案：03-1-special-relativity-basics.py](../_code/03/03-1-special-relativity-basics.py)

```python
print("""
狹義相對論的兩條基本假設：

1. 相對性原理：所有慣性參考系中，物理定律的形式都相同
2. 光速不變原理：真空中光速對所有觀察者都是常數 c
""")

c = 299792458  # m/s
print(f"光速 c = {c} m/s")
```

## 3.2 時間膨脹

當一個物體以高速運動時，從靜止觀察者的角度來看，運動物體上的時間變慢了。

### 3.2.1 時間膨脹公式

$$\Delta t = \gamma \Delta \tau$$

其中：
- $\Delta t$ 是觀察者測量的時間
- $\Delta \tau$ 是運動物體上的固有時間
- $\gamma = \frac{1}{\sqrt{1 - v^2/c^2}}$ 是洛倫茲因子

[程式檔案：03-1-special-relativity-basics.py](../_code/03/03-1-special-relativity-basics.py)

```python
v, t0, c = sp.symbols('v t0 c', positive=True)
gamma = 1 / sp.sqrt(1 - v**2 / c**2)

print(f"γ = {gamma}")

v_val = 0.9 * c
gamma_val = gamma.subs(v, v_val)
print(f"當 v = 0.9c 時，γ = {float(gamma_val):.4f}")
print(f"這表示運動中的觀察者，時間慢了 {float(gamma_val):.2f} 倍！")
```

## 3.3 長度收縮

運動方向上的長度也會收縮。

### 3.3.1 長度收縮公式

$$L = \frac{L_0}{\gamma}$$

其中 $L_0$ 是物體的固有長度。

[程式檔案：03-1-special-relativity-basics.py](../_code/03/03-1-special-relativity-basics.py)

```python
L0 = sp.symbols('L0')
L = L0 / gamma
print(f"L = L₀/γ")
print(f"當 v = 0.9c 時，L = L₀/{float(gamma_val):.4f}")
print(f"長度收縮為原本的 {float(1/gamma_val):.4f} 倍")
```

## 3.4 閔考斯基時空

狹義相對論使用四維時空，稱為閔考斯基時空。

### 3.4.1 閔考斯基度規

$$ds^2 = -c^2dt^2 + dx^2 + dy^2 + dz^2$$

度規張量：

$$\eta = \text{diag}(-1, 1, 1, 1)$$

[程式檔案：03-1-special-relativity-basics.py](../_code/03/03-1-special-relativity-basics.py)

```python
eta = sp.Array([[-1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]])
print(f"Minkowski 度規 η = \n{eta}")
```

### 3.4.2 時空間隔

時空間隔 $ds^2$ 在所有慣性系中是不變的。這是狹義相對論的核心。

- **類時間隔** ($ds^2 < 0$): 可達的因果事件
- **類空間隔** ($ds^2 > 0$): 不可達的因果事件  
- **類光間隔** ($ds^2 = 0$): 光的世界線

[程式檔案：03-1-special-relativity-basics.py](../_code/03/03-1-special-relativity-basics.py)

```python
print("""
時空間隔：
ds² = -c²dt² + dx² + dy² + dz²

分為三種類型：
- 類時間隔 (ds² < 0)：可達的因果事件
- 類空間隔 (ds² > 0)：不可達的因果事件  
- 類光間隔 (ds² = 0)：光的世界線
""")
```

## 3.5 固有時間

固有時間 $\tau$ 是粒子本身經歷的時間。

[程式檔案：03-1-special-relativity-basics.py](../_code/03/03-1-special-relativity-basics.py)

```python
t, x, y, z, ct = sp.symbols('t x y z ct')
ds2 = -c**2 * t**2 + x**2 + y**2 + z**2
print(f"ds² = {ds2}")
print(f"固有時間 τ = ∫ ds/c")
```

## 3.6 實驗驗證

### 3.6.1 著名的驗證實驗

1. **邁克爾遜-莫雷實驗** (1887): 證明光速在不同方向上相同
2. **時間膨脹驗證**: μ子壽命實驗、引力紅移實驗
3. **GPS 系統**: 必須考慮相對論效應才能準確定位

## 習題

1. 計算太空人以 0.99c 速度飛行一年後，地球過了多少時間？
2. 如果你想在有生之年到達距離地球 100 光年的星球，你需要多快的速度？
3. 證明時空間隔 $ds^2$ 在洛倫茲轉換下是不變的。
