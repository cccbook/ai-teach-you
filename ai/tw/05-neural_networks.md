# 第 5 章：神經網路與 PyTorch 套件

## 5.1 神經網路基本概念：神經元、權重、偏置

神經網路是受人腦啟發的計算模型。一個典型的神經網路由三層組成：
- **輸入層 (Input Layer)**：接收輸入資料
- **隱藏層 (Hidden Layer)**：進行特徵提取和轉換
- **輸出層 (Output Layer)**：產生最終預測結果

一個神經元的計算可以表示為：

```
y = f(Σ(wᵢ * xᵢ) + b)
```

其中：
- xᵢ 是輸入
- wᵢ 是權重
- b 是偏置
- f 是激活函數

### 5.1.1 PyTorch 簡介

PyTorch 是目前最流行的深度學習框架之一，由 Facebook AI Research 開發。它提供了：
- 強大的 GPU 加速計算能力
- 動態計算圖，方便調試
- 自動微分 (autograd) 系統
- 豐富的神經網路層和工具

## 5.2 PyTorch 張量 (Tensor) 操作

張量是 PyTorch 中的基本資料結構，可以理解為多維陣列。張量類似於 NumPy 的 ndarray，但可以在 GPU 上運算以加速計算。

[程式檔案：05-1-tensor-basics.py](../_code/05/05-1-tensor-basics.py)

```python
import torch
import numpy as np


def main():
    print("=" * 50)
    print("PyTorch Tensor Basics")
    print("=" * 50)

    print("\n1. Creating Tensors")
    print("-" * 30)
    
    scalar = torch.tensor(3.14)
    print(f"Scalar: {scalar}, shape: {scalar.shape}, dtype: {scalar.dtype}")
    
    vector = torch.tensor([1, 2, 3, 4, 5])
    print(f"Vector: {vector}, shape: {vector.shape}")
    
    matrix = torch.randn(3, 4)
    print(f"3x4 Matrix:\n{matrix}")
    
    tensor3d = torch.zeros(2, 3, 4)
    print(f"3D Tensor shape: {tensor3d.shape}")

    print("\n2. Tensor from NumPy")
    print("-" * 30)
    np_array = np.array([[1, 2], [3, 4]])
    torch_tensor = torch.from_numpy(np_array)
    print(f"NumPy: {np_array}")
    print(f"Torch: {torch_tensor}")

    print("\n3. Tensor Operations")
    print("-" * 30)
    a = torch.tensor([[1, 2], [3, 4]], dtype=torch.float32)
    b = torch.tensor([[5, 6], [7, 8]], dtype=torch.float32)
    
    print(f"a + b = \n{a + b}")
    print(f"a * b = \n{a * b}")
    print(f"a @ b (matrix multiply) = \n{a @ b}")
    print(f"a.sum() = {a.sum()}")
    print(f"a.mean() = {a.mean()}")

    print("\n4. Reshape & Squeeze")
    print("-" * 30)
    t = torch.randn(2, 3, 4)
    print(f"Original shape: {t.shape}")
    print(f"Reshape to (6, 4): {t.reshape(6, 4).shape}")
    print(f"Flatten: {t.flatten().shape}")

    print("\n5. Indexing")
    print("-" * 30)
    x = torch.tensor([[10, 20, 30], [40, 50, 60]])
    print(f"x[0] = {x[0]}")
    print(f"x[0, 1] = {x[0, 1]}")
    print(f"x[:, 1] = {x[:, 1]}")

    print("\n6. GPU/CPU Device")
    print("-" * 30)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Current device: {device}")
    tensor_cpu = torch.randn(3, 3)
    tensor_device = tensor_cpu.to(device)
    print(f"Tensor on {device}: {tensor_device.device}")


if __name__ == "__main__":
    main()
```

### 5.2.1 張量的常見創建方式

