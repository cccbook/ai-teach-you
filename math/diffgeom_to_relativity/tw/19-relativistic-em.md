# 第 19 章：電磁場的相對論形式

## 概述

馬克士威方程組在相對論之前就已經存在，但它們的形式在 Lorentz 變換下並不協變。1908 年，閔可夫斯基將電磁學納入相對論框架，發現電場和磁場實際上是同一個反對稱張量的不同分量。本章將介紹這種四維表述。

這個發現揭示了電場和磁場之間的深刻統一性。在一個觀測者看來純粹的電場，在另一個觀測者看來可能同時包含電場和磁場。這不是測量誤差，而是時空結構的固有性質——電場和磁場是「電磁場」這個統一實體的不同投影。

這種四維表述不僅在美學上令人滿意，而且在物理上極為有力：它自動確保馬克士威方程在 Lorentz 變換下保持形式不變，從而與狹義相對論完全兼容。

## 19.1 四維電磁勢

### 19.1.1 四勢

定義**四維電磁勢**（four-potential）：

$$A^\mu = (\phi/c, \vec{A})$$

其中：
- $\phi$ 是電勢（標量勢）
- $\vec{A}$ 是磁矢勢（三維向量）

在 Lorentz 規範條件下：

$$\partial_\mu A^\mu = 0$$

這個條件在 Lorentz 變換下保持形式不變。

### 19.1.2 規範變換

電磁勢不是物理可觀測量——它們可以進行規範變換而不改變物理場：

$$A^\mu \to A^\mu + \partial^\mu \chi$$

其中 $\chi(x)$ 是任意光滑函數。這就是 U(1) 規範對稱性。

物理場（電場和磁場）由 $F_{\mu\nu}$ 給出，而規範變換不改變 $F_{\mu\nu}$。

### 19.1.3 庫倫規範

在非相對論物理中，常使用庫倫規範：

$$\nabla \cdot \vec{A} = 0, \quad \phi = \text{無規範固定}$$

庫倫規範在 Lorentz 變換下不保持形式不變，但在某些計算中更方便。

## 19.2 電磁場張量

### 19.2.1 定義

**電磁場張量**定義為：

$$F_{\mu\nu} = \partial_\mu A_\nu - \partial_\nu A_\mu$$

這是一個反對稱張量：$F_{\mu\nu} = -F_{\nu\mu}$。

由於規範變換 $A_\mu \to A_\mu + \partial_\mu \chi$，而：

$$\partial_\mu\partial_\nu\chi - \partial_\nu\partial_\mu\chi = 0$$

因此 $F_{\mu\nu}$ 在規範變換下不變——它是物理可觀測量。

### 19.2.2 分量矩陣

使用 Minkowski 度規 $\eta_{\mu\nu} = \text{diag}(-1, 1, 1, 1)$，四勢分量為 $A^\mu = (\phi/c, A_x, A_y, A_z)$，因此 $A_\mu = (-\phi/c, A_x, A_y, A_z)$。

場張量的矩陣形式：

$$F_{\mu\nu} = \begin{pmatrix} 0 & -E_x/c & -E_y/c & -E_z/c \\ E_x/c & 0 & -B_z & B_y \\ E_y/c & B_z & 0 & -B_x \\ E_z/c & -B_y & B_x & 0 \end{pmatrix}$$

這個矩陣清晰地展示了電場和磁場作為同一張量分量的統一性。

### 19.2.3 統一圖像

這說明電場和磁場是同一物理實體的不同觀測表現！具體來說：

- 電場分量 $E_i = c F_{0i}$ 是時間-空間混合分量
- 磁場分量 $B_i = -\frac{1}{2}\epsilon_{ijk}F_{jk}$ 是純空間分量

當觀測者改變參考系時，$F_{\mu\nu}$ 以 Lorentz 張量的方式變換，導致電場和磁場分量混合。

## 19.3 Lorentz 力

### 19.3.1 四維形式的 Lorentz 力

帶電粒子在電磁場中的運動方程為：

$$m_0 \frac{dU^\mu}{d\tau} = q F^\mu_{\ \nu} U^\nu$$

