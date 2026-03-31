# 第十四章：希爾伯特空間——量子力學的數學舞台

## 14.1 數學與物理的結合

量子力學的強大之處不僅在於它能夠精確預言實驗結果，還在於它具有堅實的數學基礎。這個數學基礎就是**希爾伯特空間**（Hilbert Space）理論。

量子力學中的幾乎所有概念都可以用希爾伯特空間的語言來表述：
- 物理態 ↔ 希爾伯特空間中的向量
- 可觀測量 ↔ 希爾伯特空間中的厄米算符
- 測量結果 ↔ 算符的本徵值

這種抽象的數學框架不僅提供了處理量子問題的強大工具，更重要的是，它揭示了量子力學的內在結構和美。

## 14.2 向量空間的定義

**向量空間**（Vector Space）是線性代數的核心概念。讓我們回顧它的定義。

一個集合 $V$ 稱為（復）向量空間，如果對其中的任意元素（稱為向量）$\mathbf{u}, \mathbf{v}, \mathbf{w}$ 和標量（複數）$a, b$ 滿足以下公理：

**加法公理：**
1. **封閉性**：若 $\mathbf{u}, \mathbf{v} \in V$，則 $\mathbf{u} + \mathbf{v} \in V$
2. **交換律**：$\mathbf{u} + \mathbf{v} = \mathbf{v} + \mathbf{u}$
3. **結合律**：$(\mathbf{u} + \mathbf{v}) + \mathbf{w} = \mathbf{u} + (\mathbf{v} + \mathbf{w})$
4. **零向量存在**：存在 $\mathbf{0} \in V$，使得 $\mathbf{v} + \mathbf{0} = \mathbf{v}$
5. **加法逆元**：對每個 $\mathbf{v}$，存在 $-\mathbf{v}$，使得 $\mathbf{v} + (-\mathbf{v}) = \mathbf{0}$

**標量乘法公理：**
6. **封閉性**：若 $\mathbf{v} \in V$，$c \in \mathbb{C}$，則 $c\mathbf{v} \in V$
7. **結合律**：$a(b\mathbf{v}) = (ab)\mathbf{v}$
8. **單位元**：$1\mathbf{v} = \mathbf{v}$
9. **分配律**：$a(\mathbf{u} + \mathbf{v}) = a\mathbf{u} + a\mathbf{v}$
10. **分配律**：$(a+b)\mathbf{v} = a\mathbf{v} + b\mathbf{v}$

## 14.3 內積空間

**內積空間**（Inner Product Space）是具有內積結構的向量空間。

內積是兩個向量之間的運算，結果是一個複數。對於向量空間 $V$，內積 $\langle \cdot | \cdot \rangle : V \times V \to \mathbb{C}$ 滿足以下公理：

1. **正定性**：對所有 $\mathbf{v} \in V$，$\langle \mathbf{v} | \mathbf{v} \rangle \geq 0$，且等號成立當且僅當 $\mathbf{v} = \mathbf{0}$

2. **共軛對稱性**：對所有 $\mathbf{u}, \mathbf{v} \in V$，$\langle \mathbf{u} | \mathbf{v} \rangle = \langle \mathbf{v} | \mathbf{u} \rangle^*$

3. **線性性**（對第一個因子）：
   - $\langle a\mathbf{u} + b\mathbf{v} | \mathbf{w} \rangle = a\langle \mathbf{u} | \mathbf{w} \rangle + b\langle \mathbf{v} | \mathbf{w} \rangle$
   - $\langle \mathbf{w} | a\mathbf{u} + b\mathbf{v} \rangle = a^*\langle \mathbf{w} | \mathbf{u} \rangle + b^*\langle \mathbf{w} | \mathbf{v} \rangle$

注意內積對第二個因子是共軛線性的，這是量子力學的標準約定。

## 14.4 範數與距離

由內積可以導出**範數**（Norm）的概念。

向量 $\mathbf{v}$ 的範數定義為：

$$\|\mathbf{v}\| = \sqrt{\langle \mathbf{v} | \mathbf{v} \rangle}$$