```python
# 從列表創建
x = torch.tensor([1, 2, 3])

# 從 NumPy 陣列創建
import numpy as np
arr = np.array([1, 2, 3])
x = torch.from_numpy(arr)

# 特殊矩陣
torch.zeros(3, 4)      # 零矩陣
torch.ones(3, 4)       # 全 1 矩陣
torch.eye(4)           # 單位矩陣
torch.randn(3, 4)      # 標準常態分佈隨機矩陣
torch.rand(3, 4)       # [0, 1) 均勻分佈隨機矩陣
```

### 5.2.2 GPU 加速

```python
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
x = x.to(device)  # 將張量移到 GPU
```

## 5.3 autograd 自動微分機制

自動微分 (Automatic Differentiation) 是深度學習框架的核心功能。PyTorch 的 autograd 模組可以自動計算張量的梯度。

[程式檔案：05-2-autograd.py](../_code/05/05-2-autograd.py)

```python
import torch


def main():
    print("=" * 50)
    print("PyTorch Autograd - Automatic Differentiation")
    print("=" * 50)

    print("\n1. Creating Tensors with requires_grad")
    print("-" * 30)
    x = torch.tensor(2.0, requires_grad=True)
    y = torch.tensor(3.0, requires_grad=True)
    print(f"x = {x}, y = {y}")
    print(f"x.requires_grad = {x.requires_grad}")

    print("\n2. Building Computation Graph")
    print("-" * 30)
    z = x * x + y * 3 + 1
    print(f"z = x² + 3y + 1 = {z}")
    print(f"z.grad_fn: {z.grad_fn}")

    print("\n3. Backward Pass (Compute Gradients)")
    print("-" * 30)
    z.backward()
    print(f"dz/dx = {x.grad}")
    print(f"dz/dy = {y.grad}")

    print("\n4. Manual Verification")
    print("-" * 30)
    print(f"dz/dx = 2x = {2 * x.item()}")
    print(f"dz/dy = 3")

    print("\n5. Gradient Accumulation (multiple backward)")
    print("-" * 30)
    a = torch.tensor(1.0, requires_grad=True)
    b = a * 2
    b.backward()
    print(f"First backward - grad: {a.grad}")
    a.grad = None
    b = a * 2
    b.backward()
    print(f"Second backward - grad: {a.grad}")

    print("\n6. Gradients with Multi-output")
    print("-" * 30)
    x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
    y = x * 2
    y.sum().backward()
    print(f"x = {x}")
    print(f"gradients: {x.grad}")

    print("\n7. Using torch.no_grad() for Inference")
    print("-" * 30)
    w = torch.tensor([1.0, 2.0], requires_grad=True)
    with torch.no_grad():
        prediction = w[0] * 5 + w[1] * 3
        print(f"Prediction (no grad): {prediction}")
    print(f"w.requires_grad: {w.requires_grad}")

    print("\n8. Using .detach() to Get Plain Tensor")
    print("-" * 30)
    x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
    y = x * 2
    y_detached = y.detach()
    print(f"Detached: {y_detached.requires_grad}")


if __name__ == "__main__":
    main()
```

### 5.3.1 autograd 的工作原理

PyTorch 會記錄每一個操作，建立一個動態計算圖。當呼叫 `.backward()` 時，PyTorch 會自動沿著計算圖反向傳播梯度。

```python
x = torch.tensor(2.0, requires_grad=True)
y = x ** 2 + 3 * x + 1
y.backward()  # 計算 dy/dx
print(x.grad)  # 2*x + 3 = 7
```

### 5.3.2 訓練與評估模式

在訓練時，我們需要計算梯度；在推理時，不需要計算梯度：

```python
model.train()   # 訓練模式
model.eval()    # 評估模式

with torch.no_grad():
    predictions = model(x)  # 不記錄梯度
```

## 5.4 建構第一個神經網路：nn.Module

`nn.Module` 是 PyTorch 中建構神經網路的基本類別。所有自定義的網路都應該繼承這個類別。

[程式檔案：05-3-nn-module.py](../_code/05/05-3-nn-module.py)

