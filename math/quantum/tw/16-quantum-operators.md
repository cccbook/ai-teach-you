# 第十六章：量子算符——可觀測量的數學表示

## 16.1 算符的基本概念

在量子力學中，**算符**（Operator）是作用於希爾伯特空間向量上的線性變換。算符將一個態向量變換為另一個態向量：

$$|\psi'\rangle = \hat{A}|\psi\rangle$$

算符在量子力學中扮演著核心角色，因為每一個物理量（可觀測量）都對應於希爾伯特空間中的一個算符。

算符的概念是量子力學與經典力學之間最深刻的區別之一。在經典力學中，物理量是數值；在量子力學中，物理量是算符。

## 16.2 線性算符

算符 $\hat{A}$ 是**線性算符**，若對所有向量 $|\psi\rangle$、$|\phi\rangle$ 和標量 $a$、$b$：

$$\hat{A}(a|\psi\rangle + b|\phi\rangle) = a\hat{A}|\psi\rangle + b\hat{A}|\phi\rangle$$

量子力學主要討論線性算符，因為量子力學的基本原理要求態的疊加對應於算符作用的線性疊加。

## 16.3 算符的代數運算

### 16.3.1 算符加法

兩個算符的和定義為：

$$(\hat{A} + \hat{B})|\psi\rangle = \hat{A}|\psi\rangle + \hat{B}|\psi\rangle$$

算符加法滿足交換律和結合律。

### 16.3.2 算符乘法

兩個算符的積定義為：

$$(\hat{A}\hat{B})|\psi\rangle = \hat{A}(\hat{B}|\psi\rangle)$$

算符乘法一般**不可交換**：

$$[\hat{A}, \hat{B}] \equiv \hat{A}\hat{B} - \hat{B}\hat{A} \neq 0$$

這個**對易子**（commutator）在量子力學中極其重要。

### 16.3.3 對易子的性質

對易子滿足以下代數性質：
- **反對稱性**：$[\hat{A}, \hat{B}] = -[\hat{B}, \hat{A}]$
- **線性性**：$[\hat{A}, \hat{B} + \hat{C}] = [\hat{A}, \hat{B}] + [\hat{A}, \hat{C}]$
- **雅可比恆等式**：$[\hat{A}, [\hat{B}, \hat{C}]] + [\hat{B}, [\hat{C}, \hat{A}]] + [\hat{C}, [\hat{A}, \hat{B}]] = 0$

## 16.4 厄米算符

**厄米算符**（Hermitian Operator）是量子力學中最重要的算符類型。

算符 $\hat{A}$ 是厄米算符，若：

$$\hat{A} = \hat{A}^\dagger$$

其中 $\hat{A}^\dagger$ 是 $\hat{A}$ 的**伴隨算符**（adjoint），定義為：

$$\langle\phi|\hat{A}^\dagger|\psi\rangle = \langle\psi|\hat{A}|\phi\rangle^*$$

注意右邊是共軛轉置。

## 16.5 厄米算符的性質

厄米算符具有以下至關重要的性質：

### 16.5.1 本徵值為實數

**定理**：厄米算符的本徵值必為實數。

**證明**：設 $\hat{A}|\psi\rangle = a|\psi\rangle$，其中 $|\psi\rangle \neq 0$。

兩邊左乘 $\langle\psi|$：

$$\langle\psi|\hat{A}|\psi\rangle = a\langle\psi|\psi\rangle$$

取右式的厄米共軛：

$$(\langle\psi|\hat{A}|\psi\rangle)^* = a^*\langle\psi|\psi\rangle$$

但根據厄米性：

$$(\langle\psi|\hat{A}|\psi\rangle)^* = \langle\psi|\hat{A}^\dagger|\psi\rangle = \langle\psi|\hat{A}|\psi\rangle = a\langle\psi|\psi\rangle$$

因此 $a = a^*$，故 $a$ 為實數。

### 16.5.2 本徵態正交

**定理**：厄米算符對應於不同本徵值的本徵態相互正交。

**證明**：設 $\hat{A}|\psi_1\rangle = a_1|\psi_1\rangle$，$\hat{A}|\psi_2\rangle = a_2|\psi_2\rangle$，且 $a_1 \neq a_2$。

第一式左乘 $\langle\psi_2|$：

$$\langle\psi_2|\hat{A}|\psi_1\rangle = a_1\langle\psi_2|\psi_1\rangle$$

第二式左乘 $\langle\psi_1|$ 並取厄米共軛：

$$\langle\psi_1|\hat{A}|\psi_2\rangle = a_2\langle\psi_1|\psi_2\rangle \Rightarrow \langle\psi_2|\hat{A}|\psi_1\rangle = a_2^*\langle\psi_2|\psi_1\rangle$$

由於 $a_2$ 為實數，兩式相減：

$$(a_1 - a_2)\langle\psi_2|\psi_1\rangle = 0$$

因 $a_1 \neq a_2$，故 $\langle\psi_2|\psi_1\rangle = 0$，即兩態正交。

### 16.5.3 構成完整集合

**定理**：厄米算符的本徵態構成希爾伯特空間的完整正交歸一基底。

這意味著任意態可以唯一地展開為本徵態的疊加：

$$|\psi\rangle = \sum_n c_n |a_n\rangle$$

其中 $|a_n\rangle$ 是本徵值 $a_n$ 對應的本徵態。

## 16.6 物理意義

厄米算符的這些性質與物理測量密切相關：

