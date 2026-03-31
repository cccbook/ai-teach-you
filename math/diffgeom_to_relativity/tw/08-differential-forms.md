# 第 8 章：微分形式

## 概述

微分形式是處理流形上積分的強大工具。在廣義相對論中，电磁场被统一为电磁场张量（二形式），而微分形式語言為這些幾何對象提供了優雅的代數框架。本章將介紹微分形式的定義、外積運算、外微分算子、霍奇星算子，以及最重要的斯托克斯定理——這是微分幾何中最深刻的基本定理，統一了格林定理、斯托克斯定理和散度定理。

## 8.1 微分形式的基本定義

### 8.1.1 k-形式的定義

**定義（k-形式）**：

$k$ 維**微分形式**（differential form），簡稱 $k$-形式，是光滑流形上的**反對稱 $(0, k)$ 型張量場**。

換句話說，$k$-形式是 $k$ 個餘切向量的反對稱多重線性映射：
$$\omega: \underbrace{T_p^* M \times \cdots \times T_p^* M}_{k \text{ 個}} \rightarrow \mathbb{R}$$

且在任意兩個餘切向量交換時變號。

### 8.1.2 維度計算

在 $n$ 維流形上，$k$-形式的空間 $\Lambda^k(T_p^* M)$ 的維度為：
$$\dim \Lambda^k(T_p^* M) = \binom{n}{k}$$

當 $k > n$ 時，維度為零——不可能有反對稱於 $n$ 個以上向量的張量。

### 8.1.3 特殊情況

**0-形式**：光滑函數 $f: M \rightarrow \mathbb{R}$。這是微分形式的最簡單情況。

**1-形式**：餘切向量場 $\omega$，例如函數的微分 $df$。

**2-形式**：反對稱的 $(0, 2)$ 型張量場，例如电磁场张量 $F$。

**n-形式**：最高維度的微分形式，在流形上具有特殊的地位。

### 8.1.4 示例

**示例 1**：在 $\mathbb{R}^3$ 中，$dx$，$dy$，$dz$ 是三個 1-形式。

**示例 2**：在 $\mathbb{R}^3$ 中，$dx \wedge dy$，$dy \wedge dz$，$dz \wedge dx$ 是三個 2-形式。

**示例 3**：體積元 $dx \wedge dy \wedge dz$ 是 3-形式。

## 8.2 外積

### 8.2.1 外積的定義

$\alpha$ 為 $p$-形式，$\beta$ 為 $q$-形式，$\alpha$ 和 $\beta$ 的**外積**（exterior product）$\alpha \wedge \beta$ 是 $(p+q)$-形式。

### 8.2.2 分量表示

若：
$$\alpha = \frac{1}{p!} \alpha_{i_1 \cdots i_p} dx^{i_1} \wedge \cdots \wedge dx^{i_p}$$
$$\beta = \frac{1}{q!} \beta_{j_1 \cdots j_q} dx^{j_1} \wedge \cdots \wedge dx^{j_q}$$

則：
$$\alpha \wedge \beta = \frac{1}{p! q!} \alpha_{i_1 \cdots i_p} \beta_{j_1 \cdots j_q} dx^{i_1} \wedge \cdots \wedge dx^{i_p} \wedge dx^{j_1} \wedge \cdots \wedge dx^{j_q}$$

### 8.2.3 反交換性

外積是**反交換的**：
$$\alpha \wedge \beta = (-1)^{pq} \beta \wedge \alpha$$

特別地：
- $\alpha \wedge \alpha = 0$ 對任意奇數形式 $\alpha$
- $dx \wedge dy = -dy \wedge dx$

### 8.2.4 代數結構

微分形式配備外積構成**外代數**（exterior algebra）或 **格拉斯曼代數**（Grassmann algebra）。

這是克萊因（Felix Klein）在他的埃爾朗根綱領中提出的重要代數結構。

## 8.3 外微分

### 8.3.1 外微分的定義

**定義（外微分）**：

**外微分** $d$ 是從 $k$-形式到 $(k+1)$-形式的算子：
$$d: \Omega^k(M) \rightarrow \Omega^{k+1}(M)$$

### 8.3.2 分量公式

若 $\omega = \frac{1}{k!} \omega_{i_1 \cdots i_k} dx^{i_1} \wedge \cdots \wedge dx^{i_k}$，則：
$$d\omega = \frac{1}{k!} \partial_\mu \omega_{i_1 \cdots i_k} dx^\mu \wedge dx^{i_1} \wedge \cdots \wedge dx^{i_k}$$

簡化形式：
$$d\omega_{i_1 \cdots i_k} = \sum_{j=0}^k (-1)^j \partial_{i_j} \omega_{i_1 \cdots \hat{i_j} \cdots i_k}$$

### 8.3.3 基本性質

外微分 $d$ 滿足以下基本性質：

