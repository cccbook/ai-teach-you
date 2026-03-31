# 第二十六章：量子角動量理論

## 26.1 角動量本徵值問題

根據上一章的對易關係，我們要找 $\hat{L}^2$ 與 $\hat{L}_z$ 的共同本徵態。

設：

$$\hat{L}^2|\lambda, m\rangle = \lambda\hbar^2|\lambda, m\rangle$$

$$\hat{L}_z|\lambda, m\rangle = m\hbar|\lambda, m\rangle$$

## 26.2 角動量量子數

利用升降算符的性質，可以推導出：

1. **$m$ 的取值**：$m = -l, -l+1, \ldots, l-1, l$，其中 $l$ 是非負整數或半整數
2. **$\lambda$ 與 $l$ 的關係**：$\lambda = l(l+1)$

因此角動量的大小：

$$L = \sqrt{l(l+1)}\hbar$$

$z$ 分量：

$$L_z = m\hbar$$

其中：
- $l = 0, \frac{1}{2}, 1, \frac{3}{2}, 2, \ldots$
- $m = -l, -l+1, \ldots, l$

## 26.3 球諧函數

角動量本徵函數是**球諧函數**（Spherical Harmonics）$Y_{lm}(\theta, \phi)$：

$$\hat{L}^2 Y_{lm} = l(l+1)\hbar^2 Y_{lm}$$

$$\hat{L}_z Y_{lm} = m\hbar Y_{lm}$$

球諧函數的顯式形式：

$$Y_{lm}(\theta, \phi) = N_{lm} P_l^m(\cos\theta) e^{im\phi}$$

其中 $P_l^m$ 是伴隨勒讓德多項式，$N_{lm}$ 是歸一化常數。

## 26.4 球諧函數的性質

球諧函數的重要性質：

1. **正交歸一**：
$$\int_0^{2\pi} d\phi \int_0^{\pi} \sin\theta d\theta \, Y_{l'm'}^* Y_{lm} = \delta_{ll'}\delta_{mm'}$$

2. **完整性**：
$$\sum_{l=0}^{\infty} \sum_{m=-l}^{l} Y_{lm}^*(\theta', \phi') Y_{lm}(\theta, \phi) = \delta(\phi - \phi')\delta(\cos\theta - \cos\theta')$$

3. **宇稱**：
$$Y_{lm}(\pi - \theta, \phi + \pi) = (-l)^l Y_{lm}(\theta, \phi)$$

4. **最低階球諧函數**：
$$Y_{00} = \frac{1}{\sqrt{4\pi}}$$
$$Y_{10} = \sqrt{\frac{3}{4\pi}} \cos\theta$$
$$Y_{1\pm1} = \mp\sqrt{\frac{3}{8\pi}} \sin\theta e^{\pm i\phi}$$

## 26.5 升降算符的作用

升降算符 $\hat{L}_\pm$ 作用在本徵態上改變 $m$：

$$\hat{L}_\pm |l, m\rangle = \hbar \sqrt{l(l+1) - m(m \pm 1)} |l, m \pm 1\rangle$$

從 $m = l$ 的態連續作用 $\hat{L}_-$ 可以得到所有 $m$ 值；從 $m = -l$ 作用 $\hat{L}_+$ 同樣如此。

## 26.6 軌道角動量的物理意義

軌道角動量對應於粒子繞某個中心的旋轉運動。

- $l = 0$（$s$ 軌域）：球對稱，無角動量
- $l = 1$（$p$ 軌域）：類似啞鈴形
- $l = 2$（$d$ 軌域）：更複雜的形狀
- 等等

這與原子物理中光譜學的命名一致：$s, p, d, f, \ldots$

## 26.7 角動量與磁矩

運動的電荷產生磁矩。對於軌道運動：

$$\boldsymbol{\mu}_L = -\frac{e}{2m} \mathbf{L}$$

磁矩與角動量方向相反（因為電子帶負電）。

在外加磁場 $\mathbf{B}$ 中，磁勢能：

$$V = -\boldsymbol{\mu} \cdot \mathbf{B}$$

這導致了**塞曼效應**：光譜線在磁場中分裂。

## 26.8 本章小結

本章我們討論了量子角動量理論。我們發現角動量大小被量子化為 $L = \sqrt{l(l+1)}\hbar$，$z$ 分量被量子化為 $L_z = m\hbar$，其中 $l = 0, 1/2, 1, \ldots$，$m = -l, \ldots, l$。本徵函數是球諧函數 $Y_{lm}(\theta, \phi)$，它們是量子力學中處理中心勢問題的基礎。
