# 第 4 章：多變數微積分

## 概述

多變數微積分是微分幾何和廣義相對論的數學基礎。在單變數微積分中，我們處理函數 $f: \mathbb{R} \rightarrow \mathbb{R}$，研究其導數和積分。在多變數微積分中，我們將這些概念推廣到函數 $f: \mathbb{R}^n \rightarrow \mathbb{R}$ 或 $f: \mathbb{R}^n \rightarrow \mathbb{R}^m$，這對應於物理學中的場論——無論是標量場（溫度分佈）、向量場（流體速度、電磁場），還是更一般的張量場。

本章將系統回顧偏導數、梯度、散度、旋度、雅可比矩陣等重要概念，並介紹多元函數的積分理論。這些工具將為後續章節中學習流形上的微分運算奠定基礎。

## 4.1 多元函數

### 4.1.1 從單變數到多變數

在物理學和工程學中，我們經常需要描述一個量如何隨多個變數變化。例如：

- **溫度場**：$T(x, y, z)$ 是空間位置的函數
- **電勢場**：$\phi(x, y, z)$ 描述電荷產生的電勢分佈
- **壓力場**：$P(x, y, z, t)$ 描述流體中的壓力分佈（依賴於空間和時間）

這些都是多元函數的例子。

### 4.1.2 多元函數的定義

**定義（多元函數）**：

從 $\mathbb{R}^n$ 到 $\mathbb{R}$ 的函數 $f: \mathbb{R}^n \rightarrow \mathbb{R}$ 稱為**多元函數**或**純量場**。例如：
$$f(x^1, x^2, \ldots, x^n) = f(x_1, x_2, \ldots, x_n)$$

我們也經常使用向量記號：若 $x = (x^1, \ldots, x^n)$，則記 $f(x)$。

### 4.1.3 向量值函數

更一般地，**向量值函數**或**向量場**是映射：
$$\mathbf{F}: \mathbb{R}^n \rightarrow \mathbb{R}^m$$

例如，$\mathbf{F}: \mathbb{R}^3 \rightarrow \mathbb{R}^3$ 表示三維空間中的向量場：
$$\mathbf{F}(x, y, z) = (P(x,y,z), Q(x,y,z), R(x,y,z))$$

### 4.1.4 函數的圖形

單變數函數 $f: \mathbb{R} \rightarrow \mathbb{R}$ 的圖形是二維平面中的一條曲線。

二元函數 $f: \mathbb{R}^2 \rightarrow \mathbb{R}$ 的圖形是三維空間中的一個曲面：
$$z = f(x, y)$$

三元函數 $f: \mathbb{R}^3 \rightarrow \mathbb{R}$ 的圖形是四維空間中的「超曲面」，我們通常用等值面來視覺化。

## 4.2 偏導數

### 4.2.1 偏導數的定義

**定義（偏導數）**：

函數 $f(x^1, \ldots, x^n)$ 對 $x^i$ 的**偏導數**定義為：
$$\frac{\partial f}{\partial x^i} = \lim_{\Delta x^i \to 0} \frac{f(x^1, \ldots, x^i + \Delta x^i, \ldots, x^n) - f(x^1, \ldots, x^i, \ldots, x^n)}{\Delta x^i}$$

注意：在計算偏導數時，將其他變數視為常數，只對目標變數求導。

### 4.2.2 偏導數的幾何意義

在一元函數中，導數 $f'(a)$ 給出了函數圖形在點 $(a, f(a))$ 處切線的斜率。

在二元函數 $f(x, y)$ 中：

- $\partial f/\partial x$ 給出了函數圖形在 $x$ 方向的切線斜率（在固定 $y$ 下）
- $\partial f/\partial y$ 給出了函數圖形在 $y$ 方向的切線斜率（在固定 $x$ 下）

這兩個偏導數定義了函數圖形在該點的**切平面**。

### 4.2.3 偏導數的記號

常見的偏導數記號：

- **標準記號**：$\frac{\partial f}{\partial x^i}$ 或 $\partial_i f$
- **下標逗號記號**：$f_{,i} = \partial_i f$（在物理學和廣義相對論中常用）
- **向量微分算子**：$\nabla f$（梯度向量）