範數具有以下性質：
1. **非負性**：$\|\mathbf{v}\| \geq 0$，且等號成立當且僅當 $\mathbf{v} = \mathbf{0}$
2. **齊次性**：$\|c\mathbf{v}\| = |c|\|\mathbf{v}\|$
3. **三角不等式**：$\|\mathbf{u} + \mathbf{v}\| \leq \|\mathbf{u}\| + \|\mathbf{v}\|$

兩個向量之間的**距離**定義為：

$$d(\mathbf{u}, \mathbf{v}) = \|\mathbf{u} - \mathbf{v}\|$$

這使內積空間成為一度量空間。

## 14.5 正交性

兩個向量 $\mathbf{u}$ 與 $\mathbf{v}$ 稱為**正交**（orthogonal），若：

$$\langle \mathbf{u} | \mathbf{v} \rangle = 0$$

一個向量集合 $\{|\mathbf{v}_i\rangle\}$ 是**正交的**，若 $i \neq j$ 時 $\langle \mathbf{v}_i | \mathbf{v}_j \rangle = 0$。

若每個向量的範數為1，則稱為**正交歸一**（orthonormal）：

$$\langle \mathbf{v}_i | \mathbf{v}_j \rangle = \delta_{ij}$$

其中 $\delta_{ij}$ 是克羅內克δ符號。

## 14.6 正交化過程

任何有限維內積空間都存在正交歸一基底。通過**施密特正交化**（Gram-Schmidt orthogonalization）過程，可以從任意線性無關集合構造正交歸一基底。

施密特正交化步驟：
1. 令 $\mathbf{u}_1 = \mathbf{v}_1$
2. 令 $\mathbf{u}_2 = \mathbf{v}_2 - \frac{\langle \mathbf{u}_1 | \mathbf{v}_2 \rangle}{\langle \mathbf{u}_1 | \mathbf{u}_1 \rangle} \mathbf{u}_1$
3. 令 $\mathbf{u}_3 = \mathbf{v}_3 - \frac{\langle \mathbf{u}_1 | \mathbf{v}_3 \rangle}{\langle \mathbf{u}_1 | \mathbf{u}_1 \rangle} \mathbf{u}_1 - \frac{\langle \mathbf{u}_2 | \mathbf{v}_3 \rangle}{\langle \mathbf{u}_2 | \mathbf{u}_2 \rangle} \mathbf{u}_2$

然後歸一化每個向量。

## 14.7 希爾伯特空間的定義

**希爾伯特空間**（Hilbert Space）是一個**完整的**內積空間。

完整性意味著：任何柯西序列都收斂到空間內的一個元素。

什麼是柯西序列？序列 $\{|\psi_n\rangle\}$ 是柯西序列，若對任意 $\epsilon > 0$，存在 $N$ 使得對所有 $m, n > N$，都有 $\|\psi_m - \psi_n\| < \epsilon$。

完整性的要求保証了極限操作的有效性，這在量子力學的計算中非常重要。

## 14.8 有限維與無限維希爾伯特空間

在量子力學中，實際使用的希爾伯特空間有兩種類型：

**有限維空間：**
- 例如，自旋-1/2 系統的希爾伯特空間是二維的
- 所有運算都可以用有限維矩陣表示
- 數學上比較簡單

**無限維空間：**
- 例如，單粒子位置空間的希爾伯特空間是無窮維的
- 需要更謹慎的數學處理
- 例如，位置本徵態 Dirac δ函數不是真正的平方可積函數

## 14.9 可分希爾伯特空間

量子力學中使用的希爾伯特空間通常是**可分的**（separable）。

可分意味著存在一個可數稠密集。換句話說，空間中任何向量都可以用可數基底逼近。

這保証了我們可以用可數的基向量來表示任何物理態。

## 14.10 維度與基底

向量空間的**維度**是線性無關向量的最大數目。

若維度為 $n$，則任何 $n$ 個線性無關的向量構成一組**基底**（basis）。任何向量可以唯一地寫成基底的線性組合：

$$|\psi\rangle = \sum_{i=1}^n c_i|e_i\rangle$$

其中 $c_i = \langle e_i|\psi\rangle$ 是分量（坐標）。

## 14.11 連續基底

對於連續維度的希爾伯特空間（如位置空間），基底是連續的。

位置基底 $\{|x\rangle\}$ 滿足連續的正交歸一關係：

