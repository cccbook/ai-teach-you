# 第十五章：狄拉克符號——量子力學的優美語言

## 15.1 狄拉克符號的由來

**狄拉克符號**（Dirac Notation），也稱為 **bra-ket 記號**，是英國物理學家保羅·狄拉克（Paul Dirac，1902-1984）發展的一套優美而強大的符號系統，用於描述量子力學。

狄拉克在1926年至1930年間發表的一系列論文中系統地發展了這套符號。這套符號將線性代數與量子力學完美結合，至今仍是量子力學的標準語言。

狄拉克符號的核心思想是：
- **右向量**（ket）：$|\psi\rangle$ 表示量子態
- **左向量**（bra）：$\langle\psi|$ 表示對偶空間中的向量
- **內積**：$\langle\phi|\psi\rangle$ 是一個複數
- **外積**：$|\phi\rangle\langle\psi|$ 是一個算符

這套符號之所以如此成功，是因為它與具體的表示無關，適用於任何希爾伯特空間。

## 15.2 右向量（Ket）

$|\psi\rangle$ 稱為**右向量**或 **ket**，代表希爾伯特空間中的一個量子態。

這個符號由字母「k」發展而來，代表「bracket」（括號）的右半部分。

右向量的例子：
- $|0\rangle$、$|1\rangle$ 可以表示二能級系統的兩個態
- $|n\rangle$ 可以表示諧振子的第 $n$ 個能級
- $|x_0\rangle$ 可以表示位置為 $x_0$ 的位置本徵態
- $|\psi\rangle$ 可以表示任意量子態

右向量支持向量空間的所有運算：
- 加法：$|\psi\rangle + |\phi\rangle$
- 標量乘法：$c|\psi\rangle$（$c$ 為複數）

## 15.3 左向量（Bra）

每一個右向量 $|\psi\rangle$ 都對應一個**左向量**（bra）$\langle\psi|$，定義在對偶空間中。

對偶空間包含所有從希爾伯特空間到複數的線性泛函（線性函數）。

左向量與右向量之間的對應是**共軛線性**的：
- $\langle\psi| = (|\psi\rangle)^\dagger$
- 若 $|\psi\rangle = c|\phi\rangle$，則 $\langle\psi| = c^*\langle\phi|$
- 注意標量乘法變成了共軛

對偶空間的存在保証了內積的良好定義。

## 15.4 內積（Bracket）

左向量與右向量配對形成**內積**（bracket），記為 $\langle\phi|\psi\rangle$：

$$\langle\phi|\psi\rangle \in \mathbb{C}$$

這個符號由「bra」和「ket」的組合形成，非常直觀。

內積的性質：
1. **共軛對稱性**：$\langle\phi|\psi\rangle = \langle\psi|\phi\rangle^*$
2. **線性性**（對第二個因子）：$\langle\phi|(a|\psi\rangle + b|\chi\rangle) = a\langle\phi|\psi\rangle + b\langle\phi|\chi\rangle$
3. **正定性**：$\langle\psi|\psi\rangle \geq 0$，等號成立當且僅當 $|\psi\rangle = 0$

注意內積對第一個因子是共軛線性的，這是標準約定：

$$\langle a\phi + b\chi|\psi\rangle = a^*\langle\phi|\psi\rangle + b^*\langle\chi|\psi\rangle$$

## 15.5 內積的物理意義

內積在量子力學中有深刻的物理意義。

### 15.5.1 機率幅

若 $|\psi\rangle$ 是歸一化態，$|\phi\rangle$ 是某個本徵態，則 $\langle\phi|\psi\rangle$ 是測量 $|\psi\rangle$ 得到 $|\phi\rangle$ 的**機率幅**。

機率為 $|\langle\phi|\psi\rangle|^2$。

### 15.5.2 期望值

若 $\hat{A}$ 是厄米算符，則：

$$\langle A \rangle_\psi = \frac{\langle\psi|\hat{A}|\psi\rangle}{\langle\psi|\psi\rangle}$$

這是物理量 $\hat{A}$ 在態 $|\psi\rangle$ 中的期望值。

### 15.5.3 重疊積分

