# 第二十五章：經典角動量

## 25.1 經典角動量的定義

在經典力學中，**角動量**（Angular Momentum）是描述物體旋轉運動的重要物理量。

對於質量為 $m$ 、位置為 $\mathbf{r}$ 、動量為 $\mathbf{p}$ 的粒子，其角動量定義為：

$$\mathbf{L} = \mathbf{r} \times \mathbf{p} = \mathbf{r} \times m\mathbf{v}$$

寫成分量形式：

$$L_x = y p_z - z p_y$$
$$L_y = z p_x - x p_z$$
$$L_z = x p_y - y p_x$$

## 25.2 角動量的物理意義

角動量是與旋轉運動相關的守恆量：

1. **轉動慣量**：$I = mr^2$（對於質點繞原點旋轉）
2. **角速度**：$\omega = v/r$
3. **動能**：$K = \frac{1}{2}I\omega^2 = \frac{L^2}{2I}$

角動量守恆：若系統不受外力矩，總角動量守恆。

## 25.3 角動量與泊松括號

在哈密頓力學中，角動量分量之間的泊松括號為：

$$\{L_i, L_j\} = \sum_k \varepsilon_{ijk} L_k$$

其中 $\varepsilon_{ijk}$ 是Levi-Civita符號。

具體來說：

$$\{L_x, L_y\} = L_z, \quad \{L_y, L_z\} = L_x, \quad \{L_z, L_x\} = L_y$$

這是經典力學的對易關係。

## 25.4 量子化規則

根據正則量子化規則，將泊松括號替換為對易子：

$$\{A, B\} \to \frac{1}{i\hbar}[\hat{A}, \hat{B}]$$

因此角動量算符的對易關係：

$$[\hat{L}_x, \hat{L}_y] = i\hbar\hat{L}_z, \quad [\hat{L}_y, \hat{L}_z] = i\hbar\hat{L}_x, \quad [\hat{L}_z, \hat{L}_x] = i\hbar\hat{L}_y$$

或寫成向量形式：

$$\hat{\mathbf{L}} \times \hat{\mathbf{L}} = i\hbar\hat{\mathbf{L}}$$

## 25.5 角動量平方算符

定義角動量平方算符：

$$\hat{L}^2 = \hat{L}_x^2 + \hat{L}_y^2 + \hat{L}_z^2$$

可以驗證：

$$[\hat{L}^2, \hat{L}_i] = 0 \quad (i = x, y, z)$$

這意味著 $\hat{L}^2$ 與每個分量都可以同時對角化。

## 25.6 升降算符

定義角動量升降算符：

$$\hat{L}_\pm = \hat{L}_x \pm i\hat{L}_y$$

它們的對易關係：

$$[\hat{L}_z, \hat{L}_\pm] = \pm\hbar\hat{L}_\pm$$

$$[\hat{L}^2, \hat{L}_\pm] = 0$$

這些關係將用來找到角動量的本徵值。

## 25.7 球坐標表示

在位置表象中，角動量算符可以寫成球坐標 $(r, \theta, \phi)$ 的形式：

$$\hat{L}_z = -i\hbar\frac{\partial}{\partial\phi}$$

$$\hat{L}_\pm = \hbar e^{\pm i\phi}\left(\pm \frac{\partial}{\partial\theta} + i\cot\theta \frac{\partial}{\partial\phi}\right)$$

$$\hat{L}^2 = -\hbar^2\left[\frac{1}{\sin\theta}\frac{\partial}{\partial\theta}\left(\sin\theta\frac{\partial}{\partial\theta}\right) + \frac{1}{\sin^2\theta}\frac{\partial^2}{\partial\phi^2}\right]$$

## 25.8 本章小結

本章我們回顧了經典角動量的概念與量子化。經典角動量定義為 $\mathbf{L} = \mathbf{r} \times \mathbf{p}$，分量之間的泊松括號給出循環關係。通過正則量子化，我們得到了量子角動量算符的基本對易關係 $[\hat{L}_x, \hat{L}_y] = i\hbar\hat{L}_z$，這是下一章量子角動量理論的起點。
