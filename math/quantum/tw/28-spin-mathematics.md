# 第二十八章：自旋數學

## 28.1 自旋-1/2 系統

自旋-1/2 是最簡單的自旋系統，如電子、質子或中子。自旋算符 $\hat{\mathbf{S}}$ 滿足與軌道角動量相同的對易關係：

$$[\hat{S}_x, \hat{S}_y] = i\hbar\hat{S}_z, \quad \text{循環}$$

自旋平方算符 $\hat{S}^2$ 與 $\hat{S}_z$ 的共同本徵態記為 $|s, m_s\rangle$，其中：

- $s = 1/2$
- $m_s = +1/2$（自旋向上）或 $-1/2$（自旋向下）

## 28.2 泡利矩陣

自旋-1/2 算符可以用**泡利矩陣**（Pauli Matrices）表示：

$$\hat{S}_x = \frac{\hbar}{2} \sigma_x, \quad \hat{S}_y = \frac{\hbar}{2} \sigma_y, \quad \hat{S}_z = \frac{\hbar}{2} \sigma_z$$

泡利矩陣：

$$\sigma_x = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$$

$$\sigma_y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}$$

$$\sigma_z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$$

## 28.3 泡利矩陣的性質

泡利矩陣具有重要的代數性質：

1. **平方為單位矩陣**：$\sigma_i^2 = \mathbf{1}$
2. **對易關係**：$[\sigma_i, \sigma_j] = 2i\varepsilon_{ijk}\sigma_k$
3. **反對易關係**：$\{\sigma_i, \sigma_j\} = 2\delta_{ij}\mathbf{1}$
4. **行列式與 trace**：$\det(\sigma_i) = -1$，$\text{Tr}(\sigma_i) = 0$

泡利矩陣是自旋數學的核心工具。

## 28.4 自旋本徵態

$\hat{S}_z$ 的本徵態（標準基底）：

$$|+\rangle_z = \begin{pmatrix} 1 \\ 0 \end{pmatrix}, \quad |-\rangle_z = \begin{pmatrix} 0 \\ 1 \end{pmatrix}$$

本徵值：$S_z = \pm \hbar/2$

$\hat{S}_x$ 的本徵態：

$$|+\rangle_x = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ 1 \end{pmatrix}, \quad |-\rangle_x = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ -1 \end{pmatrix}$$

$\hat{S}_y$ 的本徵態：

$$|+\rangle_y = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ i \end{pmatrix}, \quad |-\rangle_y = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ -i \end{pmatrix}$$

## 28.5 旋量

自旋-1/2 粒子的波函數是**旋量**（Spinor）：

$$\chi = \begin{pmatrix} \chi_+ \\ \chi_- \end{pmatrix} = \begin{pmatrix} \langle + |\psi\rangle \\ \langle - |\psi\rangle \end{pmatrix}$$

旋量在旋轉下按照特定的表示變換，這是它與普通向量（一維張量）的根本區別。

## 28.6 自旋的測量

在任意方向 $\mathbf{n}$ 上的自旋分量：

$$\hat{S}_n = \mathbf{S} \cdot \mathbf{n} = \frac{\hbar}{2}(\sigma_x n_x + \sigma_y n_y + \sigma_z n_z)$$

測量結果為 $\pm \hbar/2$。本徵態由泡利矩陣的本徵值問題決定。

## 28.7 自旋空間

自旋態構成一個二維希爾伯特空間。任意自旋態可以寫為：

$$|\psi\rangle = \cos(\theta/2)|+\rangle_z + e^{i\phi}\sin(\theta/2)|-\rangle_z$$

這類似於Bloch球上的點，參數 $\theta$ 與 $\phi$ 是球坐標。

## 28.8 自旋與泡利矩陣的應用

泡利矩陣在物理學中到處出現：

1. **量子力學**：自旋算符的表示
2. **量子場論**：狄拉克方程中的 $\gamma$ 矩陣
3. **固態物理**：電子自旋與磁性
4. **量子資訊**：量子位元的表示

## 28.9 本章小結

本章我們討論了自旋-1/2 系統的數學描述。自旋算符可以用泡利矩陣表示，泡利矩陣具有重要的代數性質。自旋本徵態構成二維希爾伯特空間，任意自旋態可以在Bloch球上表示。旋量是自旋-1/2 粒子的波函數形式。泡利矩陣是物理學中最重要的數學工具之一。