### 4.2.4 高階偏導數

二階偏導數：
$$\frac{\partial^2 f}{\partial x^i \partial x^j} = \partial_i \partial_j f = f_{,ij}$$

更高階的偏導數定義類似。

**混合偏導數相等定理**（Clairaut 定理）：

若函數足夠光滑（在某開區域內所有二階偏導數連續），則混合偏導數相等：
$$\frac{\partial^2 f}{\partial x \partial y} = \frac{\partial^2 f}{\partial y \partial x}$$

這是因為混合導數與求導順序無關。

## 4.3 梯度

### 4.3.1 梯度的定義

**定義（梯度）**：

梯度是一個向量，指向函數增長最快的方向。對於純量場 $f: \mathbb{R}^n \rightarrow \mathbb{R}$，梯度定義為：
$$\nabla f = \left(\frac{\partial f}{\partial x^1}, \frac{\partial f}{\partial x^2}, \ldots, \frac{\partial f}{\partial x^n}\right)$$

在廣義相對論的指標記號中：
$$(\nabla f)^i = g^{ij} \partial_j f$$

注意：當使用非笛卡爾坐標系時，梯度作為向量需要通過度量來升降指標。

### 4.3.2 梯度的幾何意義

梯度具有以下重要的幾何性質：

1. **方向性**：梯度 $\nabla f$ 指向函數值增加最快的方向
2. **正交性**：梯度與函數的等值面（level set）正交
3. **大小**：梯度的模 $\|\nabla f\|$ 是方向導數的最大值

### 4.3.3 方向導數

函數 $f$ 在單位向量 $u$ 方向上的**方向導數**為：
$$D_u f = \nabla f \cdot u = (\nabla f)^i u_i$$

方向導數度量了函數沿某個方向的變化率。

**定理**：方向導數的最大值為 $\|\nabla f\|$，發生在 $u$ 與 $\nabla f$ 同向時。

### 4.3.4 示例

**示例 1**：設 $f(x, y) = x^2 + y^2$，則：
$$\nabla f = (2x, 2y)$$

在點 $(1, 1)$ 處，梯度為 $(2, 2)$，指向徑向向外。

**示例 2**：設 $f(x, y, z) = \sqrt{x^2 + y^2 + z^2} = r$，則：
$$\nabla f = \left(\frac{x}{r}, \frac{y}{r}, \frac{z}{r}\right) = \hat{r}$$

這正是單位徑向向量。

## 4.4 向量場的導數運算

### 4.4.1 向量場

從 $\mathbb{R}^n$ 到 $\mathbb{R}^n$ 的函數 $\mathbf{F}: \mathbb{R}^n \rightarrow \mathbb{R}^n$ 稱為**向量場**。例如：
$$\mathbf{F}(x, y, z) = (P(x,y,z), Q(x,y,z), R(x,y,z))$$

### 4.4.2 雅可比矩陣

向量場 $\mathbf{F} = (F^1, \ldots, F^m)$ 的**雅可比矩陣**是：
$$J_{ij} = \frac{\partial F^i}{\partial x^j}$$

這是一個 $m \times n$ 矩陣，完全描述了向量場在每點的線性近似。

對於單變數函數，雅可比矩陣退化的 $1 \times 1$ 矩陣，即普通導數。

對於向量值函數 $\mathbf{F}: \mathbb{R}^n \rightarrow \mathbb{R}^n$，雅可比矩陣是 $n \times n$ 方陣。

### 4.4.3 雅可比矩陣的幾何意義

雅可比矩陣描述了向量場的**線性近似**。若 $\mathbf{F}: \mathbb{R}^n \rightarrow \mathbb{R}^n$，則：
$$\mathbf{F}(x + \Delta x) \approx \mathbf{F}(x) + J(x) \Delta x$$

這推廣了單變數函數的微分公式 $f(x + \Delta x) \approx f(x) + f'(x) \Delta x$。

### 4.4.4 雅可比行列式

當雅可比矩陣是方陣時（即 $m = n$），其行列式 $\det(J)$ 稱為**雅可比行列式**。

