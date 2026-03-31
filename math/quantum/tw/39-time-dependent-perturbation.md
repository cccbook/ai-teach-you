# 第三十九章：含時微擾理論

## 39.1 為什麼需要含時微擾理論

在前面的章節中，我們討論了時間無關微擾理論，這些方法適用於求解定態能量本徵值和本徵態。然而，現實中大量的物理問題涉及隨時間變化的哈密頓量，這些問題需要不同的理論工具。

含時微擾理論處理的典型問題包括：
1. **原子對外加電磁場的響應**：原子在雷射或微波輻射下的行為
2. **量子躍遷**：原子從一個能級躍遷到另一個能級的過程
3. **系統與環境的相互作用**：開放量子系統的動力學
4. **含時外場問題**：如隨時間變化的電位或磁場

與時間無關的情況不同，含時問題沒有定態波函數和定態能量。我們不能使用能量本徵函數展開，而必須直接處理含時薛丁格方程式。

含時微擾理論的核心任務是：在已知系統的「未受擾」含時演化（或靜態本徵態）的基礎上，計算弱含時微擾對系統的影響。

## 39.2 含時薛丁格方程式的基本理論

考慮一個一般的含時哈密頓量：

$$H(t) = H_0 + H'(t)$$

其中 $H_0$ 是時間無關的未受擾哈密頓量，$H'(t)$ 是含時微擾。我們假設我們知道 $H_0$ 的本徵值問題：

$$H_0 |n\rangle = E_n |n\rangle$$

對於未受擾系統，如果初始時刻 $t_0$ 系統處於本徵態 $|n\rangle$，則任意時刻的演化為：

$$|n(t)\rangle_0 = e^{-iE_n(t-t_0)/\hbar} |n\rangle$$

對於一般初始狀態 $|\psi(t_0)\rangle = \sum_n c_n |n\rangle$，未受擾演化為：

$$|\psi(t)\rangle_0 = \sum_n c_n e^{-iE_n(t-t_0)/\hbar} |n\rangle$$

含時薛丁格方程式的精確解在一般情况下是困難的。我們需要尋找近似方法。

## 39.3 Dyson級數與演化算符

處理含時問題的一個強大工具是演化算符 $U(t, t_0)$，它將狀態從 $t_0$ 時刻傳播到 $t$ 時刻：

$$|\psi(t)\rangle = U(t, t_0) |\psi(t_0)\rangle$$

演化算符必須是么正的：$U^\dagger(t, t_0) U(t, t_0) = I$，以保證概率守恆。

對於含時哈密頓量，演化算符滿足：

$$i\hbar \frac{\partial}{\partial t} U(t, t_0) = H(t) U(t, t_0)$$

邊界條件：$U(t_0, t_0) = I$

這個方程式的形式解可以寫成Dyson級數：

$$U(t, t_0) = I - \frac{i}{\hbar} \int_{t_0}^t dt_1 H'(t_1) + \left(\frac{-i}{\hbar}\right)^2 \int_{t_0}^t dt_1 \int_{t_0}^{t_1} dt_2 H'(t_1) H'(t_2) + \cdots$$

Dyson級數是含時微擾理論的基礎。它將演化算符展開為微擾的冪級數。

## 39.4 相互作用繪景

含時微擾理論的另一個優雅表述是使用相互作用繪景（Interaction Picture）。相互作用繪景是海森堡繪景和薛丁格繪景的混合：算符用 $H_0$ 的時間演化，態用 $H'$ 的時間演化。

在相互作用繪景中：
- 算符：$A_I(t) = e^{iH_0 t/\hbar} A_S e^{-iH_0 t/\hbar}$
- 態：$|\psi_I(t)\rangle = e^{iH_0 t/\hbar} |\psi_S(t)\rangle$

相互作用繪景中的含時方程式為：

$$i\hbar \frac{d}{dt} |\psi_I(t)\rangle = H_I'(t) |\psi_I(t)\rangle$$

其中 $H_I'(t) = e^{iH_0 t/\hbar} H'(t) e^{-iH_0 t/\hbar}$ 是微擾的相互作用繪景形式。

