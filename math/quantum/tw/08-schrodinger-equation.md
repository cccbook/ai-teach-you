# 第八章：薛丁格方程式推導——量子力學的基本方程

## 8.1 薛丁格方程式的歷史背景

埃爾溫·薛丁格（Erwin Rudolf Josef Alexander Schrödinger，1887-1961）是二十世紀最偉大的理論物理學家之一，他的名字永遠與量子力學聯繫在一起。薛丁格出生於維也納，1910年在維也納大學獲得博士學位，此後在多所大學任教，包括蘇黎世大學、柏林大學和都柏林高級研究院。

薛丁格提出波動方程的故事充滿了传奇色彩。1925年聖誕節期間，薛丁格來到瑞士阿羅薩（Arosa）度假。根據他的傳記，他在這段時間裡「想出了」波動力學的基本方程。他後來回憶說，思想的突破來自於對德布羅意物質波假說的深入思考。

1926年，薛丁格發表了一系列論文，提出了著名的波動方程式。這些論文徹底改變了理論物理的面貌，為量子力學的發展奠定了堅實的數學基礎。同年，薛丁格證明了波動力學與海森堡的矩陣力學在數學上是等價的，這進一步確立了新量子理論的正確性。

## 8.2 含時薛丁格方程式

**含時薛丁格方程式**（Time-Dependent Schrödinger Equation）的一般形式為：

$$i\hbar\frac{\partial}{\partial t}\psi(\mathbf{r},t) = \hat{H}\psi(\mathbf{r},t)$$

其中 $\hat{H}$ 是**哈密頓算符**（Hamiltonian operator），代表系統的總能量（動能加勢能）。

對於單粒子系統，哈密頓算符為：

$$\hat{H} = -\frac{\hbar^2}{2m}\nabla^2 + V(\mathbf{r},t)$$

這裡：
- 第一項 $-\frac{\hbar^2}{2m}\nabla^2$ 是**動能項**
- 第二項 $V(\mathbf{r},t)$ 是**勢能項**

這就是量子力學的運動方程，類似於經典力學中的牛頓第二定律 $F = ma$。但與牛頓定律不同，薛丁格方程式是複數方程，描述的是機率幅的演化，而不是確定的軌道。

## 8.3 從自由粒子推導薛丁格方程式

讓我們從自由粒子出發來推導薛丁格方程式。

### 8.3.1 自由粒子的平面波

自由粒子的德布羅意平面波可以寫成：

$$\psi(x,t) = A e^{i(kx - \omega t)}$$

或者使用粒子動量 $p = \hbar k$ 和能量 $E = \hbar \omega$：

$$\psi(x,t) = A e^{i(px - Et)/\hbar}$$

### 8.3.2 對波函數求導

對時間求偏導數：

$$\frac{\partial\psi}{\partial t} = -\frac{iE}{\hbar}\psi$$

因此：

$$i\hbar\frac{\partial\psi}{\partial t} = E\psi$$

對空間求二階偏導數：

$$\frac{\partial\psi}{\partial x} = \frac{ip}{\hbar}\psi$$

$$\frac{\partial^2\psi}{\partial x^2} = \left(\frac{ip}{\hbar}\right)^2\psi = -\frac{p^2}{\hbar^2}\psi$$

### 8.3.3 代入能量動量關係

對於非相對論自由粒子，能量-動量關係為：

$$E = \frac{p^2}{2m}$$

因此：

$$-\frac{\hbar^2}{2m}\frac{\partial^2\psi}{\partial x^2} = \frac{p^2}{2m}\psi = E\psi$$

比較兩個結果，我們發現：

$$i\hbar\frac{\partial\psi}{\partial t} = -\frac{\hbar^2}{2m}\frac{\partial^2\psi}{\partial x^2}$$

這就是**一維自由粒子的薛丁格方程式**！

這個推導展示了能量-動量關係如何轉化為微分方程。量子力學的核心思想是：經典物理中的能量動量關係 $E = p^2/2m$ 在量子力學中被提升為算符方程。

## 8.4 一般勢場中的薛丁格方程式

對於在勢場 $V(x,t)$ 中運動的粒子，我們需要在方程中加入勢能項。

在經典力學中，總能量（哈密頓量）為：

$$H = \frac{p^2}{2m} + V(x,t)$$

將這個公式中的物理量替換為相應的算符：
- 動量 $p \to -i\hbar\frac{\partial}{\partial x}$
- 位置 $x \to x$
- 勢能 $V(x,t) \to V(x,t)$（假設為實函數）

我們得到哈密頓算符：

$$\hat{H} = -\frac{\hbar^2}{2m}\frac{\partial^2}{\partial x^2} + V(x,t)$$

因此，完整的含時薛丁格方程式為：

$$i\hbar\frac{\partial\psi}{\partial t} = \left[-\frac{\hbar^2}{2m}\frac{\partial^2}{\partial x^2} + V(x,t)\right]\psi$$

在三維情況下：

