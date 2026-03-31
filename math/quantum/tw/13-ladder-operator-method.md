# 第十三章：階梯算符方法——代數求解的優美技巧

## 13.1 階梯算符方法的起源

上一章我們用微分方程法求解了量子諧振子。本章我們介紹另一種更加優美和強大的方法——**階梯算符方法**，也稱為**升降算符方法**或**產生湮滅算符方法**。

這個方法由保羅·狄拉克（Paul Dirac）開創，是量子力學中最優雅的數學技巧之一。這個方法不僅可以用來求解諧振子，還可以推廣到角動量理論、量子場論等領域。

## 13.2 升降算符的定義

考慮量子諧振子。定義兩個算符：

$$\hat{a} = \sqrt{\frac{m\omega}{2\hbar}}\left(x + \frac{i\hat{p}}{m\omega}\right) = \sqrt{\frac{m\omega}{2\hbar}}\left(x + \frac{\hbar}{m\omega}\frac{d}{dx}\right)$$

$$\hat{a}^\dagger = \sqrt{\frac{m\omega}{2\hbar}}\left(x - \frac{i\hat{p}}{m\omega}\right) = \sqrt{\frac{m\omega}{2\hbar}}\left(x - \frac{\hbar}{m\omega}\frac{d}{dx}\right)$$

其中 $\hat{p} = -i\hbar\frac{d}{dx}$ 是動量算符，$\hat{a}^\dagger$ 是 $\hat{a}$ 的厄米共軛。

注意這兩個算符的定義非常巧妙：它們將位置和動量算符以特定的方式組合起來。

## 13.3 升降算符的物理意義

升降算符的命名來自它們的作用：

- $\hat{a}^\dagger$ 稱為**升算符**或**產生算符**，因為它作用於本徵態時會將系統「升」到更高能量的態
- $\hat{a}$ 稱為**降算符**或**湮滅算符**，因為它作用於本徵態時會將系統「降」到更低能量的態

在量子場論中，$\hat{a}^\dagger$ 和 $\hat{a}$ 分別稱為產生算符和湮滅算符，因為它們產生和湮滅場的量子（如光子）。

## 13.4 對易關係

讓我們計算升降算符的對易關係。

首先計算 $\hat{a}$ 和 $\hat{a}^\dagger$ 的乘積：

$$\hat{a}^\dagger\hat{a} = \frac{m\omega}{2\hbar}\left(x - \frac{i\hat{p}}{m\omega}\right)\left(x + \frac{i\hat{p}}{m\omega}\right)$$

展開：

$$= \frac{m\omega}{2\hbar}\left[x^2 + \frac{ix\hat{p}}{m\omega} - \frac{i\hat{p}x}{m\omega} + \frac{\hat{p}^2}{m^2\omega^2}\right]$$

$$= \frac{m\omega}{2\hbar}\left[x^2 + \frac{\hat{p}^2}{m^2\omega^2} + \frac{i}{m\omega}(x\hat{p} - \hat{p}x)\right]$$

利用對易關係 $[x, \hat{p}] = i\hbar$，即 $x\hat{p} - \hat{p}x = i\hbar$，我們得到：

$$\hat{a}^\dagger\hat{a} = \frac{m\omega}{2\hbar}\left[x^2 + \frac{\hat{p}^2}{m^2\omega^2} - \frac{1}{m\omega}\hbar\right]$$

$$= \frac{1}{2\hbar}\left[\frac{\hat{p}^2}{m\omega} + m\omega x^2 - \hbar\right]$$

類似地，計算 $\hat{a}\hat{a}^\dagger$：

$$\hat{a}\hat{a}^\dagger = \frac{m\omega}{2\hbar}\left(x + \frac{i\hat{p}}{m\omega}\right)\left(x - \frac{i\hat{p}}{m\omega}\right)$$

$$= \frac{1}{2\hbar}\left[\frac{\hat{p}^2}{m\omega} + m\omega x^2 + \hbar\right]$$

## 13.5 核心對易關係

由以上結果，我們得到核心對易關係：

$$[\hat{a}, \hat{a}^\dagger] = \hat{a}\hat{a}^\dagger - \hat{a}^\dagger\hat{a} = 1$$

這個對易關係極其簡單，是諧振子代數的基礎。

由這個對易關係，我們可以定義**粒子數算符**（也稱為**占有數算符**）：

$$\hat{N} = \hat{a}^\dagger\hat{a}$$

## 13.6 哈密頓算符的代數表示

現在讓我們用升降算符來表示哈密頓算符。

由前面的計算：

$$\hat{a}^\dagger\hat{a} = \frac{1}{2\hbar}\left[\frac{\hat{p}^2}{m\omega} + m\omega x^2 - \hbar\right]$$

