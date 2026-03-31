# 第 26 章：Kerr 度規

## 概述

Kerr 度規描述了旋轉黑洞的時空幾何，這是宇宙中大多數天體物理黑洞的實際形態。與靜止的 Schwarzschild 黑洞不同，旋轉黑洞具有軸對稱性，會拖曳周圍的時空結構——這種現象被稱為「參考系拖曳」（frame-dragging）。旋轉不僅改變視界形狀，還會產生 ergosphere，這是能量可以從黑洞中提取的關鍵區域。

1963 年，紐西蘭數學家 Roy Kerr 找到了描述旋轉黑洞的精確解。在此之前，物理學家只能處理靜止黑洞的問題。Kerr 的發現是廣義相對論史上的重大突破，因為它揭示了旋轉對黑洞結構的深刻影響。在現實宇宙中，大多數黑洞都有自轉——無論是通過吸積過程獲得角動量，還是由旋轉的恆星坍縮形成。 因此，Kerr 度規比 Schwarzschild 度規更符合實際的天體物理黑洞。

## 26.1 Kerr 度規的推導

### 26.1.1 對稱性假設

推導 Kerr 度規需要以下假設：

1. **軸對稱性**：時空對繞某個軸的旋轉不變，存在一個 Killing 向量 $\xi_\phi = \partial_\phi$
2. **穩態**：度規不隨時間變化，存在一個 Killing 向量 $\xi_t = \partial_t$
3. **真空**：在旋轉物體外部，$T_{\mu\nu} = 0$
4. **漸近平坦性**：遠離黑洞處，時空趨於 Minkowski 時空
5. **非零角動量**：$J \neq 0$

這些假設比 Schwarzschild 情況更複雜，因為旋轉破壞了完全的球對稱性（只剩下軸對稱）。

### 26.1.2 度規的坐標系

我們使用 Boyer-Lindquist 坐標 $(t, r, \theta, \phi)$，這是分析 Kerr 度規最方便的坐標系。在這些坐標中，度規具有簡潔的形式。徑向坐標 $r$ 與 Schwarzschild 坐標的關係是非平凡的——它們在視界附近會有所不同。

選擇 Boyer-Lindquist 坐標的原因是其類似於球座標的結構，使得度規的形式相對簡單。在這些坐標中，Kerr 度規可以寫成一個優雅的形式，清楚地顯示出各個函數。

### 26.1.3 度規函數的定義

Kerr 度規由兩個關鍵函數描述：

$$\Delta = r^2 - 2Mr + a^2$$
$$\rho^2 = r^2 + a^2\cos^2\theta$$

其中 $M$ 是黑洞質量，$a = J/M$ 是自旋參數（單位質量的角動量）。

函數 $\Delta$ 在確定視界位置時起關鍵作用。當 $\Delta = 0$ 時，徑向坐標達到視界。函數 $\rho^2$ 描述了黑洞旋轉對時空的變形——在南北極（$\theta = 0$ 或 $\pi$），$\rho^2 = r^2$；在赤道（$\theta = \pi/2$），$\rho^2 = r^2 + a^2$。

### 26.1.4 完整的線元

在 Boyer-Lindquist 坐標中，Kerr 度規的線元為：

$$ds^2 = -\left(1 - \frac{2Mr}{\rho^2}\right)dt^2 - \frac{4Mra\sin^2\theta}{\rho^2}dtd\phi + \frac{\rho^2}{\Delta}dr^2 + \rho^2 d\theta^2 + \frac{\sin^2\theta}{\rho^2}\left[(r^2 + a^2)^2 - a^2\Delta\sin^2\theta\right]d\phi^2$$

這個表達式乍看複雜，但每個項都有明確的物理意義：
- 第一項是時間分量的貢獻，顯示「時間膨脹」受旋轉影響
- 第二項是交叉項 $dt\,d\phi$，這是旋轉產生的時空拖曳效應的表現
- 第三、四項是空間徑向和角向的度規
- 最後一項是方位角的度規

