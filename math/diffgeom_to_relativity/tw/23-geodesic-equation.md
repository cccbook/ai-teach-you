# 第 23 章：測地線偏折

## 概述

在廣義相對論中，自由粒子沿測地線運動，這與牛頓力學中粒子受力運動的圖像截然不同。本章將詳細討論在彎曲時空（特別是 Schwarzschild 時空）中粒子的運動規律。

牛頓力學中，自由粒子不受力，保持靜止或勻速直線運動。但在廣義相對論中，「自由」的含義是「沿時空中的測地線運動」。這是等效原理的直接推論——自由落體觀測者感受到不到重力，因此在局部慣性參考系中沿直線運動。由於時空是彎曲的，這條「直線」在全局座標中表現為曲線。

測地線方程是廣義相對論的核心方程之一，它決定了粒子和光線在彎曲時空中的軌跡。通過研究這些軌跡，我們可以預言光線的偏折、行星的進動、黑洞周圍粒子的運動等現象——所有這些都已被觀測所證實。

## 23.1 測地線方程的回顧

### 23.1.1 測地線方程

測地線方程是「彎曲時空中的直線」所滿足的方程。對於類時曲線（粒子世界線），方程為：

$$\frac{d^2 x^\mu}{d\tau^2} + \Gamma^\mu_{\ \nu\rho} \frac{dx^\nu}{d\tau} \frac{dx^\rho}{d\tau} = 0$$

其中 $\tau$ 是仿資 proper time，$\Gamma^\mu_{\ \nu\rho}$ 是 Christoffel 符號（黎曼聯絡）。

這個方程可以從變分原理推導——它是作用量 $S = \int d\tau$ 的臨界曲線方程。

物理意義：
- 第一項 $\frac{d^2 x^\mu}{d\tau^2}$ 是曲線的加速度
- 第二項是時空曲率的效應
- 當 Christoffel 符號為零（平坦時空），方程化簡為 $d^2x^\mu/d\tau^2 = 0$，這是牛頓第一定律

### 23.1.2 零測地線

光子（$m = 0$）沿零測地線運動。對於零曲線，仿資 $\tau$ 不能用作參數，因為 $d\tau = 0$。代わりに，我們使用 affine 參數 $\lambda$：

$$\frac{d^2 x^\mu}{d\lambda^2} + \Gamma^\mu_{\ \nu\rho} \frac{dx^\nu}{d\lambda} \frac{dx^\rho}{d\lambda} = 0$$

零測地線的特徵是四速度滿足：

$$g_{\mu\nu} \dot{x}^\mu \dot{x}^\nu = 0$$

這是光子的「時空距離」為零的表達。

### 23.1.3 測地線的幾何意義

測地線是「局部最短路徑」。在黎曼幾何中，測地線有兩種等價的定義：
1. **變分定義**：弧長泛函的臨界曲線
2. **平行移動定義**：切向量沿曲線平行移動的曲線

這兩個定義在光滑流形上是等價的。平行移動定義更凸顯了測地線的幾何本性——它描述了「方向不變」的運動。

## 23.2 Schwarzschild 時空中的守恆量

### 23.2.1 能量守恆

Schwarzschild 時空是靜態的——度規不隨時間變化。這意味著存在一個時間類 Killing 向量場 $\xi^\mu = \partial_t$。

Killing 向量的性質是 $£_\xi g_{\mu\nu} = 0$，這導致沿測地線存在一個守恆量：

$$E = -g_{\mu\nu} \xi^\mu \frac{dx^\nu}{d\tau} = -g_{tt} \frac{dt}{d\tau} = \left(1 - \frac{2GM}{c^2 r}\right) \frac{dt}{d\tau}$$

物理意義：$E$ 是單位質量（或單位質量對光子）的能量。當粒子遠離黑洞（$r \to \infty$）時，$g_{tt} \to -1$，因此 $E \to dt/d\tau$，這正是無引力時的能量。

對於實際計算，我們通常設 $c = G = 1$，然後得到 $E = (1 - 2M/r)dt/d\tau$。

### 23.2.2 角動量守恆

Schwarzschild 時空也是球對稱的——對繞任意軸的旋轉不變。這給出另一個 Killing 向量場 $\xi^\mu_\phi = \partial_\phi$。

角動量守恆量為：

$$L = g_{\mu\nu} \xi^\mu_\phi \frac{dx^\nu}{d\tau} = g_{\phi\phi} \frac{d\phi}{d\tau} = r^2 \frac{d\phi}{d\tau}$$