**幾何意義**：雅可比行列式度量了映射在該點處的體積縮放因子。在變數變換中，雅可比行列式的絕對值出現在積分變換公式中。

## 4.5 散度

### 4.5.1 散度的定義

**定義（散度）**：

散度是一個將向量場映射到純量場的運算。在三維空間中：
$$\nabla \cdot \mathbf{F} = \frac{\partial P}{\partial x} + \frac{\partial Q}{\partial y} + \frac{\partial R}{\partial z}$$

在一般維度中，使用指標記號：
$$\nabla_\mu V^\mu = \partial_\mu V^\mu = \frac{\partial V^1}{\partial x^1} + \cdots + \frac{\partial V^n}{\partial x^n}$$

### 4.5.2 散度的物理意義

散度的物理意義取決於應用場景：

- **流體力學**：$\nabla \cdot \mathbf{v}$ 表示速度場的「源強度」。若 $\nabla \cdot \mathbf{v} > 0$，則該點是流體的源（流出）；若 $\nabla \cdot \mathbf{v} < 0$，則是匯（流入）。

- **電學**：$\nabla \cdot \mathbf{E} = \rho/\epsilon_0$（高斯定律的微分形式）。電場的散度正比於電荷密度。

- **熱傳導**：$\nabla \cdot (k \nabla T)$ 描述熱流的散度。

### 4.5.3 散度的性質

散度運算滿足以下線性性質：

- $\nabla \cdot (\mathbf{F} + \mathbf{G}) = \nabla \cdot \mathbf{F} + \nabla \cdot \mathbf{G}$
- $\nabla \cdot (f \mathbf{F}) = \nabla f \cdot \mathbf{F} + f \nabla \cdot \mathbf{F}$

### 4.5.4 示例

**示例 1**：設 $\mathbf{F} = (x, y, z)$，則：
$$\nabla \cdot \mathbf{F} = \frac{\partial x}{\partial x} + \frac{\partial y}{\partial y} + \frac{\partial z}{\partial z} = 3$$

**示例 2**：設 $\mathbf{F} = \frac{\mathbf{r}}{r^3} = \frac{(x, y, z)}{(x^2+y^2+z^2)^{3/2}}$（除了原點），則：
$$\nabla \cdot \mathbf{F} = 0$$

這對應於單位點源的電場（除源點外無散度）。

## 4.6 旋度

### 4.6.1 旋度的定義

**定義（旋度）**：

旋度是一個將向量場映射到向量場的運算。在三維空間中，使用行列式形式：
$$\nabla \times \mathbf{F} = \begin{vmatrix} \mathbf{i} & \mathbf{j} & \mathbf{k} \\ \frac{\partial}{\partial x} & \frac{\partial}{\partial y} & \frac{\partial}{\partial z} \\ P & Q & R \end{vmatrix}$$

展開為：
$$(\nabla \times \mathbf{F})^i = \epsilon^{ijk} \partial_j F_k$$

其中 $\epsilon^{ijk}$ 是 Levi-Civita 符號。

顯式寫出：
$$\nabla \times \mathbf{F} = \left(\frac{\partial R}{\partial y} - \frac{\partial Q}{\partial z}, \frac{\partial P}{\partial z} - \frac{\partial R}{\partial x}, \frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y}\right)$$

### 4.6.2 旋度的物理意義

旋度描述向量場的「旋轉」程度：

- 若 $\nabla \times \mathbf{F} = 0$，則 $\mathbf{F}$ 是**保守場**（無旋場）
- 若 $\nabla \times \mathbf{F} \neq 0$，則向量場在該點有旋轉分量

**示例**：

- 點電荷產生的電場 $\mathbf{E}$ 是保守場：$\nabla \times \mathbf{E} = 0$
- 點電荷產生的磁場 $\mathbf{B}$ 不是保守場：$\nabla \times \mathbf{B} \neq 0$

### 4.6.3 重要的恆等式

**定理**：對任意光滑向量場 $\mathbf{F}$：
$$\nabla \cdot (\nabla \times \mathbf{F}) = 0$$