### 26.1.5 度規矩陣

為清晰起見，寫出度規矩陣 $g_{\mu\nu}$ 的非零分量：

$$g_{tt} = -\left(1 - \frac{2Mr}{\rho^2}\right)$$
$$g_{rr} = \frac{\rho^2}{\Delta}$$
$$g_{\theta\theta} = \rho^2$$
$$g_{\phi\phi} = \frac{\sin^2\theta}{\rho^2}\left[(r^2 + a^2)^2 - a^2\Delta\sin^2\theta\right]$$
$$g_{t\phi} = g_{\phi t} = -\frac{2Mra\sin^2\theta}{\rho^2}$$

逆度規 $g^{\mu\nu}$ 為：

$$g^{tt} = \frac{(r^2+a^2)^2 - a^2\Delta\sin^2\theta}{\rho^2\Delta}$$
$$g^{rr} = \frac{\Delta}{\rho^2}$$
$$g^{\theta\theta} = \frac{1}{\rho^2}$$
$$g^{\phi\phi} = \frac{\Delta - a^2\sin^2\theta}{\rho^2\Delta\sin^2\theta}$$
$$g^{t\phi} = g^{\phi t} = \frac{2Mra}{\rho^2\Delta}$$

注意，度規行列式為：

$$g = -\rho^4\sin^2\theta$$

這與球座標 Minkowski 度規的行列式形式類似，只是用 $\rho^2$ 替換了 $r^2$。

## 26.2 視界結構

### 26.2.1 視界的位置

Kerr 黑洞的視界由 $g_{rr} \to \infty$ 的條件給出，即 $\Delta = 0$：

$$\Delta = r^2 - 2Mr + a^2 = 0$$

解這個二次方程：

$$r_\pm = M \pm \sqrt{M^2 - a^2}$$

其中 $r_+$ 是外視界（事件視界），$r_-$ 是內視界（Cauchy 視界）。

與 Reissner-Nordström 黑洞不同的是，這裡的視界位置只依賴於 $a$ 和 $M$，不依賴於電荷。與 Schwarzschild 黑洞比較，$r_+$ 總是小於 $2M$（當 $a \neq 0$ 時），這表明旋轉會「收縮」視界。

### 26.2.2 視界的幾何形狀

Kerr 黑洞的視界不是球面！它是一個在 $\theta$ 方向上變形的曲面。視界面由方程 $\Delta = 0$ 定義，即：

$$r = M + \sqrt{M^2 - a^2}$$

這是一個與 $\theta$ 無關的常數，但實際的三維視界面是二維曲面：

$$r = M + \sqrt{M^2 - a^2\cos^2\theta}$$

在南北極（$\theta = 0, \pi$），$r$ 最小；在赤道（$\theta = \pi/2$），$r$ 最大。這種扁平的形狀反映了旋轉黑洞的赤道突出。

### 26.2.3 極端 Kerr 黑洞

當 $a = M$ 時，$r_+ = r_- = M$，這是極端 Kerr 黑洞。在這種情況下，視界恰好是球面 $r = M$。

極端 Kerr 黑洞具有以下特點：
- 表面重力 $\kappa = 0$
- 視界不自發蒸發
- 角動量達到最大可能值

當 $a > M$ 時，$\Delta$ 永遠不為零，沒有視界——這形成了一個裸奇點。這與彭羅斯的宇宙審查假說相矛盾。

### 26.2.4 視界面積

Kerr 黑洞的視界面積為：

$$A = \int_0^{2\pi}\int_0^\pi \sqrt{g_{\theta\theta}g_{\phi\phi}}\, d\theta d\phi$$

計算給出：

$$A = 4\pi\left(r_+^2 + a^2\right) = 8\pi M r_+$$

注意，這與 Schwarzschild 黑洞 $A = 16\pi M^2$ 不同。對於固定的 $M$，Kerr 黑洞的面積可以更大（當 $a \to M$ 時，$r_+ \to M$，$A \to 8\pi M^2$）或更小（當 $a \to 0$ 時，回到 $16\pi M^2$）。

