# 第 7 章：向量場與張量場

## 概述

向量場和張量場是在流形的每一點都賦予一個切向量或餘切向量的光滑映射。在廣義相對論中，物質和能量由能量-動量張量場描述，而引力本身由時空的幾何（度規張量場）描述。本章將介紹向量場的代數結構（李代數）、李導數、以及流的概念——這些是描述時空動力學和幾何變換的基本工具。

## 7.1 光滑向量場的定義

### 7.1.1 從截面到向量場

在第六章中，我們看到切叢 $TM$ 的截面是為每個點 $p \in M$ 選擇一個切向量 $\sigma(p) \in T_p M$ 的映射。

**定義（光滑向量場）**：

光滑流形 $M$ 上的**向量場** $X$ 是切叢的光滑截面：
$$X: M \rightarrow TM, \quad p \mapsto X_p \in T_p M$$

這意味著 $X$ 是光滑的——在局部座標系中，其分量 $X^\mu(x)$ 是光滑函數。

### 7.1.2 向量場作為微分算子

向量場 $X$ 可以視為作用於光滑函數的**微分算子**：
$$X: C^\infty(M) \rightarrow C^\infty(M), \quad (Xf)(p) = X_p(f)$$

在座標系中，若 $X = X^\mu \partial_\mu$，則：
$$(Xf)(p) = X^\mu(p) \frac{\partial f}{\partial x^\mu}(p)$$

### 7.1.3 向量場的集合

所有光滑向量場的集合記作 $\mathfrak{X}(M)$ 或 $\Gamma(TM)$。可以驗證，$\mathfrak{X}(M)$ 在自然的加法和純量乘法下構成無窮維向量空間。

### 7.1.4 座標向量場

局部座標 $(x^\mu)$ 自然產生 $n$ 個座標向量場：
$$\frac{\partial}{\partial x^1}, \ldots, \frac{\partial}{\partial x^n}$$

在開集 $U$ 上，這些向量場構成 $\mathfrak{X}(U)$ 的局部基底——任何向量場 $X$ 都可以唯一表示為：
$$X|_U = X^\mu \frac{\partial}{\partial x^\mu}$$

其中 $X^\mu$ 是 $U$ 上的光滑函數。

## 7.2 李括號

### 7.2.1 李括號的定義

兩個向量場 $X, Y$ 的**李括號** $[X, Y]$ 是新的向量場，定義為對合作用的對易子：
$$[X, Y](f) = X(Y(f)) - Y(X(f))$$

對所有 $f \in C^\infty(M)$ 成立。

### 7.2.2 分量公式

在局部座標系中，若 $X = X^\mu \partial_\mu$，$Y = Y^\nu \partial_\nu$，則：
$$[X, Y] = (X^\nu \partial_\nu Y^\mu - Y^\nu \partial_\nu X^\mu) \partial_\mu$$

注意：這與矩陣對易子的形式相似。

### 7.2.3 李括號的代數性質

李括號滿足以下性質：

1. **雙線性**：
   $$[aX + bY, Z] = a[X, Z] + b[Y, Z]$$
   $$[Z, aX + bY] = a[Z, X] + b[Z, Y]$$

2. **反對稱性**：
   $$[X, Y] = -[Y, X]$$

3. **雅可比恆等式**：
   $$[X, [Y, Z]] + [Y, [Z, X]] + [Z, [X, Y]] = 0$$

第三個性質是最重要的——它使得 $\mathfrak{X}(M)$ 構成一個**李代數**。

## 7.3 李代數結構

### 7.3.1 李代數的定義

配備了李括號運算的向量空間 $\mathfrak{g}$ 稱為**李代數**，若滿足：

- 雙線性
- 反對稱性
- 雅可比恆等式

### 7.3.2 $\mathfrak{X}(M)$ 作為李代數

光滑向量場的集合 $\mathfrak{X}(M)$ 在李括號下構成無窮維李代數。

### 7.3.3 有限維李代數的例子

- $\mathfrak{gl}(n, \mathbb{R})$：所有 $n \times n$ 實矩陣，配備對易子 $[A, B] = AB - BA$
- $\mathfrak{so}(3)$：三維旋轉群的李代數，元素是 $3 \times 3$ 反對稱矩陣
- $\mathfrak{sl}(2, \mathbb{R})$：所有跡為零的 $2 \times 2$ 矩陣

### 7.3.4 李代數與李群的關係

每個李群 $G$ 都有其李代數 $\mathfrak{g} = T_e G$。指數映射建立了李代數與李群之間的局部聯繫：
$$\exp: \mathfrak{g} \rightarrow G$$

## 7.4 李導數

### 7.4.1 李導數的定義

向量場 $X$ 對另一向量場 $Y$ 的**李導數**（Lie derivative）$\mathcal{L}_X Y$ 定義為李括號：
$$\mathcal{L}_X Y = [X, Y]$$

