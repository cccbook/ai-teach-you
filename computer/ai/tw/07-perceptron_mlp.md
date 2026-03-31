# 第 7 章：從感知器到多層感知器

## 7.1 單層感知器 (Perceptron)

感知器是最早的神經網路模型，由 Frank Rosenblatt 於 1957 年提出。它是理解神經網路的基礎。

[程式檔案：07-1-perceptron.py](../_code/07/07-1-perceptron.py)

```python
import torch
import torch.nn as nn

print("=" * 50)
print("Single Layer Perceptron")
print("=" * 50)

class Perceptron(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(Perceptron, self).__init__()
        self.fc = nn.Linear(input_dim, output_dim)
    
    def forward(self, x):
        return self.fc(x)

model = Perceptron(2, 1)
print(f"\nModel Architecture:\n{model}")

x = torch.randn(4, 2)
y = model(x)
print(f"\nInput shape: {x.shape}")
print(f"Output shape: {y.shape}")
```

### 7.1.1 感知器的數學模型

```
y = f(w·x + b)
```

其中：
- x 是輸入向量
- w 是權重向量
- b 是偏置
- f 是激活函數（通常是符號函數或階梯函數）

### 7.1.2 感知器的限制

單層感知器只能解決線性可分的問題。例如：
- AND、OR 邏輯閘：線性可分，可以學習
- XOR 邏輯閘：非線性可分，無法學習

## 7.2 多層感知器 (MLP) 架構

多層感知器（Multi-Layer Perceptron, MLP）在輸入層和輸出層之間加入了一個或多個隱藏層，使得網路能夠學習非線性決策邊界。

[程式檔案：07-2-mlp.py](../_code/07/07-2-mlp.py)

```python
import torch
import torch.nn as nn

print("=" * 50)
print("Multi-Layer Perceptron (MLP)")
print("=" * 50)

class MLP(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(MLP, self).__init__()
        self.layer1 = nn.Linear(input_dim, hidden_dim)
        self.layer2 = nn.Linear(hidden_dim, hidden_dim)
        self.output = nn.Linear(hidden_dim, output_dim)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        x = self.relu(self.layer1(x))
        x = self.relu(self.layer2(x))
        return self.output(x)

model = MLP(784, 256, 10)
print(f"\nMLP Architecture:")
print(model)

print(f"\nTotal parameters: {sum(p.numel() for p in model.parameters()):,}")
```

### 7.2.1 MLP 的結構

```
輸入層 → 隱藏層1 → 隱藏層2 → ... → 輸出層
```

每層的輸出是：

```
h⁽ˡ⁾ = f(W⁽ˡ⁾ · h⁽ˡ⁻¹⁾ + b⁽ˡ⁾)
```

### 7.2.2 MLP 解決 XOR 問題

單層感知器無法解決 XOR 問題，但兩層 MLP 可以：

```
XOR = (x₁ AND NOT x₂) OR (NOT x₁ AND x₂)
```

透過隱藏層，MLP 可以學習到非線性的表示。

## 7.3 激活函數：Sigmoid, Tanh, ReLU, Leaky ReLU

激活函數為神經網路引入非線性，使得網路能夠學習複雜的模式。

[程式檔案：07-3-activation.py](../_code/07/07-3-activation.py)

```python
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import numpy as np

print("=" * 50)
print("Comparison of Activation Functions")
print("=" * 50)

x = torch.linspace(-5, 5, 100)

activations = {
    'Sigmoid': torch.sigmoid,
    'Tanh': torch.tanh,
    'ReLU': torch.relu,
    'Leaky ReLU': lambda x: torch.where(x > 0, x, 0.01 * x),
    'ELU': torch.nn.ELU(),
    'Swish': lambda x: x * torch.sigmoid(x),
    'Softmax': lambda x: torch.softmax(x, dim=0),
}

print("\nFunction formulas and characteristics:")
print("- Sigmoid: 1/(1+e^-x) - gradient vanishes for large |x|")
print("- Tanh: (e^x-e^-x)/(e^x+e^-x) - zero-centered")
print("- ReLU: max(0,x) - vanishing gradient solved, dying ReLU problem")
print("- Leaky ReLU: max(0.01x,x) -解決了dying ReLU")
print("- ELU: x if x>0, (e^x-1) if x<0 - smooth everywhere")
print("- Swish: x*sigmoid(x) - learnable, self-gated")
print("- Softmax: e^x_i/sum(e^x_j) - multi-class output")
```

### 7.3.1 各激活函數的特點

| 激活函數 | 公式 | 輸出範圍 | 優點 | 缺點 |
|----------|------|----------|------|------|
| Sigmoid | 1/(1+e⁻ˣ) | (0, 1) | 平滑可導 | 梯度消失 |
| Tanh | (eˣ-e⁻ˣ)/(eˣ+e⁻ˣ) | (-1, 1) | 零中心化 | 梯度消失 |
| ReLU | max(0, x) | [0, ∞) | 高效，緩解梯度消失 | Dying ReLU |
| Leaky ReLU | max(0.01x, x) | ℝ | 解決 Dying ReLU | - |
| ELU | x if x>0, α(eˣ-1) if x<0 | ℝ | 平滑，輸出接近零均值 | - |

### 7.3.2 梯度消失問題

當網路很深時，Sigmoid 和 Tanh 的梯度在反向傳播過程中會迅速變小，導致前面層的參數幾乎無法更新。ReLU 的出現有效地緩解了這個問題。

## 7.4 過擬合與正則化：Dropout, L1/L2

過擬合是機器學習中的常見問題：模型在訓練資料上表現很好，但在測試資料上表現較差。正則化是緩解過擬合的主要方法。