這意味著旋度場是**無源場**（ solenoidal field）。

## 4.7 拉普拉斯算子

### 4.7.1 拉普拉斯算子的定義

**定義（拉普拉斯算子）**：

拉普拉斯算子是梯度的散度：
$$\nabla^2 f = \nabla \cdot (\nabla f) = \partial_{ii} f = \sum_{i=1}^n \frac{\partial^2 f}{\partial (x^i)^2}$$

在指標記號中：
$$\nabla^2 f = g^{ij} \partial_i \partial_j f$$

注意：在彎曲流形上，我們使用協變導數：
$$\nabla^2 f = g^{ij} \nabla_i \nabla_j f = g^{ij} (\partial_i \partial_j f - \Gamma^k_{\ ij} \partial_k f)$$

### 4.7.2 拉普拉斯方程與泊松方程

**拉普拉斯方程**：若 $\nabla^2 f = 0$，則 $f$ 滿足**拉普拉斯方程**，稱為**調和函數**。

調和函數具有極值原理：在區域內部不能達到最大值或最小值（除非是常數）。

**泊松方程**：若 $\nabla^2 f = \rho$，則稱為**泊松方程**。

- 在牛頓引力中，$\nabla^2 \Phi = 4\pi G \rho$（$\Phi$ 是引力勢）
- 在電學中，$\nabla^2 \phi = -\rho/\epsilon_0$（$\phi$ 是電勢）

### 4.7.3 調和函數的例子

**示例 1**：$f(x, y) = x^2 - y^2$ 是調和函數嗎？
$$\nabla^2 f = \frac{\partial^2 f}{\partial x^2} + \frac{\partial^2 f}{\partial y^2} = 2 - 2 = 0$$
是的，這是調和函數。

**示例 2**：$f(x, y) = \ln r = \ln \sqrt{x^2 + y^2}$ 在除原點外是調和函數。

## 4.8 多元函數的積分

### 4.8.1 多重積分

函數 $f(x^1, \ldots, x^n)$ 在區域 $V$ 上的積分：
$$\int_V f \, dV = \int \cdots \int_V f(x^1, \ldots, x^n) \, dx^1 \cdots dx^n$$

這稱為**多重積分**或**體積積分**。

### 4.8.2 二重積分與三重積分

**二重積分**（對面積分）：
$$\iint_D f(x, y) \, dA = \iint_D f(x, y) \, dx \, dy$$

**三重積分**（對體積積分）：
$$\iiint_V f(x, y, z) \, dV = \iiint_V f(x, y, z) \, dx \, dy \, dz$$

### 4.8.3 變數變換

變數變換時，積分變換為：
$$\int_{V'} f(x') \, dV' = \int_V f(x(u)) \left| \frac{\partial(x^1, \ldots, x^n)}{\partial(u^1, \ldots, u^n)} \right| \, dU$$

其中 $\left| \frac{\partial x}{\partial u} \right|$ 是**雅可比行列式**，度量了體積元素的變換因子。

### 4.8.4 示例

**示例（極座標變換）**：

在二維極座標變換 $x = r\cos\theta$，$y = r\sin\theta$ 中：
$$\frac{\partial(x, y)}{\partial(r, \theta)} = \begin{vmatrix} \cos\theta & -r\sin\theta \\ \sin\theta & r\cos\theta \end{vmatrix} = r$$

因此：
$$\iint f(x, y) \, dx \, dy = \iint f(r\cos\theta, r\sin\theta) \, r \, dr \, d\theta$$

這個額外的 $r$ 因子正是極座標中的面積元 $dA = r \, dr \, d\theta$。

## 4.9 曲線積分與曲面積分

### 4.9.1 曲線積分

對向量場 $\mathbf{F}$ 沿曲線 $C$ 的**線積分**（對弧長）：
$$\int_C \mathbf{F} \cdot d\mathbf{r} = \int_a^b \mathbf{F}(\mathbf{r}(t)) \cdot \mathbf{r}'(t) \, dt$$

其中 $\mathbf{r}: [a, b] \rightarrow \mathbb{R}^3$ 是曲線的參數化。

