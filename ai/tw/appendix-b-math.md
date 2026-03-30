# 附錄 B：數學基礎

深度學習是建立在堅實的數學基礎之上的。本附錄將介紹理解人工智慧和機器學習所需的數學知識，包括線性代數、機率論、微積分和最優化理論。

## B.1 線性代數複習

線性代數是深度學習的數學基礎，神經網路的運算本質上就是矩陣運算。

### B.1.1 向量與矩陣

```python
import numpy as np

# 向量 (Vector)
v = np.array([1, 2, 3])
print(f"Vector: {v}")
print(f"Shape: {v.shape}")

# 矩陣 (Matrix)
A = np.array([[1, 2, 3],
              [4, 5, 6]])
print(f"Matrix:\n{A}")
print(f"Shape: {A.shape}")

# 矩陣運算
B = np.array([[7, 8, 9],
              [10, 11, 12]])

C = A + B  # 加法
C = A - B  # 減法
C = A * B  # 逐元素乘法 (Hadamard積)
C = A @ B.T  # 矩陣乘法
```

### B.1.2 矩陣基本運算

| 運算 | 說明 | 範例 |
|------|------|------|
| 轉置 | 行變列 | A.T |
| 逆矩陣 | AA⁻¹ = I | np.linalg.inv(A) |
| 行列式 | 矩陣的標量值 | np.linalg.det(A) |
| 秩 | 線性無關維度 | np.linalg.matrix_rank(A) |
| 跡 | 對角線元素和 | np.trace(A) |

### B.1.3 特殊矩陣

| 類型 | 說明 | 範例 |
|------|------|------|
| 單位矩陣 | 對角線為1 | np.eye(3) |
| 對角矩陣 | 非對角線為0 | np.diag([1,2,3]) |
| 對稱矩陣 | A = A^T | - |
| 稀疏矩陣 | 大部分元素為0 | scipy.sparse |

### B.1.4 奇異值分解 (SVD)

SVD 是最重要的矩陣分解之一，廣泛用於降維和推薦系統：

```python
A = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])

# SVD 分解: A = U Σ V^T
U, s, Vt = np.linalg.svd(A)

print(f"U:\n{U}")
print(f"Singular values: {s}")
print(f"V^T:\n{Vt}")

# 重建
Sigma = np.diag(s)
A_reconstructed = U @ Sigma @ Vt
```

### B.1.5 範數 (Norm)

範數用於度量向量或矩陣的大小：

| 範數 | 符號 | 定義 | NumPy |
|------|------|------|-------|
| L1 | \|\|x\|\|₁ | Σ|xᵢ| | np.linalg.norm(x, 1) |
| L2 | \|\|x\|\|₂ | √Σxᵢ² | np.linalg.norm(x, 2) |
| L∞ | \|\|x\|\|∞ | max|xᵢ| | np.linalg.norm(x, np.inf) |
| Frobenius | \|\|A\|\|F | √Σaᵢⱼ² | np.linalg.norm(A, 'fro') |

### B.1.6 矩陣分解總覽

```
矩陣分解家族：

┌──────────────────────────────────────────────────────┐
│                    Matrix Decomposition               │
├──────────────────────────────────────────────────────┤
│                                                      │
│  ┌─────────────┐    ┌─────────────┐                │
│  │    LU       │    │    QR       │                │
│  │  A = LU     │    │  A = QR     │                │
│  └─────────────┘    └─────────────┘                │
│                                                      │
│  ┌─────────────┐    ┌─────────────┐                │
│  │    SVD      │    │   Cholesky  │                │
│  │  A = UΣV^T │    │  A = LL^T   │                │
│  └─────────────┘    └─────────────┘                │
│                                                      │
└──────────────────────────────────────────────────────┘
```

## B.2 機率論與資訊理論

機率論是機器學習的基礎語言，用於描述不確定性和進行統計推論。

### B.2.1 基本概念

```python
# 機率分佈
p = np.array([0.1, 0.2, 0.3, 0.2, 0.2])  # 離散分佈

# 期望值
E = np.sum(p * np.arange(len(p)))  # 或 np.dot(p, indices)

# 變異數
var = np.sum(p * (np.arange(len(p)) - E)**2)

# 標準差
std = np.sqrt(var)

print(f"Expected value: {E}")
print(f"Variance: {var}")
print(f"Standard deviation: {std}")
```