$$i\hbar\frac{\partial}{\partial t}\psi(\mathbf{r},t) = \left[-\frac{\hbar^2}{2m}\nabla^2 + V(\mathbf{r},t)\right]\psi(\mathbf{r},t)$$

這個方程式是量子力學的基本假設之一，它不能從更基本的原理推導出來，而是作為理論的基本公設。

## 8.5 不含時薛丁格方程式

很多實際問題中，勢能 $V$ 與時間無關，即 $V = V(\mathbf{r})$。這時我們可以使用**分離變數法**來求解問題。

令波函數為：

$$\psi(\mathbf{r},t) = \psi(\mathbf{r})f(t)$$

代入含時薛丁格方程式：

$$i\hbar\psi(\mathbf{r})\frac{df}{dt} = f(t)\hat{H}\psi(\mathbf{r})$$

兩邊除以 $\psi(\mathbf{r})f(t)$（假設都不為零）：

$$i\hbar\frac{1}{f}\frac{df}{dt} = \frac{1}{\psi}\hat{H}\psi(\mathbf{r})$$

左邊只依賴於時間，右邊只依賴於空間。兩邊必須等於同一個常數，設為 $E$（這個常數將被證明是系統的能量本徵值）：

$$i\hbar\frac{df}{dt} = Ef \Rightarrow f(t) = e^{-iEt/\hbar}$$

這個指數函數描述了時間依賴的相位因子，這是振盪函數。

空間部分滿足：

$$\hat{H}\psi(\mathbf{r}) = E\psi(\mathbf{r})$$

這就是**不含時薛丁格方程式**（或稱為**定態薛丁格方程式**），是一個本徵值問題。

## 8.6 定態與定態波函數

不含時薛丁格方程式的解 $\psi_n(\mathbf{r})$ 稱為**定態波函數**（stationary state wave function），對應的本徵值 $E_n$ 是系統的能量本徵值。

定態具有以下重要性質：

### 8.6.1 能量確定

系統處於定態時，測量能量的結果總是確定的 $E_n$。這是因為定態是哈密頓算符的本徵態。

### 8.6.2 機率密度不變

定態的機率密度與時間無關：

$$|\psi_n(\mathbf{r},t)|^2 = |\psi_n(\mathbf{r})|^2$$

這是因為時間依賴只是整體相位因子：

$$|\psi_n(\mathbf{r},t)|^2 = |\psi_n(\mathbf{r}) e^{-iE_nt/\hbar}|^2 = |\psi_n(\mathbf{r})|^2 |e^{-iE_nt/\hbar}|^2 = |\psi_n(\mathbf{r})|^2$$

整體相位在物理上不可觀測，因此機率密度保持不變。

### 8.6.3 一般解是定態的疊加

對於一般的含時問題，波函數可以展開為定態的線性組合：

$$\psi(\mathbf{r},t) = \sum_n c_n \psi_n(\mathbf{r}) e^{-iE_n t/\hbar}$$

其中係數 $c_n$ 由初始條件決定：

$$c_n = \int \psi_n^*(\mathbf{r})\psi(\mathbf{r},0) d^3r$$

這個展開式表明，量子系統的一般狀態是定態的疊加，時間演化導致不同定態之間的相位差變化。

## 8.7 邊界條件

求解薛丁格方程式需要適當的**邊界條件**（boundary conditions）。邊界條件的選擇取決於具體的物理問題。

### 8.7.1 盒邊界條件（週期性邊界）

在一些問題中，特別是固態物理中處理晶格時，常使用週期性邊界條件：

$$\psi(\mathbf{r} + \mathbf{L}) = \psi(\mathbf{r})$$

這意味著波函數在週期性的「盒子」邊界上連續。

### 8.7.2 無限深勢阱

對於被無限高勢能牆限制的粒子，波函數在勢阱邊界處必須為零：

$$\psi(\text{邊界}) = 0$$

這保證了粒子不能穿過勢能無窮大的區域。

### 8.7.3 自然邊界條件

對於束縛態問題，波函數及其導數在無窮遠處必須有限：

$$\lim_{r \to \infty} \psi(\mathbf{r}) = 0$$

或者更一般地，波函數應該平方可積。

### 8.7.4 連續性邊界條件

在勢能跳躍的界面上（如有限勢壘），波函數及其一階導數必須連續：

$$\psi_{\text{左}} = \psi_{\text{右}}$$

$$\frac{\partial\psi_{\text{左}}}{\partial x} = \frac{\partial\psi_{\text{右}}}{\partial x}$$

這些條件來自於薛丁格方程式是二階微分方程。

## 8.8 哈密頓算符的物理意義

哈密頓算符 $\hat{H}$ 在量子力學中具有核心地位。

### 8.8.1 能量算符

在量子力學中，哈密頓算符是系統的總能量算符。測量系統能量時，測量結果是 $\hat{H}$ 的本徵值。

### 8.8.2 時間演化算符

時間演化算符為：

$$\hat{U}(t, t_0) = e^{-i\hat{H}(t-t_0)/\hbar}$$