```python
import torch
import torch.nn as nn


def main():
    print("=" * 50)
    print("Building Neural Networks with nn.Module")
    print("=" * 50)

    print("\n1. Simple MLP (Multi-Layer Perceptron)")
    print("-" * 30)

    class SimpleNet(nn.Module):
        def __init__(self, input_dim=4, hidden_dim=8, output_dim=2):
            super().__init__()
            self.fc1 = nn.Linear(input_dim, hidden_dim)
            self.relu = nn.ReLU()
            self.fc2 = nn.Linear(hidden_dim, output_dim)

        def forward(self, x):
            x = self.fc1(x)
            x = self.relu(x)
            x = self.fc2(x)
            return x

    model = SimpleNet()
    print(model)
    print(f"\nTotal parameters: {sum(p.numel() for p in model.parameters())}")

    print("\n2. Forward Pass Demo")
    print("-" * 30)
    x = torch.randn(2, 4)
    output = model(x)
    print(f"Input shape: {x.shape}")
    print(f"Output shape: {output.shape}")
    print(f"Output: \n{output}")

    print("\n3. More Complex Network with Dropout & BatchNorm")
    print("-" * 30)

    class DeepNet(nn.Module):
        def __init__(self):
            super().__init__()
            self.layers = nn.Sequential(
                nn.Linear(10, 64),
                nn.BatchNorm1d(64),
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.Linear(64, 32),
                nn.ReLU(),
                nn.Linear(32, 5)
            )

        def forward(self, x):
            return self.layers(x)

    model2 = DeepNet()
    print(model2)

    print("\n4. Accessing Parameters")
    print("-" * 30)
    for name, param in model.named_parameters():
        print(f"{name}: shape {param.shape}")

    print("\n5. Training vs Eval Mode")
    print("-" * 30)
    model.eval()
    print("model.training:", model.training)
    print("After model.eval():", not model.training)

    print("\n6. Custom Activation Function")
    print("-" * 30)

    class Swish(nn.Module):
        def forward(self, x):
            return x * torch.sigmoid(x)

    custom_net = nn.Sequential(
        nn.Linear(3, 5),
        Swish(),
        nn.Linear(5, 1)
    )
    x = torch.randn(1, 3)
    out = custom_net(x)
    print(f"Custom Swish activation: {out}")

    print("\n7. Initialize Weights")
    print("-" * 30)
    print("Default weights sample (first layer):")
    print(model.fc1.weight[0, :5])


if __name__ == "__main__":
    main()
```

### 5.4.1 使用 nn.Sequential

對於簡單的網路，可以使用 `nn.Sequential` 快速建構：

```python
model = nn.Sequential(
    nn.Linear(10, 64),
    nn.ReLU(),
    nn.Linear(64, 1)
)
```

### 5.4.2 常用層

PyTorch 提供了豐富的神經網路層：
- **線性層**：`nn.Linear(in_features, out_features)`
- **卷積層**：`nn.Conv2d(in_channels, out_channels, kernel_size)`
- **循環層**：`nn.LSTM()`, `nn.GRU()`
- **正則化**：`nn.BatchNorm1d()`, `nn.Dropout()`
- **激活函數**：`nn.ReLU()`, `nn.Sigmoid()`, `nn.Tanh()`

## 5.5 資料集與 DataLoader

`DataLoader` 是 PyTorch 中用於批量載入資料的工具。它提供了：
- 批量訓練 (Batching)
- 打亂順序 (Shuffling)
- 多程序載入 (Multi-processing)
- 記憶體管理

[程式檔案：05-4-dataloader.py](../_code/05/05-4-dataloader.py)