這個方程式與原始薛丁格方程式的形式相同，但 $H_I'(t)$ 通常比 $H(t)$ 簡單。

## 39.5 躍遷機率

含時微擾理論最重要的應用之一是計算量子躍遷的機率。考慮以下情景：

- 在 $t = t_0$ 時，系統處於 $H_0$ 的本徵態 $|i\rangle$（初始態）
- 我們想知道在 $t$ 時系統躍遷到本徵態 $|f\rangle$（終態）的機率
- 中間過程中可能存在含時微擾

假設 $t_0 = -\infty$，微擾在無窮遠過去為零。則躍遷振幅（to 一階）為：

$$a_f(t) = \langle f | \psi(t) \rangle \approx -\frac{i}{\hbar} \int_{-\infty}^{t} dt' \langle f | H'(t') | i \rangle e^{i\omega_{fi} t'}$$

其中 $\omega_{fi} = (E_f - E_i)/\hbar$ 是躍遷的Bohr頻率。

躍遷機率為 $P_{i\to f}(t) = |a_f(t)|^2$。

## 39.6 Fermi 的黃金規則

考慮微擾是單色週期勢的情況：

$$H'(t) = W e^{-i\omega t} + W^\dagger e^{i\omega t}$$

其中 $W$ 是一個與時間無關的算符。

一階躍遷機率為：

$$P_{i\to f}(t) = \frac{1}{\hbar^2} \left| \int_{-\infty}^{t} dt' \langle f | H'(t') | i \rangle e^{i\omega_{fi} t'} \right|^2$$

計算這個積分可以得到：

$$P_{i\to f}(t) = \frac{|\langle f | W | i \rangle|^2}{\hbar^2} \frac{\sin^2[(\omega_{fi} - \omega)t/2]}{[(\omega_{fi} - \omega)/2]^2} + \frac{|\langle f | W^\dagger | i \rangle|^2}{\hbar^2} \frac{\sin^2[(\omega_{fi} + \omega)t/2]}{[(\omega_{fi} + \omega)/2]^2}$$

對於大的 $t$，$\sin^2(\Delta\omega \cdot t/2)/(\Delta\omega/2)^2$ 趨於 $2\pi t \delta(\Delta\omega)$。

因此，躍遷速率（單位時間的躍遷機率）為：

$$\Gamma_{i\to f} = \frac{dP}{dt} = \frac{2\pi}{\hbar} |\langle f | W | i \rangle|^2 \delta(E_f - E_i - \hbar\omega) + \frac{2\pi}{\hbar} |\langle f | W^\dagger | i \rangle|^2 \delta(E_f - E_i + \hbar\omega)$$

這就是著名的 **Fermi 的黃金規則**（Golden Rule）。它告訴我們：

1. 躍遷速率與矩陣元 $|\langle f | W | i \rangle|^2$ 成正比
2. 能量守恆 $E_f = E_i \pm \hbar\omega$ 必須滿足
3. 躍遷到連續態時，能量守恆轉化為delta函數

## 39.7 吸收與發射

Fermi黃金規則中的兩項對應於兩種不同的物理過程：

**吸收過程**：$E_f = E_i + \hbar\omega$，系統吸收一個能量為 $\hbar\omega$ 的光子，從較低能級躍遷到較高能級。速率與 $|\langle f | W | i \rangle|^2$ 成正比。

**受激發射過程**：$E_f = E_i - \hbar\omega$，系統發射一個光子，從較高能級躍遷到較低能級。速率與 $|\langle f | W^\dagger | i \rangle|^2$ 成正比。

這兩個過程的速率相同（對於真實的 $W$，這成立）。這與熱力學平衡中的細節平衡原理一致。

注意：Fermi黃金規則不包括自發發射過程，這需要量子化的輻射場和二階微擾理論來處理。

## 39.8 緩慢開啟的微擾

考慮微擾不是突然開啟，而是逐漸增長的情況：

$$H'(t) = W e^{\eta t} \theta(-t) \quad \text{或} \quad H'(t) = W e^{\eta t} \quad \text{for} \quad t_0 \to -\infty$$

