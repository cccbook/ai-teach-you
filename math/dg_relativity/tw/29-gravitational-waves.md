# 第 29 章：引力波

## 概述

引力波是時空幾何中的擾動，以光速在時空中傳播。這些波是由加速質量產生的，攜帶著關於它們源的信息。愛因斯坦在 1916 年預言了引力波的存在，這是廣義相對論的重要預言之一。

一個世紀以來，引力波一直是物理學中最難以捉摸的預言之一。2015 年 9 月 14 日，LIGO（激光干涉儀引力波天文台）首次直接探測到引力波，標誌著引力波天文學新時代的開始。這一重大發現為觀測宇宙打開了一扇全新的窗口，使人類能夠「聽到」宇宙的聲音。

引力波的獨特之處在於它們幾乎不被物質吸收或散射，可以穿越整個宇宙而不衰減。這使得引力波成為探測黑洞、中子星等緻密天體的理想工具。

## 29.1 線性化理論

### 29.1.1 度規擾動

在遠離引力波的區域，時空幾乎是平坦的。我們可以將度規寫為 Minkowski 度規加上微小的擾動：

$$g_{\mu\nu} = \eta_{\mu\nu} + h_{\mu\nu}$$

其中 $|h_{\mu\nu}| \ll 1$，$h_{\mu\nu}$ 是引力波的度規擾動。

這被稱為「線性化」方法，因為我們將 Einstein 方程在平坦時空背景下展開，並保留到 $h$ 的一階。

### 29.1.2 逆度規

逆度規為：

$$g^{\mu\nu} = \eta^{\mu\nu} - h^{\mu\nu} + O(h^2)$$

其中 $h^{\mu\nu} = \eta^{\mu\alpha}\eta^{\nu\beta}h_{\alpha\beta}$。

### 29.1.3 Christoffel 符號

計算 Christoffel 符號，保留到 $h$ 的一階：

$$\Gamma^\lambda_{\mu\nu} = \frac{1}{2}\eta^{\lambda\sigma}\left(\partial_\mu h_{\nu\sigma} + \partial_\nu h_{\mu\sigma} - \partial_\sigma h_{\mu\nu}\right) + O(h^2)$$

### 29.1.4 Ricci 張量

Ricci 張量為：

$$R_{\mu\nu} = \partial_\lambda\Gamma^\lambda_{\mu\nu} - \partial_\mu\Gamma^\lambda_{\lambda\nu} + O(h^2)$$

代入 Christoffel 符號並化簡：

$$R_{\mu\nu} = \frac{1}{2}\Box h_{\mu\nu} - \frac{1}{2}\partial_\mu\partial_\nu h - \frac{1}{2}\partial_\nu\partial_\mu h + O(h^2)$$

其中 $h = \eta^{\alpha\beta}h_{\alpha\beta}$ 是擾動的跡，$\Box = \eta^{\mu\nu}\partial_\mu\partial_\nu$ 是達朗貝爾算符。

注意到 $h_{\mu\nu}$ 對稱，因此 $\partial_\mu\partial_\nu h = \partial_\nu\partial_\mu h$，後兩項抵消：

$$R_{\mu\nu} = \frac{1}{2}\Box h_{\mu\nu} + O(h^2)$$

### 29.1.5 Ricci 標量

Ricci 標量為：

$$R = \eta^{\mu\nu}R_{\mu\nu} + O(h^2) = \frac{1}{2}\Box h + O(h^2)$$

其中 $h = \eta^{\mu\nu}h_{\mu\nu}$。

### 29.1.6 Einstein 張量

Einstein 張量為：

$$G_{\mu\nu} = R_{\mu\nu} - \frac{1}{2}g_{\mu\nu}R = \frac{1}{2}\left(\Box h_{\mu\nu} - \partial_\mu\partial_\nu h - \eta_{\mu\nu}\Box h + \eta_{\mu\nu}\partial_\alpha\partial_\beta h^{\alpha\beta}\right) + O(h^2)$$

## 29.2 波形方程

### 29.2.1 Lorenz 規範

選擇適當的協變規範可以簡化方程。定義反對稱跡規範（Lorenz 規範）條件：

$$\partial^\nu\bar{h}_{\mu\nu} = 0$$

其中
$$\bar{h}_{\mu\nu} = h_{\mu\nu} - \frac{1}{2}\eta_{\mu\nu}h$$

