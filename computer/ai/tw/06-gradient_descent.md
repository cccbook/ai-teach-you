# 第 6 章：梯度下降法與反傳遞演算法

## 6.1 優化問題與損失函數

神經網路訓練的本質是一個優化問題：我們希望找到一組參數 θ，使得損失函數 L(θ) 最小。

```
θ* = argmin_θ L(θ)
```

損失函數衡量模型預測與真實值之間的差距。根據任務的不同，我們使用不同的損失函數：

- **均方誤差 (MSE)**：常用於迴歸任務
  ```
  L(y, ŷ) = (1/n) Σ(yᵢ - ŷᵢ)²
  ```

- **交叉熵 (Cross-Entropy)**：常用於分類任務
  ```
  L(y, ŷ) = -Σ yᵢ log(ŷᵢ)
  ```

## 6.2 梯度下降法 (Gradient Descent)

梯度下降是最基本也是最重要的優化演算法。它的核心思想是：沿著函數梯度的反方向移動參數，因為梯度指向函數增長最快的方向。

[程式檔案：06-1-gradient-descent.py](../_code/06/06-1-gradient-descent.py)

```python
import numpy as np

try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Note: matplotlib not available, skipping visualization")

def gradient_descent(f, grad_f, x0, learning_rate=0.1, max_iter=50, tolerance=1e-6):
    x = np.array(x0, dtype=float)
    path = [x.copy()]
    
    for i in range(max_iter):
        gradient = grad_f(x)
        x = x - learning_rate * gradient
        path.append(x.copy())
        
        if np.linalg.norm(gradient) < tolerance:
            break
    
    return x, np.array(path)

def f(x):
    return x[0]**2 + x[1]**2

def grad_f(x):
    return np.array([2*x[0], 2*x[1]])

def f_elliptic(x):
    return x[0]**2 + 10*x[1]**2

def grad_f_elliptic(x):
    return np.array([2*x[0], 20*x[1]])

def f_saddle(x):
    return x[0]**2 - x[1]**2

def grad_f_saddle(x):
    return np.array([2*x[0], -2*x[1]])

x0 = [4.0, 3.0]
learning_rate = 0.1

print("=" * 60)
print("Gradient Descent Visualization")
print("=" * 60)

print("\n1. Simple Quadratic: f(x,y) = x² + y²")
print(f"   Starting point: {x0}")
optimum, path = gradient_descent(f, grad_f, x0, learning_rate)
print(f"   Found optimum at: {optimum}")
print(f"   Steps taken: {len(path)-1}")
print(f"   Path: {path[:5].tolist()}...")

print("\n2. Elliptic Quadratic: f(x,y) = x² + 10y²")
print(f"   Starting point: {x0}")
optimum, path = gradient_descent(f_elliptic, grad_f_elliptic, x0, learning_rate)
print(f"   Found optimum at: {optimum}")
print(f"   Steps taken: {len(path)-1}")

print("\n3. Saddle Point: f(x,y) = x² - y²")
print(f"   Starting point: {x0}")
optimum, path = gradient_descent(f_saddle, grad_f_saddle, x0, learning_rate, max_iter=20)
print(f"   Steps taken: {len(path)-1}")
print(f"   Final point: {optimum} (saddle point behavior)")
```

### 6.2.1 梯度下降的變體

1. **批量梯度下降 (Batch GD)**：每次使用全部資料計算梯度
   - 優點：穩定的收斂方向
   - 缺點：計算量大，記憶體需求高

2. **隨機梯度下降 (SGD)**：每次使用一個樣本計算梯度
   - 優點：計算快速，能跳出局部極小
   - 缺點：收斂震盪，可能不穩定

3. **小批量梯度下降 (Mini-batch GD)**：每次使用一批樣本
   - 平衡效率和穩定性

### 6.2.2 學習率的影響

學習率是梯度下降中最重要的超參數：
- **學習率過大**：可能越過最優點，導致震盪或發散
- **學習率過小**：收斂緩慢，需要更多迭代

## 6.3 隨機梯度下降法 (SGD) 與動量

### 6.3.1 動量 (Momentum)

動量模擬物理中的慣性概念，幫助優化器沿著峽谷方向加速前進，避免在狹窄方向上的震盪。

[程式檔案：06-2-sgd-momentum.py](../_code/06/06-2-sgd-momentum.py)

```python
import numpy as np

try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Note: matplotlib not available, skipping visualization")

class SGD:
    def __init__(self, params, lr=0.01, momentum=0.0):
        self.lr = lr
        self.momentum = momentum
        self.velocity = {k: np.zeros_like(v) for k, v in params.items()}
    
    def step(self, params, gradients):
        for k in params:
            if self.momentum > 0:
                self.velocity[k] = self.momentum * self.velocity[k] - self.lr * gradients[k]
                params[k] = params[k] + self.velocity[k]
            else:
                params[k] = params[k] - self.lr * gradients[k]
        return params
```

