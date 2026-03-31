# 第 25 章：Reissner-Nordström 度規

## 概述

本章介紹帶電黑洞的時空幾何——Reissner-Nordström 度規。這是 Schwarzschild 解的帶電推廣，展示了電荷如何改變黑洞的結構和性質。Reissner-Nordström 度規是廣義相對論中第一個同時考慮質量電荷的精確解，對理解帶電黑洞的物理性質至關重要。在真實宇宙中，黑洞可能帶電（雖然可能很快被中和），這個解提供了一個重要的理論模型。

帶電黑洞與非帶電黑洞之間存在顯著差異。首先，電荷會修改視界的位置，使得內外視界都可能存在。其次，當電荷足夠大時，視界可能消失，暴露出奇點——這被稱為「裸奇點」，是物理學中不希望出現的情況。最後，帶電黑洞周圍存在強大的電磁場，這會影響物質的運動和黑洞的演化。

## 25.1 Einstein-Maxwell 方程

### 25.1.1 真空中的電磁場

在廣義相對論中，電磁場與時空幾何是耦合的。真空中的 Einstein 方程為：

$$R_{\mu\nu} - \frac{1}{2}g_{\mu\nu}R = 8\pi T_{\mu\nu}$$

當唯一的場源是電磁場時，能量-動量張量由 Maxwell 張量給出：

$$T_{\mu\nu} = \frac{1}{4\pi}\left(F_{\mu\alpha}F^\alpha_\nu - \frac{1}{4}g_{\mu\nu}F_{\alpha\beta}F^{\alpha\beta}\right)$$

其中 $F_{\mu\nu}$ 是電磁場張量，定義為：

$$F_{\mu\nu} = \partial_\mu A_\nu - \partial_\nu A_\mu$$

這裡 $A_\mu$ 是四維電磁勢。在 Lorenz 規範條件下：

$$\nabla_\mu F^{\mu\nu} = 0$$

這個規範條件確保了 Maxwell 方程在廣義相對論中的協變形式。

### 25.1.2 電磁場張量的結構

對於一個靜止的點電荷 $Q$ 位於原點，其電磁場張量在球座標中具有簡潔的形式。非零分量為：

$$F_{tr} = F^{tr} = \frac{Q}{r^2}$$
$$F_{rt} = -F_{tr} = -\frac{Q}{r^2}$$

注意，這裡我們使用度規符號 $(-,+,+,+)$。張量 $F_{\mu\nu}$ 是反對稱的，因此：

$$F_{\theta\phi} = F_{r\theta} = F_{tr} = 0$$

等等。這個簡單的結構反映了球對稱電荷分布的對稱性。

### 25.1.3 協變導數與電流

在有電磁場存在的情況下，協變導數需要考慮規範場的影響：

$$D_\mu = \nabla_\mu - iqA_\mu$$

這是 U(1) 叢上的協變導數。當然，在經典廣義相對論中，我們主要關心的是經典 Maxwell 方程和 Einstein 方程的耦合。

## 25.2 Reissner-Nordström 度規推導

### 25.2.1 對稱性假設

推導 Reissner-Nordström 度規需要以下假設：

1. **球對稱性**：時空具有 $SO(3)$ 對稱性，即對任意空間旋轉不變
2. **靜態**：度規不隨時間變化，所有 $\partial_t$ 方向的Killings向量存在
3. **真空**：在帶電物體外部，$T_{\mu\nu} = 0$（愛因斯坦方程的右邊由 Maxwell 張量貢獻，但在靜止區域，電磁場與度規是獨立的）
4. **帶電**：存在非零的電磁場，電荷量為 $Q$

這些假設與推導 Schwarzschild 度規時的假設完全相同，只是增加了電荷的存在。

### 25.2.2 度規的通用形式

球對稱靜態度規的最一般形式為：

$$ds^2 = -e^{2\Phi(r)}dt^2 + e^{2\Lambda(r)}dr^2 + r^2 d\Omega^2$$

其中 $d\Omega^2 = d\theta^2 + \sin^2\theta\, d\phi^2$ 是單位球面上的度規。函數 $\Phi(r)$ 和 $\Lambda(r)$ 只依賴於徑向座標 $r$。