**物理意義**：這表示沿曲線 $C$ 做功的總和。

### 4.9.2 曲面積分

對向量場 $\mathbf{F}$ 穿過曲面 $S$ 的**通量積分**：
$$\iint_S \mathbf{F} \cdot d\mathbf{S} = \iint_D \mathbf{F}(\mathbf{r}(u, v)) \cdot (\mathbf{r}_u \times \mathbf{r}_v) \, du \, dv$$

**物理意義**：這表示穿過曲面 $S$ 的總流量。

## 4.10 格林定理、斯托克斯定理與散度定理

### 4.10.1 格林定理（二維）

格林定理建立了平面區域上的二重積分與其邊界曲線上的線積分之間的關係：

$$\oint_{\partial D} (P \, dx + Q \, dy) = \iint_D \left(\frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y}\right) \, dA$$

這可以寫成向量形式：
$$\oint_{\partial D} \mathbf{F} \cdot \mathbf{n} \, ds = \iint_D (\nabla \times \mathbf{F}) \cdot \mathbf{k} \, dA$$

### 4.10.2 斯托克斯定理（三維曲面積分）

斯托克斯定理建立了曲面上的旋度積分與其邊界曲線上的線積分之間的關係：

$$\oint_{\partial S} \mathbf{F} \cdot d\mathbf{r} = \iint_S (\nabla \times \mathbf{F}) \cdot \mathbf{n} \, dS$$

### 4.10.3 散度定理（高斯定理）

散度定理建立了體積內的散度積分與穿過邊界曲面的通量之間的關係：

$$\iint_{\partial V} \mathbf{F} \cdot \mathbf{n} \, dS = \iiint_V (\nabla \cdot \mathbf{F}) \, dV$$

### 4.10.4 斯托克斯定理的統一形式

這三個定理——格林定理、斯托克斯定理、散度定理——是**斯托克斯定理**在三維空間中的不同表述。斯托克斯定理是描述微分形式積分的統一理論，這將在第八章（微分形式）中詳細討論。

## 4.11 泰勒級數

### 4.11.1 多元泰勒展開

函數 $f(x)$ 在點 $a$ 附近的泰勒展開：
$$f(x) = f(a) + \partial_\mu f(a) (x^\mu - a^\mu) + \frac{1}{2} \partial_\mu \partial_\nu f(a) (x^\mu - a^\mu)(x^\nu - a^\nu) + \cdots$$

在廣義相對論中，我們經常需要計算度規在某一點附近的展開，這正是這種泰勒展開的應用。

### 4.11.2 海森矩陣

二階項可用矩陣表示：
$$f(x) \approx f(a) + \nabla f(a) \cdot (x-a) + \frac{1}{2} (x-a)^T H (x-a)$$

其中 $H$ 是**海森矩陣**（Hessian matrix）：
$$H_{ij} = \frac{\partial^2 f}{\partial x^i \partial x^j}$$

海森矩陣在優化理論中扮演重要角色。

### 4.11.3 在物理學中的應用

泰勒級數常用於近似計算和建立物理理論。例如：

- **牛頓引力**：廣義相對論在弱場、低速極限下的近似
- **量子力學**：微擾理論的數學基礎
- **光學**：近軸近似的基礎

## 4.12 極值問題

### 4.12.1 臨界點

若 $\nabla f = 0$，則點 $a$ 是 $f$ 的**臨界點**。

臨界點可能是：
- **局部最小值**
- **局部最大值**
- **鞍點**（既非極大也非極小）

### 4.12.2 海森矩陣判斷

對於二階可微函數：

- 若 $H$ **正定**：局部最小值
- 若 $H$ **負定**：局部最大值
- 若 $H$ **不定**：鞍點
- 若 $H$ **半正定**或**半負定**：需要更高階導數判斷

### 4.12.3 拉格朗日乘數法

在約束 $g(x) = 0$ 下優化 $f(x)$，是物理學和工程學中的常見問題。

構造**拉格朗日函數**：
$$\mathcal{L}(x, \lambda) = f(x) + \lambda g(x)$$

