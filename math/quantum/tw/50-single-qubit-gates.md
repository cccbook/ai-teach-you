# 第五十章：單量子位元門

## 50.1 單量子位元門的基礎

單量子位元門是作用於單個量子位元的量子邏輯閘。它們是量子計算的基本構建模塊，與雙量子位元門共同構成完整的量子計算基礎。

單量子位元門的數學本質是 $SU(2)$ 群的元素——即 $2 \times 2$ 的么正矩陣（行列式為1）。這是因為單量子位元的希爾伯特空間是二維的。

單量子位元門的通用性：由於 $SU(2)$ 是一個三參數家族，任意單量子位元門都可以分解為三個旋轉的組合：
$$U(\theta, \phi, \lambda) = R_z(\phi) R_y(\theta) R_z(\lambda)$$

這意味著任意單量子位元操作都可以用旋轉門 $R_z$ 和 $R_y$ 來實現。

## 50.2 Pauli 矩陣和 Pauli 門

Pauli 矩陣是單量子位元門的基礎：
$$\sigma_x = X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}, \quad \sigma_y = Y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}, \quad \sigma_z = Z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$$

**X 門（NOT 門）**：
- 翻轉量子位元：$|0\rangle \to |1\rangle$，$|1\rangle \to |0\rangle$
- 在布洛赫球上繞 x 軸旋轉 $\pi$

**Y 門**：
- 效果：$|0\rangle \to i|1\rangle$，$|1\rangle \to -i|0\rangle$
- 在布洛赫球上繞 y 軸旋轉 $\pi$

**Z 門**：
- 效果：$|0\rangle \to |0\rangle$，$|1\rangle \to -|1\rangle$
- 在布洛赫球上繞 z 軸旋轉 $\pi$
- 不改變計算基測量的概率，只改變相位

## 50.3 Hadamard 門

Hadamard 門是量子計算中最重要的單量子位元門之一：
$$H = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$$

**作用效果**：
- $H|0\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}} = |+\rangle$
- $H|1\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}} = |-\rangle$
- $H|+\rangle = |0\rangle$
- $H|-\rangle = |1\rangle$

**布洛赫球解釋**：
- 將 z 軸極點（$|0\rangle$ 或 $|1\rangle$）映射到赤道平面
- 實現疊加態的創建

**應用**：
- 創建均等疊加態
- 在不同測量基之間轉換
- 量子平行性的基礎

## 50.4 相位門

相位門（Phase Gate）對量子位元施加相對相位：
$$S = \begin{pmatrix} 1 & 0 \\ 0 & i \end{pmatrix} = P(\pi/2)$$

**作用效果**：
- $S|0\rangle = |0\rangle$
- $S|1\rangle = i|1\rangle$
- $S|+\rangle = \frac{|0\rangle + i|1\rangle}{\sqrt{2}}$
- $S|-\rangle = \frac{|0\rangle - i|1\rangle}{\sqrt{2}}$

**T 門（T Gate）**：
$$T = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\pi/4} \end{pmatrix} = P(\pi/4)$$

T 門是非 Clifford 門的代表，是通用量子計算不可或缺的資源。

**S 門和 T 門的關係**：
- $S = T^2$
- $Z = S^2$

## 50.5 旋轉門

旋轉門實現布洛赫球上的連續旋轉：

**繞 x 軸旋轉 $R_x(\theta)$**：
$$R_x(\theta) = e^{-i\theta X/2} = \begin{pmatrix} \cos(\theta/2) & -i\sin(\theta/2) \\ -i\sin(\theta/2) & \cos(\theta/2) \end{pmatrix}$$

**繞 y 軸旋轉 $R_y(\theta)$**：
$$R_y(\theta) = e^{-i\theta Y/2} = \begin{pmatrix} \cos(\theta/2) & -\sin(\theta/2) \\ \sin(\theta/2) & \cos(\theta/2) \end{pmatrix}$$

**繞 z 軸旋轉 $R_z(\theta)$**：
$$R_z(\theta) = e^{-i\theta Z/2} = \begin{pmatrix} e^{-i\theta/2} & 0 \\ 0 & e^{i\theta/2} \end{pmatrix}$$

旋轉門是連續參數化的，提供了精細控制量子態的能力。

## 50.6 Clifford 群

Clifford 群是量子計算中非常重要的門集合：
$$C = \{U : U P U^\dagger \in \{I, X, Y, Z\} \text{ for all } P \in \{I, X, Y, Z\}\}$$

Clifford 群包括：
- Pauli 門：I, X, Y, Z
- Hadamard：H
- 相位：S (= P = Z/2)
- CNOT：CNOT

Clifford 群在容錯量子計算中有特殊地位：
- 可以用 stabilizer 形式高效模擬
- 門可以在 stabilizer 框架內實現容錯

## 50.7 非 Clifford 門

非 Clifford 門是 Clifford 群之外的門，它們不能從 Clifford 門高效模擬。

**T 門**是最重要的非 Clifford 門：
$$T = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\pi/4} \end{pmatrix}$$

**Toffoli 門**（CCNOT）也是非 Clifford 門。

非 Clifford 門的意義：
- 與 Clifford 門結合可以實現通用量子計算
- 是量子計算資源的主要消耗者
- 容錯實現需要魔術態蒸餾

## 50.8 單量子位元門的物理實現

單量子位元門可以通過多種物理機制實現：

**超導量子位元**：
- 用微波脈衝驅動
- 旋轉布洛赫球
- 門時間：10-100 ns

**離子阱**：
- 用雷射脈衝驅動
-  Raman 躍遷
- 門時間：微秒級

**量子點**：
- 用電場脈衝
- 自旋旋轉
- 門時間：皮秒到納秒

## 50.9 門保真度

門保真度是衡量量子門質量的關鍵指標。

**定義**：門保真度 $F$ 是實際門操作與理想門操作之間的相似度：
$$F = \langle \psi | U^\dagger \tilde{U} | \psi \rangle \text{ 平均 over } |\psi\rangle$$

**典型值**：
- 單量子位元門：> 99.9%
- 雙量子位元門：> 99%

**影響因素**：
- 控制噪聲
- 去相干
- 門校準誤差

## 50.10 門分解

任意單量子位元門都可以用基本門分解。

**Z-Y 分解**：任意 $U \in U(2)$ 可以分解為：
$$U = e^{i\alpha} R_z(\beta) R_y(\gamma) R_z(\delta)$$

**H-S-T 分解**：
$$U = H S H \cdot R_z(\theta) \cdot H S H$$

分解的目標是：
- 最小化門數量
- 適配硬體約束

## 50.11 單量子位元門的校準

單量子位元門需要仔細校準。

**方法**：
- 量子過程層析
- 隨機基準測試
- 機器學習優化

**校準參數**：
- 門幅度
- 門相位
- 門持續時間

自動校準是量子計算的重要技術。

## 50.12 本章小結

本章我們系統介紹了單量子位元門。

Pauli 門（X、Y、Z）提供基本的位翻轉和相位翻轉操作。Hadamard 門創建疊加態，是量子平行性的基礎。相位門（S、T）和旋轉門（$R_x$、$R_y$、$R_z$）提供精細控制。

Clifford 群（包括 Pauli、H、S、CNOT）可以高效模擬和容錯實現。非 Clifford 門（如 T）則是通用量子計算所需的資源。

單量子位元門的物理實現有多種技術，門保真度是關鍵性能指標。