這與牛頓力學中行星繞中心天體運動的角動量守恆完全類似——只是「軌道半徑」是 $r^2$ 而非 $r$。

### 23.2.3 測地線的完整性

能量守恆和角動量守恆告訴我們，Schwarzschild 時空中的測地線運動是二維的——粒子被約束在一個平面（orbital plane）上。

我們可以選擇座標使得這個平面是赤道面 $\theta = \pi/2$。則測地線運動完全由 $(r(\tau), \phi(\tau))$ 描述。

## 23.3 有效勢方法

### 23.3.1 徑向運動方程

測地線方程可以從守恆量和測地線條件推導。

類時測地線的測地線條件：

$$g_{\mu\nu} \frac{dx^\mu}{d\tau} \frac{dx^\nu}{d\tau} = -1$$

代入 Schwarzschild 度規：

$$-\left(1 - \frac{2M}{r}\right)\left(\frac{dt}{d\tau}\right)^2 + \left(1 - \frac{2M}{r}\right)^{-1}\left(\frac{dr}{d\tau}\right)^2 + r^2\left(\frac{d\phi}{d\tau}\right)^2 = -1$$

利用守恆量 $E$ 和 $L$：

$$\left(1 - \frac{2M}{r}\right)\left(\frac{dt}{d\tau}\right)^2 = E^2$$
$$r^2\left(\frac{d\phi}{d\tau}\right)^2 = L^2$$

代入並整理，得到徑向運動方程：

$$\frac{1}{2}\left(\frac{dr}{d\tau}\right)^2 + V_{\text{eff}}(r) = \frac{E^2}{2}$$

其中有效勢能為：

$$V_{\text{eff}}(r) = -\frac{M}{r} + \frac{L^2}{2r^2} - \frac{ML^2}{r^3}$$

恢復 $G$ 和 $c$：

$$V_{\text{eff}}(r) = -\frac{GM}{r} + \frac{L^2}{2r^2} - \frac{GML^2}{c^2 r^3}$$

### 23.3.2 各項的物理意義

有效勢能的三項有清晰的物理起源：

1. **牛頓引力勢** $V_1 = -\frac{GM}{r}$
   - 這是牛頓萬有引力的勢能
   - 當 $r \to \infty$ 時趨於零
   - 當 $r \to 0$ 時趨於 $-\infty$

2. **離心勢壘** $V_2 = \frac{L^2}{2r^2}$
   - 這對應於軌道角動量產生的「離心力」
   - 阻止粒子落入中心
   - 當 $r \to 0$ 時趨於 $+\infty$

3. **廣義相對論修正** $V_3 = -\frac{GML^2}{c^2 r^3}$
   - 這是廣義相對論獨有的項
   - 來自時空彎曲
   - 當 $r \to 0$ 時趨於 $-\infty$（吸引）
   - 這項使得內部存在一個局部極小值

### 23.3.3 有效勢的圖像

有效勢 $V_{\text{eff}}(r)$ 的圖像顯示：

- 當 $r \to \infty$ 時，$V \to 0$（從負側）
- 當 $r \to 0$ 時，$V \to -\infty$
- 中間區域存在一個勢壘（局部最大值）
- 對於足夠大的 $L$，勢壘頂部對應於準穩定圓軌道

## 23.4 圓軌道

### 23.4.1 圓軌道的條件

圓軌道對應於 $dr/d\tau = 0$，因此 $V_{\text{eff}}(r) = E^2/2$ 且 $dV_{\text{eff}}/dr = 0$。

從 $dV/dr = 0$：

$$\frac{dV_{\text{eff}}}{dr} = \frac{GM}{r^2} - \frac{L^2}{r^3} + \frac{3GML^2}{c^2 r^4} = 0$$

解出 $r$：

$$r = \frac{L^2}{GM}\left(1 \pm \sqrt{1 - \frac{12G^2M^2}{c^2 L^2}}\right)$$

兩個根：
- **外根**（取 + 號）：對應於穩定或準穩定圓軌道
- **內根**（取 - 號）：對應於不穩定圓軌道

### 23.4.2 穩定性條件

圓軌道的穩定性由 $d^2V/dr^2$ 決定。

計算：

$$\frac{d^2V}{dr^2} = -\frac{2GM}{r^3} + \frac{3L^2}{r^4} - \frac{12GML^2}{c^2 r^5}$$

穩定條件 $d^2V/dr^2 > 0$ 給出：

$$r > r_{\text{isco}} = \frac{6GM}{c^2}$$

### 23.4.3 ISCO——最後穩定圓軌道