```python
import torch
from torch.utils.data import Dataset, DataLoader


def main():
    print("=" * 50)
    print("DataLoader and Custom Datasets")
    print("=" * 50)

    print("\n1. Custom Dataset")
    print("-" * 30)

    class MyDataset(Dataset):
        def __init__(self, x_data, y_data):
            self.x = torch.tensor(x_data, dtype=torch.float32)
            self.y = torch.tensor(y_data, dtype=torch.float32)

        def __len__(self):
            return len(self.x)

        def __getitem__(self, idx):
            return self.x[idx], self.y[idx]

    X = [[i, i+1, i+2] for i in range(10)]
    y = [[i * 2] for i in range(10)]
    dataset = MyDataset(X, y)
    print(f"Dataset length: {len(dataset)}")
    print(f"First sample: {dataset[0]}")

    print("\n2. DataLoader with Batching")
    print("-" * 30)
    dataloader = DataLoader(dataset, batch_size=4, shuffle=True)

    for batch_idx, (batch_x, batch_y) in enumerate(dataloader):
        print(f"Batch {batch_idx}: x.shape={batch_x.shape}, y.shape={batch_y.shape}")
        print(f"  batch_x: {batch_x}")
        print(f"  batch_y: {batch_y.tolist()}")
        if batch_idx >= 1:
            break

    print("\n3. Using TensorDataset")
    print("-" * 30)
    from torch.utils.data import TensorDataset
    x = torch.randn(100, 5)
    y = torch.randn(100, 1)
    tensor_ds = TensorDataset(x, y)
    loader = DataLoader(tensor_ds, batch_size=10, shuffle=False)
    for bx, by in loader:
        print(f"Batch: x={bx.shape}, y={by.shape}")
        break

    print("\n4. DataLoader Options")
    print("-" * 30)
    loader = DataLoader(
        dataset,
        batch_size=4,
        shuffle=True,
        num_workers=0,
        drop_last=False
    )
    print(f"batch_size=4, shuffle=True, drop_last=False")

    print("\n5. Custom Dataset with Transform")
    print("-" * 30)

    class TransformedDataset(Dataset):
        def __init__(self, data, transform=None):
            self.data = data
            self.transform = transform

        def __len__(self):
            return len(self.data)

        def __getitem__(self, idx):
            sample = self.data[idx]
            if self.transform:
                sample = self.transform(sample)
            return sample

    data = [torch.tensor([i]) for i in range(5)]
    transform_ds = TransformedDataset(data, transform=lambda x: x * 2)
    print(f"Original: {data[2]}")
    print(f"After transform: {transform_ds[2]}")

    print("\n6. IterableDataset")
    print("-" * 30)

    class IterableData(torch.utils.data.IterableDataset):
        def __iter__(self):
            for i in range(8):
                yield torch.tensor([i]), torch.tensor([i * 10])

    iter_ds = IterableData()
    iter_loader = DataLoader(iter_ds, batch_size=3)
    for batch in iter_loader:
        print(f"Iterable batch: {batch}")
        break


if __name__ == "__main__":
    main()
```

### 5.5.1 自定義 Dataset

自定義 Dataset 需要實現三個方法：
- `__init__()`：初始化資料
- `__len__()`：返回資料集大小
- `__getitem__()`：返回單個樣本

### 5.5.2 DataLoader 參數

```python
loader = DataLoader(
    dataset,
    batch_size=32,      # 每批樣本數
    shuffle=True,        # 是否打亂順序
    num_workers=4,       # 載入程序的數量
    drop_last=False,     # 是否丟棄最後一批不完整的樣本
    pin_memory=True      # 是否將資料固定在記憶體中
)
```

## 5.6 訓練迴圈與反向傳播

一個完整的訓練迴圈包含以下步驟：
1. 前向傳播 (Forward Pass)
2. 計算損失 (Compute Loss)
3. 反向傳播 (Backward Pass)
4. 更新參數 (Update Parameters)

[程式檔案：05-5-training-loop.py](../_code/05/05-5-training-loop.py)

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader


