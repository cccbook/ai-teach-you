# 第 6 章：切空間與餘切空間

## 概述

切空間與餘切空間是流形上微分結構的核心構件。在前一章中，我們已經介紹了流形上切向量的抽象定義。本章將深入探討切空間和餘切空間的代數結構，它們的對偶關係，以及在不同座標系中的分量表示。這些概念在廣義相對論中具有根本的重要性：時空的每一點都有一個切空間，代表該點所有可能的速度方向；而餘切空間則代表該點所有可測量物理量（如能量密度）的梯度。

## 6.1 切空間的抽象定義

### 6.1.1 切向量的幾何來源

在微分幾何中，切向量的概念有著明確的幾何動機。考慮三維空間中的曲面（如地球表面）和位於曲面上的曲線。曲線的切向量描述了曲線的方向，這個向量「切於」曲面。

然而，在抽象流形上，我們不能直接使用歐氏空間中的切向量概念，因為流形本身不是歐氏空間。我們需要一個純粹的、抽象的定義。

### 6.1.2 通過曲線定義切向量

**定義（切向量——曲線等價類）**：

設 $M$ 為 $n$ 維光滑流形，$p \in M$。考慮所有光滑曲線 $\gamma: (-\epsilon, \epsilon) \rightarrow M$ 滿足 $\gamma(0) = p$。

兩條曲線 $\gamma_1$ 和 $\gamma_2$ 在 $p$ 點被認為是**等價的**，若在任意局部座標系 $(x^\mu)$ 中：
$$\left.\frac{d x^\mu \circ \gamma_1}{dt}\right|_{t=0} = \left.\frac{d x^\mu \circ \gamma_2}{dt}\right|_{t=0}$$

這個等價類定義了 $p$ 點的一個**切向量**。

### 6.1.3 方向導數觀點

另一種等價的定義將切向量視為**方向導數算子**。

**定義（切向量——方向導數）**：

對光滑函數 $f \in C^\infty(M)$，定義方向導數：
$$X_p(f) = \left.\frac{d(f \circ \gamma)}{dt}\right|_{t=0}$$

這個算子 $X_p$ 作用於光滑函數並產生實數，且滿足：
1. 線性性：$X_p(f + g) = X_p(f) + X_p(g)$
2. 萊布尼茨法則：$X_p(fg) = f(p) X_p(g) + g(p) X_p(f)$

### 6.1.4 定義的等價性

這兩種定義是等價的。若兩條曲線在第一種定義下等價，則它們產生的方向導數算子相同。反過來，每個滿足上述兩個條件的算子都來自某條曲線。

這種等價性表明：我們可以將切向量視為「作用於函數的導數算子」，而不必依賴於具體的曲線。

### 6.1.5 切空間的向量空間結構

所有切向量的集合記作 $T_p M$，稱為 $p$ 點的**切空間**。

可以驗證，$T_p M$ 在以下運算下構成 $n$ 維向量空間：

**加法**：$(X_p + Y_p)(f) = X_p(f) + Y_p(f)$
**純量乘法**：$(a X_p)(f) = a X_p(f)$

零向量對應於「靜止」的曲線（任意方向都無變化）。

## 6.2 座標基底與自然基底

### 6.2.1 座標向量場

設 $(U, \phi)$ 為包含 $p$ 的圖，局部座標為 $(x^1, \ldots, x^n)$。定義**座標向量場**（或基向量）：
$$\left.\frac{\partial}{\partial x^\mu}\right|_p$$

這是切向量，作用於光滑函數 $f$ 為：
$$\left.\frac{\partial}{\partial x^\mu}\right|_p(f) = \partial_\mu (f \circ \phi^{-1})(\phi(p))$$

這正是我們熟悉的偏導數在點 $p$ 的值。

### 6.2.2 切空間的自然基底

**定理**：

在點 $p$ 的切空間 $T_p M$ 中，集合 $\left\{\left.\frac{\partial}{\partial x^1}\right|_p, \ldots, \left.\frac{\partial}{\partial x^n}\right|_p\right\}$ 構成一組基底，稱為**自然基底**或**座標基底**。