### 25.2.3 計算 Ricci 張量

為求解 Einstein-Maxwell 方程，我們需要計算 Christoffel 符號和非零的 Ricci 張量分量。使用線元：

$$g_{tt} = -e^{2\Phi(r)}, \quad g_{rr} = e^{2\Lambda(r)}, \quad g_{\theta\theta} = r^2, \quad g_{\phi\phi} = r^2\sin^2\theta$$

逆度規為：

$$g^{tt} = -e^{-2\Phi(r)}, \quad g^{rr} = e^{-2\Lambda(r)}, \quad g^{\theta\theta} = \frac{1}{r^2}, \quad g^{\phi\phi} = \frac{1}{r^2\sin^2\theta}$$

非零的 Christoffel 符號為：

$$\Gamma^r_{tt} = e^{2(\Phi-\Lambda)}\Phi', \quad \Gamma^r_{rr} = \Lambda', \quad \Gamma^r_{\theta\theta} = -re^{-2\Lambda}$$
$$\Gamma^r_{\phi\phi} = -r\sin^2\theta\, e^{-2\Lambda}, \quad \Gamma^\theta_{r\theta} = \frac{1}{r}, \quad \Gamma^\theta_{\phi\phi} = -\sin\theta\cos\theta$$
$$\Gamma^\phi_{r\phi} = \frac{1}{r}, \quad \Gamma^\phi_{\theta\phi} = \cot\theta$$

其中 $'$ 表示對 $r$ 的導數。

### 25.2.4 Ricci 張量分量

計算 Ricci 張量 $R_{\mu\nu} = \partial_\alpha\Gamma^\alpha_{\mu\nu} - \partial_\mu\partial_\nu\ln\sqrt{-g} + \Gamma^\alpha_{\mu\nu}\Gamma_{\alpha\lambda}^\lambda - \Gamma^\alpha_{\mu\lambda}\Gamma^\lambda_{\nu\alpha}$，得到：

$$R_{tt} = e^{2(\Phi-\Lambda)}\left[\Phi'' + (\Phi')^2 - \Phi'\Lambda' - \frac{2\Phi'}{r}\right]$$
$$R_{rr} = -\Phi'' - (\Phi')^2 + \Phi'\Lambda' + \frac{2\Lambda'}{r}$$
$$R_{\theta\theta} = e^{-2\Lambda}\left[r(\Lambda' - \Phi') - 1\right] + 1$$
$$R_{\phi\phi} = \sin^2\theta\, R_{\theta\theta}$$

其他分量為零。

### 25.2.5 Einstein 方程求解

Einstein 方程為 $R_{\mu\nu} = 8\pi(T_{\mu\nu} - \frac{1}{2}g_{\mu\nu}T)$，其中 $T_{\mu\nu}$ 是 Maxwell 能量-動量張量。

對於球對稱靜態電磁場，Maxwell 張量的非零分量為：

$$F_{tr} = \frac{Q}{r^2}, \quad F^{tr} = -\frac{Q}{r^2}e^{-2(\Phi+\Lambda)}$$

計算 Maxwell 張量：

$$T_{tt} = \frac{Q^2}{8\pi r^4}e^{2(\Phi+\Lambda)}, \quad T_{rr} = -\frac{Q^2}{8\pi r^4}$$
$$T_{\theta\theta} = \frac{Q^2}{8\pi r^2}, \quad T_{\phi\phi} = \frac{Q^2}{8\pi r^2}\sin^2\theta$$

跡為 $T = -\frac{Q^2}{2\pi r^4}$。

### 25.2.6 求解 $tt$ 分量

從 $R_{tt}$ 方程：

$$R_{tt} = 8\pi\left(T_{tt} - \frac{1}{2}g_{tt}T\right) = 8\pi\left(\frac{Q^2}{8\pi r^4}e^{2(\Phi+\Lambda)} + \frac{1}{2}e^{2\Phi}\frac{Q^2}{2\pi r^4}\right) = \frac{Q^2}{r^4}e^{2(\Phi+\Lambda)}$$

即：

$$\Phi'' + (\Phi')^2 - \Phi'\Lambda' - \frac{2\Phi'}{r} = \frac{Q^2}{r^4}$$

