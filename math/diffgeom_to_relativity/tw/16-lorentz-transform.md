# 第 16 章：洛倫茲變換

## 概述

洛倫茲變換是連接不同慣性參考系的數學工具。它們是保持 Minkowski 度量不變的線性變換，構成了龐加萊群的子群。本章將詳細推導洛倫茲矩陣的結構，並探討其重要的物理後果。

洛倫茲變換是狹義相對論的數學基礎。它們告訴我們如何在不同慣性參考系之間轉換物理量——時間座標、空間座標、速度、能量、動量等。這些變換確保了物理定律在所有慣性系中具有相同的形式。

## 16.1 洛倫茲變換的推導

### 16.1.1 基本要求

洛倫茲變換 $\Lambda^\mu_{\ \nu}$ 必須滿足：

$$\eta_{\mu\nu} \Lambda^\mu_{\ \rho} \Lambda^\nu_{\ \sigma} = \eta_{\rho\sigma}$$

這確保了時空間隔不變：

$$ds^2 = \eta_{\mu\nu} dx^\mu dx^\nu = \eta_{\rho\sigma} dx'^\rho dx'^\sigma$$

這個條件稱為**洛倫茲條件**。

### 16.1.2 矩陣形式

寫成矩陣形式：

$$\Lambda^T \eta \Lambda = \eta$$

其中 $\eta = \text{diag}(-1, 1, 1, 1)$ 是 Minkowski 度量。

這是一個矩陣方程，包含 10 個獨立方程（對稱張量的分量數）。

### 16.1.3 行列式條件

從這個方程可得：

$$(\det\Lambda)^2 = 1 \Rightarrow \det\Lambda = \pm 1$$

物理上相關的變換取 $\det\Lambda = +1$（不含空間反演）。

另一個條件來自於時間方向：$SO^+(3,1)$ 要求保持時間方向和手性。

## 16.2 洛倫茲 boost

### 16.2.1 沿 x 方向的 boost

沿 $x$ 方向的洛倫茲 boost 矩陣為：

$$\Lambda = \begin{pmatrix} \gamma & -\beta\gamma & 0 & 0 \\ -\beta\gamma & \gamma & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}$$

其中：
$$\beta = \frac{v}{c}, \quad \gamma = \frac{1}{\sqrt{1-\beta^2}}$$

這個矩陣將 $(t, x)$ 座標變換為 $(t', x')$。

### 16.2.2 變換公式

將矩陣作用於事件坐標：

$$ct' = \gamma(ct - \beta x)$$
$$x' = \gamma(x - \beta ct)$$
$$y' = y$$
$$z' = z$$

或者寫成更常見的形式：

$$t' = \gamma\left(t - \frac{vx}{c^2}\right)$$
$$x' = \gamma(x - vt)$$

### 16.2.3 逆變換

逆變換只需將 $v \to -v$（或 $\beta \to -\beta$）：

$$\Lambda^{-1} = \begin{pmatrix} \gamma & \beta\gamma & 0 & 0 \\ \beta\gamma & \gamma & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}$$

這給出：

$$t = \gamma\left(t' + \frac{vx'}{c^2}\right)$$
$$x = \gamma(x' + vt')$$

### 16.2.4 一般方向的 boost

沿任意方向 $\hat{n}$ 的 boost 矩陣：

$$\Lambda^\mu_{\ \nu} = \begin{pmatrix} \gamma & -\gamma\beta n_i \\ -\gamma\beta n_i & \delta_{ij} + (\gamma-1)n_i n_j \end{pmatrix}$$

其中 $n_i$ 是方向 $\hat{n}$ 的分量。

## 16.3 速度加成公式

### 16.3.1 為什麼簡單相加不正確

在牛頓力學中，速度簡單相加：$u' = u + v$。

但這與光速不變原理矛盾！如果光速在所有慣性系中都等於 $c$，那麼速度就不能簡單相加。

### 16.3.2 正確的速度加成

兩個速度不能簡單相加。一維情況下：

$$u' = \frac{u - v}{1 - \frac{uv}{c^2}}$$

這是從 $S'$ 觀測到物體相對於 $S$ 的速度（$S'$ 以速度 $v$ 相對於 $S$ 運動）。

