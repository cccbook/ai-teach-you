# 第 33 章：數值相對論入門

## 概述

數值相對論是應用計算機數值方法求解愛因斯坦場方程的學科。雖然愛因斯坦方程在某些對稱情況下有解析解（如 Schwarzschild、Kerr 度規），但在更一般的物理情況下——如兩個黑洞相互繞轉並最終合併——解析求解是不可能的。這時，數值相對論提供了理解這些系統的唯一可靠方法。

數值相對論的歷史可以追溯到 1960 年代，但這個領域長期面臨嚴重的數值不穩定性問題。直到 2005 年的「突破」——芝加哥大學的模擬團隊成功模擬了雙黑洞合併——數值相對論才真正成為實用的工具。這一突破為 2015 年 LIGO 探測引力波奠定了理論基礎。

數值相對論的核心挑戰在於廣義相對方程本身的複雜性。方程是非線性的、高度耦合的，而且包含約束條件。數值求解這些方程需要巧妙的數學處理、強大的計算資源和精細的數值技巧。

## 33.1 3+1 分解

### 33.1.1 動機

廣義相對論是一個协變理論——時空坐標的選擇是任意的。這既是理論的優美之處，也是數值求解的困難所在。

為了解方程，我們需要：
1. 固定 Gauge（座標條件）
2. 將四維方程分解為 3+1 維
3. 分離約束方程和演化方程

3+1 分解是實現這一切的數學框架。

### 33.1.2 空間-時間分離

將時空流形 $\mathcal{M}$ 分解為一族空間超曲面 $\Sigma_t$，每個超曲面是三維空間。

引入：
- **餘切函數** $\alpha(t, x^i)$：測量超曲面上不同點的固有时流逝
- **位移向量** $\beta^i(t, x^i)$：測量超曲面之間的相對位移

度規分解為：

$$ds^2 = -\alpha^2 dt^2 + \gamma_{ij}(dx^i + \beta^i dt)(dx^j + \beta^j dt)$$

這被稱為**線元**或**ADM 度規**（Arnowitt-Deser-Misner 形式）。

### 33.1.3 空間度規

三維空間度規 $\gamma_{ij}$ 是超曲面上的誘導度規：

$$\gamma_{ij} = g_{\mu\nu}e_i^\mu e_j^\nu$$

其中 $e_i^\mu = \partial x^\mu/\partial x^i$ 是超曲面的切向量。

$\gamma_{ij}$ 描述了每個超曲面的幾何。

### 33.1.4 外延曲率

外延曲率 $K_{ij}$ 描述超曲面如何在四維時空中彎曲：

$$K_{ij} = \frac{1}{2\alpha}\left(\partial_t \gamma_{ij} - \nabla_i\beta_j - \nabla_j\beta_i\right)$$

其中 $\nabla_i$ 是空間協變導數。

$K_{ij}$ 是對稱張量，描述：
- 膨脹：$K = \gamma^{ij}K_{ij}$
- 剪切：$K_{ij} - \frac{1}{3}\gamma_{ij}K$
- 旋轉：不存在（超曲面無扭轉）

## 33.2 Einstein 方程的分解

### 33.2.1 Einstein 方程的回顧

Einstein 方程為：

$$G_{\mu\nu} = 8\pi T_{\mu\nu}$$

其中 $G_{\mu\nu} = R_{\mu\nu} - \frac{1}{2}g_{\mu\nu}R$ 是 Einstein 張量。

在 3+1 分解中，這個方程被分解為：
- 約束方程：定義初始數據
- 演化方程：描述時間演化

### 33.2.2 哈密頓約束

哈密頓約束來自 $G_{00}$ 分量：

$$R + K^2 - K_{ij}K^{ij} = 16\pi\rho$$

其中：
- $R$ 是三維空間 Ricci 標量
- $K_{ij}$ 是外延曲率
- $\rho = T_{\mu\nu}n^\mu n^\nu$ 是能量密度（相對於靜止觀測者）

這個方程不包含時間導數——它是一個約束，必須在每個時刻滿足。

### 33.2.3 動量約束

動量約束來自 $G_{0i}$ 分量：

$$D_j(K^{ij} - \gamma^{ij}K) = 8\pi S^i$$

其中 $D_j$ 是空間協變導數，$S^i = -\gamma^{ij}n^\mu T_{\mu j}$ 是動量密度。

動量約束同樣是約束——不包含時間導數。

### 33.2.4 演化方程

演化方程來自 $G_{ij}$ 分量：