1. **線性性**：$d(\alpha + \beta) = d\alpha + d\beta$
2. **萊布尼茨法則**：
   $$d(\alpha \wedge \beta) = d\alpha \wedge \beta + (-1)^p \alpha \wedge d\beta$$
   其中 $p$ 為 $\alpha$ 的次數
3. **冪零性**：
   $$d^2 = 0 \quad \text{（即 } d \circ d = 0 \text{）}$$

### 8.3.4 特殊情況

- **0-形式（函數）**：
  $$df = \partial_\mu f \, dx^\mu$$
  這正是函數的微分。

- **1-形式**：
  $$d\omega = d(\omega_\mu dx^\mu) = \partial_\mu \omega_\nu \, dx^\mu \wedge dx^\nu$$

## 8.4 閉形式與恰當形式

### 8.4.1 閉形式

**定義（閉形式）**：

若 $\omega$ 滿足 $d\omega = 0$，則稱 $\omega$ 為**閉形式**（closed form）。

### 8.4.2 恰當形式

**定義（恰當形式）**：

若存在 $\alpha$ 使得 $\omega = d\alpha$，則稱 $\omega$ 為**恰當形式**（exact form）。

### 8.4.3 龐加萊引理

**定理（龐加萊引理）**：

恰當形式必為閉形式（因為 $d^2 = 0$）。

龐加萊引理說明：在**單連通**開集上，閉形式也是恰當的。

### 8.4.4 de Rham 上同調

閉形式與恰當形式的差異催生了**de Rham 上同調**理論：
$$H^k(M) = \frac{\ker(d: \Omega^k \rightarrow \Omega^{k+1})}{\text{im}(d: \Omega^{k-1} \rightarrow \Omega^k)}$$

de Rham 上同調群是流形的拓撲不變量。

## 8.5 霍奇星算子

### 8.5.1 霍奇星算子的定義

**定義（霍奇星算子）**：

**霍奇星算子**（Hodge star operator）$\ast$ 將 $k$-形式映射為 $(n-k)$-形式：
$$\ast: \Omega^k(M) \rightarrow \Omega^{n-k}(M)$$

這需要流形具有**定向**和**度量**。

### 8.5.2 分量公式

在 $n$ 維定向流形上：
$$(\ast \omega)_{\mu_{k+1} \cdots \mu_n} = \frac{1}{k!} \epsilon_{\mu_{k+1} \cdots \mu_n \nu_1 \cdots \nu_k} \omega^{\nu_1 \cdots \nu_k}$$

其中 $\epsilon_{\mu_1 \cdots \mu_n}$ 是 Levi-Civita 張量密度。

### 8.5.3 霍奇星算子的性質

1. **雙重霍奇星**：
   $$\ast \ast \omega = (-1)^{k(n-k)} \omega$$

2. **對標準基的作用**：
   $$\ast(dx^{i_1} \wedge \cdots \wedge dx^{i_k}) = \pm dx^{j_1} \wedge \cdots \wedge dx^{j_{n-k}}$$

### 8.5.4 示例

在 $\mathbb{R}^3$ 中：
$$\ast dx = dy \wedge dz$$
$$\ast dy = dz \wedge dx$$
$$\ast dz = dx \wedge dy$$
$$\ast(dx \wedge dy) = dz$$

## 8.6 餘微分與拉普拉斯-德拉姆算子

### 8.6.1 餘微分的定義

**定義（餘微分）**：

**餘微分**（codifferential）$d^\dagger$ 是外微分的「伴隨」算子：
$$d^\dagger = (-1)^{n(k+1)+1} \ast d \ast$$

作用於 $k$-形式給出 $(k-1)$-形式。

### 8.6.2 拉普拉斯-德拉姆算子

**定義（拉普拉斯-德拉姆算子）**：

$$\Delta = dd^\dagger + d^\dagger d$$

這是微分形式上的「拉普拉斯算子」。

### 8.6.3 調和形式

若 $\Delta \omega = 0$，則 $\omega$ 稱為**調和形式**。

根據霍奇定理，調和形式與 de Rham 上同調一一對應。

## 8.7 斯托克斯定理

### 8.7.1 斯托克斯定理的陳述

**定理（斯托克斯定理）**：

設 $M$ 為取向 $n$ 維流形，$\omega$ 為 $(n-1)$-形式（光滑且具有良好的行為），則：
$$\int_M d\omega = \int_{\partial M} \omega$$

其中 $\partial M$ 是 $M$ 的邊界，取向與 $M$ 相容。

### 8.7.2 特殊情況

- **格林定理**：$n = 2$，$\omega = P\,dx + Q\,dy$
- **經典斯托克斯定理**：$n = 3$，$\omega$ 為 1-形式
- **散度定理**：$n = 3$，$\omega$ 為 2-形式

### 8.7.3 物理意義

斯托克斯定理聯繫了區域的整體性質（通過區域積分）與其邊界上的局部性質（通過邊界積分）。

在物理學中，這對應於各種守恆定律：

- **能量守恆**：穿過閉合表面的能量流等於區域內能量的變化
- **電荷守恆**：穿過閉合表面的電流等於區域內電荷的變化