$$r_{\text{isco}} = \frac{6GM}{c^2}$$

這就是著名的**最後穩定圓軌道**（Innermost Stable Circular Orbit，ISCO）。

物理意義：
- 當 $r > r_{\text{isco}}$ 時，圓軌道是穩定的——小擾動會導致振盪而非墜落
- 當 $r < r_{\text{isco}}$ 時，圓軌道是不穩定的——粒子將迅速螺旋落入黑洞
- ISCO 是黑洞吸積盤的物理內邊界

對於 Schwarzschild 黑洞，ISCO 在 $r = 6M$（自然單位）。恢復常數後為 $r_{\text{isco}} = 6GM/c^2 = 3r_s$，其中 $r_s = 2GM/c^2$ 是 Schwarzschild 半徑。

### 23.4.4 不同角動量下的軌道

當角動量 $L$ 變化時：

- **$L > L_{\text{isco}}$**：存在穩定圓軌道和外不穩定圓軌道
- **$L = L_{\text{isco}}$**：兩個根合併，恰好在 ISCO
- **$L < L_{\text{isco}}$**：沒有穩定圓軌道，粒子將直接落入黑洞

ISCO 處的角動量：

$$L_{\text{isco}} = 2\sqrt{3}\, GM/c$$

## 23.5 光子的偏折

### 23.5.1 光子的有效勢

對於零測地線（光子），有效勢的推導類似，只是測地線條件為 $g_{\mu\nu}\dot{x}^\mu\dot{x}^\nu = 0$。

光子有效勢為：

$$V_{\text{eff}}(r) = \frac{L^2}{2r^2}\left(1 - \frac{2GM}{c^2 r}\right)$$

這個有效勢的特點：
- 當 $r \to \infty$ 時，$V \to 0$
- 當 $r \to 0$ 時，$V \to -\infty$
- 當 $r = 3GM/c^2$ 時，$V$ 達到最大值

光子沒有穩定圓軌道——任何圓軌道都是不穩定的。

### 23.5.2 瞄準參數

定義瞄準參數（impact parameter）$b$：

$$b = \frac{L}{E}$$

這是光子「瞄準」黑洞的最近距離（如果沒有引力偏折）。

對於來自無窮遠的光子，$E = 1$（設光速 $c = 1$），因此 $b = L$。

### 23.5.3 偏折角計算

光子從無窮遠來到近日點 $r_0$ 再回到無窮遠，總偏折角為：

$$\Delta\phi = 2\int_{r_0}^{\infty} \frac{dr}{r^2\sqrt{1 - \frac{2M}{r} - \frac{b^2}{r^2}}}$$

計算給出：

$$\Delta\phi = \frac{4GM}{c^2 b}$$

這就是愛因斯坦的著名結果——光線偏折角是牛頓理論預言的兩倍。

### 23.5.4 數值計算

對於掠過太陽邊緣的光子：
- $M = M_\odot = 1.989 \times 10^{30}$ kg
- $G = 6.674 \times 10^{-11}$ m³/(kg·s²)
- $c = 2.998 \times 10^8$ m/s
- $b \approx R_\odot = 6.96 \times 10^8$ m

計算偏折角：

$$\Delta\phi = \frac{4 \times 6.674 \times 10^{-11} \times 1.989 \times 10^{30}}{(2.998 \times 10^8)^2 \times 6.96 \times 10^8} \approx 1.75''$$

這與 1919 年日食觀測的結果一致！

## 23.6 引力紅移

### 23.6.1 靜止觀測者

考慮在 Schwarzschild 時空中靜止在 $r$ 處的觀測者。這個觀測者的四速度為：

$$u^\mu = \frac{1}{\sqrt{-g_{tt}}}\frac{\partial}{\partial t} = \frac{1}{\sqrt{1 - 2M/r}}\frac{\partial}{\partial t}$$

光子從 $r_{\text{emit}}$ 發射，到達 $r_{\text{rec}}$ 被接收。

發射光子的頻率（相對於發射者的固有时）：

$$\nu_{\text{emit}} = -k_\mu u^\mu_{\text{emit}} = \frac{\omega}{\sqrt{1 - 2M/r_{\text{emit}}}}$$

接收光子的頻率：

$$\nu_{\text{rec}} = \frac{\omega}{\sqrt{1 - 2M/r_{\text{rec}}}}$$

因此頻率比：

$$\frac{\nu_{\text{rec}}}{\nu_{\text{emit}}} = \sqrt{\frac{1 - 2M/r_{\text{emit}}}{1 - 2M/r_{\text{rec}}}}$$