這是牛頓第二定律的四維推廣。右邊是四維 Lorentz 力。

這個方程是協變的——它在任何慣性系中具有完全相同的形式。

### 19.3.2 三維形式

將四維方程投影到空間分量，得到熟悉的三維 Lorentz 力公式：

$$\vec{F} = q(\vec{E} + \vec{v} \times \vec{B})$$

這正是經典電磁學中的 Lorentz 力公式！

推導：時間分量給出功率方程：

$$m_0 \frac{dU^0}{d\tau} = q F^0_{\ \nu} U^\nu = q \vec{E} \cdot \vec{v}/c$$

這與 $dE/dt = \vec{F} \cdot \vec{v}$ 一致。

### 19.3.3 物理意義

Lorentz 力公式有深刻的物理意義：
- 電場對電荷施力：$\vec{F}_E = q\vec{E}$
- 磁場對運動電荷施力：$\vec{F}_B = q\vec{v} \times \vec{B}$

磁力的特點：
- 不做功（$\vec{F}_B \cdot \vec{v} = 0$）
- 只改變運動方向，不改變速度大小
- 總是垂直於速度

## 19.4 馬克士威方程的四維形式

### 19.4.1 無源方程

馬克士威方程的兩個無源方程為：

$$\nabla \cdot \vec{B} = 0$$
$$\nabla \times \vec{E} = -\frac{\partial \vec{B}}{\partial t}$$

它們可以合併為一個協變方程：

$$F_{[\mu\nu,\rho]} = 0 \quad \Leftrightarrow \quad \partial_{[\mu} F_{\nu\rho]} = 0$$

其中 $[\mu\nu\rho]$ 表示完全反對稱。

這可以寫成優雅的外微分形式：

$$dF = 0$$

這表明 $F$ 是閉形式（closed form），因此在單連通區域內可以寫為 $F = dA$。

### 19.4.2 有源方程

馬克士威方程的兩個有源方程為：

$$\nabla \cdot \vec{E} = \frac{\rho}{\epsilon_0}$$
$$\nabla \times \vec{B} = \mu_0 \vec{J} + \mu_0 \epsilon_0 \frac{\partial \vec{E}}{\partial t}$$

它們可以合併為：

$$F^{\mu\nu}_{\ \ \ ;\nu} = \mu_0 J^\mu$$

其中 $J^\mu = (c\rho, \vec{J})$ 是四維電流密度。

這也可以寫成外微分形式：

$$d \star F = \star J$$

其中 $\star F$ 是 $F$ 的 Hodge 對偶。

### 19.4.3 連續性方程

從有源方程的協變散度：

$$\partial_\mu F^{\mu\nu} = \mu_0 J^\nu$$

得到：

$$\partial_\nu J^\nu = 0$$

這正是電荷守恆方程 $\partial_t\rho + \nabla \cdot \vec{J} = 0$。

## 19.5 电磁场的变换

### 19.5.1 電場的變換

考慮兩個慣性系 $S$ 和 $S'$，$S'$ 以速度 $v$ 沿 $x$ 軸相對於 $S$ 運動。 Lorentz 變換下，場張量的分量按照：

$$F'^{\mu\nu} = \Lambda^\mu_{\ \alpha} \Lambda^\nu_{\ \beta} F^{\alpha\beta}$$

對於電場和磁場：

平行於速度方向：
$$\vec{E}'_\parallel = \vec{E}_\parallel$$

垂直於速度方向：
$$\vec{E}'_\perp = \gamma(\vec{E}_\perp + \vec{v} \times \vec{B})$$

### 19.5.2 磁場的變換

磁場的變換規則：

平行於速度方向：
$$\vec{B}'_\parallel = \vec{B}_\parallel$$

垂直於速度方向：
$$\vec{B}'_\perp = \gamma\left(\vec{B}_\perp - \frac{\vec{v}}{c^2} \times \vec{E}\right)$$

### 19.5.3 物理意義

這些變換公式揭示了電場和磁場的相對性：

1. **運動的磁鐵產生電場**：如果在一個參考系中只有磁場（$\vec{E} = 0$），而在另一個參考系中觀測到電場和磁場的混合。