其中 $\eta \to 0^+$ 是一個小的正數，用於確保在無窮遠過去微擾為零。

這個「adiabatic turn-on」確保了正確的邊界條件。在計算躍遷振幅時：

$$a_f(t) = -\frac{i}{\hbar} \lim_{\eta \to 0^+} \int_{-\infty}^{t} dt' \langle f | W | i \rangle e^{i(\omega_{fi} - \omega + i\eta)t'}$$

對於 $t \to \infty$：

$$a_f(\infty) = -\frac{i}{\hbar} \langle f | W | i \rangle \frac{e^{i(\omega_{fi} - \omega)t}}{i(\omega_{fi} - \omega + i\eta)}$$

取極限 $\eta \to 0^+$：

$$a_f(\infty) = \frac{\langle f | W | i \rangle}{\hbar(\omega_{fi} - \omega + i0^+)}$$

躍遷機率：

$$P_{i\to f} = \frac{|\langle f | W | i \rangle|^2}{\hbar^2 [(\omega_{fi} - \omega)^2 + \eta^2]}$$

## 39.9 二階微擾理論

有時一階微擾為零（例如，矩陣元為零），這時我們需要考慮二階微擾。對於躍遷振幅，二階項為：

$$a_f^{(2)} = \left(\frac{-i}{\hbar}\right)^2 \sum_n \int_{-\infty}^{\infty} dt_1 \int_{-\infty}^{t_1} dt_2 \langle f | H'(t_1) | n \rangle \langle n | H'(t_2) | i \rangle e^{i\omega_{fn}t_1} e^{i\omega_{ni}t_2}$$

其中 $|n\rangle$ 是所有可能的中間態。

二階躍遷在以下情況中很重要：
1. 一階矩陣元為零的躍遷（如某些選擇規則禁止的躍遷）
2. 兩個光子過程（如雙光子吸收或喇曼散射）
3. 共振附近的動力學（中間態與初始或終態能量接近）

## 39.10 週期微擾與離散能級的動力學

當微擾是時間的週期函數時，系統的行為更加豐富。除了躍遷到連續態，還可以發生能級之間的週期性能量交換。

考慮兩個能級 $|1\rangle$ 和 $|2\rangle$ 之間的共振耦合。哈密頓量為：

$$H = \begin{pmatrix} E_1 & W e^{-i\omega t} \\ W^* e^{i\omega t} & E_2 \end{pmatrix}$$

當 $\omega \approx \omega_{21} = (E_2 - E_1)/\hbar$ 時，會發生Rabbi振盪——系統在兩個能級之間週期性振盪。

這種振盪是雷射物理、核磁共振（NMR）和許多其他現象的基礎。

## 39.11 Sudden近似

與緩慢開啟相反，有時微擾的變化非常快速，以至於在微擾變化的瞬間，系統狀態來不及調整。這稱為Sudden近似。

例如：如果系統初始處於 $|i\rangle$，然後哈密頓量突然從 $H_0$ 變為 $H$，則：

$$P_{i\to f} = |\langle f | i \rangle|^2$$

其中 $|f\rangle$ 是新哈密頓量 $H$ 的本徵態。

Sudden近似的適用條件：微擾的變化時間 $\tau \ll 1/\omega_{if}$，其中 $\omega_{if}$ 是相關的Bohr頻率。

## 39.12 本章小結

本章我們系統介紹了含時微擾理論的基本框架和主要結果。我們從Dyson級數和演化算符出發，建立了處理含時問題的數學工具。

相互作用繪景提供了一種優雅的方式來分離快速振盪和慢變化，使得含時問題的處理更加清晰。

Fermi的黃金規則是含時微擾理論最重要的結果之一。它告訴我們，在弱週期微擾下，躍遷到連續態的速率與矩陣元的平方成正比，並受到能量守恆約束。

我們還討論了二階微擾理論、週期微擾與Rabi振盪、以及Sudden近似。這些工具和方法在原子物理、分子物理、固態物理和量子光學中都有廣泛應用。

在下一章中，我們將應用這些理論來討論原子與光的相互作用——這是量子光學和雷射物理的基礎。