求解**拉格朗日方程組**：
$$\nabla_x \mathcal{L} = 0, \quad \nabla_\lambda \mathcal{L} = 0$$

**示例**：在約束 $x^2 + y^2 = 1$ 下優化 $f(x, y) = xy$。

## 4.13 隱函數定理

### 4.13.1 定理陳述

**定理（隱函數定理）**：

若 $F: \mathbb{R}^{n+m} \rightarrow \mathbb{R}^m$ 在點 $(a, b)$ 附近滿足：

1. $F(a, b) = 0$
2. 雅可比矩陣 $\frac{\partial F^i}{\partial y^j}(a, b)$ 可逆（即行列式非零）

則存在唯一的光滑函數 $f: \mathbb{R}^n \rightarrow \mathbb{R}^m$ 使得：
$$F(x, f(x)) = 0$$

### 4.13.2 幾何意義

隱函數定理保證了由方程 $F(x, y) = 0$ 定義的集合在局部是一個良好的 $n$ 維流形。

例如，方程 $x^2 + y^2 + z^2 = 1$ 在局部定義了球面 $S^2$（二維流形）。

這是微分幾何中流形定義的關鍵基礎！

## 重點回顧

| 概念 | 說明 |
|------|------|
| 偏導數 $\partial_i$ | 保持其他變數不變的導數 |
| 梯度 $\nabla f$ | 指向函數增長最快方向的向量 |
| 雅可比矩陣 | 向量場的線性近似矩陣 |
| 散度 $\nabla \cdot \mathbf{F}$ | 向量場的源強度 |
| 旋度 $\nabla \times \mathbf{F}$ | 向量場的旋轉程度 |
| 拉普拉斯算子 $\nabla^2$ | 梯度的散度 |
| 格林定理 | 2D 區域積分與邊界積分的關係 |
| 斯托克斯定理 | 3D 曲面積分與邊界積分的關係 |
| 散度定理 | 體積積分與表面積分的關係 |
| 海森矩陣 | 二階偏導數矩陣 |
| 隱函數定理 | 方程定義流形的條件 |

## 練習題

1. **偏導數計算**：計算 $f(x, y, z) = x^2 y + y^2 z + z^2 x$ 的所有一階偏導數 $\partial f/\partial x$，$\partial f/\partial y$，$\partial f/\partial z$，以及二階偏導數。

2. **梯度與方向導數**：設 $f(x, y) = x^2 + xy + y^2$，求：
   - 梯度 $\nabla f$
   - 在點 $(1, 1)$ 處，沿方向 $\mathbf{u} = (1/\sqrt{2}, 1/\sqrt{2})$ 的方向導數
   - 函數增長最快的方向

3. **散度與旋度**：求向量場 $\mathbf{F} = (yz, xz, xy)$ 的散度和旋度，並解釋結果的物理意義。

4. **散度定理應用**：使用散度定理計算向量場 $\mathbf{F} = (x, y, z)$ 穿過半徑為 $R$ 的球面的總通量。

5. **格林定理驗證**：驗證格林定理對於向量場 $\mathbf{F} = (-y, x)$ 和單位圓區域 $D$。

6. **拉普拉斯方程**：驗證函數 $f(x, y) = \ln\sqrt{x^2 + y^2}$ 除了原點外滿足拉普拉斯方程 $\nabla^2 f = 0$。

7. **變數變換**：使用極座標變換計算二重積分 $\iint_D (x^2 + y^2) \, dA$，其中 $D$ 是單位圓 $x^2 + y^2 \leq 1$。

8. **海森矩陣**：設 $f(x, y) = x^3 - 3xy + y^3$，求其臨界點並使用海森矩陣判斷每個臨界點的類型。

9. **隱函數定理應用**：由方程 $F(x, y) = x^2 + y^2 - 1 = 0$ 定義單位圓。驗證在點 $(1, 0)$ 附近可以將 $y$ 表達為 $x$ 的函數，並求 $dy/dx$。

10. **泰勒展開**：將函數 $f(x, y) = e^{x+y}$ 在點 $(0, 0)$ 附近展開到二階項。