def main():
    print("=" * 50)
    print("Complete Training Loop in PyTorch")
    print("=" * 50)

    torch.manual_seed(42)

    print("\n1. Prepare Data")
    print("-" * 30)
    n_samples = 200
    X = torch.randn(n_samples, 1) * 5
    y = 3 * X + 5 + torch.randn(n_samples, 1) * 2

    train_size = int(0.8 * n_samples)
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    train_ds = TensorDataset(X_train, y_train)
    test_ds = TensorDataset(X_test, y_test)

    train_loader = DataLoader(train_ds, batch_size=16, shuffle=True)
    test_loader = DataLoader(test_ds, batch_size=16)

    print(f"Training samples: {len(train_ds)}")
    print(f"Test samples: {len(test_ds)}")

    print("\n2. Define Model")
    print("-" * 30)

    class LinearRegression(nn.Module):
        def __init__(self):
            super().__init__()
            self.linear = nn.Linear(1, 1)

        def forward(self, x):
            return self.linear(x)

    model = LinearRegression()
    print(model)
    print(f"Initial weights: weight={model.linear.weight.item():.4f}, bias={model.linear.bias.item():.4f}")

    print("\n3. Define Loss and Optimizer")
    print("-" * 30)
    criterion = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01)
    print(f"Loss: MSE")
    print(f"Optimizer: SGD, lr=0.01")

    print("\n4. Training Loop")
    print("-" * 30)
    n_epochs = 20

    for epoch in range(n_epochs):
        model.train()
        train_loss = 0.0
        for batch_x, batch_y in train_loader:
            optimizer.zero_grad()
            predictions = model(batch_x)
            loss = criterion(predictions, batch_y)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()

        train_loss /= len(train_loader)

        if (epoch + 1) % 5 == 0:
            model.eval()
            with torch.no_grad():
                test_pred = model(X_test)
                test_loss = criterion(test_pred, y_test).item()
            print(f"Epoch {epoch+1}/{n_epochs} - Train Loss: {train_loss:.4f} - Test Loss: {test_loss:.4f}")

    print("\n5. Final Results")
    print("-" * 30)
    model.eval()
    with torch.no_grad():
        train_pred = model(X_train)
        test_pred = model(X_test)
        train_mse = criterion(train_pred, y_train).item()
        test_mse = criterion(test_pred, y_test).item()

    print(f"Final weight: {model.linear.weight.item():.4f}")
    print(f"Final bias: {model.linear.bias.item():.4f}")
    print(f"Train MSE: {train_mse:.4f}")
    print(f"Test MSE: {test_mse:.4f}")

    print("\n6. Save and Load Model")
    print("-" * 30)
    torch.save(model.state_dict(), "model.pth")
    print("Saved model.state_dict() to 'model.pth'")

    model2 = LinearRegression()
    model2.load_state_dict(torch.load("model.pth"))
    model2.eval()
    print("Loaded model from 'model.pth'")

    with torch.no_grad():
        pred = model2(torch.tensor([[5.0]]))
    print(f"Prediction for x=5: {pred.item():.4f}")


if __name__ == "__main__":
    main()
```

### 5.6.1 標準訓練迴圈

```python
for epoch in range(n_epochs):
    # 訓練階段
    model.train()
    for batch_x, batch_y in train_loader:
        optimizer.zero_grad()       # 梯度歸零
        predictions = model(batch_x) # 前向傳播
        loss = criterion(predictions, batch_y)  # 計算損失
        loss.backward()              # 反向傳播
        optimizer.step()            # 更新參數
    
    # 評估階段
    model.eval()
    with torch.no_grad():
        # ... 評估模型
```

### 5.6.2 模型保存與載入

```python
# 保存
torch.save(model.state_dict(), 'model.pth')

# 載入
model = MyModel()
model.load_state_dict(torch.load('model.pth'))
model.eval()
```

### 5.6.3 常用優化器

PyTorch 提供了多種優化器：
- `optim.SGD()`：隨機梯度下降
- `optim.Adam()`：Adam 優化器
- `optim.RMSprop()`：RMSprop 優化器
- `optim.AdamW()`：AdamW 優化器（帶權重衰減）

## 5.7 總結

本章介紹了 PyTorch 的基礎知識：

| 主題 | 核心概念 |
|------|----------|
| 張量 (Tensor) | 多維陣列，PyTorch 的基本資料結構 |
| autograd | 自動微分，計算梯度的核心機制 |
| nn.Module | 建構神經網路的基本類別 |
| DataLoader | 批量載入和管理資料的工具 |
| 訓練迴圈 | 前向傳播 → 計算損失 → 反向傳播 → 更新參數 |

掌握這些基礎知識後，我們就可以開始學習更複雜的神經網路架構和訓練技巧。在下一章中，我們將深入探討梯度下降演算法和反向傳播的原理。