## 26.3 Ergosphere

### 26.3.1 靜止極限面

ergosphere 是 Kerr 時空中一個獨特的區域，位於外視界之外。在這個區域中，靜止觀測者（$r, \theta$ 恆定的觀測者）不可能存在——所有粒子都被迫隨黑洞旋轉。

靜止極限面由 $g_{tt} = 0$ 給出：

$$g_{tt} = -\left(1 - \frac{2Mr}{\rho^2}\right) = 0$$

即：

$$r_E(\theta) = M + \sqrt{M^2 - a^2\cos^2\theta}$$

這就是 ergosphere 的邊界。

### 26.3.2 Ergosphere 的幾何

Ergosphere 是一個橢球面，比外視界 $r_+$ 更大。在赤道（$\theta = \pi/2$）：

$$r_E = M + \sqrt{M^2 - a^2} = r_+$$

在南北極（$\theta = 0, \pi$）：

$$r_E = M + \sqrt{M^2 - a^2} = r_+$$

實際上，$r_E \geq r_+$ 總是成立，等號成立於赤道。這個結論看似矛盾，但仔細檢查代數：

$$\sqrt{M^2 - a^2\cos^2\theta} \geq \sqrt{M^2 - a^2}$$

這成立是因為 $\cos^2\theta \leq 1$，所以 $a^2\cos^2\theta \leq a^2$，因此：

$$M^2 - a^2\cos^2\theta \geq M^2 - a^2$$

對兩邊開根號（都是非負數）：

$$\sqrt{M^2 - a^2\cos^2\theta} \geq \sqrt{M^2 - a^2}$$

加上 $M$：

$$M + \sqrt{M^2 - a^2\cos^2\theta} \geq M + \sqrt{M^2 - a^2}$$

因此 $r_E(\theta) \geq r_+$，等號成立於 $\theta = \pi/2$（赤道）。

### 26.3.3 Ergosphere 的物理意義

在 ergosphere 內部（$r_+ < r < r_E$），度規的 $g_{tt} > 0$，這意味著時間類方向與空間方向互換。具體來說：

$$g_{tt} = -\left(1 - \frac{2Mr}{\rho^2}\right) > 0 \implies \frac{2Mr}{\rho^2} > 1 \implies r > r_E$$

在這個區域內：
- 粒子可以具有負能量（相對於無窮遠觀測者）
- 靜止是不可能的——所有粒子都被迫繞黑洞旋轉
- 這種拖曳效應是時空結構被旋轉扭曲的結果

## 26.4 參考系拖曳效應

### 26.4.1 拖曳頻率

Kerr 時空中，靜止是不可能的，因為時空本身被黑洞的旋轉拖曳。觀測者要保持固定的 $(r, \theta)$，必須具有非零的 $\phi$ 速度。

零超曲面（光錐）的結構揭示了這種拖曳效應。沿徑向發出的光線的角速度為：

$$\Omega \equiv \frac{d\phi}{dt} = \frac{g_{t\phi}}{g_{\phi\phi}} = -\frac{2Mra}{\rho^2[(r^2+a^2)^2 - a^2\Delta\sin^2\theta]}$$

這是光線被拖曳的角速度。對於靜止觀測者，其角速度為：

$$\omega = -\frac{g_{t\phi}}{g_{\phi\phi}} = \frac{2Mra}{\rho^2[(r^2+a^2)^2 - a^2\Delta\sin^2\theta]}$$

在視界 $r_+$ 上，無論 $\theta$ 如何，$\omega$ 趨近於最大可能值 $\omega_H = a/(r_+^2 + a^2)$。

### 26.4.2 靜止極限

當 $a \to 0$ 時，$\omega \to 0$，時空拖曳效應消失，回到 Schwarzschild 情況。當 $a \to M$（極端 Kerr）時，拖曳效應最大。

