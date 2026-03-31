# 第 8 章：卷積神經網路 (CNN)

卷積神經網路 (Convolutional Neural Network, CNN) 是深度學習在電腦視覺領域的重大突破。與傳統的全連接神經網路不同，CNN 利用卷積運算來有效處理圖像資料，能夠自動學習空間層次化的特徵。本章將介紹 CNN 的核心組件，包括卷積層、池化層，以及經典的 CNN 架構。

## 8.1 卷積層與卷積運算

卷積層是 CNN 的核心組件，它透過卷積運算在輸入圖像上滑動卷積核（kernel），提取各種特徵。卷積核是一個小的矩陣（例如 3×3 或 5×5），它會與輸入圖像的局部區域進行元素乘法並求和。

[程式檔案：08-1-convolution.py](../_code/08/08-1-convolution.py)

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

print("=" * 60)
print("08-1: Convolution Operation")
print("=" * 60)

batch_size = 1
in_channels = 1
height, width = 5, 5
out_channels = 1
kernel_size = 3

input_tensor = torch.randn(batch_size, in_channels, height, width)
kernel = torch.randn(out_channels, in_channels, kernel_size, kernel_size)

print(f"\nInput shape: {input_tensor.shape}")
print(f"Kernel shape: {kernel.shape}")

conv = nn.Conv2d(in_channels, out_channels, kernel_size, bias=False)
conv.weight.data = kernel

output = conv(input_tensor)

print(f"\nOutput shape: {output.shape}")
print(f"\nInput tensor:\n{input_tensor.squeeze()}")
print(f"\nKernel:\n{kernel.squeeze()}")
print(f"\nConvolution output:\n{output.squeeze()}")
```

### 8.1.1 卷積運算的原理

卷積運算可以理解為一個卷積核在輸入圖像上滑動，對每個位置計算局部加权和：

```
輸出[i,j] = Σₖ Σₗ 輸入[i+k, j+l] × 卷積核[k,l]
```

這個過程類似於用放大鏡在圖像上逐處觀察，每個位置都提取一種特定的局部特徵。

### 8.1.2 卷積層的關鍵參數

| 參數 | 說明 | 影響 |
|------|------|------|
| Kernel Size | 卷積核大小 | 較大的核能捕捉更大範圍的特徵 |
| Stride | 滑動步長 | 步長越大，輸出越小 |
| Padding | 邊緣填充 | 保持空間尺寸，控制輸出大小 |
| In/Out Channels | 輸入/輸出通道數 | 決定特徵圖的數量和深度 |

### 8.1.3 手動卷積運算

讓我們驗證 PyTorch 卷積的結果是否與手動計算一致：

```python
print("\n--- Manual Convolution ---")
input_np = input_tensor.squeeze().numpy()
kernel_np = kernel.squeeze().numpy()
manual_output = torch.zeros(3, 3)
for i in range(3):
    for j in range(3):
        manual_output[i, j] = torch.sum(
            input_np[i:i+3, j:j+3] * kernel_np
        )
print(f"Manual convolution result:\n{manual_output}")
```

### 8.1.4 多通道輸入

現實中的圖像通常有多個通道（如 RGB 圖像有三個通道）。多通道卷積將每個通道的特徵圖與對應的卷積核進行卷積，然後求和：

```python
print("\n--- Multiple Channels ---")
input_multi = torch.randn(1, 3, 5, 5)
conv_multi = nn.Conv2d(3, 8, 3)
output_multi = conv_multi(input_multi)
print(f"Input (3 channels): {input_multi.shape}")
print(f"Output (8 channels): {output_multi.shape}")
print(f"Number of parameters: {sum(p.numel() for p in conv_multi.parameters())}")
```

## 8.2 池化層 (Pooling)：Max Pooling, Average Pooling

池化層是 CNN 中另一個重要的組件，它用於減少特徵圖的空間尺寸，同時保留最重要的特徵資訊。池化操作在每個局部區域內進行，常見的有最大池化和平均池化。

[程式檔案：08-2-pooling.py](../_code/08/08-2-pooling.py)

```python
import torch
import torch.nn as nn

print("=" * 60)
print("08-2: Pooling Operations")
print("=" * 60)

input_tensor = torch.randn(1, 1, 4, 4)
print(f"\nInput shape: {input_tensor.shape}")
print(f"Input tensor:\n{input_tensor.squeeze()}")

