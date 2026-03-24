# 附錄 A：PyTorch 深度學習框架詳解

PyTorch 是目前最流行的深度學習框架之一，由 Facebook 的人工智慧研究團隊開發。本附錄將系統介紹 PyTorch 的核心概念、張量運算、模型建構、以及訓練技巧。

## A.1 PyTorch 與 TensorFlow 比較

PyTorch 和 TensorFlow 是目前最主流的兩大深度學習框架。

### A.1.1 框架特點對比

| 特性 | PyTorch | TensorFlow |
|------|---------|------------|
| 開發者 | Meta (Facebook) | Google |
| 動態計算圖 | 是 | 否 (TF 2.0 後支援 Eager Mode) |
| 靜態計算圖 | 透過 TorchScript | 原生支援 |
| 學習曲線 | 較平緩 | 較陡峭 |
| 部署工具 | TorchServe | TensorFlow Serving |
| 產業應用 | 研究為主 | 研究+部署並重 |
| GPU 支援 | CUDA 完善 | CUDA + TPU |

### A.1.2 PyTorch 的優勢

| 優勢 | 說明 |
|------|------|
| 動態圖 | 調試直觀，支援 Python 控制流 |
| Python 優先 | 與 Python 生態深度整合 |
| 研究友好 | 廣泛用於學術研究 |
| 易學易用 | API 設計優雅 |

### A.1.3 PyTorch 安裝

```bash
# 使用 pip 安裝
pip install torch torchvision torchaudio

# 使用 conda 安裝
conda install pytorch torchvision torchaudio -c pytorch

# 確認安裝
python -c "import torch; print(torch.__version__)"
```

## A.2 張量運算與 GPU 加速

張量 (Tensor) 是 PyTorch 中的核心數據結構，類似於 NumPy 的 ndarray，但支援 GPU 加速。

### A.2.1 張量創建

```python
import torch
import numpy as np

# 從 Python 列表創建
x = torch.tensor([1, 2, 3, 4, 5])
print(f"From list: {x}")

# 從 NumPy 數組創建
np_array = np.array([[1, 2], [3, 4]])
x = torch.from_numpy(np_array)
print(f"From numpy: {x}")

# 創建特定形狀的張量
zeros = torch.zeros(3, 4)      # 全零
ones = torch.ones(2, 3)       # 全一
rand = torch.rand(4, 5)       # 均匀分佈 [0, 1)
randn = torch.randn(3, 3)     # 標準正態分佈
empty = torch.empty(2, 2)     # 未初始化

# 創建特定數值範圍
arange = torch.arange(0, 10, 2)      # [0, 2, 4, 6, 8]
linspace = torch.linspace(0, 1, 5)    # [0, 0.25, 0.5, 0.75, 1]
```

### A.2.2 張量屬性

```python
x = torch.randn(3, 4, 5)

print(f"Shape: {x.shape}")      # torch.Size([3, 4, 5])
print(f"dtype: {x.dtype}")      # torch.float32
print(f"device: {x.device}")    # cpu
print(f"ndim: {x.ndim}")        # 3 (維度數)
print(f"numel: {x.numel()}")    # 60 (總元素數)
```

### A.2.3 張量運算

```python
a = torch.tensor([[1, 2], [3, 4]])
b = torch.tensor([[5, 6], [7, 8]])

# 基本運算
c = a + b          # 加法
c = torch.add(a, b) # 等效寫法
c = a - b          # 減法
c = a * b          # 逐元素乘法
c = a / b          # 逐元素除法
c = a @ b          # 矩陣乘法

# 求和、平均、最大、最小
total = a.sum()
mean = a.mean()
max_val = a.max()
min_val = a.min()

# 索引和切片
row = a[0, :]      # 第一行
col = a[:, 1]      # 第二列
sub = a[0:2, 0:2] # 子矩陣

# 形狀變換
x = torch.randn(12)
x = x.view(3, 4)  # 改變形狀 (共享內存)
x = x.reshape(6, 2) # 類似 view，但可能複製數據
x = x.squeeze()    # 移除維度為 1 的軸
x = x.unsqueeze(0) # 添加維度

# 轉置
x = x.t()          # 2D 轉置
x = x.transpose(0, 1) # 任意軸交換
x = x.permute(2, 0, 1) # 任意重排列
```