$$\langle x|x'\rangle = \delta(x - x')$$

任意態的波函數：

$$|\psi\rangle = \int \psi(x) |x\rangle dx$$

其中 $\psi(x) = \langle x|\psi\rangle$ 是波函數。

這裡的積分理解為Lebesgue積分或Riemann積分。

## 14.12 希爾伯特空間的直和

若 $V$ 與 $W$ 是兩個希爾伯特空間，則 $V \oplus W$ 包含形如 $(\mathbf{v}, \mathbf{w})$ 的向量，維度為 $\dim V + \dim W$。

直和對應於複合系統中各部分不糾纏的情況。

## 14.13 希爾伯特空間的張量積

兩個希爾伯特空間的**張量積** $V \otimes W$ 是另一種重要的組合方式。

張量積用於描述多粒子系統。

例如，兩個 qubit 的張量積空間是 $2 \times 2 = 4$ 維的。

張量積空間中的向量可以寫為：

$$|\psi\rangle = \sum_{i,j} c_{ij} |v_i\rangle \otimes |w_j\rangle$$

## 14.14 希爾伯特空間的典型例子

讓我們看一些典型的希爾伯特空間例子：

**例子1：$\mathbb{C}^n$**
- $n$ 維復向量空間
- 內積：$\langle \mathbf{u} | \mathbf{v} \rangle = \sum_i u_i^* v_i$
- 例如，單 qubit 的狀態空間

**例子2：$L^2(\mathbb{R})$**
- 平方可積函數空間
- 內積：$\langle f | g \rangle = \int_{-\infty}^{\infty} f^*(x) g(x) dx$
- 例如，單粒子位置空間

**例子3：$\ell^2$**
- 平方可和序列空間
- 內積：$\langle \{a_n\} | \{b_n\} \rangle = \sum_n a_n^* b_n$
- 例如，諧振子的數態空間

## 14.15 里斯-菲舍爾定理

**里斯-菲舍爾定理**（Riesz-Fischer Theorem）是連接連續基底和離散基底的橋樑。

這個定理表明，$L^2$ 空間中的任何正交歸一序列都可以用來定義一組基向量，任何函數都可以展開為這些基向量的疊加。

這保証了我們可以用離散的諧振子數態或連續的位置基底來表示任何量子態。

## 14.16 希爾伯特空間與量子力學

現在我們可以看到希爾伯特空間如何為量子力學提供數學框架：

**物理態 ↔ 希爾伯特空間中的單位向量**
- 態向量 $|\psi\rangle$ 必須歸一化：$\langle\psi|\psi\rangle = 1$
- 疊加原理：線性組合仍是物理態

**可觀測量 ↔ 希爾伯特空間中的厄米算符**
- 厄米算符的本徵值是實數
- 本徵向量構成正交歸一基底

**測量結果 ↔ 算符的本徵值**
- 測量得到本徵值
- 測量後態坍縮到本徵態

## 14.17 希爾伯特空間的公理化

量子力學的公理化表述基於希爾伯特空間。讓我們陳述這些公理：

**公理1（態）**：封閉系統的狀態由希爾伯特空間中的單位向量描述。

**公理2（可觀測量）**：可觀測量由希爾伯特空間中的厄米算符描述。

**公理3（測量）**：測量可觀測量得到其本徵值，測量到本徵值 $a$ 的概率為 $|\langle a|\psi\rangle|^2$。

**公理4（演化）**：封閉系統的時間演化由薛丁格方程式描述。

## 14.18 希爾伯特空間的限制

希爾伯特空間框架也有其局限性：

1. **並非所有數學對象都有物理意義**：例如，Dirac δ函數不是 $L^2$ 函數，需要引入「廣義函數」概念

2. **連續譜的處理**：連續譜本徵態需要特殊的數學處理

3. **無界算符**：物理算符（如位置和動量）是無界的，這帶來數學上的困難

## 14.19 本章小結

本章我們介紹了希爾伯特空間的基本概念。希爾伯特空間是具有內積結構的完整向量空間，是量子力學的數學基礎。我們討論了向量空間、內積、範數、正交性、維度與基底、連續基底、張量積等概念，以及希爾伯特空間如何為量子力學提供數學框架。這些數學工具對於理解量子力學的理論結構至關重要。
