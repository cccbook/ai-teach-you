# 第 22 章：Schwarzschild 解

## 概述

Schwarzschild 解是愛因斯坦場方程的第一個精確解，描述了靜態球對稱真空時空。這個解是卡爾·史瓦西（Karl Schwarzschild）在 1916 年——愛因斯坦發表場方程後僅一個月——計算出來的。這是廣義相對論歷史上的一個里程碑，開啟了現代黑洞物理學的大門。

Schwarzschild 解不僅是理解黑洞的基礎，也是計算太陽系內引力效應（如光線偏折、行星近日點進動）的出發點。雖然光線偏折和近日點進動可以用微擾方法計算，但 Schwarzschild 度規提供了精確的框架。

## 22.1 靜態球對稱度量的推導

### 22.1.1 假設

推導 Schwarzschild 解需要以下假設：

1. **靜態**：度規不隨時間變化，$\partial_t g_{\mu\nu} = 0$
2. **球對稱**：存在繞任意空間原點的旋轉對稱性
3. **真空**：能量-動量張量為零，$T_{\mu\nu} = 0$
4. **漸近平坦性**：當 $r \to \infty$ 時，度規趨近於 Minkowski 度規

這些假設反映了球對稱引力源（如恆星、行星）的物理情況。

### 22.1.2 一般形式

在球座標 $(t, r, \theta, \phi)$ 中，最一般的靜態球對稱度規為：

$$ds^2 = -e^{2\alpha(r)} dt^2 + e^{2\beta(r)} dr^2 + r^2 d\Omega^2$$

其中 $d\Omega^2 = d\theta^2 + \sin^2\theta\, d\phi^2$，函數 $\alpha(r)$ 和 $\beta(r)$ 只依賴於徑向座標 $r$。

我們可以通過 $r$ 的重新定義，將度規化為更簡單的形式。

### 22.1.3 簡化

定義新的徑向函數：
$$A(r) = e^{2\alpha(r)}, \quad B(r) = e^{2\beta(r)}$$

度規寫為：
$$ds^2 = -A(r) c^2 dt^2 + B(r) dr^2 + r^2 d\Omega^2$$

當 $r \to \infty$ 時，$A \to 1$，$B \to 1$，恢復 Minkowski 度規。

## 22.2 Schwarzschild 度量

### 22.2.1 解

將上述度規形式代入真空 Einstein 方程 $R_{\mu\nu} = 0$，得到兩個獨立方程：