內積可以理解為兩個態的「重疊」程度。內積越大，兩個態越「相似」。

## 15.6 外積

兩個向量可以形成**外積**，記為 $|\phi\rangle\langle\psi|$，這是一個**算符**（而非複數）：

$$(|\phi\rangle\langle\psi|)|\chi\rangle = |\phi\rangle\langle\psi|\chi\rangle = \langle\psi|\chi\rangle |\phi\rangle$$

外積在量子力學中非常重要，可以用來構造投影算符等。

## 15.7 投影算符

**投影算符**（Projection Operator）可以用外積構造。

若 $\{|e_i\rangle\}$ 是正交歸一基底，則投影到 $|e_i\rangle$ 的算符為：

$$P_i = |e_i\rangle\langle e_i|$$

這個算符的作用是：
$$P_i |\psi\rangle = |e_i\rangle\langle e_i|\psi\rangle = \langle e_i|\psi\rangle |e_i\rangle$$

投影算符滿足：
- $P_i^2 = P_i$（冪等性）
- $P_i^\dagger = P_i$（厄米性）
- $P_i P_j = 0$ 若 $i \neq j$（正交性）

## 15.8 基底與表示

**正交歸一基底**（Orthonormal Basis）$\{|e_i\rangle\}$ 滿足：

$$\langle e_i | e_j \rangle = \delta_{ij}$$

任意態可以展開為：

$$|\psi\rangle = \sum_i |e_i\rangle\langle e_i|\psi\rangle = \sum_i c_i |e_i\rangle$$

其中 $c_i = \langle e_i|\psi\rangle$ 是分量（坐標）。

這個展開式的意義是：將態向量投影到每個基向量，得到的分量就是內積。

## 15.9 封閉性關係

由正交歸一基底的定義，我們得到：

**封閉性關係**（Completeness Relation）或**識別關係**：

$$\sum_i |e_i\rangle\langle e_i| = \mathbf{1}$$

這意味著單位算符可以展開為外積之和。

這個關係極其重要，它告訴我們可以在任意表象中插入單位算符：

$$|\psi\rangle = \mathbf{1}|\psi\rangle = \sum_i |e_i\rangle\langle e_i|\psi\rangle$$

## 15.10 連續基底

對於連續變量的情形（如位置與動量），基底是連續的。

### 15.10.1 位置基底

位置基底 $\{|x\rangle\}$ 滿足：

$$\langle x|x'\rangle = \delta(x - x')$$

其中 $\delta$ 是 Dirac δ函數。

任意態的波函數：

$$\psi(x) = \langle x|\psi\rangle$$

封閉性關係：

$$\int |x\rangle\langle x| dx = \mathbf{1}$$

### 15.10.2 動量基底

動量基底 $\{|p\rangle\}$ 滿足：

$$\langle p|p'\rangle = \delta(p - p')$$

波函數（動量空間）：

$$\tilde{\psi}(p) = \langle p|\psi\rangle$$

封閉性關係：

$$\int |p\rangle\langle p| dp = \mathbf{1}$$

## 15.11 表象變換

不同表象之間的變換由內積給出。

### 15.11.1 位置-動量變換

位置基底與動量基底之間的關係由傅立葉變換給出：

$$\langle x|p\rangle = \frac{1}{\sqrt{2\pi\hbar}} e^{ipx/\hbar}$$

$$\langle p|x\rangle = \frac{1}{\sqrt{2\pi\hbar}} e^{-ipx/\hbar}$$

### 15.11.2 波函數的傅立葉變換

由位置表象到動量表象的變換：

$$\psi(x) = \frac{1}{\sqrt{2\pi\hbar}} \int \tilde{\psi}(p) e^{ipx/\hbar} dp$$

$$\tilde{\psi}(p) = \frac{1}{\sqrt{2\pi\hbar}} \int \psi(x) e^{-ipx/\hbar} dx$$

這是量子力學中最重要的變換之一。

## 15.12 算符的表示

在基底 $\{|e_i\rangle\}$ 中，算符 $\hat{A}$ 可以表示為矩陣：

$$A_{ij} = \langle e_i|\hat{A}|e_j\rangle$$