因此：

$$\hat{H} = \frac{\hat{p}^2}{2m} + \frac{1}{2}m\omega^2 x^2 = \hbar\omega\left(\hat{a}^\dagger\hat{a} + \frac{1}{2}\right) = \hbar\omega\left(\hat{N} + \frac{1}{2}\right)$$

這個結果極其簡潔！哈密頓算符只是粒子數算符的簡單函數。

## 13.7 本徵值問題的代數求解

現在讓我們利用對易關係來求解本徵值問題。

設 $|\psi\rangle$ 是 $\hat{N}$ 的本徵態，本徵值為 $n$：

$$\hat{N}|\psi\rangle = n|\psi\rangle$$

那麼：

$$\hat{H}|\psi\rangle = \hbar\omega\left(n + \frac{1}{2}\right)|\psi\rangle$$

因此能量本徵值為：

$$E_n = \hbar\omega\left(n + \frac{1}{2}\right)$$

這與微分方程法的結果完全一致！

現在我們需要證明 $n$ 只能是非負整數。

## 13.8 本徵值譜的確定

讓我們研究升降算符對本徵態的作用。

### 13.8.1 升算符的作用

計算 $\hat{N}$ 作用於 $\hat{a}^\dagger|\psi\rangle$：

$$\hat{N}(\hat{a}^\dagger|\psi\rangle) = \hat{a}^\dagger\hat{a}\hat{a}^\dagger|\psi\rangle = \hat{a}^\dagger(\hat{a}^\dagger\hat{a} + 1)|\psi\rangle$$

利用對易關係 $[\hat{a}, \hat{a}^\dagger] = 1$，即 $\hat{a}\hat{a}^\dagger = \hat{a}^\dagger\hat{a} + 1$，我們得到：

$$\hat{N}(\hat{a}^\dagger|\psi\rangle) = \hat{a}^\dagger(\hat{N} + 1)|\psi\rangle = (n + 1)\hat{a}^\dagger|\psi\rangle$$

因此，$\hat{a}^\dagger|\psi\rangle$ 是 $\hat{N}$ 的本徵態，本徵值為 $n + 1$！

這就是為什麼 $\hat{a}^\dagger$ 稱為升算符——它將本徵值增加1。

### 13.8.2 降算符的作用

類似地，計算 $\hat{N}$ 作用於 $\hat{a}|\psi\rangle$：

$$\hat{N}(\hat{a}|\psi\rangle) = \hat{a}^\dagger\hat{a}\hat{a}|\psi\rangle = \hat{a}(\hat{a}^\dagger\hat{a} - 1)|\psi\rangle$$

利用對易關係 $[\hat{a}, \hat{a}^\dagger] = 1$，即 $\hat{a}^\dagger\hat{a} = \hat{a}\hat{a}^\dagger - 1$，我們得到：

$$\hat{N}(\hat{a}|\psi\rangle) = \hat{a}(\hat{N} - 1)|\psi\rangle = (n - 1)\hat{a}|\psi\rangle$$

因此，$\hat{a}|\psi\rangle$ 是 $\hat{N}$ 的本徵態，本徵值為 $n - 1$！

這就是為什麼 $\hat{a}$ 稱為降算符——它將本徵值減少1。

## 13.9 粒子數的下界

升降算符的特點是它們改變本徵值。讓我們看看會發生什麼。

假設 $|\psi\rangle$ 是 $\hat{N}$ 的本徵態，本徵值為 $n$。

如果我們反覆作用 $\hat{a}$，會得到一系列態：

$$|\psi\rangle, \hat{a}|\psi\rangle, \hat{a}^2|\psi\rangle, \ldots$$

它們的本徵值分別為 $n, n-1, n-2, \ldots$

這個過程不能無限期繼續。為什麼？

## 13.10 本徵值的非負性

粒子數算符 $\hat{N} = \hat{a}^\dagger\hat{a}$ 是**正算符**。

對於任何態 $|\phi\rangle$：

$$\langle\phi|\hat{N}|\phi\rangle = \langle\phi|\hat{a}^\dagger\hat{a}|\phi\rangle = \|\hat{a}|\phi\rangle\|^2 \geq 0$$

因此，$\hat{N}$ 的本徵值 $n$ 必須是非負的：$n \geq 0$。

## 13.11 粒子數的整數性

現在我們知道 $n \geq 0$。但 $n$ 必須是整數。

設 $n$ 不是整數。則 $n, n-1, n-2, \ldots$ 可以一直減下去，直到變成負數——但這是不可能的，因為本徵值必須非負。

因此，減法過程必須在某個非負整數處終止。

設 $n_0$ 是最小的本徵值。如果 $n_0$ 不是零，則 $n_0 - 1$ 也是一個本徵值，與 $n_0$ 的最小性矛盾。