被稱為「跡反轉」擾動。

在這個規範下，Einstein 方程簡化為：

$$\Box\bar{h}_{\mu\nu} = -\frac{16\pi G}{c^4}T_{\mu\nu}$$

這與電磁波的波形方程形式相同。

### 29.2.2 真空中的波動方程

在真空區域（$T_{\mu\nu} = 0$），波形方程為：

$$\Box\bar{h}_{\mu\nu} = 0$$

這是標準的波動方程，顯示引力波以光速傳播。

### 29.2.3 平面波解

波動方程的平面波解為：

$$\bar{h}_{\mu\nu} = A_{\mu\nu} e^{ik_\rho x^\rho}$$

其中 $k^\mu$ 是波四矢量，$A_{\mu\nu}$ 是常數振幅張量。

波動方程 $\Box\bar{h}_{\mu\nu} = 0$ 給出：

$$k_\rho k^\rho = 0$$

這確認了引力波是類光的——以光速傳播。

Lorenz 規範條件 $\partial^\nu\bar{h}_{\mu\nu} = 0$ 給出：

$$k^\nu A_{\mu\nu} = 0$$

即振幅張量與波矢量正交。

## 29.3 橫向無跡（TT）規範

### 29.3.1 規範自由度

引力場具有協變規範對稱性（微分同胚）。我們可以進行座標變換：

$$x^\mu \to x^\mu + \xi^\mu(x)$$

這不會改變物理觀測量，但會改變 $h_{\mu\nu}$ 的形式。

我們可以利用這個自由度進一步簡化度規擾動。

### 29.3.2 TT 規範條件

選擇 TT 規範（橫向無跡規範），定義以下條件：

1. **橫向條件**：傳播方向的正交分量為零
   $$\partial^j h_{ij} = 0 \quad (i,j = 1,2,3)$$

2. **無跡條件**：
   $$\eta^{ij}h_{ij} = 0 \quad \Rightarrow \quad h_{11} + h_{22} = 0$$

3. **時間分量為零**：
   $$h_{0\mu} = 0$$

這些條件完全固定了規範自由度（除了兩個剩餘自由度，對應於兩個極化狀態）。

### 29.3.3 極化張量

在 TT 規範下，沿 $z$ 方向傳播的引力波的度規擾動矩陣為：

$$h_{ij}^{\text{TT}} = h_+(t - z/c)\begin{pmatrix} 1 & 0 & 0 \\ 0 & -1 & 0 \\ 0 & 0 & 0 \end{pmatrix} + h_\times(t - z/c)\begin{pmatrix} 0 & 1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 0 \end{pmatrix}$$

這顯示了引力波的兩個極化模式：
- **$+$ 極化**：主軸沿 $x$ 和 $y$ 方向
- **$\times$ 極化**：主軸旋轉 45°

### 29.3.4 物理意義

TT 規範的度規擾動只有空間-空間分量，描述時空的幾何變形：
- $h_+$ 使 $x$ 方向伸展、$y$ 方向壓縮
- $h_\times$ 使 $x$ 和 $y$ 軸旋轉 45° 後的兩個方向交替伸展和壓縮

## 29.4 引力波的效應

### 29.4.1 自由測試粒子的運動

考慮自由測試粒子在引力波影響下的運動。在 TT 規範中，粒子受到引力波的影響來自 Christoffel 符號。

粒子的運動方程（測地線方程）：
$$\frac{d^2x^i}{d\tau^2} + \Gamma^i_{\mu\nu}\frac{dx^\mu}{d\tau}\frac{dx^\nu}{d\tau} = 0$$

對於低速粒子（$dx^i/d\tau \ll c\, dt/d\tau$），保留到 $h$ 的一階：

$$\frac{d^2x^i}{dt^2} \approx -c^2\Gamma^i_{00} - 2c^2\Gamma^i_{0j}\frac{v^j}{c} + O(h^2)$$

在 TT 規範下，$\Gamma^i_{00} = 0$，因此：

$$\frac{d^2x^i}{dt^2} \approx -2\Gamma^i_{0j}v^j$$

計算 Christoffel 符號：

$$\Gamma^i_{0j} = \frac{1}{2}h_{ij,\;0} + O(h^2)$$

因此：
$$\frac{d^2x^i}{dt^2} \approx -h_{ij,\;0}v^j$$

### 29.4.2 固有距離的變化