1. **測量結果是實數**：可觀測量的測量結果必為實數，對應於厄米算符的本徵值必為實數
2. **正交態無干擾**：測量得到不同本徵值對應的態相互正交，測量互不干擾
3. **測量必得本徵值**：任意量子態測量可觀測量，必得相應本徵值

## 16.7 么正算符

**么正算符**（Unitary Operator） $\hat{U}$ 滿足：

$$\hat{U}^\dagger \hat{U} = \hat{U}\hat{U}^\dagger = \mathbf{1}$$

么正算符的性質：
1. **保持內積**：$\langle\hat{U}\phi|\hat{U}\psi\rangle = \langle\phi|\psi\rangle$
2. **保持範數**：$\|\hat{U}\psi\| = \|\psi\|$
3. **時間演化算符**：$e^{-i\hat{H}t/\hbar}$ 是么正的

么正算符代表時間演化、空間旋轉、洛倫茲變換等物理變換。

## 16.8 反厄米算符

**反厄米算符**（Anti-Hermitian Operator） $\hat{A}$ 滿足：

$$\hat{A}^\dagger = -\hat{A}$$

反厄米算符的本徵值為純虛數。在量子力學中，某些時間反演算符是反厄米的。

## 16.9 投影算符

**投影算符**（Projection Operator） $\hat{P}$ 滿足：

$$\hat{P}^2 = \hat{P}, \quad \hat{P}^\dagger = \hat{P}$$

投影算符將態向量投影到某個子空間。

若 $\{|e_i\rangle\}$ 是正交歸一基底，則投影到 $|e_i\rangle$ 的算符為：

$$P_i = |e_i\rangle\langle e_i|$$

所有投影算符之和：

$$\sum_i P_i = \mathbf{1}$$

## 16.10 基本算符

在量子力學中，一些基本算符包括：

### 16.10.1 位置算符

$$\hat{x}|x\rangle = x|x\rangle$$

在位置表象中，$\hat{x}$ 就是乘法運算：

$$\hat{x}\psi(x) = x\psi(x)$$

### 16.10.2 動量算符

$$\hat{p}|p\rangle = p|p\rangle$$

在位置表象中：

$$\hat{p} = -i\hbar\frac{\partial}{\partial x}$$

這是量子力學的基本假設之一。

### 16.10.3 哈密頓算符

$$\hat{H} = \frac{\hat{p}^2}{2m} + V(\hat{x})$$

哈密頓算符是系統的總能量算符。

## 16.11 對易關係

對易關係是量子力學的核心。

### 16.11.1 基本對易關係

**位置-動量對易子**：

$$[\hat{x}, \hat{p}] = i\hbar$$

這是量子力學中最基本、最重要的對易關係，是不確定性原理的根源。

### 16.11.2 角動量對易關係

$$[\hat{L}_x, \hat{L}_y] = i\hbar\hat{L}_z, \quad \text{循環}$$

### 16.11.3 升降算符

$$[\hat{a}, \hat{a}^\dagger] = 1$$

## 16.12 算符函數

給定算符 $\hat{A}$，可以定義算符的函數，如 $f(\hat{A})$。

若 $\hat{A}$ 有本徵展開：

$$\hat{A} = \sum_n a_n |n\rangle\langle n|$$

則：

$$f(\hat{A}) = \sum_n f(a_n) |n\rangle\langle n|$$

例如，指數算符 $e^{i\hat{A}t/\hbar}$ 在時間演化中非常重要。

## 16.13 算符的跡

算符 $\hat{A}$ 的**跡**（trace）定義為：

$$\text{Tr}(\hat{A}) = \sum_n \langle n|\hat{A}|n\rangle$$

跡與基底無關。跡的重要性質：
- $\text{Tr}(\hat{A}\hat{B}) = \text{Tr}(\hat{B}\hat{A})$
- $\text{Tr}(|\psi\rangle\langle\phi|) = \langle\phi|\psi\rangle$

## 16.14 對易與可同時測量

若兩個算符 $\hat{A}$ 與 $\hat{B}$ 對易：$[\hat{A}, \hat{B}] = 0$，則它們有共同的本徵態集合，可以同時測量。

若 $[\hat{A}, \hat{B}] \neq 0$，則不能同時精確測量，這是不確定性原理的體現。

## 16.15 算符的冪

算符的冪定義為重複作用：

$$\hat{A}^2|\psi\rangle = \hat{A}(\hat{A}|\psi\rangle)$$

例如：

$$\hat{x}^2\psi(x) = x^2\psi(x)$$

$$\hat{p}^2\psi(x) = -\hbar^2\frac{d^2\psi}{dx^2}$$

## 16.16 算符的指數函數

算符的指數函數通過級數定義：

$$e^{\hat{A}} = \sum_{n=0}^{\infty} \frac{\hat{A}^n}{n!}$$

么正算符可以寫為：

$$\hat{U} = e^{-i\hat{A}}$$

其中 $\hat{A}$ 是厄米算符。

## 16.17 算符等式

一些有用的算符等式：

**貝克豪斯-坎貝爾恆等式**（Baker-Campbell-Hausdorff formula）：

$$e^{\hat{A}}\hat{B}e^{-\hat{A}} = \hat{B} + [\hat{A}, \hat{B}] + \frac{1}{2!}[\hat{A}, [\hat{A}, \hat{B}]] + \cdots$$

這個等式在處理時間演化和微擾論時非常有用。

## 16.18 本章小結

本章我們介紹了量子算符的基本概念。我們討論了線性算符、厄米算符（物理量對應）、么正算符（變換）、投影算符、基本算符（位置、動量、哈密頓）以及重要的對易關係。算符是量子力學數學框架的核心要素。