### 23.6.2 紅移

定義紅移 $z$：

$$1 + z = \frac{\nu_{\text{emit}}}{\nu_{\text{rec}}} = \sqrt{\frac{1 - 2M/r_{\text{rec}}}{1 - 2M/r_{\text{emit}}}}$$

當 $r_{\text{rec}} \to \infty$（接收者在無窮遠）：

$$1 + z = \frac{1}{\sqrt{1 - 2M/r_{\text{emit}}}}$$

這表明從引力源表面發射的光會發生紅移。

### 23.6.3 Pound-Rebka 實驗

1959 年，Pound 和 Rebka 在哈佛大學的傑弗遜塔上進行了精確的引力紅移實驗。

實驗設置：
- 高度差：$h = 22.5$ m
- 發射源：$^{57}$Fe 的 14.4 keV 伽馬射線
- 接收器：在塔底部

理論預言的紅移：

$$z = \frac{gh}{c^2} = \frac{9.8 \times 22.5}{(3 \times 10^8)^2} \approx 2.5 \times 10^{-15}$$

實驗結果：
- 測量值：$(2.56 \pm 0.25) \times 10^{-15}$
- 理論值：$2.46 \times 10^{-15}$

這是廣義相對論的首次實驗室驗證！

## 23.7 近日點進動

### 23.7.1 偏心軌道的運動

對於非圓軌道，粒子將在近日點（最近距離）和遠日點（最遠距離）之間振盪。

近日點和遠日點由 $dr/d\tau = 0$ 決定，即 $V_{\text{eff}}(r) = E^2/2$。

定義偏心率 $e$ 和半通徑 $p$：

$$r_{\text{min}} = \frac{p}{1+e}, \quad r_{\text{max}} = \frac{p}{1-e}$$

### 23.7.2 進動角

軌道不是閉合的——近日點會逐漸移動。每次公轉後，近日點進動的角度為：

$$\Delta\phi = 2\pi - 2\phi_{\text{perihelion}}$$

廣義相對論預言的進動率為：

$$\Delta\phi = \frac{6\pi GM}{c^2 a(1-e^2)}$$

其中 $a$ 是軌道半長軸，$e$ 是偏心率。

### 23.7.3 水星的進動

水星的軌道參數：
- 半長軸：$a = 5.79 \times 10^{10}$ m
- 偏心率：$e = 0.2056$

代入公式：

$$\Delta\phi = \frac{6\pi \times 6.674 \times 10^{-11} \times 1.989 \times 10^{30}}{(2.998 \times 10^8)^2 \times 5.79 \times 10^{10} \times (1 - 0.2056^2)}$$

$$\approx 43'' \text{/世紀}$$

這與觀測到的「異常」進動 $43.03''$/世紀精確吻合！

## 23.8 時間延遲

### 23.8.1 Shapiro 延遲

當光線經過大質量天體附近時，其路徑會被彎曲，這導致光程比平坦時空更長。因此，從行星反射的雷達信號在經過太陽附近時會延遲到達。

時間延遲為：

$$\Delta t = -\frac{2GM}{c^3}\ln\left(\frac{4r_e r_p}{b^2}\right)$$

其中 $r_e$ 和 $r_p$ 分別是地球和行星的半徑，$b$ 是瞄準參數。

### 23.8.2 觀測驗證

從地球向金星和水星發射雷達信號並接收回波：
- 理論預言的延遲：約 $10^{-4}$ 秒
- 觀測精度：優於 $0.1\%$

## 23.9 數值計算示例

以下 Python 代碼計算 Schwarzschild 時空中的粒子軌道：

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def geodesic_equation(tau, y, E, L, M=1.0):
    """Schwarzschild 時空中的測地線方程"""
    r, theta, phi, dr, dtheta, dphi = y
    
    # 避免 r = 0
    if r < 2.1 * M:
        return [0, 0, 0, 0, 0, 0]
    
    # Christoffel 符號（非零分量）
    # G^r_tt
    G_rtt = (2*M / r**2) * (1 - 2*M/r)
    # G^r_rr
    G_rrr = -M / (r * (r - 2*M))
    # G^r_theta_theta
    G_rtheta = -(r - 2*M)
    # G^r_phi_phi
    G_rphi = -(r - 2*M) * np.sin(theta)**2
    # G^theta_r_theta
    G_theta_rtheta = 1/r
    # G^theta_phi_phi
    G_theta_phi = -np.sin(theta) * np.cos(theta)
    # G^phi_r_phi
    G_phi_rphi = 1/r
    # G^phi_theta_phi
    G_phi_theta = np.cos(theta) / np.sin(theta)
    
    # 二階導數
    d2r = G_rtt * (E / (1 - 2*M/r))**2 + G_rrr * dr**2 + G_rtheta * dtheta**2 + G_rphi * dphi**2
    d2theta = 2*G_theta_rtheta * dr * dtheta + G_theta_phi * dphi**2
    d2phi = 2*G_phi_rphi * dr * dphi + 2*G_phi_theta * dtheta * dphi
    
    return [dr, dtheta, dphi, d2r, d2theta, d2phi]