從 $S$ 觀測到 $u$（物體速度），從 $S'$ 觀測到 $u'$，則：

$$u' = \frac{u - v}{1 - \frac{uv}{c^2}}$$

### 16.3.3 張量形式

速度加成公式可以從四速度的 Lorentz 變換推導：

$$u'^\mu = \Lambda^\mu_{\ \nu} u^\nu$$

空間分量給出速度變換。

### 16.3.4 極限行為

當 $v \ll c$，公式還原為牛頓形式 $u' \approx u - v$。

當 $u = c$：
$$u' = \frac{c - v}{1 - v/c} = c$$

光速不變！這是 Lorentz 變換的基本性質。

## 16.4 Lorentz 收縮

### 16.4.1 長度收縮

運動方向上的長度會收縮：

$$L' = \frac{L}{\gamma}$$

其中 $L$ 是物體的固有長度（靜止參考系中測量）。

這稱為**Lorentz 收縮**或**菲佐-洛倫茲收縮**。

### 16.4.2 驗證

長度測量需要在「同時」測量兩端。在相對論中，「同時」是相對的——這導致了長度收縮。

考慮一把運動中的尺子。對於尺子靜止的觀測者，測量兩端是同時的。但對於另一個觀測者，測量兩端的時刻是不同的——這導致測量到的長度不同。

### 16.4.3 物理意義

這是真實的物理效應，已被無數實驗驗證。例如：
- 粒子物理中的不穩定粒子壽命在運動中延長
- 加速器中的粒子束長度收縮

重要的是，這不是知覺效應或測量誤差——運動物體在運動方向上確實收縮了。

## 16.5 時間膨脹

### 16.5.1 時間膨脹

運動的時鐘走得更慢：

$$\Delta t' = \gamma \Delta \tau$$

其中 $\Delta\tau$ 是時鐘的固有時（時鐘自身測量的時間）。

這稱為**時間膨脹**或**動鍾變慢**。

### 16.5.2 光鐘論證

考慮一個理想光鐘（光子來回反射於兩面鏡子之間）。

在光鐘的靜止系中，來回一次的時間為 $\Delta\tau = 2d/c$。

在運動的觀測者看來，光子的路徑是斜線，因此來回一次的時間為 $\Delta t = 2d/(c\sqrt{1-v^2/c^2}) = \gamma\Delta\tau$。

### 16.5.3 實驗驗證

**μ子壽命延長**：μ子在大氣層頂部產生，以接近光速運動。由於時間膨脹，它們的壽命延長，能夠到達地面。

**航空鐘實驗**：Hafele-Keating 實驗將原子鐘放在飛機上環繞地球，返回後與地面鐘比較。

**GPS 系統**：GPS 衛星上的原子鐘由於時間膨脹和引力效應，每天約走快 45 微秒（相對於地面）。

## 16.6 Lorentz 群的結構

### 16.6.1 Lorentz 群的定義

$$O(3,1) = \{ \Lambda : \Lambda^T \eta \Lambda = \eta \}$$

這是保持 Minkowski 度量不變的變換群。

維度：6 維（3 個旋轉 + 3 個 boost）。

### 16.6.2 連續性子群

$SO^+(3,1)$ 是保持方向和時間順序的子群：
- $\det\Lambda = +1$
- $\Lambda^0_{\ 0} \geq 1$

這是物理上相關的連續變換群。

### 16.6.3 分離子群

離散子群包括：
- **空間反演**（P）：$\det\Lambda = -1$，$\Lambda^0_{\ 0} = 1$
- **時間反演**（T）：$\det\Lambda = -1$，$\Lambda^0_{\ 0} = -1$
- **CPT 變換**：空間 + 時間 + 粒子-反粒子

### 16.6.4 李代數

Lorentz 代數 $\mathfrak{so}(3,1)$ 有六個生成元：
- 三個旋轉生成元：$M_{ij}$（對應 $SO(3)$）
- 三個 boost 生成元：$N_i$

對易關係：
$$[M_{ij}, M_{kl}] = i(\eta_{jk}M_{il} - \eta_{ik}M_{jl} - \eta_{jl}M_{ik} + \eta_{il}M_{jk})$$
$$[M_{ij}, N_k] = i(\eta_{jk}N_i - \eta_{ik}N_j)$$
$$[N_i, N_j] = -iM_{ij}$$