### B.2.2 常用機率分佈

| 分佈 | 說明 | 參數 | 應用 |
|------|------|------|------|
| 伯努利 | 0/1 事件 | p | 二分類 |
| 二項 | n次伯努利 | n, p | 計數 |
| 泊松 | 稀疏計數 | λ | 事件頻率 |
| 均勻 | 等機率 | a, b | 隨機採樣 |
| 正態 | 高斯分佈 | μ, σ | 噪聲建模 |
| 指數 | 衰減過程 | λ | 壽命分析 |

### B.2.3 條件機率與貝葉斯定理

```
貝葉斯定理：

P(A|B) = P(B|A) × P(A) / P(B)

• P(A|B): 後驗機率 (Posterior)
• P(B|A): 似然 (Likelihood)  
• P(A): 先驗 (Prior)
• P(B): 證據 (Evidence)
```

```python
# 範例：垃圾郵件分類
P_spam = 0.3      # 垃圾郵件先驗
P_not_spam = 0.7  # 正常郵件先驗
P(word|spam) = 0.8   # 詞彙在垃圾郵件中的條件機率
P(word|not_spam) = 0.1  # 詞彙在正常郵件中的條件機率

# 詞彙出現在垃圾郵件中的機率
P(word) = P(word|spam) * P_spam + P(word|not_spam) * P_not_spam

# 後驗機率
P_spam_word = (P(word|spam) * P_spam) / P(word)
print(f"P(spam|word) = {P_spam_word:.4f}")
```

### B.2.4 最大似然估計 (MLE)

MLE 是最常用的參數估計方法：

```python
import scipy.stats as stats

# 假設數據來自正態分佈
data = np.array([1.2, 2.1, 1.8, 2.5, 2.2, 1.9, 2.3, 2.0])

# MLE 估計
mu_mle = np.mean(data)
sigma_mle = np.std(data, ddof=0)

print(f"MLE: μ = {mu_mle:.4f}, σ = {sigma_mle:.4f}")

# 使用 scipy 驗證
loc, scale = stats.norm.fit(data)
print(f"scipy.fit: loc = {loc:.4f}, scale = {scale:.4f}")
```

### B.2.5 資訊理論

資訊理論量化信息的內容，是機器學習的重要工具：

```python
def entropy(p):
    """計算熵 H(X) = -Σ p(x) log p(x)"""
    p = np.array(p)
    p = p[p > 0]  # 移除零概率
    return -np.sum(p * np.log2(p))

def kl_divergence(p, q):
    """計算 KL 散度 DKL(P||Q)"""
    p = np.array(p)
    q = np.array(q)
    return np.sum(p * np.log2(p / q))

def cross_entropy(p, q):
    """計算交叉熵 H(P,Q) = -Σ p(x) log q(x)"""
    return entropy(p) + kl_divergence(p, q)

# 範例
p = [0.5, 0.5]  # 均勻分佈
q = [0.9, 0.1]  # 偏斜分佈

H_p = entropy(p)
DKL = kl_divergence(p, q)

print(f"Entropy of P: {H_p:.4f} bits")
print(f"KL divergence: {DKL:.4f}")
```

### B.2.6 重要公式

| 公式 | 說明 |
|------|------|
| 熵 | $H(X) = -\sum_x P(x) \log P(x)$ |
| 聯合熵 | $H(X,Y) = -\sum_{x,y} P(x,y) \log P(x,y)$ |
| 條件熵 | $H(X|Y) = H(X,Y) - H(Y)$ |
| 互信息 | $I(X;Y) = H(X) - H(X|Y)$ |
| 交叉熵 | $H(P,Q) = -\sum_x P(x) \log Q(x)$ |

## B.3 微積分與梯度

微積分，特別是微分，是優化演算法的數學基礎。

### B.3.1 導數與偏導數