### 25.2.7 求解 $rr$ 分量

從 $R_{rr}$ 方程：

$$R_{rr} = 8\pi\left(T_{rr} - \frac{1}{2}g_{rr}T\right) = 8\pi\left(-\frac{Q^2}{8\pi r^4} + \frac{1}{2}e^{2\Lambda}\frac{Q^2}{2\pi r^4}\right) = \frac{Q^2}{r^4}e^{2\Lambda}$$

即：

$$-\Phi'' - (\Phi')^2 + \Phi'\Lambda' - \frac{2\Lambda'}{r} = \frac{Q^2}{r^4}$$

### 25.2.8 聯立求解

將 $tt$ 和 $rr$ 分量相加：

$$- \frac{2}{r}(\Phi' + \Lambda') = \frac{2Q^2}{r^4}e^{2\Lambda}$$

化簡得：

$$\Phi' + \Lambda' = -\frac{Q^2}{r^3}e^{2\Lambda}$$

定義 $f(r) = e^{-2\Lambda}$，則 $e^{2\Lambda} = 1/f$，$\Lambda' = -\frac{f'}{2f}$，$\Phi' = -\Lambda' - \frac{Q^2}{r^3}e^{2\Lambda} = \frac{f'}{2f} - \frac{Q^2}{r^3f}$。

另一方面，$R_{\theta\theta}$ 分量給出：

$$r(\Lambda' - \Phi') - 1 + f = 0$$

代入 $\Phi'$ 和 $\Lambda'$：

$$r\left(-\frac{f'}{2f} - \frac{f'}{2f} + \frac{Q^2}{r^3f}\right) - 1 + f = 0$$

化簡：

$$-\frac{rf'}{f} + \frac{Q^2}{r^2 f} - 1 + f = 0$$

$$rf' = f^2 - f + \frac{Q^2}{r^2}f = f\left(f - 1 + \frac{Q^2}{r^2}\right)$$

這給出一階微分方程。解為：

$$f(r) = 1 - \frac{2M}{r} + \frac{Q^2}{r^2}$$

其中 $M$ 是積分常數，稍後證明這是黑洞的質量。

### 25.2.9 完整的 Reissner-Nordström 度規

因此，度規函數為：

$$e^{2\Phi} = e^{-2\Lambda} = 1 - \frac{2M}{r} + \frac{Q^2}{r^2}$$

完整的線元為：

$$ds^2 = -\left(1 - \frac{2M}{r} + \frac{Q^2}{r^2}\right)dt^2 + \left(1 - \frac{2M}{r} + \frac{Q^2}{r^2}\right)^{-1}dr^2 + r^2 d\Omega^2$$

這就是 Reissner-Nordström 度規。積分常數 $M$ 對應於黑洞的 ADM 質量，$Q$ 對應於總電荷。

## 25.3 視界結構

### 25.3.1 視界的位置

Reissner-Nordström 度規中的視界由 $g_{rr} \to \infty$ 的位置給出，即度規函數的根：

$$f(r) = 1 - \frac{2M}{r} + \frac{Q^2}{r^2} = 0$$

這是關於 $r$ 的二次方程：

$$r^2 - 2Mr + Q^2 = 0$$

解為：

$$r_\pm = M \pm \sqrt{M^2 - Q^2}$$

這裡 $r_+$ 是事件視界（外視界），$r_-$ 是 Cauchy 視界（內視界）。

### 25.3.2 視界數量的分類

根據 $Q$ 和 $M$ 的關係，視界結構可以分為三類：

**情況 1：$M^2 > Q^2$（普通黑洞）**

這時 $\sqrt{M^2 - Q^2}$ 是實數且小於 $M$，因此存在兩個正實根：

$$r_+ = M + \sqrt{M^2 - Q^2} > 0$$
$$r_- = M - \sqrt{M^2 - Q^2} > 0$$

黑洞的結構類似於 Schwarzschild 黑洞，但多了一個內視界 $r_-$。從 $r_+$ 外部可以逃離黑洞，但從 $r_-$ 內部無法逃離。在 $r_-$ 和 $r_+$ 之間的區域稱為「黑洞外核」（outer core）或「過渡區」。

**情況 2：$M^2 = Q^2$（極端黑洞）**

這時 $\sqrt{M^2 - Q^2} = 0$，兩個根重合：

$$r_+ = r_- = M$$

這是極端 Reissner-Nordström 黑洞。外視界和內視界合併，消去了中間的奇異區域。極端黑洞具有一些獨特的性質，例如它的表面重力為零（正如我們將在下一節看到的）。

**情況 3：$M^2 < Q^2$（裸奇點）**

這時 $\sqrt{M^2 - Q^2}$ 是虛數，沒有實數根！這意味著不存在視界，時空奇點完全暴露在外。這就是「裸奇點」，是物理學家不希望出現的情況，因為在奇點附近物理定律會失效。

彭羅斯提出了「宇宙審查假說」（cosmic censorship conjecture），認為在一般初始條件下，裸奇點不會在物理過程中形成。這個假說至今仍未被證明或推翻。

### 25.3.3 視界的幾何意義

視界 $r_+$ 是事件視界——一旦穿過這個界面，任何信號都無法逃離黑洞到達外部觀測者。這是因果性的結果：視界內部的未來光錐完全指向黑洞內部。

內視界 $r_-$ 是 Cauchy 視界。經典廣義相對論中，Cauchy 視界是決定性可能失效的邊界——初始數據在視界外部給定時，無法唯一預測穿過 Cauchy 視界後的演化。這與時空奇異性的穩定性密切相關。

### 25.3.4 面積定理

黑洞的面積永遠不會減少（類似於熱力學第二定律）。對於 Reissner-Nordström 黑洞，視界面積為：

$$A = 4\pi r_+^2 = 4\pi\left(M + \sqrt{M^2 - Q^2}\right)^2$$

可以驗證，當物質落入黑洞時（假設電荷被中和或質量增加），面積確實增加。

## 25.4 奇點結構

### 25.4.1 $r = 0$ 處的奇點

當 $r \to 0$ 時，度規函數 $f(r) \to -\infty$，這表明存在時空奇點。檢查曲率不變量：

$$R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma} = \frac{48M^2}{r^6} - \frac{96MQ^2}{r^6} + \frac{56Q^4}{r^6} = \frac{48(M^2 - 2MQ^2/r + 7Q^2/6Q^2)}{r^6}$$

實際計算給出：

$$R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma} = \frac{48M^2 - 144MQ^2/r + 168Q^2}{r^6}$$