# 參數
M = 1.0  # 黑洞質量
E = 0.95  # 能量
L = 2.5  # 角動量

# 初始條件：近日點
r0 = 10 * M  # 初始徑向距離
phi0 = 0  # 初始方位角
theta0 = np.pi / 2  # 赤道面

# dr/dtau 近日點條件：dV/dr = 0
# 簡化計算：設 dr/dtau = 0
dr0 = 0
dphi0 = L / r0**2
dtheta0 = 0

y0 = [r0, theta0, phi0, dr0, dtheta0, dphi0]

# 積分
tau_span = (0, 500)
tau_eval = np.linspace(0, 500, 10000)

solution = solve_ivp(
    geodesic_equation, 
    tau_span, 
    y0, 
    args=(E, L, M),
    t_eval=tau_eval,
    rtol=1e-10, 
    atol=1e-12
)

# 提取結果
r = solution.y[0]
phi = solution.y[2]

# 繪圖
plt.figure(figsize=(10, 10))
plt.subplot(1, 1, 1, projection='polar')

# 黑洞
theta_grid = np.linspace(0, 2*np.pi, 100)
plt.plot(theta_grid, 2*M * np.ones_like(theta_grid), 'k-', linewidth=2, label='視界 r=2M')
plt.fill(theta_grid, 2*M * np.ones_like(theta_grid), 'k', alpha=0.3)

# 軌道
plt.plot(phi, r, 'b-', linewidth=0.5, label='粒子軌道')

plt.xlabel('φ')
plt.title(f'Schwarzschild 時空中的粒子軌道 (E={E}, L={L})')
plt.legend()
plt.grid(True)
plt.savefig('geodesic_orbit.png', dpi=150)
plt.show()

# 近日點進動
r_peri = []
for i in range(len(r)-1):
    if r[i] < r[i+1] and r[i] < r[i-1]:
        r_peri.append(r[i])

if len(r_peri) >= 2:
    phi_diff = phi[1] - phi[0]  # 簡化估計
    print(f"近日點半徑: {np.mean(r_peri):.2f}")
```

## 重點回顧

| 概念 | 說明 |
|------|------|
| 測地線方程 | $\ddot{x}^\mu + \Gamma^\mu_{\nu\rho}\dot{x}^\nu\dot{x}^\rho = 0$ |
| 能量守恆 | $E = (1-2M/r)\dot{t}$ |
| 角動量守恆 | $L = r^2\dot{\phi}$ |
| 有效勢能 | $V_{\text{eff}} = -GM/r + L^2/2r^2 - GML^2/c^2r^3$ |
| ISCO | $r_{\text{isco}} = 6GM/c^2$ |
| 光線偏折 | $\Delta\phi = 4GM/c^2b$ |
| 引力紅移 | $1+z = 1/\sqrt{1-2M/r}$ |

## 練習題

1. **有效勢推導**：從 Schwarzschild 度規和守恆量出發，推導類時粒子的有效勢能表達式。

2. **光線偏折**：計算光子經過太陽邊緣（$b = R_\odot$）的偏折角，與愛丁頓的觀測結果比較。

3. **ISCO 證明**：證明 Schwarzschild 時空中最後穩定圓軌道的半徑為 $r_{\text{isco}} = 6GM/c^2$。

4. **光子軌道**：討論為什麼光子在 Schwarzschild 時空中沒有穩定圓軌道。計算光子「捕獲截面」的大小。

5. **引力紅移**：從 $r = 10M$ 處發射的光子，到達無窮遠時的紅移量是多少？

6. **近日點進動**：使用後牛頓近似，估算水星的近日點進動率，與觀測值比較。

7. **時空延遲**：計算從地球向金星發射雷達信號並返回的最大時間延遲（考慮太陽引力）。

8. **極端質量比**：當角動量 $L$ 接近臨界值時，討論粒子軌道的性質。

9. **徑向自由落體**：計算從靜止（$r = r_0$）自由落體到黑洞所需的固有時。