```python
# 導數的定義
def derivative(f, x, h=1e-5):
    """數值微分"""
    return (f(x + h) - f(x - h)) / (2 * h)

# 範例：f(x) = x^2
f = lambda x: x**2
x = 3.0
print(f"f'({x}) = {derivative(f, x)}")  # 應該接近 6

# 偏導數
def partial_derivative(f, x, idx, h=1e-5):
    """計算第 idx 個變數的偏導數"""
    x_plus = x.copy()
    x_minus = x.copy()
    x_plus[idx] += h
    x_minus[idx] -= h
    return (f(x_plus) - f(x_minus)) / (2 * h)

# 範例：f(x,y) = x^2 + y^2
f = lambda x: x[0]**2 + x[1]**2
x = np.array([3.0, 4.0])
print(f"∂f/∂x = {partial_derivative(f, x, 0)}")  # 6
print(f"∂f/∂y = {partial_derivative(f, x, 1)}")  # 8
```

### B.3.2 梯度

梯度是偏導數的向量，推廣到多維：

$$\nabla f = \left[\frac{\partial f}{\partial x_1}, \frac{\partial f}{\partial x_2}, ..., \frac{\partial f}{\partial x_n}\right]$$

```python
def gradient(f, x, h=1e-5):
    """計算梯度"""
    grad = np.zeros_like(x)
    for i in range(len(x)):
        grad[i] = partial_derivative(f, x, i, h)
    return grad

# 範例
x = np.array([3.0, 4.0])
grad = gradient(f, x)
print(f"Gradient: {grad}")  # [6, 8]
print(f"Gradient norm: {np.linalg.norm(grad)}")  # 10
```

### B.3.3 鏈式法則

鏈式法则是深度學習反向傳播的數學基礎：

```python
# 複合函數：h(x) = f(g(x))
# h'(x) = f'(g(x)) × g'(x)

# 範例：
# f(y) = y^2
# g(x) = sin(x)
# h(x) = sin^2(x)

# h'(x) = 2sin(x) × cos(x) = sin(2x)

import sympy as sp
x = sp.symbols('x')
h = sp.sin(x)**2
dh = sp.diff(h, x)
print(f"h'(x) = {sp.simplify(dh)}")  # 2*sin(x)*cos(x) = sin(2x)
```

### B.3.4 雅可比矩陣與海森矩陣

```python
# 雅可比矩陣：一階偏導數矩陣
# J[i,j] = ∂f_i/∂x_j

# 範例：
# f1(x,y) = x^2 + y
# f2(x,y) = x + y^2

x, y = sp.symbols('x y')
f1 = x**2 + y
f2 = x + y**2

J = sp.Matrix([f1, f2]).jacobian([x, y])
print(f"Jacobian:\n{J}")

# 海森矩陣：二階偏導數矩陣
# H[i,j] = ∂²f/∂x_i∂x_j

H = sp.Matrix([f1]).hessian([x, y])
print(f"Hessian:\n{H}")
```

### B.3.5 重要微分公式

| 函數 | 導數 |
|------|------|
| $x^n$ | $nx^{n-1}$ |
| $e^x$ | $e^x$ |
| $\ln(x)$ | $1/x$ |
| $\sin(x)$ | $\cos(x)$ |
| $\cos(x)$ | $-\sin(x)$ |
| $\sigma(x)$ | $\sigma(x)(1-\sigma(x))$ |

## B.4 最優化理論

最優化是機器學習的核心，目標是找到使目標函數最小或最大的參數。

### B.4.1 梯度下降法

梯度下降是最基礎的優化算法：

```python
def gradient_descent(f, grad_f, x0, lr=0.1, max_iter=100, tol=1e-6):
    """梯度下降法"""
    x = x0.copy()
    history = [x.copy()]
    
    for i in range(max_iter):
        gradient = grad_f(x)
        x = x - lr * gradient
        history.append(x.copy())
        
        if np.linalg.norm(gradient) < tol:
            break
    
    return x, history

# 範例：最小化 f(x,y) = x^2 + y^2
f = lambda x: x[0]**2 + x[1]**2
grad_f = lambda x: np.array([2*x[0], 2*x[1]])

x0 = np.array([5.0, 5.0])
x_opt, history = gradient_descent(f, grad_f, x0, lr=0.1)

print(f"Optimal: {x_opt}")
print(f"Function value: {f(x_opt):.6f}")
```

### B.4.2 梯度下降變體