因此，$\dim T_p M = n$。

### 6.2.3 切向量的分量

若 $v \in T_p M$，則 $v$ 可以唯一表示為：
$$v = v^\mu \left.\frac{\partial}{\partial x^\mu}\right|_p$$

其中係數 $v^\mu$ 稱為 $v$ 在座標系 $(x^\mu)$ 中的**分量**。

### 6.2.4 曲線的速度向量

對於曲線 $\gamma(t)$，其在 $t = 0$ 處的速度向量（切向量）為：
$$\dot{\gamma}(0) = \left.\frac{dx^\mu}{dt}\right|_{t=0} \left.\frac{\partial}{\partial x^\mu}\right|_p$$

因此，曲線的速度分量正是 $\frac{dx^\mu}{dt}$。

## 6.3 餘切空間

### 6.3.1 餘切空間的定義

**定義（餘切空間）**：

餘切空間是切空間的對偶空間：
$$T_p^* M = (T_p M)^*$$

$T_p^* M$ 中的元素稱為**餘切向量**、**餘向量**或**1-形式**。

根據對偶空間的定義，餘切向量是從切空間到 $\mathbb{R}$ 的線性泛函。

### 6.3.2 對偶基

若 $\left\{\frac{\partial}{\partial x^\mu}|_p\right\}$ 是 $T_p M$ 的基底，則其對偶基 $\{(dx^\mu)_p\} \subset T_p^* M$ 定義為：
$$(dx^\mu)_p\left(\frac{\partial}{\partial x^\nu}|_p\right) = \delta^\mu_\nu = \begin{cases} 1 & \mu = \nu \\ 0 & \mu \neq \nu \end{cases}$$

這組對偶基也構成 $T_p^* M$ 的基底。

### 6.3.3 餘切向量的分量

若有餘切向量 $\omega \in T_p^* M$，則：
$$\omega = \omega_\mu (dx^\mu)_p$$

其中分量 $\omega_\mu = \omega\left(\frac{\partial}{\partial x^\mu}|_p\right)$。

## 6.4 函數的微分

### 6.4.1 微分作為餘切向量

光滑函數 $f \in C^\infty(M)$ 在 $p$ 點的**微分** $df_p$ 是一個特殊的餘切向量，定義為：
$$df_p(v) = v(f)$$

對所有 $v \in T_p M$。

### 6.4.2 微分的分量

在座標系中：
$$df = \frac{\partial f}{\partial x^\mu} dx^\mu$$

因此，$(df)_\mu = \partial_\mu f$，即餘切向量的分量正是函數的偏導數。

### 6.4.3 函數的梯度

函數的微分 $df$ 是餘切向量。若在流形上配備了度量 $g$，則可以通過指標升降將 $df$ 提升為向量：
$$\nabla f = g^{-1}(df)$$

這就是**梯度向量**。

### 6.4.4 梯度與方向導數

對於任意切向量 $v$：
$$df(v) = v(f) = \langle \nabla f, v \rangle$$

這推廣了歐氏空間中梯度與方向導數的關係。

## 6.5 拉回與前推

### 6.5.1 光滑映射的微分

設 $F: M \rightarrow N$ 為光滑映射，$p \in M$，$q = F(p) \in N$。

$F$ 在 $p$ 點的**微分**（或**前推**）定義為：
$$dF_p: T_p M \rightarrow T_q N$$

對 $v \in T_p M$ 和 $g \in C^\infty(N)$：
$$(dF_p(v))(g) = v(g \circ F)$$

### 6.5.2 分量表示

在局部座標系中，若 $F = (F^1, \ldots, F^m)$，則：
$$dF_p\left(\frac{\partial}{\partial x^\mu}\right) = \frac{\partial F^\nu}{\partial x^\mu} \frac{\partial}{\partial y^\nu}$$

因此，微分 $dF_p$ 的矩陣表示正是雅可比矩陣。

### 6.5.3 拉回映射