在無窮遠處，$\omega \to 0$，因為時空恢復平坦。但在靠近黑洞處，拖曳效應變得很強——即使你不斷努力逆時針旋轉，你仍然會被時空拖向與黑洞旋轉相同的方向。

## 26.5 彭羅斯過程

### 26.5.1 負能量軌道

彭羅斯過程（Penrose process）是從旋轉黑洞提取能量的一種機制，由 Roger Penrose 在 1969 年提出。這個過程利用 ergosphere 中的負能量軌道。

在 ergosphere 內部，存在負能量軌道——即在無窮遠處測量能量為負的粒子。這個「負能量」是通過在局部參考系中的正動能與時空拖曳效應的組合實現的。

### 26.5.2 能量提取機制

彭羅斯過程的步驟如下：

1. 一個具有正能量 $E_0 > 0$ 的粒子進入 ergosphere
2. 粒子分裂成兩個粒子：$A$ 和 $B$
3. 粒子 $A$ 具有負能量 $E_A < 0$，落入黑洞
4. 粒子 $B$ 逃逸到無窮遠，具有能量 $E_B = E_0 - E_A > E_0$

結果：無窮遠觀測者測量到粒子 $B$ 的能量 $E_B$ 大於初始能量 $E_0$。黑洞吸收了負能量，因此其總能量減少。

### 26.5.3 能量守恆與角動量守恆

彭羅斯過程需要滿足能量守恆和角動量守恆：

$$E_0 = E_A + E_B$$
$$L_0 = L_A + L_B$$

黑洞的質量變化為：

$$\Delta M = E_A < 0$$

黑洞的角動量變化為：

$$\Delta J = L_A < 0$$

這表明彭羅斯過程可以同時從黑洞提取能量和角動量。

### 26.5.4 最大提取效率

通過彭羅斯過程可以提取的最大能量是黑洞總能量的約 29%。這個極限出現在當黑洞達到極端狀態（$a = M$）時。在那之後，ergosphere 消失，負能量軌道不再可能。

## 26.6 Blandford-Znajek 機制

### 26.6.1 磁場能量提取

Blandford-Znajek 機制是另一種從旋轉黑洞提取能量的方式，通過磁場實現。這是活動星系核和類星體等宇宙中最明亮天體的標準能量來源模型。

在這個機制中：
- 旋轉黑洞周圍存在強磁場（由吸積盤或外部等離子體產生）
- 旋轉的時空拖曳磁力線
- 磁應力在黑洞附近產生電場
- 能量沿磁力線向外傳輸

### 26.6.2 功率估計

Blandford-Znajek 功率的量綱分析給出：

$$P \sim B^2 r_H^2 a^2$$

其中 $B$ 是特徵磁場強度。對於典型的超大質量黑洞：
- $M \sim 10^9 M_\odot$
- $B \sim 10^4$ G
- 功率可達 $10^{46}$ erg/s

這與觀測到的類星體亮度一致。

## 26.7 Killing 張量與守恆量

### 26.7.1 Carter 常數

對於 Kerr 度規，存在一個額外的運動積分——Carter 常數 $Q$。這源於一個 Killing 張量 $K_{\mu\nu}$：

$$K_{\mu\nu} = \rho^2\left(\delta_\mu^\theta\delta_\nu^\theta + \cot^2\theta\delta_\mu^\phi\delta_\nu^\phi\right) - a^2\sin^2\theta\delta_\mu^t\delta_\nu^t$$

Carter 常數的定義為：

$$Q = K_{\mu\nu}u^\mu u^\nu = \rho^4(u^\theta)^2 + a^2\sin^2\theta(u^t)^2 - 2aLu^t + L^2\cot^2\theta$$

這個守恆量使得 Kerr 黑洞周圍粒子的運動是完全可積的。

### 26.7.2 測地線運動

具有 Carter 常數後，粒子的四維運動可以約化為兩個一維運動（徑向和極向）。這與 Schwarzschild 情況類似，但更複雜：

$$m^2\dot{r}^2 = \tilde{E}^2 - V_r(r;\tilde{E},L,Q)$$
$$m^2\dot{\theta}^2 = V_\theta(\theta;L,Q)$$