$$\partial_t K_{ij} = \nabla_i\nabla_j\alpha - \alpha\left(R_{ij} + KK_{ij} - 2K_{ik}K^k_j\right) + \mathcal{L}_\beta K_{ij} - 8\pi\alpha S_{ij}$$

這個方程包含時間導數，描述外延曲率如何演化。

另一個演化方程是 $\partial_t \gamma_{ij}$，由 $K_{ij}$ 的定義給出。

## 33.3 約束方程的求解

### 33.3.1 初始數據問題

要開始數值模擬，需要提供初始數據：
- $\gamma_{ij}$：初始超曲面的空間度規
- $K_{ij}$：初始外延曲率

這些必須滿足約束方程：
$$R + K^2 - K_{ij}K^{ij} = 16\pi\rho$$
$$D_j(K^{ij} - \gamma^{ij}K) = 8\pi S^i$$

這是一個橢圓型方程組的邊值問題。

### 33.3.2 共形分解

求解約束方程的標準方法是共形分解。將度規寫為：

$$\gamma_{ij} = \psi^4 \bar{\gamma}_{ij}$$

其中 $\psi$ 是共形因子，$\bar{\gamma}_{ij}$ 是參考度規（通常選為平坦或球對稱）。

約束方程可以重寫為關於 $\psi$ 和其他量的方程。

### 33.3.3 Lichnerowicz-York 方程

在無物質（$T_{\mu\nu} = 0$）的情況下，約束方程簡化為：

$$\bar{D}^2\psi = -\frac{1}{8}\bar{A}_{ij}\bar{A}^{ij}\psi^{-7}$$

其中 $\bar{A}_{ij}$ 是與 $K_{ij}$ 相關的 trace-free 部分。

這是**Lichnerowicz 方程**，是一個非線性橢圓方程。

### 33.3.4 Bowen-York 數據

Bowen 和 York 提出了具有明確形式解的初始數據：

$$K_{ij} = \frac{3}{2r^2}\left[n_i P_j + n_j P_i - \gamma_{ij}(n^k P_k)\right] + \frac{3}{r^3}\epsilon_{kij}S^k$$

其中：
- $P^i$ 是線性動量
- $S^i$ 是角動量
- $n^i$ 是徑向單位向量

這些數據對應於具有特定物理參數的孤立系統。

## 33.4 數值方法

### 33.4.1 有限差分

有限差分是離散化偏微分方程的最基本方法。

將連續函數 $f(x)$ 離散化為網格點 $f_i = f(x_i)$，然後用有限差分近似導數：

$$\partial_x f \approx \frac{f_{i+1} - f_{i-1}}{2\Delta x} \quad \text{（中心差分）}$$
$$\partial_x^2 f \approx \frac{f_{i+1} - 2f_i + f_{i-1}}{(\Delta x)^2} \quad \text{（二階導數）}$$

精度由差分近似的階數決定。

### 33.4.2 譜方法

譜方法使用函數的展開來表示解：

$$f(x) = \sum_n a_n \phi_n(x)$$

其中 $\phi_n(x)$ 是基函數（如球諧函數、Chebyshev 多項式）。

優點：
- 精度極高（指數收斂）
- 適合對稱問題

缺點：
- 對於非光滑函數不適用
- 對應用域幾何有限制

### 33.4.3 約束傳播

約束傳播方法不直接求解約束方程，而是在演化過程中監控約束的違反程度。

約束方程應該在整個演化過程中保持滿足。實際上，由於數值誤差，它們會逐漸偏離零。

約束傳播方法有時被稱為「輕觸」方法，因為它們不試圖嚴格求解約束。

### 33.4.4 芝加哥格式

芝加哥格式（Chicago scheme）是由芝加哥大學發展的約束求解方法：

1. **自由演化**：忽略約束，只演化 Einstein 方程
2. **約束監控**：監控約束的違反程度
3. **修正**：必要時應用約束修正

这种方法在 2005 年成功模擬了雙黑洞合併。

### 33.4.5 移動穿刺點

對於黑洞數值模擬，使用「穿刺」（puncture）表示黑洞：

- 度規在穿刺點是奇異的
- 但物理量（如曲率）是良好的
- 約束方程在穿刺點需要特殊處理

移動穿刺點方法跟踪每個黑洞的位置，允許它們相互繞轉。

## 33.5 自適應網格細化

### 33.5.1 多層次網格

數值相對論模擬需要在不同尺度上解析物理：