print("\n--- Max Pooling ---")
max_pool = nn.MaxPool2d(kernel_size=2)
output_max = max_pool(input_tensor)
print(f"MaxPool2d(2x2): {output_max.shape}")
print(f"Output:\n{output_max.squeeze()}")
```

### 8.2.1 最大池化 (Max Pooling)

最大池化在每個池化窗口中取最大值，這有助於保留最顯著的特征，例如邊緣和角落：

```
┌─────────┬─────────┐
│  1    3 │  2    8 │     Max Pooling 2x2
├─────────┼─────────┤      →  6    9
│  4    6 │  5    9 │
└─────────┴─────────┘
```

### 8.2.2 平均池化 (Average Pooling)

平均池化計算每個窗口內的平均值，這會產生更平滑的特徵表示：

```python
print("\n--- Average Pooling ---")
avg_pool = nn.AvgPool2d(kernel_size=2)
output_avg = avg_pool(input_tensor)
print(f"AvgPool2d(2x2): {output_avg.shape}")
print(f"Output:\n{output_avg.squeeze()}")
```

### 8.2.3 全域池化 (Global Pooling)

全域池化將整個特徵圖合併成一個值，常用於將 CNN 的特徵圖轉換為固定長度的向量，以便連接到全連接層：

```python
print("\n--- Global Pooling ---")
global_max = nn.AdaptiveMaxPool2d(1)
global_avg = nn.AdaptiveAvgPool2d(1)
print(f"AdaptiveMaxPool2d(1): {global_max(input_tensor).shape}")
print(f"AdaptiveAvgPool2d(1): {global_avg(input_tensor).shape}")
```

### 8.2.4 池化層的作用

1. **降低維度**：減少特徵圖的尺寸，降低計算量
2. **特徵不變性**：對小的平移和變換具有魯棒性
3. **防止過擬合**：減少參數數量，提供正則化效果
4. **擴大感受野**：讓後續層能看到更大的輸入區域

## 8.3 經典 CNN 架構：LeNet, AlexNet, VGG, ResNet

多年來，研究者提出了許多經典的 CNN 架構，它們在 ImageNet 競賽中取得了突破性成果。讓我們逐一介紹這些重要的架構。

### 8.3.1 LeNet-5：第一個成功的 CNN

LeNet-5 由 Yann LeCun 等人於 1998 年提出，是第一個成功應用於手寫數字識別的 CNN 架構。

[程式檔案：08-3-lenet.py](../_code/08/08-3-lenet.py)

```python
import torch
import torch.nn as nn

print("=" * 60)
print("08-3: LeNet-5 Architecture")
print("=" * 60)

class LeNet5(nn.Module):
    def __init__(self, num_classes=10):
        super(LeNet5, self).__init__()
        self.conv1 = nn.Conv2d(1, 6, 5, padding=2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, num_classes)
        self.pool = nn.AvgPool2d(2, 2)
        self.tanh = nn.Tanh()

    def forward(self, x):
        x = self.pool(self.tanh(self.conv1(x)))
        x = self.pool(self.tanh(self.conv2(x)))
        x = x.view(x.size(0), -1)
        x = self.tanh(self.fc1(x))
        x = self.tanh(self.fc2(x))
        x = self.fc3(x)
        return x

model = LeNet5()
print(f"\nLeNet-5 Architecture:")
print(model)
```

LeNet-5 的架構特點：
- 使用平均池化
- 激活函數為 Tanh
- 兩個卷積層和三個全連接層
- 參數量約 60,000 個

### 8.3.2 AlexNet：深度學習的復興

AlexNet 由 Alex Krizhevsky 等人於 2012 年提出，在 ImageNet 競賽中以壓倒性優勢獲勝，被譽為深度學習革命的起點。

[程式檔案：08-4-alexnet.py](../_code/08/08-4-alexnet.py)

```python
import torch
import torch.nn as nn

print("=" * 60)
print("08-4: AlexNet Architecture")
print("=" * 60)