| 算法 | 說明 | 更新規則 |
|------|------|----------|
| SGD | 隨機梯度下降 | $x_{t+1} = x_t - \eta \nabla f_i(x_t)$ |
| Momentum | 帶動量 | $v_{t+1} = \gamma v_t + \eta \nabla f(x_t)$ |
| Nesterov | Nesterov 加速 | 先看下一步再更新 |
| Adagrad | 自適應學習率 | 根據歷史調整 |
| RMSprop | 指數加權 | 使用指數移動平均 |
| Adam | 自適應+momentum | 結合 Adagrad 和 RMSprop |

```python
# Momentum
def momentum(f, grad_f, x0, lr=0.1, gamma=0.9, max_iter=100):
    x = x0.copy()
    v = np.zeros_like(x)
    
    for i in range(max_iter):
        gradient = grad_f(x)
        v = gamma * v + lr * gradient
        x = x - v
    
    return x

# Adam
def adam(f, grad_f, x0, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8, max_iter=100):
    x = x0.copy()
    m = np.zeros_like(x)
    v = np.zeros_like(x)
    
    for t in range(1, max_iter+1):
        gradient = grad_f(x)
        
        m = beta1 * m + (1 - beta1) * gradient
        v = beta2 * v + (1 - beta2) * (gradient ** 2)
        
        m_hat = m / (1 - beta1 ** t)
        v_hat = v / (1 - beta2 ** t)
        
        x = x - lr * m_hat / (np.sqrt(v_hat) + eps)
    
    return x
```

### B.4.3 學習率调度

```python
# 1. 階梯衰減
scheduler = StepLR(optimizer, step_size=10, gamma=0.1)

# 2. 指數衰減
scheduler = ExponentialLR(optimizer, gamma=0.95)

# 3. 餘弦退火
scheduler = CosineAnnealingLR(optimizer, T_max=50)

# 4. 熱身 + 餘弦
scheduler = WarmupCosineScheduler(optimizer, warmup_epochs=5, max_epochs=100)

# 訓練循環中使用
for epoch in range(epochs):
    train()
    scheduler.step()
```

### B.4.4 約束優化

```python
# 投影梯度下降
def projected_gradient_descent(f, grad_f, x0, lr, max_iter, projection):
    """約束優化：投影到可行集"""
    x = x0.copy()
    
    for i in range(max_iter):
        gradient = grad_f(x)
        x = x - lr * gradient
        x = projection(x)  # 投影到約束域
    
    return x

# 範例：約束在 [0,1] 範圍內
projection = lambda x: np.clip(x, 0, 1)
```

### B.4.5 拉格朗日乘數

拉格朗日乘數是處理約束優化的重要工具：

```python
# 最小化 f(x,y) = x^2 + y^2
# 約束：x + y = 1

# 拉格朗日函數：L(x,y,λ) = x^2 + y^2 + λ(x + y - 1)

# 偏導數設為零：
# ∂L/∂x = 2x + λ = 0 → x = -λ/2
# ∂L/∂y = 2y + λ = 0 → y = -λ/2
# ∂L/∂λ = x + y - 1 = 0

# 代入：-λ/2 - λ/2 = 1 → λ = -1
# 最優解：x = y = 0.5

# 使用 sympy 求解
x, y, lam = sp.symbols('x y lam')
L = x**2 + y**2 + lam * (x + y - 1)

solutions = sp.solve([sp.diff(L, x), sp.diff(L, y), sp.diff(L, lam)], [x, y, lam])
print(f"Optimal solution: x={solutions[x]}, y={solutions[y]}")
```

## B.5 總結

| 數學領域 | 核心概念 | 在 ML/DL 中的應用 |
|----------|----------|-------------------|
| 線性代數 | 矩陣、向量、範數 | 神經網路計算、SVD 降維 |
| 機率論 | 條件機率、貝葉斯 | 統計學習、生成模型 |
| 資訊理論 | 熵、互信息 | 損失函數、特徵選擇 |
| 微積分 | 梯度、鏈式法則 | 反向傳播、優化 |
| 最優化 | 梯度下降、Adam | 模型訓練 |

扎實的數學基礎是深入理解人工智慧和機器學習的關鍵。這些數學工具不僅幫助我們理解現有算法的原理，也是開發新方法的基礎。