2. **運動的電荷產生磁場**：如果在一個參考系中只有電場（$\vec{B} = 0$），而在另一個參考系中觀測到磁場。

這解釋了為什麼「磁力」是電力的相對論效應——磁場本質上是電場在運動觀測者眼中的表現。

### 19.5.4 統一理解的例子

**例子 1**：平行板電容器在静止系中只有電場，沒有磁場。如果觀測者相對於電容器運動，會測量到磁場。

**例子 2**：一根導線中流動的電流在靜止觀測者看來產生環繞導線的磁場。但從導線中電子的角度看，電子靜止，離子運動，產生電場——這就是電場的磁場等價。

## 19.6 电磁场的能动张量

### 19.6.1 定義

電磁場的能量-動量張量定義為：

$$T^{\mu\nu} = \frac{1}{\mu_0} \left( F^{\mu\alpha} F^\nu_{\ \alpha} - \frac{1}{4} \eta^{\mu\nu} F_{\alpha\beta} F^{\alpha\beta} \right)$$

這個張量是對稱的：$T^{\mu\nu} = T^{\nu\mu}$。

### 19.6.2 物理意義

能量-動量張量的分量有清晰的物理意義：

**能量密度**：
$$T^{00} = \frac{\epsilon_0}{2}(E^2 + c^2 B^2) = \frac{1}{2}(\epsilon_0 E^2 + B^2/\mu_0)$$

**能量流密度（Poynting 向量）**：
$$T^{0i} = \frac{1}{\mu_0}(\vec{E} \times \vec{B})_i = S_i$$

這是單位面積的功率流。

**動量密度**：
$$T^{i0} = \epsilon_0(\vec{E} \times \vec{B})_i = \frac{S_i}{c^2}$$

**應力張量**：
$$T^{ij} = \frac{1}{\mu_0}\left[E_i E_j + c^2 B_i B_j - \frac{1}{2}\delta_{ij}(E^2 + c^2 B^2)\right]$$

### 19.6.3 守恆方程

能量-動量張量滿足協變守恆：

$$\partial_\mu T^{\mu\nu} = - F^\nu_{\ \mu} J^\mu$$

右邊是 Lorentz 力密度——電磁場對電荷的作用力。

當沒有電荷（$J^\mu = 0$）時：

$$\partial_\mu T^{\mu\nu} = 0$$

這表明能量和動量在局部守恆。

## 19.7 平面电磁波

### 19.7.1 波動方程

在真空中（$J^\mu = 0$），馬克士威方程導出波動方程：

$$\Box A^\mu = 0$$

其中 $\Box = \eta^{\mu\nu}\partial_\mu\partial_\nu$ 是達朗貝爾算符。

### 19.7.2 平面波解

平面电磁波的解為：

$$A^\mu = A_0^\mu e^{ik_\nu x^\nu}$$

其中 $k_\nu$ 是波四矢量，滿足 $k_\mu k^\mu = 0$（光子的質量為零）。

波四矢量的分量：
- $k^0 = \omega/c$（角頻率）
- $\vec{k}$（波矢量）

頻率與波數的關係：$\omega = c|\vec{k}|$。

### 19.7.3 橫波性

电磁波是橫波：電場和磁場都垂直於傳播方向。

對於沿 $z$ 軸傳播的波：

$$\vec{E} = E_0 \hat{x} \cos(kz - \omega t)$$
$$\vec{B} = B_0 \hat{y} \cos(kz - \omega t)$$

且 $E_0 = c B_0$，$\vec{E} \perp \vec{B} \perp$ 傳播方向。

## 19.8 數值計算示例

