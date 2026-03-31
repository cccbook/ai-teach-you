# 第二十九章：角動量耦合

## 29.1 角動量耦合問題

當系統包含多個角動量時（如兩個電子或多個粒子），需要將它們的角動量「耦合」成總角動量。

問題：給定兩個角動量 $\mathbf{j}_1$ 與 $\mathbf{j}_2$，求總角動量 $\mathbf{J} = \mathbf{j}_1 + \mathbf{j}_2$ 的本徵值與本徵態。

## 29.2 耦合與未耦合基底

**未耦合基底**（Uncoupled Basis）：

$$|j_1, m_1\rangle \otimes |j_2, m_2\rangle \equiv |j_1, m_1; j_2, m_2\rangle$$

維度：$(2j_1+1)(2j_2+1)$

**耦合基底**（Coupled Basis）：

$$|J, M\rangle$$

其中 $J$ 是總角動量量子數，$M$ 是總角動量 $z$ 分量。

## 29.3 Clebsch-Gordan 係數

未耦合基底與耦合基底之間的轉換由**Clebsch-Gordan係數**（CG係數）給出：

$$|J, M\rangle = \sum_{m_1, m_2} |j_1, m_1; j_2, m_2\rangle \langle j_1, m_1; j_2, m_2 | J, M\rangle$$

CG係數滿足：
- 選擇定則：$m_1 + m_2 = M$
- $J$ 的取值：$|j_1 - j_2| \leq J \leq j_1 + j_2$

## 29.4 三角條件

兩個角動量耦合時，總角動量 $J$ 的取值滿足**三角條件**：

$$|j_1 - j_2| \leq J \leq j_1 + j_2$$

且 $J$ 為整數或半整數（與 $j_1 + j_2$ 相同）。

例如：
- $j_1 = 1/2$，$j_2 = 1/2$：$J = 0, 1$
- $j_1 = 1$，$j_2 = 1/2$：$J = 1/2, 3/2$

## 29.5 CG係數的計算

CG係數有解析表達式，可以通過遞推關係或查表計算。

更實用的是使用Wigner 3j符號。

## 29.6 Wigner 3j 符號

**Wigner 3j 符號**是CG係數的更對稱形式：

$$\begin{pmatrix} j_1 & j_2 & J \\ m_1 & m_2 & -M \end{pmatrix} = \frac{1}{\sqrt{2J+1}} \langle j_1 m_1; j_2 m_2 | J, -M \rangle$$

3j 符號有簡單的對稱性質，在角動量耦合計算中非常有用。

## 29.7 例子：兩個自旋-1/2

兩個自旋-1/2 粒子：
- 未耦合基底：$|\uparrow\uparrow\rangle, |\uparrow\downarrow\rangle, |\downarrow\uparrow\rangle, |\downarrow\downarrow\rangle$
- 耦合基底：$|J=1, M=1\rangle, |J=1, M=0\rangle, |J=1, M=-1\rangle, |J=0, M=0\rangle$

轉換關係：
- $|1, 1\rangle = |\uparrow\uparrow\rangle$
- $|1, 0\rangle = \frac{1}{\sqrt{2}}(|\uparrow\downarrow\rangle + |\downarrow\uparrow\rangle)$
- $|1, -1\rangle = |\downarrow\downarrow\rangle$
- $|0, 0\rangle = \frac{1}{\sqrt{2}}(|\uparrow\downarrow\rangle - |\downarrow\uparrow\rangle)$

注意：$|0, 0\rangle$ 是反對稱的**單重態**，$|1, M\rangle$ 是對稱的三重態。

## 29.8 角動量耦合的應用

角動量耦合在以下領域有重要應用：

1. **原子光譜**： LS耦合、jj耦合
2. **核物理**： 核殼層模型
3. **分子物理**： 轉動-振動耦合
4. **粒子物理**： 強子的夸克模型

## 29.9 本章小結

本章我們討論了角動量耦合。我們介紹了未耦合與耦合基底、Clebsch-Gordan係數與三角條件，並給出了兩個自旋-1/2 耦合為單重態與三重態的例子。CG係數是處理多角動量系統的關鍵工具。