[程式檔案：07-4-regularization.py](../_code/07/07-4-regularization.py)

```python
import torch
import torch.nn as nn

print("=" * 50)
print("Regularization: Dropout, L1/L2")
print("=" * 50)

print("\n--- Dropout ---")
class NetWithDropout(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 256)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(256, 10)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        return self.fc2(x)
```

### 7.4.1 Dropout

Dropout 在訓練時隨機將部分神經元的輸出設為零：

```
訓練時：y = W · (x ⊙ mask) + b
測試時：y = W · x + b (使用完整網路)
```

mask 是一個伯努利隨機變數，每個元素以機率 p 被設為 1，以機率 1-p 被設為 0。

### 7.4.2 L2 正則化 (Weight Decay)

L2 正則化在損失函數中加入權重的平方和：

```
L_total = L_original + λ * Σw²
```

這鼓勵權重趨向較小的值，減少模型複雜度。

### 7.4.3 L1 正則化

L1 正則化使用權重的絕對值：

```
L_total = L_original + λ * Σ|w|
```

L1 正則化會產生稀疏的權重，某些權重會被推到 exactly 零。

## 7.5 Batch Normalization 與層標準化

Batch Normalization (BatchNorm) 是深度學習中的一項重要技術，它透過標準化每層的輸入來加速訓練和穩定梯度。

[程式檔案：07-5-batchnorm.py](../_code/07/07-5-batchnorm.py)

```python
import torch
import torch.nn as nn

print("=" * 50)
print("Batch Normalization")
print("=" * 50)

print("\n--- Manual Batch Norm ---")
def batch_norm_manual(x, gamma, beta, eps=1e-5):
    mean = x.mean(dim=0, keepdim=True)
    var = x.var(dim=0, keepdim=True, unbiased=False)
    x_norm = (x - mean) / torch.sqrt(var + eps)
    return gamma * x_norm + beta

print("\n--- PyTorch BatchNorm1d ---")
bn = nn.BatchNorm1d(10)
x = torch.randn(32, 10)
y = bn(x)
print(f"Before BN - mean: {x.mean().item():.4f}, std: {x.std().item():.4f}")
print(f"After BN  - mean: {y.mean().item():.4f}, std: {y.std().item():.4f}")
```

### 7.5.1 BatchNorm 的原理

對於一個 mini-batch B = {x₁, x₂, ..., xₘ}：

1. 計算均值：μ_B = (1/m) Σxᵢ
2. 計算方差：σ²_B = (1/m) Σ(xᵢ - μ_B)²
3. 標準化：x̂ᵢ = (xᵢ - μ_B) / √(σ²_B + ε)
4. 線性變換：yᵢ = γx̂ᵢ + β

其中 γ 和 β 是可學習的參數。

### 7.5.2 BatchNorm 的優點

1. **加速收斂**：減少內部協變量偏移 (Internal Covariate Shift)
2. **允許較高的學習率**：標準化使得梯度更穩定
3. **正則化效果**：每個 batch 的統計特性略有不同，引入了一些噪聲
4. **減少對初始化的敏感性**：輸入被標準化到穩定的分佈

### 7.5.3 層標準化 (Layer Normalization)

與 BatchNorm 不同，LayerNorm 在樣本維度上進行標準化：

```
μᵢ = (1/H) Σⱼ xᵢⱼ
σ²ᵢ = (1/H) Σⱼ (xᵢⱼ - μᵢ)²
```

LayerNorm 不依賴於 batch 大小，適合 RNN 等場景。

## 7.6 實作：MNIST 手寫數字分類

讓我們用 MLP 實作一個 MNIST 手寫數字分類器。

[程式檔案：07-6-mnist-mlp.py](../_code/07/07-6-mnist-mlp.py)

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

print("=" * 50)
print("MNIST Digit Classification with MLP")
print("=" * 50)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"\nUsing device: {device}")

class MNISTMLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(784, 256)
        self.bn1 = nn.BatchNorm1d(256)
        self.fc2 = nn.Linear(256, 128)
        self.bn2 = nn.BatchNorm1d(128)
        self.fc3 = nn.Linear(128, 10)
        self.dropout = nn.Dropout(0.3)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        x = self.flatten(x)
        x = self.relu(self.bn1(self.fc1(x)))
        x = self.dropout(x)
        x = self.relu(self.bn2(self.fc2(x)))
        x = self.dropout(x)
        return self.fc3(x)
```

### 7.6.1 MNIST 資料集

MNIST 包含 70,000 張 28×28 像素的手寫數字圖片：
- 訓練集：60,000 張
- 測試集：10,000 張
- 10 個類別（數字 0-9）

### 7.6.2 訓練流程

1. 載入資料並標準化
2. 建立模型、損失函數和優化器
3. 迭代訓練：
   - 前向傳播
   - 計算損失
   - 反向傳播
   - 更新參數
4. 在測試集上評估

### 7.6.3 注意事項

- 輸入需要標準化到 [0, 1] 或 [-1, 1] 範圍
- Dropout 在訓練時啟用，評估時禁用
- BatchNorm 在訓練時使用 batch 統計量，評估時使用移動平均

## 7.7 總結

本章介紹了從感知器到多層感知器的發展歷程：

| 主題 | 關鍵點 |
|------|--------|
| 感知器 | 單層，線性可分 |
| MLP | 多層，可學習非線性模式 |
| 激活函數 | 引入非線性，ReLU 最常用 |
| Dropout | 緩解過擬合 |
| L1/L2 | 權重衰減 |
| BatchNorm | 加速訓練，穩定梯度 |

MLP 是深度學習的基礎，雖然現在更流行 CNN 和 Transformer，但理解 MLP 對於學習更複雜的架構至關重要。