動量的更新公式：
```
v_t = β * v_{t-1} + (1 - β) * ∇L
θ_t = θ_{t-1} - lr * v_t
```

其中 β 通常設為 0.9。

### 6.3.2 Nesterov 動量

Nesterov 動量是動量的改進版本，它先根據累積的動量預估未來位置，然後計算梯度：

```
v_t = β * v_{t-1} + ∇L(θ_{t-1} - lr * β * v_{t-1})
θ_t = θ_{t-1} - lr * v_t
```

## 6.4 Adam、RMSprop 等優化器

現代深度學習中，各種自適應學習率優化器層出不窮。讓我們了解幾種最常用的優化器。

[程式檔案：06-3-optimizer.py](../_code/06/06-3-optimizer.py)

```python
import numpy as np

class Adam(Optimizer):
    def __init__(self, params, lr=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8):
        super().__init__(params, lr)
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.m = {k: np.zeros_like(v) for k, v in params.items()}
        self.v = {k: np.zeros_like(v) for k, v in params.items()}
        self.t = 0
    
    def step(self, gradients):
        self.t += 1
        for k in self.params:
            self.m[k] = self.beta1 * self.m[k] + (1 - self.beta1) * gradients[k]
            self.v[k] = self.beta2 * self.v[k] + (1 - self.beta2) * (gradients[k] ** 2)
            
            m_hat = self.m[k] / (1 - self.beta1 ** self.t)
            v_hat = self.v[k] / (1 - self.beta2 ** self.t)
            
            self.params[k] = self.params[k] - self.lr * m_hat / (np.sqrt(v_hat) + self.epsilon)
        return self.params
```

### 6.4.1 Adam 優化器

Adam (Adaptive Moment Estimation) 結合了動量和 RMSprop 的優點：

1. **動量**：使用梯度的指數移動平均（一階矩估計）
2. **RMSprop**：使用梯度平方的指數移動平均（二階矩估計）
3. **偏差校正**：對初期估計進行偏差校正

Adam 的預設參數：
- β₁ = 0.9（一階矩估計的衰減率）
- β₂ = 0.999（二階矩估計的衰減率）
- ε = 10⁻⁸（數值穩定性）

### 6.4.2 其他優化器

- **RMSprop**：Adapts learning rate based on gradient magnitudes
- **AdaGrad**：對稀疏梯度效果好，但學習率會持續衰減
- **AdaDelta**：解決 AdaGrad 學習率衰減過快的問題
- **AdamW**：Adam 加上解耦的權重衰減

## 6.5 反傳遞演算法 (Backpropagation) 原理解說

反向傳播是訓練神經網路的核心演算法。它利用鏈式法則，從輸出層向輸入層計算梯度。

[程式檔案：06-4-backprop.py](../_code/06/06-4-backprop.py)

```python
import numpy as np

print("=" * 60)
print("Backpropagation Algorithm Explanation")
print("=" * 60)

print("""
Backpropagation is the algorithm used to compute gradients of the loss 
with respect to weights in neural networks using the chain rule.

Key Concepts:
1. Forward Pass: Compute output given input
2. Loss Computation: Measure prediction error
3. Backward Pass: Propagate error gradients back through network
4. Chain Rule: ∂L/∂w = ∂L/∂a * ∂a/∂z * ∂z/∂w
""")

class SimpleNeuralNetwork:
    def __init__(self):
        np.random.seed(42)
        self.W1 = np.random.randn(3, 2) * 0.5
        self.b1 = np.zeros((3, 1))
        self.W2 = np.random.randn(1, 3) * 0.5
        self.b2 = np.zeros((1, 1))
    
    def sigmoid(self, z):
        return 1 / (1 + np.exp(-np.clip(z, -500, 500)))
    
    def sigmoid_derivative(self, a):
        return a * (1 - a)
    
    def relu(self, z):
        return np.maximum(0, z)
    
    def relu_derivative(self, a):
        return (a > 0).astype(float)
    
    def forward(self, X):
        self.X = X
        self.z1 = self.W1 @ X + self.b1
        self.a1 = self.relu(self.z1)
        self.z2 = self.W2 @ self.a1 + self.b2
        self.a2 = self.sigmoid(self.z2)
        return self.a2
    
    def backward(self, y, learning_rate=0.1):
        m = y.shape[1]
        
        dz2 = self.a2 - y
        dW2 = (1/m) * dz2 @ self.a1.T
        db2 = (1/m) * np.sum(dz2, axis=1, keepdims=True)
        
        da1 = self.W2.T @ dz2
        dz1 = da1 * self.relu_derivative(self.a1)
        dW1 = (1/m) * dz1 @ self.X.T
        db1 = (1/m) * np.sum(dz1, axis=1, keepdims=True)
        
        self.W2 -= learning_rate * dW2
        self.b2 -= learning_rate * db2
        self.W1 -= learning_rate * dW1
        self.b1 -= learning_rate * db1
        
        return dW1, dW2
```