因此，$n_0 = 0$。

由升降算符的作用，我們得到 $n$ 可以是 $0, 1, 2, 3, \ldots$ 所有非負整數！

## 13.12 基態的存在

讓我們找出基態。

基態 $|0\rangle$ 滿足：

$$\hat{a}|0\rangle = 0$$

這是升降算符語言中的「消滅條件」。

在位置表象中：

$$\hat{a}|0\rangle = 0 \Rightarrow \sqrt{\frac{m\omega}{2\hbar}}\left(x + \frac{\hbar}{m\omega}\frac{d}{dx}\right)\psi_0(x) = 0$$

整理得：

$$\frac{d\psi_0}{dx} = -\frac{m\omega}{\hbar}x\psi_0$$

積分得到：

$$\psi_0(x) = N_0 e^{-\frac{m\omega x^2}{2\hbar}}$$

其中 $N_0$ 是歸一化常數。

這正是量子諧振子的基態波函數！

## 13.13 數態表示

現在我們可以生成所有激發態。

由升降算符的作用：

$$\hat{a}^\dagger|0\rangle = \sqrt{1}|1\rangle$$
$$\hat{a}^\dagger|1\rangle = \sqrt{2}|2\rangle$$
$$\hat{a}^\dagger|2\rangle = \sqrt{3}|3\rangle$$

一般地：

$$|n\rangle = \frac{(\hat{a}^\dagger)^n}{\sqrt{n!}}|0\rangle$$

這些態 $|n\rangle$ 構成一組正交歸一基底，稱為**數態**或**占有數態**。

## 13.14 升降算符的矩陣表示

在數態基底 $\{|n\rangle\}$ 中，升降算符的矩陣表示非常簡單：

$$\hat{a} = \begin{pmatrix}
0 & \sqrt{1} & 0 & 0 & \cdots \\
0 & 0 & \sqrt{2} & 0 & \cdots \\
0 & 0 & 0 & \sqrt{3} & \cdots \\
\vdots & \vdots & \vdots & \vdots & \ddots
\end{pmatrix}$$

$$\hat{a}^\dagger = \begin{pmatrix}
0 & 0 & 0 & 0 & \cdots \\
\sqrt{1} & 0 & 0 & 0 & \cdots \\
0 & \sqrt{2} & 0 & 0 & \cdots \\
0 & 0 & \sqrt{3} & 0 & \cdots \\
\vdots & \vdots & \vdots & \vdots & \ddots
\end{pmatrix}$$

$$\hat{N} = \text{diag}(0, 1, 2, 3, \ldots)$$

這些矩陣形式對於實際計算非常有用。

## 13.15 相干態

**相干態**（Coherent State）是升降算符的本徵態：

$$\hat{a}|\alpha\rangle = \alpha|\alpha\rangle$$

其中 $\alpha$ 是任意複數。

相干態可以展開為數態：

$$|\alpha\rangle = e^{-|\alpha|^2/2} \sum_{n=0}^{\infty} \frac{\alpha^n}{\sqrt{n!}}|n\rangle$$

相干態在量子光學中有重要應用，描述雷射場。

## 13.16 與微分方程法的比較

代數法的優點：
1. 避免了繁瑣的微分方程求解
2. 物理圖像清晰（升降算符）
3. 易於推廣到其他系統
4. 便於計算期望值和矩陣元

微分方程法的優點：
1. 可以直接得到波函數的顯式表達
2. 適合處理邊界條件複雜的問題
3. 便於理解波函數的漸近行為

兩種方法是互補的。

## 13.17 方法的推廣

升降算符方法可以推廣到許多其他問題。

### 13.17.1 角動量理論

角動量升降算符 $J_\pm = J_x \pm iJ_y$ 滿足對易關係：

$$[J_z, J_\pm] = \pm\hbar J_\pm$$

這與諧振子的升降算符對易關係形式相同！

### 13.17.2 超對稱量子力學

超對稱量子力學利用與諧振子代數類似的結構來研究量子系統的性質。

### 13.17.3 量子場論

在量子場論中，場的激發被量子化為粒子。產生和湮滅算符正是升降算符的推廣。

## 13.18 本章小結

本章我們介紹了升降算符方法。我們定義了諧振子的升降算符，發現它們滿足簡單的對易關係 $[\hat{a}, \hat{a}^\dagger] = 1$。利用這個對易關係，我們推導出能量本徵值 $E_n = \hbar\omega(n + 1/2)$，並找到了基態條件 $\hat{a}|0\rangle = 0$。我們還介紹了數態表示和相干態。升降算符方法是量子力學中最優雅的數學技巧之一，在角動量理論和量子場論中有重要推廣應用。