這度量了 $Y$ 沿著 $X$ 方向的變化率。

### 7.4.2 對函數的李導數

對光滑函數 $f$，李導數就是向量場的作用：
$$\mathcal{L}_X f = X(f) = df(X)$$

### 7.4.3 對張量場的李導數

李導數可以推廣到任意張量場。對於 $(p, q)$ 型張量場 $T$，$\mathcal{L}_X T$ 是同類型的張量場，定義為：
$$\mathcal{L}_X T = \lim_{t \to 0} \frac{(\Phi_X^t)^* T - T}{t}$$

其中 $\Phi_X^t$ 是 $X$ 的流（見下一節）。

### 7.4.4 協變導數與李導數

協變導數 $\nabla_X$ 和李導數 $\mathcal{L}_X$ 都是沿向量場方向的導數，但它們有不同的性質：

- 協變導數涉及聯絡，適用於所有張量場
- 李導數不涉及聯絡，但只能用於張量場

## 7.5 流與積分曲線

### 7.5.1 流的定義

向量場 $X$ 的**流**（flow）$\Phi_X$ 是滿足以下條件的光滑映射：
$$\Phi_X: \mathcal{D} \subset \mathbb{R} \times M \rightarrow M$$

其中定義域 $\mathcal{D}$ 是開集，且：
$$\frac{d}{dt}\Phi_X(t, p) = X_{\Phi_X(t, p)}$$
$$\Phi_X(0, p) = p$$

$\Phi_X(t, p)$ 表示從 $p$ 點出發，沿 $X$ 方向移動時間 $t$ 後到達的點。

### 7.5.2 積分曲線

對於固定 $p$，曲線 $\gamma(t) = \Phi_X(t, p)$ 稱為 $X$ 過 $p$ 點的**積分曲線**（integral curve）或**軌跡**（trajectory）。

積分曲線是微分方程 $\dot{\gamma}(t) = X_{\gamma(t)}$ 的解。

### 7.5.3 局部存在唯一性

對每個點 $p \in M$，存在鄰域 $U$ 和 $\epsilon > 0$，使得流定義在 $(-\epsilon, \epsilon) \times U$ 上。

這是常微分方程基本定理的直接推論。

### 7.5.4 流的性質

流具有以下重要性質：

1. **群性質**：
   $$\Phi_X(t + s, p) = \Phi_X(t, \Phi_X(s, p))$$
   $$\Phi_X(0, p) = p$$
   $$\Phi_X(-t, \Phi_X(t, p)) = p$$

2. **光滑性**：$\Phi_X$ 是光滑的

## 7.6 向量場的指數映射

### 7.6.1 完整向量場

若流的定義域是整個 $\mathbb{R} \times M$，則稱 $X$ 為**完整向量場**（complete）。

例如，$\mathbb{R}^n$ 上的線性向量場 $X = v^\mu \partial_\mu$（$v$ 為常向量）是完整的。

### 7.6.2 指數映射

對完整向量場 $X$，定義**指數映射**：
$$\exp(tX)(p) = \Phi_X(t, p)$$

這推廣了李群情況下的指數映射。

### 7.6.3 與李代數的聯繫

對於李群的左不變向量場，指數映射正是李群指數映射在向量場上的限制。

## 7.7 余向量場與張量場

### 7.7.1 余向量場

**余向量場**（cotangent field）或 **1-形式場** $\omega$ 是光滑映射：
$$\omega: M \rightarrow T^*M, \quad p \mapsto \omega_p \in T_p^* M$$

在局部座標系中：
$$\omega = \omega_\mu dx^\mu$$

其中 $\omega_\mu$ 是光滑函數。

### 7.7.2 張量場

$(p, q)$ 型**張量場** $T$ 是光滑映射：
$$T: M \rightarrow T^p_q M$$

其中 $T^p_q M$ 是 $(p, q)$ 型張量的叢。

張量場在物理學中極其重要：

- 度量張量場 $g_{\mu\nu}$：(0, 2) 型
- 黎曼曲率張量場 $R^\rho_{\ \mu\nu\sigma}$：(1, 3) 型
- 能量-動量張量場 $T_{\mu\nu}$：(0, 2) 型
- 电磁场张量 $F_{\mu\nu}$：(0, 2) 型

## 7.8 張量場的代數運算

### 7.8.1 張量積

$(p_1, q_1)$ 型張量場 $S$ 與 $(p_2, q_2)$ 型張量場 $T$ 的張量積是 $(p_1+p_2, q_1+q_2)$ 型張量場：
$$(S \otimes T)^{i_1 \cdots i_{q_1} j_1 \cdots j_{q_2}}_{k_1 \cdots k_{p_1} l_1 \cdots l_{p_2}} = S^{i_1 \cdots i_{q_1}}_{k_1 \cdots k_{p_1}} T^{j_1 \cdots j_{q_2}}_{l_1 \cdots l_{p_2}}$$