這是一個**么正算符**（unitary operator），保證了時間演化過程中機率守恆：

$$\hat{U}^\dagger \hat{U} = \hat{U} \hat{U}^\dagger = \mathbf{1}$$

### 8.8.3 本徵值問題決定系統能譜

求解不含時薛丁格方程式 $\hat{H}\psi = E\psi$ 決定了系統的能譜：
- 離散譜（束縛態）
- 連續譜（游離態或自由態）

不同的物理系統有不同的哈密頓算符形式：

- **自由粒子**：$\hat{H} = -\frac{\hbar^2}{2m}\nabla^2$
- **氫原子**：$\hat{H} = -\frac{\hbar^2}{2m}\nabla^2 - \frac{e^2}{4\pi\varepsilon_0 r}$
- **諧振子**：$\hat{H} = -\frac{\hbar^2}{2m}\frac{d^2}{dx^2} + \frac{1}{2}m\omega^2 x^2$
- **自旋粒子在磁場中**：$\hat{H} = -\boldsymbol{\mu} \cdot \mathbf{B} = -\gamma \mathbf{B} \cdot \hat{\mathbf{S}}$

## 8.9 機率守恆與連續性方程

從含時薛丁格方程式可以推導出機率守恆。讓我們在三維情況下進行推導。

定義機率密度：

$$\rho(\mathbf{r},t) = |\psi(\mathbf{r},t)|^2 = \psi^*\psi$$

定義機率流密度：

$$\mathbf{j} = \frac{\hbar}{2mi}(\psi^*\nabla\psi - \psi\nabla\psi^*)$$

現在計算機率密度的時間導數：

$$\frac{\partial\rho}{\partial t} = \psi^*\frac{\partial\psi}{\partial t} + \psi\frac{\partial\psi^*}{\partial t}$$

利用含時薛丁格方程式：

$$i\hbar\frac{\partial\psi}{\partial t} = -\frac{\hbar^2}{2m}\nabla^2\psi + V\psi$$

取複共軛：

$$-i\hbar\frac{\partial\psi^*}{\partial t} = -\frac{\hbar^2}{2m}\nabla^2\psi^* + V\psi^*$$

代入並整理：

$$\frac{\partial\rho}{\partial t} = \frac{i\hbar}{2m}(\psi^*\nabla^2\psi - \psi\nabla^2\psi^*) = -\nabla \cdot \mathbf{j}$$

因此：

$$\frac{\partial\rho}{\partial t} + \nabla \cdot \mathbf{j} = 0$$

這就是**連續性方程**（continuity equation），與電磁學中的形式完全相同。

這個方程的物理意義是：機率既不能產生也不能消滅，只能在空間中流動。這是量子力學內在一致性的重要表現。

## 8.10 能量本徵值問題

不含時薛丁格方程式 $\hat{H}\psi = E\psi$ 是一個本徵值問題。一般來說：

1. **只有當 $E$ 取特定值（本徵值）時，方程才有物理上可接受的解**

2. **本徵值通常形成離散的譜（對於束縛態）或連續的譜（對於游離態）**

3. **每個本徵值對應一個或多個本徵函數（本徵態）**

4. **本徵函數相互正交**

$$\int \psi_m^*(\mathbf{r})\psi_n(\mathbf{r}) d^3r = \delta_{mn}$$

這些性質與數學中的厄米算符理論一致，這正是量子力學使用希爾伯特空間數學框架的原因。

## 8.11 薛丁格方程式的地位

薛丁格方程式在物理學中的地位是無與倫比的。

它與以下方程式並列為理論物理學的基本方程：
- 牛頓運動定律（經典力學）
- 馬克士威方程組（ electromagnetism ）
- 愛因斯坦場方程式（廣義相對論）
- 狄拉克方程式（相對論量子力學）

但與牛頓定律不同，薛丁格方程式描述的不是確定的軌道，而是機率幅的演化。這反映了微觀世界與宏觀世界的根本差異。

## 8.12 薛丁格方程式的局限性

薛丁格方程式是一個非相對論方程，它在以下情況下失效：

1. **當粒子速度接近光速時**，需要使用相對論方程（如克萊因-戈登方程式或狄拉克方程式）

2. **當涉及自旋等相對論效應時**，薛丁格方程式不能描述自旋自由度

3. **當需要考慮粒子產生和湮滅時**，需要使用量子場論

這些局限性推動了量子力學的進一步發展。

## 8.13 本章小結

本章我們詳細討論了薛丁格方程式。含時薛丁格方程式 $i\hbar\partial_t\psi = \hat{H}\psi$ 是量子力學的基本動力學方程，決定了波函數的時間演化。對於與時間無關的勢能，可以使用分離變數法得到不含時薛丁格方程式 $\hat{H}\psi = E\psi$，這是一個能量本徵值問題。我們還討論了邊界條件、哈密頓算符的物理意義、機率守恆以及能量本徵值問題的性質。薛丁格方程式是量子力學的核心方程，它開創了用微分方程描述量子系統的新時代。