其中 $\tilde{E} = E/m$，$L$ 是角動量，$V_r$ 和 $V_\theta$ 是有效勢能。

## 26.8 黑洞熱力學與 Kerr 度規

### 26.8.1 表面重力

Kerr 黑洞的表面重力為：

$$\kappa = \frac{r_+ - r_-}{2(r_+^2 + a^2)} = \frac{\sqrt{M^2 - a^2}}{M(r_+ + \sqrt{r_+^2 - a^2})}$$

在極端情況 $a = M$ 時，$\kappa = 0$。

### 26.8.2 熵

Bekenstein-Hawking 熵：

$$S = \frac{A}{4} = 2\pi M\left(M + \sqrt{M^2 - a^2}\right)$$

### 26.8.3 第一定律

Kerr 黑洞熱力學的第一定律：

$$dM = \kappa\, dA/2 + \Omega_H\, dJ$$

其中 $\Omega_H = a/(r_+^2 + a^2)$ 是視界的角速度。

## 26.9 Penrose 圖與時空結構

### 26.9.1 最大拓展

Kerr 時空可以進行最大解析拓展。由於 Kerr 度規不具有球對稱性，其 Penrose 圖比 Schwarzschild 情況更為複雜。

 Kerr 時空的結構包含：
- 無窮遠的外部區域（兩個「宇宙」）
- 兩個 ergosphere
- 兩個視界
- 一個奇異性（環形奇點）

### 26.9.2 環形奇點

Kerr 黑洞的奇點不是點，而是一個環。這是因為在 $r = 0$ 且 $\theta = \pi/2$ 處，曲率發散：

$$R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma} \propto \frac{(r^2 + a^2\cos^2\theta)^2}{\rho^8}$$

當 $\theta = \pi/2$ 且 $r = 0$ 時，奇點存在；但當 $\theta \neq \pi/2$ 時，$r = 0$ 不是奇點（因為 $\rho^2 = a^2\cos^2\theta \neq 0$）。這形成了一個位於 $z = 0$ 平面、半徑為 $a$ 的環。

## 26.10 Kerr 度規與觀測

### 26.10.1 M87* 黑洞成像

2019 年，事件視界望遠鏡（Event Horizon Telescope）發布了 M87 星系中心黑洞的首張影像。這張影像顯示了一個質量約 $6.5 \times 10^9 M_\odot$ 的超大質量黑洞。

測量結果與 Kerr 度規預測一致。黑洞周圍的亮環是吸積盤發出的光被引力彎曲形成的。影像中的不對稱性表明黑洞在旋轉。

### 26.10.2 噴流與能量

M87 的噴流延伸超過 5000 光年。噴流的能量來源可能是 Blandford-Znajek 機制——從旋轉黑洞提取能量並沿磁力線傳輸。

## 26.11 數值計算示例

以下 Python 代碼計算 Kerr 黑洞的視界和 ergosphere：