## 16.7 Thomas precession

### 16.7.1 定義

接連的 Lorentz boosts 產生旋轉——這是 **Thomas precession**。

當電子在原子中受到核的庫侖力加速時，其自旋軸會緩慢進動。

### 16.7.2 公式

Thomas 進動的角頻率：

$$\vec{\omega}_T = \frac{\gamma^2}{\gamma + 1}\frac{\vec{a} \times \vec{v}}{c^2}$$

其中 $\vec{a}$ 是加速度，$\vec{v}$ 是速度。

### 16.7.3 物理重要性

Thomas precession 在原子物理中很重要：

- 解釋了原子光譜中的精細結構分裂
- 是自旋-軌道耦合的一部分
- 導致自旋的進動

數值上，Thomas 進動是自旋-軌道耦合中的重要修正，約為直接的 $1/2$。

## 16.8 Lorentz 變換的幾何

### 16.8.1 時空圖

Lorentz 變換可以在時空圖中視覺化：
- 時間軸和空間軸相互傾斜
- 光錐保持不變
- 固有時和固有長度是 Lorentz 不變量

### 16.8.2 雙曲旋轉

Lorentz boost 可以視為時空平面上的雙曲旋轉：

$$ct' = ct\cosh\eta - x\sinh\eta$$
$$x' = -ct\sinh\eta + x\cosh\eta$$

其中 $\eta = \text{artanh}(v/c)$ 是 rapidity（快速度）。

### 16.8.3 Rapidity 空間

Rapidity 的範圍是 $(-\infty, +\infty)$，對應於速度的 $(-c, +c)$。

Rapidity 的疊加是簡單的相加：
$$\eta_{\text{total}} = \eta_1 + \eta_2$$

這比速度的疊加簡單得多。

## 16.9 四維表述的優點

### 16.9.1 協變性

四維表述自動確保物理定律在 Lorentz 變換下保持形式不變。

### 16.9.2 統一性

時間和空間被統一為四維時空：
- 事件：$(ct, x, y, z)$
- 四速度：$U^\mu = dx^\mu/d\tau$
- 四動量：$P^\mu = mU^\mu$

### 16.9.3 不變量

Lorentz 不變量簡化計算：
- $U^\mu U_\mu = -c^2$
- $P^\mu P_\mu = -m^2c^2$
- $F_{\mu\nu}F^{\mu\nu}$

## 重點回顧

| 概念 | 說明 |
|------|------|
| Lorentz 變換 | 保持 Minkowski 度量不變 |
| Lorentz boost | 兩個慣性系之間的相對運動 |
| $\gamma$ 因子 | $1/\sqrt{1-v^2/c^2}$ |
| 速度加成 | $u' = (u-v)/(1-uv/c^2)$ |
| 長度收縮 | $L' = L/\gamma$ |
| 時間膨脹 | $\Delta t' = \gamma \Delta \tau$ |
| Thomas precession | 接連 boosts 的幾何效應 |
| Rapidity | $\eta = \text{artanh}(v/c)$ |

## 練習題

1. **Lorentz 變換驗證**：驗證 Lorentz boost 矩陣滿足 $\Lambda^T \eta \Lambda = \eta$。

2. **速度加成**：推導一維速度加成公式，並計算當 $v_1 = 0.8c$，$v_2 = 0.8c$ 時，相對速度是多少。

3. **長度收縮**：計算以 $0.9c$ 速度運動的物體，其長度收縮為原來的多少分之一。

4. **光速不變**：證明兩個光速相加仍為光速。計算如果光速在所有慣性系中都等於 $c$，會導致什麼樣的速度加成公式。

5. **雙生子計算**：哥哥以 $0.99c$ 的速度飛往 10 光年外的恆星並返回。計算兩兄弟的年齡差。

6. **Thomas precession**：計算電子在氫原子中的 Thomas 進動頻率，討論它與自旋-軌道耦合的關係。

7. **Rapidity**：證明 rapidity 的疊加公式 $\eta_{\text{total}} = \eta_1 + \eta_2$。

8. **時空圖**：畫出 Lorentz 變換的時空圖，標明事件、光錐和固有時。