$F$ 還誘導一個從 $N$ 的餘切空間到 $M$ 的餘切空間的**拉回映射**：
$$F^*: T_q^* N \rightarrow T_p^* M$$

對 $\omega \in T_q^* N$ 和 $v \in T_p M$：
$$(F^*\omega)(v) = \omega(dF_p(v))$$

### 6.5.4 拉回與函數

對於光滑函數 $f: N \rightarrow \mathbb{R}$，拉回 $F^*f = f \circ F$ 是 $M$ 上的光滑函數。

拉回映射將餘切向量「拉回」到原流形上，這在物理學中用於比較不同點的物理量。

## 6.6 指標變換與協變/逆變分量

### 6.6.1 基底變換

考慮從舊座標 $(x^\mu)$ 到新座標 $(x'^\nu)$ 的變換。過渡矩陣為：
$$\Lambda^\nu_{\ \mu} = \frac{\partial x'^\nu}{\partial x^\mu}$$

其逆為：
$$(\Lambda^{-1})^\mu_{\ \nu} = \frac{\partial x^\mu}{\partial x'^\nu}$$

### 6.6.2 切向量的變換

切向量 $v = v^\mu \partial_\mu = v'^\nu \partial'_\nu$ 的分量變換為：
$$v'^\nu = (\Lambda^{-1})^\nu_{\ \mu} v^\mu = \frac{\partial x^\mu}{\partial x'^\nu} v^\mu$$

這是**逆變變換**——使用過渡矩陣的逆。

### 6.6.3 餘切向量的變換

餘切向量 $\omega = \omega_\mu dx^\mu = \omega'_\nu dx'^\nu$ 的分量變換為：
$$\omega'_\nu = \Lambda^\mu_{\ \nu} \omega_\mu = \frac{\partial x'^\nu}{\partial x^\mu} \omega_\mu$$

這是**協變變換**——使用過渡矩陣本身。

### 6.6.4 指標記號的回顧

這正是第一章中介紹的指標記號的幾何來源：

- **上指標**（逆變分量）：使用過渡矩陣的逆變換
- **下指標**（協變分量）：使用過渡矩陣本身變換

## 6.7 切叢與餘切叢

### 6.7.1 切叢的定義

將流形上所有點的切空間「粘合」在一起，構成一個新的流形：
$$TM = \bigsqcup_{p \in M} T_p M$$

這稱為 $M$ 的**切叢**（tangent bundle）。

可以證明，$TM$ 自身是一個 $2n$ 維光滑流形。

### 6.7.2 餘切叢

類似地，**餘切叢**為：
$$T^*M = \bigsqcup_{p \in M} T_p^* M$$

也是 $2n$ 維光滑流形。

### 6.7.3 投影映射

存在自然投影：
$$\pi: TM \rightarrow M, \quad \pi(v_p) = p$$
$$\pi: T^*M \rightarrow M, \quad \pi(\omega_p) = p$$

這些投影將每個切（餘切）向量映射到其基點。

### 6.7.4 截面

**截面**（section）是流形上的「向量場」：

$$\sigma: M \rightarrow TM, \quad \pi(\sigma(p)) = p$$

換句話說，截面為每個 $p \in M$ 選擇一個切向量 $\sigma(p) \in T_p M$。

光滑截面正是我們之前定義的**光滑向量場**。

## 6.8 浸沒與正則子流形

### 6.8.1 浸沒

**定義（浸沒）**：

光滑映射 $F: M \rightarrow N$ 稱為**浸沒**（submersion），若對每個 $p \in M$，微分 $dF_p: T_p M \rightarrow T_{F(p)} N$ 是滿射。

浸沒在局部像是「投影」——每個點的像是維數較低的光滑子流形。

### 6.8.2 正則值

**定義（正則值）**：

若 $c \in N$ 是映射 $F: M \rightarrow N$ 的正則值，即對所有 $p \in F^{-1}(c)$，$dF_p$ 是滿射，則 $F^{-1}(c)$ 是 $M$ 的光滑子流形。

### 6.8.3 例子：球面

考慮映射 $F: \mathbb{R}^{n+1} \rightarrow \mathbb{R}$，$F(x) = \|x\|^2$。

$1$ 是 $F$ 的正則值嗎？我們需要計算微分：
$$dF_x(v) = 2 \langle x, v \rangle$$

這在 $x \neq 0$ 時是滿射（因為 $\mathbb{R}$ 是一維的）。因此，$1$ 是正則值，$S^n = F^{-1}(1)$ 是 $\mathbb{R}^{n+1}$ 的光滑子流形。

## 6.9 在廣義相對論中的應用

### 6.9.1 時空的切叢

在廣義相對論中，時空流形 $\mathcal{M}$ 的切叢 $T\mathcal{M}$ 具有特殊的重要性。$T\mathcal{M}$ 中的每個點 $(p, v)$ 代表：

- $p \in \mathcal{M}$：時空中的事件
- $v \in T_p\mathcal{M}$：該事件處的速度向量

### 6.9.2 四速度

質點的世界線是 $\mathcal{M}$ 中的曲線 $\gamma(\tau)$。其四速度是：
$$U^\mu = \frac{dx^\mu}{d\tau}$$

這是切向量，描述了質點在時空中的運動方向。

### 6.9.3 能量動量向量

能量動量是餘切向量的一個例子。考慮能量函數 $E$：
$$dE_p(v) = \text{沿方向 } v \text{ 的能量變化率}$$

這將在愛因斯坦場方程中扮演重要角色。

## 重點回顧

| 概念 | 說明 |
|------|------|
| 切向量 | 曲線的方向導數算子 |
| 切空間 $T_p M$ | 過 $p$ 點所有切向量的集合，$n$ 維向量空間 |
| 座標基底 | $\left\{\partial/\partial x^\mu\|_p\right\}$ |
| 餘切空間 $T_p^* M$ | 切空間的對偶空間 |
| 對偶基 | $\{dx^\mu\|_p\}$ |
| 微分 $df$ | 函數的梯度（餘切向量） |
| 拉回 $F^*$ | 餘切空間之間的映射 |
| 前推 $dF_p$ | 切空間之間的映射 |
| 切叢 $TM$ | 所有切空間的集合 |
| 截面 | 選擇每點一個向量的映射（向量場） |

## 練習題

1. **切空間維度**：證明：若 $M$ 是 $n$ 維流形，$p \in M$，則 $T_p M$ 是 $n$ 維向量空間。

2. **方向導數算子**：設 $X_p$ 為 $p$ 點的切向量。證明：$X_p$ 作用於常數函數給出零。

3. **座標基底**：設 $f: \mathbb{R}^n \rightarrow \mathbb{R}$ 為光滑函數。求 $df_p$ 並驗證 $(df)_\mu = \partial_\mu f$。

4. **餘切向量**：設 $\omega \in T_p^* M$，$v \in T_p M$。證明：配對 $\omega(v)$ 是雙線性的。

5. **微分運算**：設 $F: M \rightarrow N$ 為光滑映射，$f: N \rightarrow \mathbb{R}$ 光滑。證明：$F^*(df) = d(f \circ F)$。

6. **指標變換**：考慮從直角座標 $(x, y)$ 到極座標 $(r, \theta)$ 的變換。求切向量 $v = (1, 1)$ 在極座標中的分量。

7. **拉回映射**：設 $F: \mathbb{R}^2 \rightarrow \mathbb{R}^2$，$F(x, y) = (x^2, y^2)$。計算拉回 $F^*(dx)$ 和 $F^*(dy)$。

8. **切叢**：描述 $TS^1$ 的結構（作為流形）。$TS^1$ 同構於什麼？

9. **正則值**：考慮映射 $F: \mathbb{R}^3 \rightarrow \mathbb{R}$，$F(x, y, z) = x^2 + y^2 + z^2$。哪些值是正則值？$F^{-1}(1)$ 是什麼？

10. **四速度**：考慮相對論中的四速度 $U^\mu = \gamma(c, \vec{v})$。驗證 $U^\mu U_\mu = -c^2$。