```python
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def kerr_horizons(M, a):
    """計算 Kerr 黑洞的視界"""
    discriminant = M**2 - a**2
    if discriminant < 0:
        return None, None  # 裸奇點
    else:
        r_plus = M + np.sqrt(discriminant)
        r_minus = M - np.sqrt(discriminant)
        return r_plus, r_minus

def ergosphere(M, a, theta):
    """計算 ergosphere 的徑向位置"""
    return M + np.sqrt(M**2 - a**2 * np.cos(theta)**2)

# 參數
M = 1.0
a_values = [0.0, 0.5, 0.9, 0.99]

theta = np.linspace(0, np.pi, 100)

fig, axes = plt.subplots(2, 2, figsize=(12, 10), subplot_kw=dict(polar=True))

for ax, a in zip(axes.flat, a_values):
    r_plus, r_minus = kerr_horizons(M, a)
    
    # 繪製視界
    if r_plus is not None:
        r_horizon = r_plus * np.ones_like(theta)
        ax.plot(theta, r_horizon, 'b-', linewidth=2, label=f'視界 r+={r_plus:.2f}')
    
    # 繪製 ergosphere
    r_ergo = ergosphere(M, a, theta)
    ax.plot(theta, r_ergo, 'r--', linewidth=2, label='Ergosphere')
    
    ax.set_title(f'a = {a}M')
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.legend(loc='upper right')

plt.suptitle('Kerr 黑洞：視界與 Ergosphere')
plt.tight_layout()
plt.savefig('kerr_horizons.png', dpi=150)
plt.show()

# 3D 可視化
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

theta_grid = np.linspace(0, np.pi, 50)
phi_grid = np.linspace(0, 2*np.pi, 50)
THETA, PHI = np.meshgrid(theta_grid, phi_grid)

a = 0.9
r_plus = kerr_horizons(M, a)[0]

X = r_plus * np.sin(THETA) * np.cos(PHI)
Y = r_plus * np.sin(THETA) * np.sin(PHI)
Z = r_plus * np.cos(THETA)

ax.plot_surface(X, Y, Z, alpha=0.5, cmap='Blues')

a_param = 0.9 * M
r_ergo = ergosphere(M, a_param, THETA)
X_ergo = r_ergo * np.sin(THETA) * np.cos(PHI)
Y_ergo = r_ergo * np.sin(THETA) * np.sin(PHI)
Z_ergo = r_ergo * np.cos(THETA)

ax.plot_surface(X_ergo, Y_ergo, Z_ergo, alpha=0.3, cmap='Reds')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Kerr 黑洞視界與 Ergosphere (3D)')
plt.savefig('kerr_3d.png', dpi=150)
plt.show()
```

## 重點回顧

| 概念 | 說明 |
|------|------|
| Kerr 度規 | 旋轉黑洞的精確解 |
| 自旋參數 $a$ | $a = J/M$，單位質量的角動量 |
| 函數 $\Delta$ | $\Delta = r^2 - 2Mr + a^2$ |
| 函數 $\rho^2$ | $\rho^2 = r^2 + a^2\cos^2\theta$ |
| 外視界 $r_+$ | $M + \sqrt{M^2 - a^2}$ |
| 內視界 $r_-$ | $M - \sqrt{M^2 - a^2}$ |
| Ergosphere | $r_E = M + \sqrt{M^2 - a^2\cos^2\theta}$ |
| Carter 常數 | 額外的運動積分 |
| 彭羅斯過程 | 從 ergosphere 提取能量 |
| Blandford-Znajek | 磁場能量提取機制 |

## 練習題

1. **視界分析**：證明 Kerr 度規的外視界 $r_+$ 總是小於 Schwarzschild 半徑 $2M$（當 $a \neq 0$ 時）。討論這個結果的物理意義。

2. **極端極限**：當 $a \to M$ 時，繪製 Kerr 度規的視界和 ergosphere。證明在赤道上視界與 ergosphere 重合。

3. **Ergosphere 體積**：計算 ergosphere 的體積（作為 $M$ 和 $a$ 的函數）。

4. **彭羅斯過程**：詳細推導彭羅斯過程的能量增益，證明：
   $$\Delta E = E_0 - E_B = -E_A > 0$$

5. **拖曳頻率**：計算零測地線的角速度 $\omega = d\phi/dt$。在視界上，這個值趨近於什麼？

6. **Carter 常數**：驗證 $K_{\mu\nu}$ 是一個 Killing 張量（滿足 $\nabla_{(\lambda}K_{\mu\nu)} = 0$）。

7. **熵的計算**：計算 Kerr 黑洞的 Bekenstein-Hawking 熵，驗證：
   $$S = 2\pi M\left(M + \sqrt{M^2 - a^2}\right)$$

8. **環形奇點**：解釋為什麼 Kerr 黑洞的奇點是環形而非球形。計算奇點的半徑。

9. **M87 黑洞**：根據事件視界望遠鏡的觀測數據，討論如何確定黑洞的自旋。