兩個相鄰自由測試粒子之間的固有距離由度規決定：

$$dl^2 = \delta_{ij}dx^i dx^j + h_{ij}dx^i dx^j$$

引力波導致固有距離的週期性變化：
- 當 $h_+ > 0$ 時，$x$ 方向伸展，$y$ 方向收縮
- 當 $h_+ < 0$ 時，$x$ 方向收縮，$y$ 方向伸展

對於小擾動，相對距離變化為：
$$\frac{\delta L}{L} \sim \frac{1}{2}h$$

### 29.4.3 幾何圖像

引力波可以理解為時空織物的漣漪：
- 波前是垂直於傳播方向的平面
- 度規擾動使時空在傳播方向上交替拉伸和壓縮
- 這種效應是橫向的——垂直於傳播方向

## 29.5 能量動量攜帶

### 29.5.1 赝能量動量張量

引力波攜帶能量和動量。在線性化理論中，引力波的能量動量可以用「贗」張量描述：

$$t^{\mu\nu} = \frac{c^2}{32\pi G}\langle\partial^\mu\bar{h}_{\alpha\beta}\partial^\nu\bar{h}^{\alpha\beta}\rangle$$

其中 $\langle \rangle$ 表示在幾個波長尺度上的平均。

### 29.5.2 引力波的能量密度

對於沿 $z$ 方向傳播的平面波，能量密度為：

$$\rho_{\text{GW}} = t^{00} = \frac{c^2}{32\pi G}\langle\dot{h}_+^2 + \dot{h}_\times^2\rangle$$

這顯示引力波攜帶正的能量。

### 29.5.3 引力波的功率

對於振幅為 $h$ 的單色波：
$$\rho_{\text{GW}} = \frac{c^2 h^2 \omega^2}{32\pi G}$$

## 29.6 波源

### 29.6.1 四極子輻射

線性化理論中的引力波源是運動質量的四極矩。

真空中的波動方程解為：

$$\bar{h}^{\mu\nu}(t, \mathbf{x}) = \frac{4G}{c^4}\int d^3x'\,\frac{T^{\mu\nu}(t - |\mathbf{x} - \mathbf{x}'|/c, \mathbf{x}')}{|\mathbf{x} - \mathbf{x}'|}$$

在長波長近似下（波源尺寸 $\ll$ 波長），這個積分可以用多極展開。

主要的輻射項來自流體的四極矩：

$$I_{ij}(t) = \int d^3x'\,\rho(t, \mathbf{x}')\,x'_i x'_j$$

 monopole（單極子）項不產生引力波（能量守恆），dipole（偶極子）項也不產生（動量守恆）。最低階的引力波來自 quadrupole（四極子）。

### 29.6.2 四極矩公式

遠離波源處的引力波為：

$$h_{ij}^{\text{TT}}(t, \mathbf{x}) = \frac{2G}{c^4 r}\frac{d^2 I_{ij}}{dt^2}(t - r/c)$$

其中 $r = |\mathbf{x}|$ 是到波源的距離，$I_{ij}$ 是四極矩張量的 trace-free 部分。

### 29.6.3 總功率

各向同性四極子引力波的總功率為：

$$P = \frac{G}{5c^5}\sum_{i,j}\left|\dddot{I}_{ij}\right|^2$$

這是引力波攜帶的總能量。

## 29.7 雙星系統

### 29.7.1 牛頓雙星的四極矩

考慮兩個質量 $m_1$ 和 $m_2$ 繞共同質心運動的系統。

在質心框架中，四極矩的時間導數為：

$$\dddot{I}_{ij} = 2\mu\, a\, v\, (表達式涉及軌道幾何)$$

其中 $\mu = m_1 m_2/(m_1 + m_2)$ 是約化質量，$a$ 是軌道半長軸，$v$ 是相對速度。

### 29.7.2 軌道衰減

雙星系統通過發射引力波損失能量，導致軌道週期逐漸縮短。

能量守恆給出：

$$\frac{dE}{dt} = -P_{\text{GW}}$$

其中 $E$ 是雙星軌道能量，$P_{\text{GW}}$ 是引力波功率。

對於圓軌道：
$$E = -\frac{G m_1 m_2}{2a}$$

引力波功率：
$$P_{\text{GW}} = \frac{32}{5}\frac{G^4}{c^5}\frac{m_1^2 m_2^2 (m_1 + m_2)}{a^5}$$