當 $r \to 0$ 時，Kretschmann 標量發散，因此 $r = 0$ 確實是時空奇點。

### 25.4.2 奇點的電荷依賴性

對於非零電荷的奇點，曲率不變量包含 $Q^2$ 項。這與 Schwarzschild 奇點（純質量奇點）不同。在 Schwarzschild 情況下，$Q = 0$，Kretschmann 標量為 $R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma} \propto M^2/r^6$。

## 25.5 測地線運動

### 25.5.1 守恆量

對於靜態球對稱度規，存在兩個 Killing 向量：$\xi_t = \partial_t$ 和 $\xi_\phi = \partial_\phi$。因此，對於任何粒子的測地線，有兩個守恆量：

$$E = -g_{\mu\nu}\xi^\mu_{(t)}u^\nu = \left(1 - \frac{2M}{r} + \frac{Q^2}{r^2}\right)\frac{dt}{d\tau}$$
$$L = g_{\mu\nu}\xi^\mu_{(\phi)}u^\nu = r^2\frac{d\phi}{d\tau}$$

其中 $E$ 是無單位質量的能量（類似於 Schwarzschild 情況中的 $E$），$L$ 是角動量。

### 25.5.2 有效勢能

對於類時測地線（質量 $m > 0$ 的粒子），徑向運動方程為：

$$\frac{1}{2}\left(\frac{dr}{d\tau}\right)^2 + V_{\text{eff}}(r) = \frac{E^2 - m^2}{2m^2}$$

其中有效勢能為：

$$V_{\text{eff}}(r) = \frac{m^2}{2}\left(1 - \frac{2M}{r} + \frac{Q^2}{r^2}\right)\left(1 + \frac{L^2}{m^2 r^2}\right)$$