### A.2.4 GPU 加速

```python
# 檢查 GPU 是否可用
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU count: {torch.cuda.device_count()}")
if torch.cuda.is_available():
    print(f"GPU name: {torch.cuda.get_device_name(0)}")

# 張量移到 GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
x = torch.randn(1000, 1000)
x_gpu = x.to(device)  # 或 x.cuda()

# 模型移到 GPU
model = MyModel()
model = model.to(device)

# 多 GPU 訓練
if torch.cuda.device_count() > 1:
    model = torch.nn.DataParallel(model)
```

## A.3 nn.Module 與模型建構

`nn.Module` 是 PyTorch 中所有神經網路模組的基類。

### A.3.1 簡單模型範例

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class SimpleNN(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)
    
    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

# 使用模型
model = SimpleNN(input_size=784, hidden_size=256, num_classes=10)
print(model)

# 查看模型參數
for name, param in model.named_parameters():
    print(f"{name}: {param.shape}")
```

### A.3.2 常用層

| 層 | 說明 |
|------|------|
| nn.Linear | 全連接層 |
| nn.Conv2d | 2D 卷積層 |
| nn.Conv1d | 1D 卷積層 |
| nn.LSTM | 長短期記憶網路 |
| nn.GRU | 門控循環單元 |
| nn.BatchNorm2d | 批量標準化 |
| nn.Dropout | Dropout 正則化 |
| nn.Embedding | 詞嵌入層 |
| nn.MultiheadAttention | 多頭注意力 |

### A.3.3 卷積神經網路範例

```python
class CNN(nn.Module):
    def __init__(self, num_classes=10):
        super(CNN, self).__init__()
        
        # 卷積層 1
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.pool1 = nn.MaxPool2d(2, 2)
        
        # 卷積層 2
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        self.pool2 = nn.MaxPool2d(2, 2)
        
        # 全連接層
        self.fc1 = nn.Linear(64 * 8 * 8, 256)
        self.fc2 = nn.Linear(256, num_classes)
        
        self.dropout = nn.Dropout(0.5)
    
    def forward(self, x):
        # Conv Block 1
        x = self.pool1(F.relu(self.bn1(self.conv1(x))))
        
        # Conv Block 2
        x = self.pool2(F.relu(self.bn2(self.conv2(x))))
        
        # Flatten
        x = x.view(x.size(0), -1)
        
        # FC
        x = self.dropout(F.relu(self.fc1(x)))
        x = self.fc2(x)
        
        return x
```

### A.3.4 Transformer 模型

```python
class TransformerClassifier(nn.Module):
    def __init__(self, vocab_size, d_model, num_heads, num_layers, num_classes):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.pos_encoding = PositionalEncoding(d_model)
        
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model, 
            nhead=num_heads, 
            dim_feedforward=d_model * 4
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers)
        
        self.fc = nn.Linear(d_model, num_classes)
    
    def forward(self, x):
        # x: [batch_size, seq_len]
        x = self.embedding(x) * math.sqrt(self.d_model)
        x = self.pos_encoding(x)
        
        # x: [seq_len, batch_size, d_model]
        x = x.transpose(0, 1)
        x = self.transformer(x)
        
        # 取最後一個位置
        x = x[-1, :, :]
        
        return self.fc(x)
```

## A.4 訓練技巧與除錯

### A.4.1 完整訓練流程

```python
import torch.optim as optim

def train_model(model, train_loader, val_loader, epochs=10, lr=0.001):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    
    # 損失函數
    criterion = nn.CrossEntropyLoss()
    
    # 優化器
    optimizer = optim.Adam(model.parameters(), lr=lr)
    
    # 學習率調整
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.1)
    
    for epoch in range(epochs):
        # 訓練階段
        model.train()
        train_loss = 0.0
        train_correct = 0
        train_total = 0
        
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            _, predicted = outputs.max(1)
            train_total += labels.size(0)
            train_correct += predicted.eq(labels).sum().item()
        
        scheduler.step()
        
        # 驗證階段
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                
                val_loss += loss.item()
                _, predicted = outputs.max(1)
                val_total += labels.size(0)
                val_correct += predicted.eq(labels).sum().item()
        
        print(f"Epoch {epoch+1}/{epochs}")
        print(f"Train Loss: {train_loss/len(train_loader):.4f}, "
              f"Train Acc: {100*train_correct/train_total:.2f}%")
        print(f"Val Loss: {val_loss/len(val_loader):.4f}, "
              f"Val Acc: {100*val_correct/val_total:.2f}%")