class AlexNet(nn.Module):
    def __init__(self, num_classes=1000):
        super(AlexNet, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, 11, stride=4, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(3, stride=2),
            
            nn.Conv2d(64, 192, 5, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(3, stride=2),
            
            nn.Conv2d(192, 384, 3, padding=1),
            nn.ReLU(inplace=True),
            
            nn.Conv2d(384, 256, 3, padding=1),
            nn.ReLU(inplace=True),
            
            nn.Conv2d(256, 256, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(3, stride=2),
        )
        
        self.avgpool = nn.AdaptiveAvgPool2d((6, 6))
        
        self.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(256 * 6 * 6, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Linear(4096, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x
```

AlexNet 的創新之處：
- 使用 ReLU 激活函數（比 Tanh 快很多）
- 使用 Dropout 防止過擬合
- 使用 GPU 加速訓練
- 數據增強（隨機裁剪、翻轉）
- 局部響應標準化 (LRN)

### 8.3.3 ResNet：殘差連接的突破

ResNet (Residual Network) 由微軟研究院於 2015 年提出，透過殘差連接解決了深度網路的梯度消失問題，使得訓練數百層的網路成為可能。

[程式檔案：08-5-resnet.py](../_code/08/08-5-resnet.py)

```python
import torch
import torch.nn as nn

print("=" * 60)
print("08-5: ResNet Architecture")
print("=" * 60)

class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super(ResidualBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, 3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, 3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, 1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )

    def forward(self, x):
        out = torch.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        out = torch.relu(out)
        return out
```

### 8.3.4 殘差連接的原理

殘差連接的核心思想是讓網路學習殘差（輸入與輸出之間的差異），而不是直接學習完整的映射：

```
輸出 = F(x) + x
```

其中 F(x) 是網路學習的殘差映射，x 是捷徑連接。這種設計使得即使網路很深，梯度也能夠直接流向淺層，緩解了梯度消失問題。

## 8.4 遷移學習 (Transfer Learning) 與微調

遷移學習是深度學習中的一項重要技術，它利用在大規模資料集（如 ImageNet）上預訓練好的模型，作為新任務的起點。這種方法特別適用于資料量較少的場景。

[程式檔案：08-6-transfer-learning.py](../_code/08/08-6-transfer-learning.py)

```python
import torch
import torch.nn as nn

print("=" * 60)
print("08-6: Transfer Learning and Fine-Tuning")
print("=" * 60)

print("\n--- Loading Pretrained Model ---")
model = nn.Sequential(
    nn.Conv2d(3, 64, 3, padding=1),
    nn.ReLU(),
    nn.AdaptiveAvgPool2d((1, 1)),
    nn.Flatten(),
    nn.Linear(64, 10)
)

print("Created a dummy model (simulating pretrained)")

print("\n--- Freezing Layers ---")
for param in model[:3].parameters():
    param.requires_grad = False

print("Frozen first 3 layers (conv, relu, pool)")
```

### 8.4.1 遷移學習的策略

根據資料量和任務相似度，可以採用不同的策略：

| 策略 | 適用場景 | 方法 |
|------|----------|------|
| 特徵提取 | 資料少，任務相似 | 凍結預訓練層，只訓練新添加的分類器 |
| 部分微調 | 資料中等 | 凍結淺層，微調深層 |
| 完全微調 | 資料充足 | 所有層都進行微調 |

### 8.4.2 微調的實作

```python
print("\n--- Fine-Tuning Strategy ---")
def apply_fine_tuning(model, strategy='full'):
    if strategy == 'full':
        for param in model.parameters():
            param.requires_grad = True
    elif strategy == 'classifier':
        for param in model[:-1].parameters():
            param.requires_grad = False
    elif strategy == 'partial':
        layers_to_freeze = list(model.children())[:3]
        for layer in layers_to_freeze:
            for param in layer.parameters():
                param.requires_grad = False
    return model
```

### 8.4.3 使用預訓練模型

PyTorch 的 torchvision 提供了多種預訓練模型：

```python
print("\n--- Using torchvision models ---")
try:
    from torchvision.models import resnet18, ResNet18_Weights
    model_resnet = resnet18(weights=ResNet18_Weights.DEFAULT)
    print(f"ResNet18 loaded: {sum(p.numel() for p in model_resnet.parameters()):,} params")
    
    model_resnet.fc = nn.Linear(512, 10)
    print("Replaced final layer for 10-class classification")
except Exception as e:
    print(f"Note: {e}")
```

### 8.4.4 資料增強

遷移學習中常用的資料增強策略：

```python
print("\n--- Data Augmentation for Transfer Learning ---")
from torchvision import transforms
train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])
```

## 8.5 目標檢測：YOLO, R-CNN 系列

目標檢測是電腦視覺中的核心任務之一，不僅要識別圖像中的物體類別，還要定位它們的位置。近年來，出現了許多優秀的目標檢測演算法。

### 8.5.1 兩階段檢測器：R-CNN 系列

R-CNN 系列採用「先候選再分類」的策略：

1. **R-CNN**：使用 Selective Search 產生候選區域，對每個區域進行 CNN 特徵提取和分類
2. **Fast R-CNN**：共享卷積計算，所有候選區域共享特徵圖
3. **Faster R-CNN**：用區域提議網路 (RPN) 替代 Selective Search

### 8.5.2 單階段檢測器：YOLO

YOLO (You Only Look Once) 將目標檢測問題重新定義為單次回歸問題，直接從完整圖像預測邊界框和類別：

```
輸入圖像 → 網路 → 邊界框 + 類別概率
```

YOLO 的優點：
- 速度快，適合即時應用
- 端到端訓練
- 全域上下文資訊

### 8.5.3 主流方法的比較

| 方法 | 速度 | 精度 | 典型應用 |
|------|------|------|----------|
| R-CNN | 慢 | 高 | 精確檢測 |
| Fast R-CNN | 中 | 高 | 平衡場景 |
| Faster R-CNN | 中 | 很高 | 工業應用 |
| YOLO | 快 | 中高 | 即時應用 |
| SSD | 快 | 中高 | 邊緣設備 |

## 8.6 實作：CIFAR-10 影像分類

讓我們用 CNN 實作一個 CIFAR-10 影像分類器。

[程式檔案：08-7-cifar10-cnn.py](../_code/08/08-7-cifar10-cnn.py)

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms

print("=" * 60)
print("08-7: CIFAR-10 Classification")
print("=" * 60)

class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super(SimpleCNN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(32, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Dropout(0.25),
            
            nn.Conv2d(32, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Conv2d(64, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Dropout(0.25),
            
            nn.Conv2d(64, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Conv2d(128, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Dropout(0.25),
        )
        
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 4 * 4, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x
```

### 8.6.1 CIFAR-10 資料集

CIFAR-10 包含 60,000 張 32×32 像素的彩色圖像，分為 10 個類別：
- 飛機、汽車、鳥、貓、鹿
- 狗、青蛙、馬、船、卡車

### 8.6.2 資料預處理

```python
print("\n--- Data Transforms ---")
train_transform = transforms.Compose([
    transforms.RandomCrop(32, padding=4),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2470, 0.2435, 0.2616))
])

test_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2470, 0.2435, 0.2616))
])
```

### 8.6.3 訓練配置

```python
print("\n--- Training Configuration ---")
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.5)

print(f"Optimizer: Adam(lr=0.001)")
print(f"Scheduler: StepLR(step_size=10, gamma=0.5)")
print(f"Criterion: CrossEntropyLoss")
```

### 8.6.4 訓練迴圈

```python
print("\n--- Simulated Training Loop (1 epoch) ---")
x = torch.randn(4, 3, 32, 32)
y = torch.randint(0, 10, (4,))

optimizer.zero_grad()
outputs = model(x)
loss = criterion(outputs, y)
loss.backward()
optimizer.step()

print(f"Batch input: {x.shape}")
print(f"Batch output: {outputs.shape}")
print(f"Loss: {loss.item():.4f}")
```

## 8.7 總結

本章介紹了卷積神經網路的核心概念和經典架構：

| 主題 | 關鍵點 |
|------|--------|
| 卷積層 | 局部連接、權重共享、特徵提取 |
| 池化層 | Max/Average Pooling、降維、不變性 |
| LeNet-5 | 第一個成功的 CNN |
| AlexNet | 深度學習革命的起點 |
| ResNet | 殘差連接解決梯度消失 |
| 遷移學習 | 預訓練模型加速開發 |
| 目標檢測 | R-CNN、YOLO 等演算法 |

CNN 的發明徹底改變了電腦視覺領域，使得影像分類、物體檢測、語義分割等任務達到了前所未有的精度。在下一章中，我們將介紹另一種重要的神經網路架構：循環神經網路 (RNN)，它專門用於處理序列資料。