```python
import numpy as np
import matplotlib.pyplot as plt

def lorentz_transform_fields(E, B, beta, gamma):
    """Lorentz 變換電磁場
    假設速度沿 x 方向
    """
    Ex_parallel = E[0]
    Ey_perp = E[1]
    Ez_perp = E[2]
    
    Bx_parallel = B[0]
    By_perp = B[1]
    Bz_perp = B[2]
    
    # 電場變換
    E_prime_x = Ex_parallel
    E_prime_y = gamma * (Ey_perp + beta * Bz_perp)
    E_prime_z = gamma * (Ez_perp - beta * By_perp)
    
    # 磁場變換
    B_prime_x = Bx_parallel
    B_prime_y = gamma * (By_perp - beta * Ez_perp)
    B_prime_z = gamma * (Bz_perp + beta * Ey_perp)
    
    return np.array([E_prime_x, E_prime_y, E_prime_z]), \
           np.array([B_prime_x, B_prime_y, B_prime_z])

# 例子：在 S' 系中只有純電場
E_prime = np.array([0, 1, 0])  # V/m
B_prime = np.array([0, 0, 0])  # T
beta = 0.8
gamma = 1 / np.sqrt(1 - beta**2)

E, B = lorentz_transform_fields(E_prime, B_prime, beta, gamma)

print(f"在 S' 系中：")
print(f"  E' = {E_prime}")
print(f"  B' = {B_prime}")
print()
print(f"在 S 系中（β = {beta}）：")
print(f"  E = {E}")
print(f"  B = {B}")
print()
print(f"驗證：|E| = {np.linalg.norm(E)}, |B| = {np.linalg.norm(B)}")
print(f"      E/B = {np.linalg.norm(E)/np.linalg.norm(B):.4f} ≈ c = 1")

# 繪圖：場變換與速度的關係
beta_values = np.linspace(0, 0.99, 100)
E_y = np.zeros_like(beta_values)
B_z = np.zeros_like(beta_values)

for i, beta in enumerate(beta_values):
    gamma = 1 / np.sqrt(1 - beta**2)
    E_y[i] = gamma  # E'_y = 1
    B_z[i] = gamma * beta  # B'_z = beta

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(beta_values, E_y)
plt.xlabel('β = v/c')
plt.ylabel('E_y / E\'_y')
plt.title('電場的 Lorentz 變換')
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(beta_values, B_z)
plt.xlabel('β = v/c')
plt.ylabel('B_z / E\'_y')
plt.title('磁場的 Lorentz 變換')
plt.grid(True)

plt.tight_layout()
plt.savefig('em_field_transform.png', dpi=150)
plt.show()
```

## 重點回顧

| 概念 | 說明 |
|------|------|
| 四維勢 $A^\mu$ | $(\phi/c, \vec{A})$ |
| 电磁场张量 $F_{\mu\nu}$ | $F_{\mu\nu} = \partial_\mu A_\nu - \partial_\nu A_\mu$ |
| Lorentz 力 | $m dU^\mu/d\tau = q F^\mu_{\ \nu} U^\nu$ |
| 馬克士威方程 | $dF = 0$, $d\star F = \star J$ |
| 能量-動量張量 | $T^{\mu\nu} = (F^{\mu\alpha}F^\nu_{\ \alpha} - \frac{1}{4}\eta^{\mu\nu}F^2)/\mu_0$ |
| 場變換 | $\vec{E}_\perp' = \gamma(\vec{E}_\perp + \vec{v} \times \vec{B})$ |

## 練習題

1. **不變量**：驗證 $F_{\mu\nu}F^{\mu\nu}$ 和 $\frac{1}{2}\epsilon^{\mu\nu\rho\sigma}F_{\mu\nu}F_{\rho\sigma}$ 是 Lorentz 不變量。

2. **場變換**：推導電場和磁場的 Lorentz 變換公式，驗證變換矩陣。

3. **無源方程**：驗證 $dF = 0$ 給出 $\nabla \cdot \vec{B} = 0$ 和 $\nabla \times \vec{E} = -\partial\vec{B}/\partial t$。

4. **均勻磁場**：均勻磁場 $\vec{B}$ 在沿磁場方向以速度 $v$ 運動的觀測者看來是什麼樣的？

5. **蹤**：證明 $F^\mu_{\ \mu} = 0$。

6. **能量-動量張量**：計算平面电磁波的能量密度和Poynting向量。

7. **平面波**：驗證平面电磁波解 $A^\mu = A_0^\mu e^{ik_\nu x^\nu}$ 滿足 Lorentz 規範。

8. **Poynting 向量**：證明對静止電荷分佈，總Poynting向量為零，但能量-動量張量非零。