```

### A.4.2 常用優化器

| 優化器 | 說明 |
|--------|------|
| SGD | 隨機梯度下降，可帶動量 |
| Adam | 自適應學習率，效果好 |
| AdamW | Adam + 權重衰減 |
| RMSprop | 自適應學習率，適合 RNN |
| Adagrad | 適合稀疏數據 |

### A.4.3 正則化技巧

```python
# 1. Dropout
model = nn.Sequential(
    nn.Linear(784, 256),
    nn.ReLU(),
    nn.Dropout(0.5),  # 訓練時隨機丢弃 50%
    nn.Linear(256, 10)
)

# 2. L2 正則化 (Weight Decay)
optimizer = torch.optim.Adam(model.parameters(), weight_decay=0.01)

# 3. Batch Normalization
model = nn.Sequential(
    nn.Linear(784, 256),
    nn.BatchNorm1d(256),
    nn.ReLU()
)

# 4. Early Stopping
best_val_loss = float('inf')
patience = 5
counter = 0

for epoch in range(epochs):
    # 訓練...
    
    if val_loss < best_val_loss:
        best_val_loss = val_loss
        counter = 0
        # 保存最佳模型
        torch.save(model.state_dict(), 'best_model.pth')
    else:
        counter += 1
        if counter >= patience:
            print("Early stopping!")
            break
```

### A.4.4 模型保存與載入

```python
# 保存整個模型
torch.save(model, 'model.pth')
model = torch.load('model.pth')

# 僅保存參數 (推薦)
torch.save(model.state_dict(), 'model_weights.pth')
model.load_state_dict(torch.load('model_weights.pth'))

# 斷點保存
checkpoint = {
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss,
}
torch.save(checkpoint, 'checkpoint.pth')

# 恢復訓練
checkpoint = torch.load('checkpoint.pth')
model.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
epoch = checkpoint['epoch']
```

### A.4.5 除錯技巧

```python
# 1. 使用 torch.set_printoptions 調整輸出
torch.set_printoptions(precision=4, linewidth=200)

# 2. 梯度裁剪
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

# 3. 檢查梯度
for name, param in model.named_parameters():
    if param.grad is not None:
        print(f"{name}: grad norm = {param.grad.norm()}")

# 4. 記憶體監控
print(f"GPU memory allocated: {torch.cuda.memory_allocated()/1e9:.2f} GB")
print(f"GPU memory cached: {torch.cuda.memory_reserved()/1e9:.2f} GB")

# 5. 使用 autograd 檢查
x = torch.randn(5, requires_grad=True)
y = x * 2
print(f"Grad_fn: {y.grad_fn}")  # MulBackward0
```

### A.4.6 GPU 訓練最佳化

```python
# 1. 資料並行
model = nn.DataParallel(model)

# 2. 混合精度訓練
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

for inputs, labels in train_loader:
    inputs, labels = inputs.cuda(), labels.cuda()
    
    optimizer.zero_grad()
    
    with autocast():
        outputs = model(inputs)
        loss = criterion(outputs, labels)
    
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()

# 3. 記憶體效率技巧
torch.backends.cudnn.benchmark = True  # 自動選擇最快算法
model.eval()  # 評估模式
with torch.no_grad():  # 不計算梯度
    # 推理
```

## A.5 總結

| 主題 | 關鍵點 |
|------|--------|
| 張量運算 | 創建、索引、形狀變換、GPU 移動 |
| 模型建構 | nn.Module、forward 方法、常用層 |
| 訓練流程 | 損失函數、優化器、訓練循環 |
| 實用技巧 | 保存載入、除錯、正則化 |

PyTorch 以其動態計算圖和直觀的 API，成為深度學習研究和開發的首選框架。掌握 PyTorch 的核心概念和技巧，將使你能夠高效地實現和實驗各種深度學習模型。