因此：
$$\dot{a} = -\frac{64}{5}\frac{G^3 m_1 m_2 (m_1 + m_2)}{c^5 a^3}$$

這導致軌道收縮和週期縮短。

### 29.7.3 脈衝雙星 PSR B1913+16

1974 年發現的 Hulse-Taylor 脈衝雙星提供了引力波存在的間接證據。

觀測數據：
- 軌道週期：$P_b = 7.75$ 小時
- 週期變化率：$\dot{P}_b = -2.418 \times 10^{-12}$
- 理論預言：$\dot{P}_b = -2.402 \times 10^{-12}$（引力波損耗）
- 吻合精度：0.1%

這是廣義相對論的最精確驗證之一。

## 29.8 LIGO 探測

### 29.8.1 干涉儀原理

LIGO 使用邁克爾孫干涉儀探測引力波。干涉儀的兩臂垂直，各長 $L = 4$ km。

當引力波通過時，兩臂的長度發生差異變化：
$$\delta L = h\, L$$

其中 $h$ 是引力波應變。

### 29.8.2 靈敏度

LIGO 的目標靈敏度：
$$h \sim 10^{-23}/\sqrt{\text{Hz}}$$

這意味著 4 km 臂長的位移約為：
$$\delta L \sim 10^{-19}\text{ m}$$

這是質子大小的 $10^{-8}$ 倍！

### 29.8.3 GW150914 事件

2015 年 9 月 14 日，LIGO 首次探測到引力波。

事件參數：
- 兩個黑洞質量：$36^{+5}_{-4} M_\odot$ 和 $29^{+4}_{-4} M_\odot$
- 合併後黑洞質量：$62 \pm 4 M_\odot$
- 能量損失：$3.0 \pm 0.5 M_\odot c^2$
- 峰值功率：$3.6 \times 10^{49}$ W
- 距離：$410^{+180}_{-160}$ Mpc
- 紅移：$z \approx 0.09$

這個事件的波形與廣義相對論的數值模擬完全一致。

### 29.8.4 黑洞合併的相位

黑洞合併的引力波形可分為三個階段：
1. **緩慢逼近**（inspiral）：兩個黑洞螺旋靠近，頻率逐漸增加
2. **合併**（merger）：兩個黑洞接觸並合併
3. **鈴宕**（ringdown）：合併後的黑洞發出衰減的引力波

每個階段都可以用不同的理論方法處理：
- inspiral：後牛頓近似
- merger：數值相對論
- ringdown：黑洞微擾理論

## 29.9 雙中子星合併

### 29.9.1 GW170817 事件

2017 年 8 月 17 日，LIGO 和 Virgo 探測到雙中子星合併事件 GW170817。

這是歷史上首次同時探測到引力波和電磁波的同一天體事件：
- 引力波信號持續約 100 秒
- 伽馬射線暴在引力波觸發後 1.7 秒到達
- 光學對應體在 11 小時後被觀測到

### 29.9.2 多信使天文學

GW170817 開啟了多信使天文學的新時代：
- 引力波提供了合併質量和距離
- 伽馬射線暴顯示合併產生超相對論噴流
- 光學和紅外觀測確認了 kilonova——重元素合成

### 29.9.3 哈勃常數測量

GW170817 提供了測量哈勃常數的新方法：
- 引力波給出距離：$d = 40^{+7}_{-8}$ Mpc
- 光學對應體的紅移：$z = 0.0097$
- 哈勃常數：$H_0 = 70^{+12}_{-8}$ km/s/Mpc

這與 Planck 和 SH0ES 測量一致，提供了獨立的約束。

## 29.10 數值計算示例

以下 Python 代碼模擬引力波對干涉儀的影響：