注意這與 Schwarzschild 情況的區別：中間多了一項 $Q^2/r^2$。

### 25.5.3 視界的影響

視界 $r_+$ 總是小於 Schwarzschild 半徑 $2M$（當 $Q \neq 0$ 時）。這意味著帶電黑洞的視界更靠近奇點。當 $Q \to M$ 時，$r_+ \to M$，而 $2M$ 保持不變。

## 25.6 極端 Reissner-Nordström 黑洞

### 25.6.1 極端極限

當 $|Q| = M$ 時，取極限 $Q \to M$，得到極端 Reissner-Nordström 度規：

$$ds^2 = -\left(1 - \frac{M}{r}\right)^2 dt^2 + \left(1 - \frac{M}{r}\right)^{-2}dr^2 + r^2 d\Omega^2$$

注意這裡 $f(r) = (1 - M/r)^2$，因此 $e^{2\Phi} = e^{-2\Lambda} = (1 - M/r)^2$。

### 25.6.2 表面重力

黑洞的表面重力定義為：

$$\kappa = \lim_{r \to r_+}\frac{\sqrt{(\nabla\xi)^2}}{-\xi}$$

其中 $\xi = \partial_t$ 是時間類Killings向量。對於 Reissner-Nordström 黑洞：

$$\kappa = \frac{r_+ - r_-}{2r_+^2}$$

在極端情況 $r_+ = r_- = M$ 下，$\kappa = 0$。這與黑洞熱力學一致——極端黑洞的溫度為零。

### 25.6.3 物理意義

表面重力為零意味著：
1. 極端黑洞的視界上沒有「拉力」——粒子可以靜止在視界上
2. 由 Hawking 辐射公式，溫度 $T = \hbar\kappa/(2\pi k_B) = 0$，沒有熱輻射
3. 極端黑洞是穩定的，不會蒸發

## 25.7 黑洞熱力學

### 25.7.1 黑洞 entropy

黑洞熱力學第一定律：

$$dM = \kappa\, dA/2 + \Phi_H\, dQ$$

其中 $\Phi_H = Q/r_+$ 是視界電勢。熵為：

$$S = \frac{k_B c^3 A}{4G\hbar} = \frac{k_B c^3 \pi r_+^2}{G\hbar}$$

這是著名的 Bekenstein-Hawking 熵公式。

### 25.7.2 Smarr 公式

對於 Reissner-Nordström 黑洞，Smarr 公式給出：

$$M = 2\sqrt{\pi A}\left(\frac{\kappa}{8\pi G} + \frac{\Phi_H}{2}\right)$$

這與廣義均勻化條件一致。

## 25.8 Penrose 圖

### 25.8.1 最大拓展

Reissner-Nordström 時空可以進行最大解析拓展。Penrose 圖顯示了完整的因果結構。

圖中有四個區域：
1. **區域 I**（外部）：$r > r_+$，漸近平坦區域
2. **區域 II**（黑洞內部）：$r_- < r < r_+$，黑洞內部
3. **區域 III**（奇點區域）：$r < r_-$，Cauchy 視界內
4. **區域 IV**（白洞/另一個宇宙）：穿過 $r_-$ 後的區域

### 25.8.2 內視界的穩定性

與 Schwarzschild 黑洞的奇點不同，Reissner-Nordström 黑洞的內視界可能是時空中的非奇異邊界。考慮光線在內視界附近的行為：聚焦效應可能將奇點替換為一個震盪的內部區域。

## 25.9 物理應用

### 25.9.1 帶電黑洞的形成

在自然界中，黑洞通過超新星爆發或緻密天體合併形成。形成的黑洞通常會快速中和電荷，因為周圍的等離子體會吸引異號電荷並排斥同號電荷。然而，在某些極端情況（如快速旋轉中子星的磁流體動力學坍縮），可能形成短暫的帶電黑洞。

### 25.9.2 統一理論中的 Reissner-Nordström 解

在超弦理論和其他統一理論中，Reissner-Nordström 度規推廣到更高維度。5 維時空中的帶電黑洞解稱為 Tangherlini 解，而帶有多種電荷的黑洞解出現在弦論中。這些解在理解量子引力方面起重要作用。

## 25.10 數值計算示例