- 黑洞附近：需要高分辨率
- 遠處：只需要低分辨率

自適應網格細化（AMR）自動調整網格分辨率：

- 在需要精度的區域使用細網格
- 在其他區域使用粗網格
- 網格層次動態調整

### 33.5.2 嵌套盒方法

嵌套盒方法使用嵌套的直角網格：
- 最細的網格包圍感興趣的區域
- 每個粗網格覆蓋相鄰的更大區域
- 網格之間應用邊界條件

### 33.5.3 確保精度

AMR 需要確保：
- 不同網格層次之間的一致性
- 約束在所有層次都滿足
- 總能量-動量的準確計算

## 33.6 雙黑洞合併

### 33.6.1 合併的三個階段

雙黑洞合併可以分為三個階段：

1. **緩慢逼近（Inspiral）**
   - 兩個黑洞相互繞轉
   - 逐漸靠近
   - 能量通過引力波輻射損失
   - 後牛頓近似有效

2. **合併（Merger）**
   - 黑洞接觸並合併
   - 強非線性動力學
   - 大量引力波發射
   - 需要數值模擬

3. **鈴宕（Ringdown）**
   - 合併後的黑洞震盪
   - 發射衰減的引力波
   - 可以用黑洞微擾理論描述

### 33.6.2 質量比

質量比 $q = M_1/M_2$（設 $M_1 > M_2$）是關鍵參數：
- $q = 1$：兩個黑洞質量相等
- $q \gg 1$：一個黑洞遠比另一個大

極端質量比帶來數值挑戰：
- 小的黑洞需要極高分辨率
- 需要很長時間才能靠近

### 33.6.3 自旋

黑洞的自旋也是重要參數：
- 黑洞可以同向或逆向旋轉
- 自旋影響 ISCO 的位置
- 自旋影響引力波波形

## 33.7 引力波提取

### 33.7.1 遠場極限

在遠離波源（$r \to \infty$）處，引力波可以用 Newmann-Penrose 標量 $\Psi_4$ 提取：

$$\Psi_4 = -R_{\alpha\beta\gamma\delta} l^\alpha m^\beta l^\gamma m^\delta$$

其中 $l^\mu$ 和 $m^\mu$ 是特定的光like 矢量。

引力波能量為：

$$\frac{dE}{dt} = \frac{1}{16\pi}\lim_{r\to\infty}\int|\Psi_4|^2 r^2 d\Omega$$

### 33.7.2 波形

引力波波形是時間序列 $h_+(t)$ 和 $h_\times(t)$。

這些波形可以與後牛頓預言比較，並用於：
- 約束黑洞參數
- 測量距離
- 測試廣義相對論

### 33.7.3 信噪比

探測器中的信噪比（SNR）為：

$$\rho^2 = 4\int_0^\infty\frac{|\tilde{h}(f)|^2}{S_n(f)}df$$

其中 $S_n(f)$ 是噪聲功率譜密度。

高 SNR 對於可靠檢測和參數估計至關重要。

## 33.8 軟件和資源

### 33.8.1 主要數值相對論代碼

| 代碼名稱 | 機構 | 特點 |
|----------|------|------|
| SpEC | Caltech/Cornell | 譜方法，雙黑洞 |
| BAM | Jena/Potsdam | 有限差分，AMR |
| LEAN | AEI | 黑洞模擬 |
| Cactus | AEI/LLNL | 框架代碼 |
| Whisky | Perimeter | GRMHD |

### 33.8.2 計算資源

數值相對論模擬需要大量計算資源：
- 單次雙黑洞模擬：數万到數百萬 CPU 小時
- 參數空間探索：數百萬 CPU 小時
- 使用超級計算機和 GPU 加速

### 33.8.3 波形數據庫

數值相對論模擬的結果被存儲在波形數據庫中：
- **SXS (Simulating eXtreme Spacetimes)**: https://data.black-holes.org
- **RIT**: Rochester Institute of Technology
- **GaTech**: Georgia Tech

這些波形被用於 LIGO 數據分析。

## 33.9 數值相對論的應用

### 33.9.1 LIGO 數據分析

數值相對論波形是 LIGO 數據分析的關鍵：
- 提供模板進行匹配濾波
- 約束黑洞質量、 spin
- 測試廣義相對論

### 33.9.2 黑洞陰影

數值模擬也用於黑洞陰影的預言：
- 黑洞陰影的大小和形狀
- 光子環的結構
- 與觀測比較

### 33.9.3 宇宙學應用