### 6.5.1 鏈式法則

假設我們有複合函數：L = f(g(h(x)))

根據鏈式法則：
```
∂L/∂x = ∂L/∂g * ∂g/∂h * ∂h/∂x
```

在神經網路中，每層的梯度都可以用類似的方式計算。

### 6.5.2 反向傳播的步驟

1. **前向傳播**：計算每層的輸出
2. **計算輸出層誤差**：δᴸ = ∂L/∂aᴸ * ∂aᴸ/∂zᴸ
3. **反向傳播誤差**：δˡ = (Wˡ⁺¹)ᵀ * δˡ⁺¹ * ∂aˡ/∂zˡ
4. **計算梯度**：∂L/∂Wˡ = δˡ * (aˡ⁻¹)ᵀ

## 6.6 數值梯度範例：(x-1)² + (y-2)² + (z-3)² 找最低點

數值梯度是一種驗證解析梯度的有效方法。它使用極限定義來近似計算梯度。

[程式檔案：06-5-numerical-gradient.py](../_code/06/06-5-numerical-gradient.py)

```python
import numpy as np

print("=" * 60)
print("Numerical Gradient Computation")
print("=" * 60)

def f(x, y, z):
    return (x - 1)**2 + (y - 2)**2 + (z - 3)**2

def analytical_gradient(x, y, z):
    df_dx = 2 * (x - 1)
    df_dy = 2 * (y - 2)
    df_dz = 2 * (z - 3)
    return np.array([df_dx, df_dy, df_dz])

def numerical_gradient(f, x, y, z, h=1e-5):
    grad = np.zeros(3)
    
    grad[0] = (f(x + h, y, z) - f(x - h, y, z)) / (2 * h)
    grad[1] = (f(x, y + h, z) - f(x, y - h, z)) / (2 * h)
    grad[2] = (f(x, y, z + h) - f(x, y, z - h)) / (2 * h)
    
    return grad
```

數值梯度的公式（中心差分法）：
```
f'(x) ≈ (f(x + h) - f(x - h)) / 2h
```

其中 h 通常選擇 10⁻⁵ 左右，太小會有數值誤差，太大則近似不準確。

## 6.7 手刻神經網路範例：參考 micrograd 架構

micrograd 是一個極簡的自動微分引擎，展示了現代深度學習框架的核心原理。

[程式檔案：06-6-micrograd.py](../_code/06/06-6-micrograd.py)

```python
import math
from collections import defaultdict

print("=" * 60)
print("Micrograd: Hand-crafted Neural Network")
print("=" * 60)

print("""
Micrograd is a tiny autograd engine that demonstrates the core ideas
behind automatic differentiation. It builds a computational graph
and computes gradients using the chain rule.

Key Components:
1. Value: A scalar with gradients
2. Operators: +, -, *, /, exp, log, relu, sigmoid, tanh
3. Backward: Computes gradients using chain rule
""")

class Value:
    def __init__(self, data, _children=(), _op=''):
        self.data = float(data)
        self.grad = 0.0
        self._backward = lambda: None
        self._prev = set(_children)
        self._op = _op
    
    def __repr__(self):
        return f"Value(data={self.data:.4f}, grad={self.grad:.4f})"
    
    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), '+')
        
        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward
        return out
    
    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), '*')
        
        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward
        return out
    
    def relu(self):
        out = Value(max(0, self.data), (self,), 'ReLU')
        
        def _backward():
            self.grad += (self.data > 0) * out.grad
        out._backward = _backward
        return out
    
    def backward(self):
        topo = []
        visited = set()
        
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)
        
        build_topo(self)
        self.grad = 1.0
        
        for v in reversed(topo):
            v._backward()
```

### 6.7.1 micrograd 的核心思想

1. **動態計算圖**：每次前向傳播時動態建立計算圖
2. **反向拓撲排序**：按照拓撲順序執行反向傳播
3. **梯度累積**：葉節點的梯度會累加

### 6.7.2 從 micrograd 到 PyTorch

micrograd 展示了自動微分的基本原理，而 PyTorch 在此基礎上增加了：
- GPU 加速
- 向量化計算
- 大規模並行計算
- 豐富的神經網路層

## 6.8 總結

本章介紹了梯度下降和反向傳播的核心概念：

| 主題 | 關鍵概念 |
|------|----------|
| 梯度下降 | 沿梯度反方向更新參數 |
| 學習率 | 控制更新步長 |
| 動量 | 加速收斂，減少震盪 |
| Adam | 自適應學習率優化器 |
| 反向傳播 | 鏈式法則計算梯度 |
| 數值梯度 | 驗證解析梯度的工具 |

這些概念是深度學習的基石。掌握它們後，我們就能理解更複雜的神經網路架構和訓練技巧。