## 8.8 电磁场作为微分形式

### 8.8.1 四維時空中的微分形式

在四維時空中，微分形式具有特殊的結構。

**0-形式**：電勢 $\phi$、磁勢等

**1-形式**：四維电磁势
$$A = A_\mu dx^\mu$$

### 8.8.2 电磁场张量

电磁场张量是 $A$ 的外微分：
$$F = dA = \frac{1}{2} F_{\mu\nu} dx^\mu \wedge dx^\nu$$

其中 $F_{\mu\nu} = \partial_\mu A_\nu - \partial_\nu A_\mu$。

### 8.8.3 麦克斯韦方程的微分形式

麥克斯韋方程在微分形式語言中變得極其簡潔：

1. **法拉第方程**（齊次方程）：
   $$dF = 0$$

2. **高斯-麥克斯韋方程**（非齊次方程）：
   $$d \ast F = \ast J$$

其中 $J$ 是電流 3-形式。

### 8.8.4 物理意義

- $dF = 0$ 對應於「不存在磁單極」和「感應定律」
- $d \ast F = \ast J$ 對應於「高斯定律」和「安培定律（含位移電流）」

## 8.9 例子：在 $\mathbb{R}^3$ 中

### 8.9.1 微分形式基底

在 $\mathbb{R}^3$ 中，標準基底為：
$$dx, \quad dy, \quad dz$$

### 8.9.2 1-形式

$$\omega = P\,dx + Q\,dy + R\,dz$$

### 8.9.3 2-形式

$$\alpha = \frac{1}{2} \alpha_{ij} dx^i \wedge dx^j = A_x \, dy \wedge dz + A_y \, dz \wedge dx + A_z \, dx \wedge dy$$

### 8.9.4 運算對應

| 微分形式 | 梯度 | 旋度 | 散度 |
|----------|------|------|------|
| $f$ (0-形式) | $df$ | — | — |
| $\omega$ (1-形式) | — | $d\omega$ | $\ast d \ast \omega$ |
| $\alpha$ (2-形式) | — | $\ast d \ast \alpha$ | $d\alpha$ |
| $\beta$ (3-形式) | — | — | $\ast d \ast \beta$ |

## 8.10 積分的幾何意義

### 8.10.1 k-形式的積分

$k$-形式在 $k$ 維定向流形上的積分：
$$\int_M \omega$$

這推廣了多元函數的積分概念。

### 8.10.2 變換公式

在定向微分同胚 $\phi: M \rightarrow N$ 下：
$$\int_N \omega = \int_M \phi^* \omega$$

這推廣了變數變換公式。

## 重點回顧

| 概念 | 說明 |
|------|------|
| k-形式 | 反對稱 $(0, k)$ 型張量場 |
| 外積 $\wedge$ | 反交換的乘法運算 |
| 外微分 $d$ | 從 $k$-形式到 $(k+1)$-形式 |
| 閉形式 | $d\omega = 0$ |
| 恰當形式 | $\omega = d\alpha$ |
| 龐加萊引理 | 單連通開集上閉形式必恰當 |
| 霍奇星算子 $\ast$ | $k$-形式到 $(n-k)$-形式 |
| 餘微分 $d^\dagger$ | 外微分的伴隨算子 |
| 斯托克斯定理 | $\int_M d\omega = \int_{\partial M} \omega$ |

## 練習題

1. **外積計算**：在 $\mathbb{R}^4$ 中，計算 $dx \wedge dy \wedge dz$ 和 $dt \wedge dx$。

2. **外微分**：計算 $d(x\,dy + y\,dz + z\,dx)$。

3. **閉形式與恰當形式**：驗證 $d(dx) = 0$，並討論是否所有閉形式都是恰當的。

4. **反交換性**：證明：若 $\alpha$ 為 $p$-形式，$\beta$ 為 $q$-形式，則 $\alpha \wedge \beta = (-1)^{pq} \beta \wedge \alpha$。

5. **霍奇星算子**：在 $\mathbb{R}^3$ 中，計算 $\ast(dx)$，$\ast(dx \wedge dy)$。

6. **麦克斯韦方程**：使用微分形式語言證明 $dF = 0$ 對應於不存在磁單極。

7. **斯托克斯定理**：在 $\mathbb{R}^3$ 中驗證斯托克斯定理對向量場 $\mathbf{F} = (-y, x, 0)$ 和單位圓盤。

8. **龐加萊引理**：在 $\mathbb{R}^2 \setminus \{0\}$ 中，證明 $d\theta = \frac{-y\,dx + x\,dy}{x^2+y^2}$ 是閉形式但不是恰當形式。

9. **拉普拉斯-德拉姆算子**：計算作用於函數 $f$ 的拉普拉斯-德拉姆算子 $\Delta f$。

10. **電荷守恆**：解釋為什麼麥克斯韋方程 $d \ast F = \ast J$ 在微分形式語言中自然包含電荷守恆。