數值相對論也應用於宇宙學：
- 宇宙微波背景的形成
- 引力透鏡的數值模擬
- 宇宙大尺度結構

## 33.10 Python 示例

以下 Python 代碼演示了簡單的數值相對論概念：

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def schwarzschild_geodesic(y, tau, E, L, a=0):
    """計算 Schwarzschild 時空中的測地線
    y = [r, theta, phi, dr/dtau, dtheta/dtau, dphi/dtau]
    """
    r, theta, phi, dr, dtheta, dphi = y
    
    # 參數
    M = 1.0
    
    # 有效勢能
    V_eff = (1 - 2*M/r) * (L**2/r**2 + a**2/r**2)
    dV_dr = -2*(1 - 2*M/r)*L**2/r**3 + L**2*(1 - 2*M/r)/r**4 * 2*M + a**2*(2*M/r**3)
    
    # 徑向運動方程
    dr_dtau = dr
    d2r_dtau2 = 0.5 * dV_dr / E
    
    return [dr, d2r_dtau2, dtheta, 0, dphi, 0]

# 初始條件：赤道面上的圓軌道
M = 1.0
r0 = 6 * M  # ISCO
v_phi = np.sqrt(M / r0)
E = (1 - 2*M/r0) / np.sqrt(1 - 3*M/r0)
L = r0 * v_phi

y0 = [r0, np.pi/2, 0, 0, 0, v_phi]

# 積分
tau = np.linspace(0, 1000, 10000)
solution = odeint(schwarzschild_geodesic, y0, tau, args=(E, L))

r = solution[:, 0]
phi = solution[:, 2]

# 繪圖
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.plot(r * np.cos(phi), r * np.sin(phi), 'b-', linewidth=0.5)
theta_grid = np.linspace(0, 2*np.pi, 100)
plt.plot(2*M * np.cos(theta_grid), 2*M * np.sin(theta_grid), 'k-', linewidth=2, label='事件視界')
plt.xlabel('x / M')
plt.ylabel('y / M')
plt.title('Schwarzschild 時空中的測地線')
plt.legend()
plt.axis('equal')
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(tau, r, 'r-')
plt.xlabel('原時 τ / M')
plt.ylabel('r / M')
plt.title('徑向距離隨時間變化')
plt.grid(True)

plt.tight_layout()
plt.savefig('geodesic_orbit.png', dpi=150)
plt.show()

print(f"軌道週期（固有時）: {2 * np.pi * r0**1.5 / M:.2f} M")
```

## 重點回顧

| 概念 | 說明 |
|------|------|
| 3+1 分解 | 時空分解為空間+時間 |
| ADM 度規 | $ds^2 = -\alpha^2 dt^2 + \gamma_{ij}(dx^i + \beta^i dt)(dx^j + \beta^j dt)$ |
| 外延曲率 $K_{ij}$ | 超曲面彎曲的度量 |
| 哈密頓約束 | $R + K^2 - K_{ij}K^{ij} = 16\pi\rho$ |
| 動量約束 | $D_j(K^{ij} - \gamma^{ij}K) = 8\pi S^i$ |
| Lichnerowicz 方程 | 約束方程的標準形式 |
| 穿刺表示 | 表示黑洞的數值方法 |
| SpEC/BAM | 主要數值相對論代碼 |

## 練習題

1. **3+1 分解**：推導 ADM 度規中度規分量的表達式：$g_{tt}$、$g_{ti}$、$g_{ij}$。

2. **約束方程**：驗證哈密頓約束和動量約束不包含 $\partial_t$ 導數，因此是真正的約束。

3. **ISC0**：計算 Schwarzschild 黑洞 ISCO 的位置，證明 $r = 6GM/c^2$。

4. **有效勢能**：對於 Schwarzschild 時空中的類時測地線，導出徑向運動方程的有效勢能。

5. **數值精度**：比較有限差分和譜方法的收斂率，解釋為什麼譜方法通常更精確。

6. **能量提取**：從 $\Psi_4$ 導出引力波能量的表達式。

7. **信噪比**：給定一個波形模板，計算其在 LIGO 靈敏度曲線下的信噪比。

8. **黑洞合併階段**：描述雙黑洞合併的三個階段，並解釋為什麼每個階段需要不同的處理方法。

9. **約束傳播**：比較約束傳播方法和約束求解方法，討論它們各自的優缺點。

10. **波形模板**：解釋數值相對論波形如何被用於 LIGO 數據分析。