以下 Python 代碼計算 Reissner-Nordström 黑洞的視界位置：

```python
import numpy as np
import matplotlib.pyplot as plt

def horizons(M, Q):
    """計算 Reissner-Nordström 黑洞的視界"""
    discriminant = M**2 - Q**2
    if discriminant < 0:
        return None, None  # 裸奇點
    elif discriminant == 0:
        return M, M  # 極端黑洞
    else:
        r_plus = M + np.sqrt(discriminant)
        r_minus = M - np.sqrt(discriminant)
        return r_plus, r_minus

# 測試不同參數
masses = np.linspace(0.5, 2.0, 100)
charges = [0.0, 0.5, 1.0, 1.5]

plt.figure(figsize=(10, 6))
for Q in charges:
    r_plus_list = []
    r_minus_list = []
    for M in masses:
        r_plus, r_minus = horizons(M, Q)
        if r_plus is not None:
            r_plus_list.append(r_plus)
            r_minus_list.append(r_minus)
        else:
            r_plus_list.append(np.nan)
            r_minus_list.append(np.nan)
    plt.plot(masses, r_plus_list, label=f'Q = {Q} (外視界)')
    if Q > 0:
        plt.plot(masses, r_minus_list, '--', label=f'Q = {Q} (內視界)')

plt.xlabel('質量 M')
plt.ylabel('視界半徑')
plt.title('Reissner-Nordström 黑洞視界')
plt.legend()
plt.grid(True)
plt.savefig('reissner_nordstrom_horizons.png', dpi=150)
plt.show()
```

這個代碼生成了不同電荷值下，視界半徑隨質量的變化曲線。

## 重點回顧

| 概念 | 說明 |
|------|------|
| Reissner-Nordström 度規 | $ds^2 = -\left(1-\frac{2M}{r}+\frac{Q^2}{r^2}\right)dt^2 + \left(1-\frac{2M}{r}+\frac{Q^2}{r^2}\right)^{-1}dr^2 + r^2d\Omega^2$ |
| 外視界 $r_+$ | $M + \sqrt{M^2 - Q^2}$ |
| 內視界 $r_-$ | $M - \sqrt{M^2 - Q^2}$ |
| 極端黑洞 | $Q = M$，$r_+ = r_-$，$\kappa = 0$ |
| 裸奇點 | $Q > M$，沒有視界 |
| 表面重力 | $\kappa = \frac{r_+ - r_-}{2r_+^2}$ |
| 面積 | $A = 4\pi r_+^2$ |

## 練習題

1. **視界分析**：考慮一個電子（$m_e \approx 9.11 \times 10^{-28}$ g，$e \approx 4.8 \times 10^{-10}$ esu）形成的 Reissner-Nordström 黑洞。計算其視界半徑並與 Schwarzschild 半徑比較。電子是否會形成裸奇點？

2. **極端極限**：證明當 $Q \to M$ 時，Reissner-Nordström 度規趨近於：
   $$ds^2 = -\left(1 - \frac{M}{r}\right)^2 dt^2 + \left(1 - \frac{M}{r}\right)^{-2} dr^2 + r^2 d\Omega^2$$
   
3. **能量條件**：討論 Einstein 方程的弱能量條件如何限制帶電黑洞的形成。特別是，證明 $M^2 \geq Q^2$ 與某些能量條件有關。

4. **Penrose 圖**：畫出 Reissner-Nordström 時空的 Penrose 圖，標明各個區域和 Killing 向量。

5. **表面重力計算**：計算 Reissner-Nordström 黑洞的表面重力，驗證：
   $$\kappa = \frac{r_+ - r_-}{2r_+^2}$$
   
   然後證明在極端情況 $r_+ = r_-$ 時，$\kappa = 0$。

6. **有效勢能**：對於類光測地線（$m = 0$），導出有效勢能並討論光子在視界附近的行為。

7. **Charged 星體**：考慮一個均勻帶電球星體。當它坍縮時，在什麼條件下會形成裸奇點而非黑洞？

8. **熱力學**：利用黑洞熱力學第一定律，導出 Reissner-Nordström 黑洞的熵：
   $$S = \frac{A}{4} = \pi r_+^2$$