### 7.8.2 指標縮併

張量場的指標縮併是對一個上指標和一個下指標進行求和的運算：
$$T^{\cdots i \cdots}_{\cdots i \cdots} = g^{ij} T^{\cdots i \cdots}_{\cdots j \cdots}$$

### 7.8.3 對稱化與反對稱化

對張量場的指標進行對稱化或反對稱化，產生對稱或反對稱張量場：
$$T_{(\mu\nu)} = \frac{1}{2}(T_{\mu\nu} + T_{\nu\mu})$$
$$T_{[\mu\nu]} = \frac{1}{2}(T_{\mu\nu} - T_{\nu\mu})$$

## 7.9 Killing 向量場

### 7.9.1 等度規映射

光滑流形 $(M, g)$ 上的**等度規映射**（isometry）是保持度量不變的光滑微分同胚 $\phi$：
$$\phi^* g = g$$

### 7.9.2 Killing 向量場的定義

若向量場 $X$ 生成的流是等度規映射，則稱 $X$ 為 **Killing 向量場**。

### 7.9.3 Killing 方程

等價地，$X$ 是 Killing 向量場當且僅當：
$$\mathcal{L}_X g_{\mu\nu} = 0$$

展開為：
$$X_\rho g_{\mu\nu} + X_\mu g_{\rho\nu} + X_\nu g_{\rho\mu} = 0$$

這就是著名的 **Killing 方程**。

### 7.9.4 物理意義

Killing 向量場對應於時空的**對稱性**。根據諾特定理，每個 Killing 向量場都對應一個守恆定律：

- 時間平移對稱 → 能量守恆
- 空間旋轉對稱 → 角動量守恆
- 空間平移對稱 → 動量守恆

## 7.10 旋度、散度與梯度（場的版本）

### 7.10.1 梯度

純量場 $f$ 的**梯度**是 1-形式場：
$$\nabla f = df$$

若配備度量，則可將梯度提升為向量場。

### 7.10.2 旋度

在三維流形上，向量場 $X$ 的**旋度**是：
$$(\nabla \times X)_\mu = \epsilon_{\mu\nu\rho} \nabla^\nu X^\rho$$

### 7.10.3 散度

向量場 $X$ 的**散度**是：
$$\nabla_\mu X^\mu$$

這推廣了 $\mathbb{R}^3$ 中的散度概念到一般流形。

## 重點回顧

| 概念 | 說明 |
|------|------|
| 向量場 | 流形上每點的切向量 |
| 李括號 $[X, Y]$ | 兩個向量場的對易子 |
| 李代數 | 配備了李括號的向量空間 |
| 李導數 $\mathcal{L}_X$ | 沿 $X$ 方向的導數 |
| 流 $\Phi_X$ | 沿向量場的積分曲線 |
| 指數映射 | $\exp(tX)$ |
| 張量場 | 每點賦予張量的光滑映射 |
| Killing 向量場 | 生成等度規變化的向量場 |
| Killing 方程 | $\mathcal{L}_X g = 0$ |
| 散度 $\nabla_\mu X^\mu$ | 向量場的散度 |

## 練習題

1. **李括號計算**：在 $\mathbb{R}^2$ 中，計算 $X = y\partial_x - x\partial_y$ 和 $Y = \partial_x$ 的李括號 $[X, Y]$。

2. **積分曲線**：求向量場 $X = x\partial_x + y\partial_y$ 在 $\mathbb{R}^2 \setminus \{0\}$ 中的積分曲線。

3. **李導數**：設 $X = \partial_x$，$Y = y\partial_y$。計算 $\mathcal{L}_X Y$ 和 $\mathcal{L}_Y X$。

4. **Killing 向量場**：驗證 $X = \partial_t$ 是 Minkowski 時空 $(\mathbb{R}^4, \eta)$ 的 Killing 向量場。

5. **散度**：計算向量場 $X = (x, y, z)$ 在歐氏空間中的散度。

6. **張量場類型**：判斷以下表達式的張量場類型：
   - $X_\mu Y_\nu$
   - $g_{\mu\nu}$
   - $\nabla_\rho X^\rho$

7. **Killing 方程**：在二維球面上，驗證 $X = \partial_\phi$ 是否是 Killing 向量場。

8. **流與指數映射**：設 $X$ 為完整向量場。證明：對任意 $p \in M$，曲線 $t \mapsto \exp(tX)(p)$ 是 $X$ 的積分曲線。

9. **雅可比恆等式**：驗證李括號滿足雅可比恆等式。

10. **能量守恆**：解釋為什麼 Minkowski 時空中的時間平移對稱性（Killing 向量場 $\partial_t$）導致能量守恆。