從 $R_{tt} = 0$：
$$\frac{A'}{rB} + \frac{1}{r^2} - \frac{1}{r^2B} = 0$$

從 $R_{rr} = 0$：
$$-\frac{A'}{rA} + \frac{1}{r^2} - \frac{1}{r^2B} = 0$$

求解這些方程：

由兩式相減：
$$\frac{A'}{rB} + \frac{A'}{rA} = 0 \Rightarrow A = \frac{C}{B}$$

其中 $C$ 是積分常數。

由 $r \to \infty$ 時 $A \to 1$，得 $C = 1$，因此 $B = 1/A$。

將 $B = 1/A$ 代入任一方程：
$$\frac{A'}{rA^2} + \frac{1}{r^2} - A = 0$$

整理：
$$A' + \left(\frac{1}{r} - r\right)A^2 = \frac{1}{r}A = 0$$

這個方程的解為：
$$A(r) = 1 - \frac{2GM}{c^2 r}$$

其中 $M$ 是積分常數，稍後證明這是引力源的質量。

因此：
$$B(r) = \frac{1}{A(r)} = \frac{1}{1 - \frac{2GM}{c^2 r}}$$

### 22.2.2 完整的 Schwarzschild 度規

$$\boxed{ds^2 = -\left(1 - \frac{2GM}{c^2 r}\right) c^2 dt^2 + \left(1 - \frac{2GM}{c^2 r}\right)^{-1} dr^2 + r^2 d\Omega^2}$$

這就是 Schwarzschild 度規。使用自然單位 $G = c = 1$：
$$ds^2 = -\left(1 - \frac{2M}{r}\right) dt^2 + \left(1 - \frac{2M}{r}\right)^{-1} dr^2 + r^2 d\Omega^2$$

### 22.2.3 常用記號

**Schwarzschild 半徑**：
$$r_s = \frac{2GM}{c^2}$$

這是黑洞事件視界的位置。

度規可以寫為：
$$ds^2 = -\left(1 - \frac{r_s}{r}\right) dt^2 + \left(1 - \frac{r_s}{r}\right)^{-1} dr^2 + r^2 d\Omega^2$$

### 22.2.4 分量

Schwarzschild 度規的矩陣分量：

$$g_{\mu\nu} = \begin{pmatrix} -(1 - r_s/r) & 0 & 0 & 0 \\ 0 & (1 - r_s/r)^{-1} & 0 & 0 \\ 0 & 0 & r^2 & 0 \\ 0 & 0 & 0 & r^2\sin^2\theta \end{pmatrix}$$

逆矩陣：

$$g^{\mu\nu} = \begin{pmatrix} -(1 - r_s/r)^{-1} & 0 & 0 & 0 \\ 0 & (1 - r_s/r) & 0 & 0 \\ 0 & 0 & r^{-2} & 0 \\ 0 & 0 & 0 & r^{-2}\sin^{-2}\theta \end{pmatrix}$$

## 22.3 Schwarzschild 半徑的意義

### 22.3.1 事件視界

當 $r = r_s$ 時：
- $g_{tt} = 0$：時間座標失去意義
- $g_{rr} \to \infty$：徑向座標也失去意義

$r = r_s$ 是**事件視界**——任何東西（包括光）都無法從內部逃逸。

視界是時空的因果邊界：$r < r_s$ 區域中的任何信號都無法到達 $r > r_s$ 區域。

### 22.3.2 數值估計

對於不同天體：

| 天體 | 質量 | Schwarzschild 半徑 |
|------|------|-------------------|
| 太陽 | $2.0 \times 10^{30}$ kg | 3.0 km |
| 地球 | $6.0 \times 10^{24}$ kg | 9 mm |
| 人馬座 A* | $8 \times 10^{36}$ kg | $2.4 \times 10^{10}$ m |

地球的 Schwarzschild 半徑只有約 9 毫米——如果地球被壓縮到這個大小，就會變成黑洞！

### 22.3.3 奇點

當 $r \to 0$ 時，曲率不變量發散：
$$R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma} \propto \frac{1}{r^6}$$

$r = 0$ 是時空奇點——廣義相對論在這裡失效，需要量子引力來描述。

## 22.4 測地線方程

### 22.4.1 守恆量

Schwarzschild 時空有兩個 Killing 向量：
- $\xi^\mu = \partial_t$：能量守恆
- $\xi^\mu_\phi = \partial_\phi$：角動量守恆

能量：
$$E = -g_{\mu\nu}\xi^\mu u^\nu = \left(1 - \frac{r_s}{r}\right)\frac{dt}{d\tau}$$

角動量：
$$L = g_{\mu\nu}\xi^\mu_\phi u^\nu = r^2\frac{d\phi}{d\tau}$$

### 22.4.2 有效勢

類時粒子的徑向運動方程可寫為有效勢形式：
$$\frac{1}{2}\left(\frac{dr}{d\tau}\right)^2 + V_{\text{eff}}(r) = \frac{E^2}{2}$$

其中有效勢：
$$V_{\text{eff}}(r) = -\frac{GM}{r} + \frac{L^2}{2r^2} - \frac{GML^2}{c^2 r^3}$$

### 22.4.3 圓軌道

穩定圓軌道存在於：
$$r > r_{\text{isco}} = \frac{6GM}{c^2}$$

$r_{\text{isco}}$ 是最後穩定圓軌道（Innermost Stable Circular Orbit）。

## 22.5 光線偏折

### 22.5.1 零測地線

對於光子（零質量），測地線方程與類時粒子類似，但參數化不同。

光子的有效勢：
$$V_{\text{eff}}(r) = \frac{L^2}{2r^2}\left(1 - \frac{r_s}{r}\right)$$

### 22.5.2 偏折角

光子經過大質量天體時的總偏折角：
$$\Delta\phi = \frac{4GM}{c^2 b}$$

其中 $b$ 是瞄準參數（impact parameter）。

### 22.5.3 1919 年日食實驗

1919 年，Arthur Eddington 率隊觀測日食，測量星光經過太陽時的偏折：
- 理論預言：$1.75''$（愛因斯坦的完整計算）
- 牛頓理論預言：$0.87''$
- Eddington 的測量：$1.98'' \pm 0.30''$

這次觀測使愛因斯坦的理論廣為人知。

### 22.5.4 引力透鏡

大質量天體會彎曲背景光源的光線，產生：
- 雙重像或多重像
- 愛因斯坦環
- 光弧

這是現代天文學中的重要觀測工具，用於探測不可見的質量。

## 22.6 水星近日點進動

### 22.6.1 牛頓預言

在牛頓引力中，考慮其他行星的攝動後，理論計算與觀測值有約 $43''$/世紀的差距。

### 22.6.2 廣義相對論修正

使用 Schwarzschild 度規計算近日點進動：
$$\Delta\phi = \frac{6\pi GM}{c^2 a(1-e^2)}$$

其中 $a$ 是軌道半長軸，$e$ 是偏心率。

### 22.6.3 水星的異常

對於水星：
- $a = 5.79 \times 10^{10}$ m
- $e = 0.2056$
- $M = M_\odot$

計算給出：
$$\Delta\phi \approx 43'' \text{/世紀}$$

與觀測到的異常精確吻合！

## 22.7 引力時間延遲

### 22.7.1 Shapiro 延遲

當信號經過大質量天體附近時，光程比平坦時空更長，導致時間延遲。

從 Schwarzschild 度規計算，時間延遲為：
$$\Delta t = -\frac{2GM}{c^3}\ln\left(\frac{4r_E r_S}{b^2 c^2}\right)$$

其中 $r_E$ 和 $r_S$ 是發射器和接收器的徑向距離，$b$ 是瞄準參數。

### 22.7.2 實驗驗證

1964 年，Irwin Shapiro 提議用行星雷達回波驗證這個效應：
- 雷達信號從地球發射，經過太陽附近，到達金星或水星，然後返回
- 往返時間比平坦時空預言長約 $10^{-4}$ 秒
- 觀測精度：約 5%

後來的卡西尼號測量將精度提高到約 0.002%。

## 22.8 Kruskal 座標

### 22.8.1 座標奇點

Schwarzschild 座標在 $r = r_s$ 有奇異性——度規分量發散。但這只是座標奇點，不是物理奇點。

### 22.8.2 Kruskal 座標

引入 Kruskal 座標 $(V, U)$：
$$V = \sqrt{\frac{r}{r_s} - 1}\, e^{r/(2r_s)}\sinh\left(\frac{t}{2r_s}\right)$$
$$U = \sqrt{\frac{r}{r_s} - 1}\, e^{r/(2r_s)}\cosh\left(\frac{t}{2r_s}\right)$$

在這些座標中，Schwarzschild 度規為：
$$ds^2 = \frac{4r_s^3}{r}e^{-r/r_s}(dV^2 - dU^2) + r^2 d\Omega^2$$

其中 $r$ 由 $V^2 - U^2 = (r/r_s - 1)e^{r/r_s}$ 給出。

### 22.8.3 最大延拓

Kruskal 圖顯示了 Schwarzschild 時空的最大延拓：
- 區域 I ($r > r_s$, $V > |U|$)：外部宇宙
- 區域 II ($r < r_s$, $V > 0$)：黑洞內部
- 區域 III ($r > r_s$, $V < -|U|$)：另一個宇宙
- 區域 IV ($r < r_s$, $V < 0$)：白洞內部

連接區域 I 和 III 的是蟲洞（Einstein-Rosen 橋），但它是不可穿越的。

## 22.9 潮汐力

### 22.9.1 Riemann 張量

Schwarzschild 時空的非零 Riemann 分量：
$$R_{trtr} = -\frac{2GM}{c^2 r^3}$$
$$R_{t\theta t\theta} = \frac{GMr}{c^2}(1 - \frac{r_s}{r})$$
$$R_{t\phi t\phi} = \frac{GMr\sin^2\theta}{c^2}(1 - \frac{r_s}{r})$$
$$R_{r\theta r\theta} = -\frac{GM}{c^2 r}(1 - \frac{r_s}{r})^{-1}$$
$$R_{r\phi r\phi} = -\frac{GM}{c^2 r}(1 - \frac{r_s}{r})^{-1}\sin^2\theta$$
$$R_{\theta\phi\theta\phi} = \frac{2GMr\sin^2\theta}{c^2}$$

### 22.9.2 潮汐加速度

兩個相隔 $\xi^r$ 的自由粒子之間的相對加速度：
$$\frac{D^2\xi^r}{d\tau^2} = -R^r_{\.trt}\xi^r = -\frac{2GM}{c^2 r^3}\xi^r$$

## 重點回顧

| 概念 | 說明 |
|------|------|
| Schwarzschild 度量 | $ds^2 = -(1-2M/r)dt^2 + (1-2M/r)^{-1}dr^2 + r^2d\Omega^2$ |
| Schwarzschild 半徑 | $r_s = 2GM/c^2$ |
| 事件視界 | $r = r_s$，光無法逃逸 |
| 光線偏折 | $\Delta\phi = 4GM/(c^2 b)$ |
| 近日點進動 | $\Delta\phi = 6\pi GM/(c^2 a(1-e^2))$ |
| ISCO | $r_{\text{isco}} = 6GM/c^2$ |

## 練習題

1. **度規推導**：將一般靜態球對稱度規代入 Einstein 方程，驗證 Schwarzschild 解。

2. **光線偏折**：計算光子經過太陽邊緣（$b = R_\odot$）的偏折角，與 Eddington 的觀測結果比較。

3. **水星進動**：使用以下參數計算水星的近日點進動：
   - $M = M_\odot$，$a = 5.79 \times 10^{10}$ m，$e = 0.2056$

4. **視界**：解釋為什麼 $r = r_s$ 是事件視界而非物理奇點。

5. **潮汐力**：計算靠近 Schwarzschild 黑洞的宇航員感受到的潮汐加速度。

6. **固有時**：計算從靜止於 $r = 10M$ 處的觀測者，經過 $\Delta t = 100M$ 的座標時間後，固有時過了多少？

7. **逃逸速度**：證明在 $r = r_s$ 處，逃逸速度等於光速。
