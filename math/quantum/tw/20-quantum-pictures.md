# 第二十章：量子力學的繪景——薛丁格、海森堡與相互作用

## 20.1 三種等價的描述方式

量子力學可以用三種等價的**繪景**（Picture）來描述：
1. **薛丁格繪景**（Schrödinger Picture）
2. **海森堡繪景**（Heisenberg Picture）
3. **相互作用繪景**（Interaction Picture）

這三種繪景在數學上等價，但在處理不同問題時有不同的方便性。

## 20.2 薛丁格繪景

在**薛丁格繪景**中：
- 態向量 $|\psi_S(t)\rangle$ 隨時間演化
- 算符 $\hat{A}_S$ 不顯含時間（除非原來就含時間）
- 時間演化由薛丁格方程式決定

含時薛丁格方程式：
$$i\hbar\frac{d}{dt}|\psi_S(t)\rangle = \hat{H}|\psi_S(t)\rangle$$

形式解：
$$|\psi_S(t)\rangle = \hat{U}(t, t_0)|\psi_S(t_0)\rangle$$

其中時間演化算符：
$$\hat{U}(t, t_0) = e^{-i\hat{H}(t-t_0)/\hbar}$$

時間演化算符是**么正**的：
$$\hat{U}^\dagger\hat{U} = \hat{U}\hat{U}^\dagger = \mathbf{1}$$

## 20.3 海森堡繪景

在**海森堡繪景**中：
- 態向量 $|\psi_H\rangle$ 不隨時間變化（等於初始的薛丁格態）
- 算符 $\hat{A}_H(t)$ 隨時間演化
- 演化由海森堡方程式決定

薛丁格態與海森堡態的關係：
$$|\psi_H\rangle = \hat{U}^\dagger(t, t_0)|\psi_S(t)\rangle = |\psi_S(t_0)\rangle$$

薛丁格算符與海森堡算符的關係：
$$\hat{A}_H(t) = \hat{U}^\dagger(t, t_0) \hat{A}_S \hat{U}(t, t_0)$$

海森堡方程式：
$$\frac{d\hat{A}_H}{dt} = \frac{i}{\hbar}[\hat{H}, \hat{A}_H] + \left(\frac{\partial \hat{A}}{\partial t}\right)_H$$

## 20.4 兩種繪景的等價性

讓我們驗證兩種繪景給出相同的測量結果。

在薛丁格繪景中，期望值：
$$\langle A \rangle_S(t) = \langle\psi_S(t)|\hat{A}_S|\psi_S(t)\rangle$$

代入時間演化：
$$= \langle\psi_S(t_0)|\hat{U}^\dagger \hat{A}_S \hat{U}|\psi_S(t_0)\rangle = \langle\psi_H|\hat{A}_H(t)|\psi_H\rangle = \langle A \rangle_H(t)$$

兩種繪景給出相同的期望值！

## 20.5 什麼時候使用哪種繪景

**薛丁格繪景**的優點：
- 態向量的演化比較直觀
- 適合處理與時間有關的微擾理論
- 適合計算躍遷機率

**海森堡繪景**的優點：
- 算符的演化類似經典運動方程
- 便於討論物理量的時間關係
- 在某些形式理論中更方便

## 20.6 相互作用繪景

**相互作用繪景**（也稱為Dyson繪景）是第三種描述方式，適用於系統哈密頓可以分為兩部分的情形：

$$\hat{H} = \hat{H}_0 + \hat{V}(t)$$

其中：
- $\hat{H}_0$ 是可解的部分
- $\hat{V}(t)$ 是微擾（可能依賴時間）

在相互作用繪景中：
- 態向量用 $\hat{H}_0$ 的本徵態展開
- 態與算符都演化，但方式不同

相互作用繪景中的演化方程：
- 態：$i\hbar\frac{d}{dt}|\psi_I(t)\rangle = \hat{V}_I(t)|\psi_I(t)\rangle$
- 算符：$\frac{d\hat{A}_I}{dt} = \frac{i}{\hbar}[\hat{H}_0, \hat{A}_I] + \left(\frac{\partial \hat{A}}{\partial t}\right)_I$

其中：
$$\hat{A}_I(t) = e^{i\hat{H}_0 t/\hbar} \hat{A}_S e^{-i\hat{H}_0 t/\hbar}$$
$$\hat{V}_I(t) = e^{i\hat{H}_0 t/\hbar} \hat{V}(t) e^{-i\hat{H}_0 t/\hbar}$$

## 20.7 Dyson級數

在相互作用繪景中，態的演化可以寫成Dyson級數。

時間演化算符：
$$\hat{U}_I(t, t_0) = \sum_{n=0}^{\infty} \frac{(-i)^n}{\hbar^n} \int_{t_0}^{t} dt_1 \int_{t_0}^{t_1} dt_2 \cdots \int_{t_0}^{t_{n-1}} dt_n \hat{V}_I(t_1)\hat{V}_I(t_2)\cdots\hat{V}_I(t_n)$$

這個表達式看起來很複雜，但物理意義很清晰：它是微擾的逐階展開。

更緊湊的積分表達式：
$$\hat{U}_I(t, t_0) = \text{T exp}\left[-\frac{i}{\hbar}\int_{t_0}^{t} \hat{V}_I(t') dt'\right]$$

其中 T 是**時間排序算符**，它保証較晚時間的算符在左側。

## 20.8 與微擾論的關係

相互作用繪景是**時間相關微擾理論**的基礎。

一級近似的躍遷機率幅：
$$c_{m}^{(1)}(t) = -\frac{i}{\hbar} \int_{t_0}^{t} \langle m|\hat{V}_I(t')|i\rangle dt'$$

這就是著名的**費米黃金規則**的推導起點。

## 20.9 三種繪景的比較

讓我們用表格總結三種繪景的特點：

| 特點 | 薛丁格繪景 | 海森堡繪景 | 相互作用繪景 |
|------|------------|------------|--------------|
| 態演化 | 服從薛丁格方程式 | 不變 | 僅由 $\hat{V}$ 決定 |
| 算符演化 | 不變（除非顯含時間） | 服從海森堡方程式 | 由 $\hat{H}_0$ 決定 |
| 適用場合 | 一般場合 | 理論分析 | 微擾論 |

## 20.10 繪景的實際應用

讓我們討論一些實際應用。

### 20.10.1 諧振子的演化

在薛丁格繪景中，態以 $e^{-iE_n t/\hbar}$ 振盪。

在海森堡繪景中，算符以相同頻率振盪：
$$\hat{x}(t) = \sqrt{\frac{\hbar}{2m\omega}}(ae^{-i\omega t} + a^\dagger e^{i\omega t})$$

### 20.10.2 躍遷機率

在相互作用繪景中，躍遷機率由 Dyson 級數給出。

### 20.10.3 散射理論

在相互作用繪景中，散射問題可以方便地處理。

## 20.11 繪景與詮釋的區別

注意：「繪景」與「詮釋」是兩個不同的概念。

**繪景**（picture）是純數學的區分，三種繪景給出完全相同的物理預言。

**詮釋**（interpretation）涉及對量子態物理意義的哲學理解，如哥本哈根詮釋、多世界詮釋等。

## 20.12 本章小結

本章我們介紹了量子力學的三種等價描述方式：薛丁格繪景、海森堡繪景與相互作用繪景。薛丁格繪景中態向量演化，算符固定；海森堡繪景中態固定，算符演化；相互作用繪景適用於可分離為主要部分與微擾的系統，廣泛應用於時間相關微擾理論。三種繪景在數學上等價，選擇哪種取決於問題的方便性。