```python
import numpy as np
import matplotlib.pyplot as plt

def gravitational_wave_strain(t, h0, f, phi0=0):
    """計算引力波應變
    t: 時間陣列
    h0: 應變幅度
    f: 引力波頻率
    phi0: 初相位
    """
    omega = 2 * np.pi * f
    return h0 * np.cos(omega * t + phi0)

def interferometer_signal(t, L, h0, f, theta, phi):
    """計算干涉儀輸出信號
    L: 臂長
    theta, phi: 引力波入射方向
    """
    # 簡化假設：引力波沿 z 方向入射
    # 兩個臂的應變
    h_plus = h0 * np.cos(2 * np.pi * f * t)
    h_cross = h0 * np.sin(2 * np.pi * f * t)
    
    # 臂 1 沿 x 方向，臂 2 沿 y 方向
    # 干涉儀輸出與臂長差的變化成正比
    delta_h = (L/2) * (h_plus - h_cross)
    
    return delta_h

# 參數
L = 4000  # 4 km
h0 = 1e-21  # 典型的引力波應變
f = 150  # Hz (LIGO 敏感頻段)

# 時間
t = np.linspace(0, 0.1, 10000)  # 0.1 秒

# 計算信號
delta_h = interferometer_signal(t, L, h0, f, 0, 0)

# 繪圖
plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.plot(t * 1000, delta_h * 1e18, 'b-')
plt.xlabel('時間 (ms)')
plt.ylabel('位移 (10^-18 m)')
plt.title('引力波引起的臂長差變化')
plt.grid(True)

plt.subplot(2, 2, 2)
# 頻譜分析
from scipy.fft import fft, fftfreq
signal_fft = fft(delta_h)
freq = fftfreq(len(t), t[1] - t[0])
plt.plot(freq[:len(freq)//2], np.abs(signal_fft[:len(freq)//2]))
plt.xlabel('頻率 (Hz)')
plt.ylabel('振幅')
plt.title('頻譜')
plt.xlim(0, 500)
plt.grid(True)

plt.subplot(2, 2, 3)
# 不同頻率
for f_test in [50, 100, 200, 400]:
    signal = interferometer_signal(t, L, h0, f_test, 0, 0)
    plt.plot(t * 1000, signal * 1e18, label=f'f={f_test} Hz')
plt.xlabel('時間 (ms)')
plt.ylabel('位移 (10^-18 m)')
plt.title('不同頻率的信號')
plt.legend()
plt.grid(True)

plt.subplot(2, 2, 4)
# 不同幅度
for h_test in [1e-22, 1e-21, 1e-20, 1e-19]:
    signal = interferometer_signal(t, L, h_test, f, 0, 0)
    plt.plot(t * 1000, signal * 1e18, label=f'h={h_test:.0e}')
plt.xlabel('時間 (ms)')
plt.ylabel('位移 (10^-18 m)')
plt.title('不同幅度的信號')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('gravitational_wave_detection.png', dpi=150)
plt.show()
```

## 重點回顧

| 概念 | 說明 |
|------|------|
| 度規擾動 | $g_{\mu\nu} = \eta_{\mu\nu} + h_{\mu\nu}$ |
| 波形方程 | $\Box h_{\mu\nu} = -16\pi G T_{\mu\nu}/c^4$ |
| TT 規範 | 橫向無跡條件 |
| 極化模式 | $+$ 和 $\times$ 兩種 |
| 四極子輻射 | 最低階引力波源 |
| 引力波功率 | $P = \frac{G}{5c^5}\sum|\dddot{I}_{ij}|^2$ |
| LIGO | 激光干涉儀引力波天文台 |
| GW150914 | 首次直接探測的引力波事件 |

## 練習題

1. **引力波應變**：估計 LIGO 的探測靈敏度 $h \sim 10^{-23}$ 對應的臂長變化（$L = 4$ km）。

2. **GW150914 能量**：計算 GW150914 事件中轉化為引力波的能量（$3 M_\odot c^2$）相當於多少次太陽質量的完全質能轉化？

3. **四極矩公式**：推導四極子引力波的功率公式，證明：
   $$P = \frac{G}{5c^5}\sum_{i,j}\left|\dddot{I}_{ij}\right|^2$$

4. **雙星軌道衰減**：對於 PSR B1913+16，使用以下參數計算理論的 $\dot{P}_b$：
   - $m_1 = 1.441 M_\odot$，$m_2 = 1.387 M_\odot$
   - $P_b = 7.75$ 小時，$e = 0.617$

5. **引力波頻率**：對於質量為 $30 M_\odot$ 的兩個黑洞合併，估計：
   - inspiral 最後一圈的頻率
   - ringdown 的特徵頻率

6. **TT 規範**：驗證 TT 規範下的度規擾動矩陣是 trace-free 和橫向的。

7. **干涉儀靈敏度**：解釋為什麼 LIGO 需要長臂和功率回收來提高靈敏度。

8. **多信使天文學**：討論 GW170817 如何同時使用引力波和電磁波信息來約束宇宙學。