這個矩陣的第 $i$ 行第 $j$ 列元素是從 $|e_j\rangle$ 到 $|e_i\rangle$ 的矩陣元。

算符作用於態：

$$\hat{A}|\psi\rangle = \sum_i |e_i\rangle\langle e_i|\hat{A}|\psi\rangle = \sum_i |e_i\rangle \sum_j A_{ij} c_j$$

其中 $c_j = \langle e_j|\psi\rangle$ 是 $|\psi\rangle$ 的分量。

## 15.13 狄拉克符號的優勢

狄拉克符號相比傳統的函數記號有諸多優勢：

1. **與基底無關**：符號本身就體現了向量的本質，不依賴於具體表示
2. **計算簡便**：內積、外積、算符作用等操作形式簡潔
3. **推廣容易**：容易推廣到多粒子系統、複合系統等
4. **物理清晰**：將測量機率幅與內積聯繫起來
5. **對稱美觀**：符號本身就體現了數學結構的對稱性

## 15.14 運算規則總結

讓我們總結狄拉克符號的基本運算規則：

**內積**：
$$\langle\phi|\psi\rangle$$

**外積**：
$$|\phi\rangle\langle\psi|$$

**算符作用**：
$$\hat{A}|\psi\rangle$$

**期望值**：
$$\langle\psi|\hat{A}|\psi\rangle$$

**插入識別關係**：
$$|\psi\rangle = \mathbf{1}|\psi\rangle = \sum_i |e_i\rangle\langle e_i|\psi\rangle$$

## 15.15 具體計算示例

讓我們用狄拉克符號進行一些具體計算。

### 15.15.1 展開定理

若 $|\psi\rangle$ 是任意態，$\{|e_i\rangle\}$ 是正交歸一基底，則：

$$|\psi\rangle = \sum_i c_i |e_i\rangle$$

其中 $c_i = \langle e_i|\psi\rangle$。

驗證：

$$\sum_i |e_i\rangle\langle e_i|\psi\rangle = \sum_i |e_i\rangle c_i = |\psi\rangle$$

### 15.15.2 矩陣元的計算

算符 $\hat{A}$ 在基底 $\{|e_i\rangle\}$ 中的矩陣元為：

$$A_{ij} = \langle e_i|\hat{A}|e_j\rangle$$

### 15.15.3 表象變換

從基底 $\{|e_i\rangle\}$ 變換到基底 $\{|f_j\rangle\}$，變換矩陣為：

$$U_{ij} = \langle e_i|f_j\rangle$$

新基底的態：

$$|f_j\rangle = \sum_i U_{ij}|e_i\rangle$$

## 15.16 與向量記號的比較

傳統的向量記號將向量寫為列矩陣：
$$\begin{pmatrix} c_1 \\ c_2 \\ \vdots \end{pmatrix}$$

狄拉克符號寫為 $|c\rangle$，更加抽象和優美。

內積 $\langle a|b\rangle$ 對應於行向量乘以列向量：
$$\begin{pmatrix} a_1^* & a_2^* & \cdots \end{pmatrix} \begin{pmatrix} b_1 \\ b_2 \\ \vdots \end{pmatrix}$$

算符 $\hat{A}$ 作用於 $|b\rangle$ 給出 $|c\rangle = \hat{A}|b\rangle$，對應於矩陣乘法。

## 15.17 狄拉克符號的哲學意義

狄拉克符號不僅是一種方便的數學工具，還反映了量子力學的深刻哲學。

符號的抽象性與量子態的抽象性相呼應：物理態本身不依賴於我們如何描述它。這與量子力學的測量問題和實在性問題有深刻的聯繫。

## 15.18 本章小結

本章我們介紹了狄拉克符號（bra-ket 記號）。我們討論了右向量 $|\psi\rangle$、左向量 $\langle\psi|$、內積 $\langle\phi|\psi\rangle$、外積 $|\phi\rangle\langle\psi|$、連續基底（位置與動量）等概念。狄拉克符號是量子力學的標準數學語言，優美而強大，與具體表示無關，適用於任何希爾伯特空間。
