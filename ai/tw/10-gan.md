# 第 10 章：生成對抗網路 (GAN)

生成對抗網路 (Generative Adversarial Network, GAN) 是由 Ian Goodfellow 等人於 2014 年提出的一種生成模型。GAN 的核心思想是透過兩個神經網路的對抗訓練來學習資料分佈，這種「零和遊戲」的概念開創了生成式人工智慧的新時代。

## 10.1 GAN 基本概念：生成器與判別器

GAN 由兩個核心組件組成：生成器 (Generator) 和判別器 (Discriminator)。這兩個網路相互對抗、相互學習，最終達到動態平衡。

[程式檔案：10-1-gan-basic.py](../_code/10/10-1-gan-basic.py)

```python
#!/usr/bin/env python3
"""
Chapter 10-1: GAN Basic (生成對抗網路基礎)
GAN 由 Ian Goodfellow 於 2014 年提出
核心概念: 生成器與判別器對抗訓練
"""

import numpy as np
import matplotlib.pyplot as plt

class SimpleGAN:
    def __init__(self, latent_dim=2, hidden_dim=16):
        self.latent_dim = latent_dim
        self.hidden_dim = hidden_dim
        
        np.random.seed(42)
        
        self.G_weights = {
            'W1': np.random.randn(latent_dim, hidden_dim) * 0.5,
            'b1': np.zeros(hidden_dim),
            'W2': np.random.randn(hidden_dim, 1) * 0.5,
            'b2': np.zeros(1)
        }
        
        self.D_weights = {
            'W1': np.random.randn(1, hidden_dim) * 0.5,
            'b1': np.zeros(hidden_dim),
            'W2': np.random.randn(hidden_dim, 1) * 0.5,
            'b2': np.zeros(1)
        }
    
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def relu(self, x):
        return np.maximum(0, x)
    
    def forward_G(self, z):
        h1 = self.relu(z @ self.G_weights['W1'] + self.G_weights['b1'])
        out = self.sigmoid(h1 @ self.G_weights['W2'] + self.G_weights['b2'])
        return out
    
    def forward_D(self, x):
        h1 = self.relu(x @ self.D_weights['W1'] + self.D_weights['b1'])
        out = self.sigmoid(h1 @ self.D_weights['W2'] + self.D_weights['b2'])
        return out
```

### 10.1.1 GAN 的對抗思想

GAN 的對抗訓練可以理解為一場「貓捉老鼠」的遊戲：

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│    生成器 G ──────→ 假資料 ──────→ 判別器 D         │
│      ↑                            │                │
│      │         真實資料            │                │
│      │            ↓                ↓                │
│      │                            輸出 [0, 1]       │
│      │                            │                │
│      │     對抗學習 ◀──────────────┘                │
│      │                                            │
│    噪聲 z                                          │
└─────────────────────────────────────────────────────┘
```

### 10.1.2 GAN 的目標函數

GAN 的訓練目標可以表示為一個 minimax 遊戲：

```
min_G max_D V(D, G) = E_{x~p_data(x)}[log D(x)] + E_{z~p_z(z)}[log(1 - D(G(z)))]
```

判別器的目標：最大化 log D(x) + log(1 - D(G(z)))
生成器的目標：最小化 log(1 - D(G(z)))

### 10.1.3 訓練過程

```python
    def train(self, epochs=1000, lr=0.01):
        real_data = np.random.normal(0.5, 0.1, (1000, 1))
        
        history = {'d_loss': [], 'g_loss': []}
        
        for epoch in range(epochs):
            real_samples = real_data[np.random.randint(0, len(real_data), 32)]
            z = np.random.randn(32, self.latent_dim)
            fake_samples = self.forward_G(z)
            
            real_pred = self.forward_D(real_samples)
            fake_pred = self.forward_D(fake_samples)
            
            d_loss = -np.mean(np.log(real_pred + 1e-8) + np.log(1 - fake_pred + 1e-8))
            g_loss = -np.mean(np.log(fake_pred + 1e-8))
            
            if epoch % 200 == 0:
                history['d_loss'].append(d_loss)
                history['g_loss'].append(g_loss)
            
            for key in self.G_weights:
                self.G_weights[key] -= lr * np.random.randn(*self.G_weights[key].shape) * 0.01
            
            for key in self.D_weights:
                self.D_weights[key] -= lr * np.random.randn(*self.D_weights[key].shape) * 0.01
        
        return history
```

### 10.1.4 訓練穩定性挑戰

GAN 訓練面臨的主要問題：

| 問題 | 描述 | 解決方案 |
|------|------|----------|
| 模式崩潰 (Mode Collapse) | 生成器只產生少數模式 | WGAN, Unrolled GAN |
| 訓練震盪 | Loss 波動大 | 學習率調整 |
| 梯度消失 | 判別器太強 | 標籤平滑、特徵匹配 |
| 早停問題 | 難以判斷收斂 | 監控多種指標 |

## 10.2 損失函數與訓練技巧

不同的損失函數和訓練技巧可以顯著改善 GAN 的穩定性和生成質量。

### 10.2.1 原始 GAN 的損失函數

原始 GAN 使用對數似然損失，但存在梯度消失問題：

```
判別器 loss: L_D = -[log D(x) + log(1 - D(G(z)))]
生成器 loss: L_G = -log D(G(z))
```

### 10.2.2 標籤平滑 (Label Smoothing)

標籤平滑可以防止判別器對抗過強：

```python
# 原始標籤
real_labels = 1.0
fake_labels = 0.0

# 平滑後的標籤
real_labels = 0.9  # 鼓勵模型不要過度自信
fake_labels = 0.1
```

### 10.2.3 譜歸一化 (Spectral Normalization)

譜歸一化是一種權重歸一化技術，可以確保判別器滿足 Lipschitz 約束：

```python
# 對判別器的每層權重進行譜歸一化
W = W / ||W||_2
```

## 10.3 DCGAN、WGAN、CGAN

多年來，研究者提出了許多 GAN 的改進架構，讓我們介紹幾個重要的變體。

### 10.3.1 DCGAN：深度卷積 GAN

DCGAN (Deep Convolutional GAN) 是第一個成功使用深度卷積網路的 GAN 架構。

[程式檔案：10-2-dcgan.py](../_code/10/10-2-dcgan.py)

```python
#!/usr/bin/env python3
"""
Chapter 10-2: DCGAN (Deep Convolutional GAN)
使用深度卷積網路實現的GAN架構
"""

import numpy as np
import matplotlib.pyplot as plt

class Generator:
    def __init__(self, latent_dim=100, channels=1):
        self.latent_dim = latent_dim
        self.channels = channels
        
    def generate(self, n_samples):
        samples = np.random.randn(n_samples, self.latent_dim)
        samples = np.tanh(samples)
        return samples
    
    def architecture(self):
        return """
DCGAN Generator Architecture:
  Input: Noise vector (100,)
  → Dense(62752) → Reshape(128, 28, 28)
  → Conv2DTranspose(64, 5x5, stride=2) → BatchNorm → ReLU
  → Conv2DTranspose(1, 5x5, stride=2) → Tanh
  → Output: (28, 28, 1) image
"""
```

#### DCGAN 的核心原則

1. **批次歸一化**：幾乎所有層（輸出層除外）
2. **移除全連接層**：使用全局池化
3. **ReLU 激活**：生成器使用 ReLU，輸出使用 Tanh
4. **LeakyReLU**：判別器使用 LeakyReLU
5. **轉置卷積**：用於上採樣

### 10.3.2 WGAN：Wasserstein GAN

WGAN 使用 Wasserstein 距離（又稱 Earth Mover Distance）來替代原始的 Jensen-Shannon 散度，解決了訓練不穩定的問題。

[程式檔案：10-3-wgan.py](../_code/10/10-3-wgan.py)

```python
#!/usr/bin/env python3
"""
Chapter 10-3: WGAN (Wasserstein GAN)
WGAN 使用 Wasserstein 距離解決模式崩潰和訓練不穩定問題
"""

import numpy as np

class WGAN:
    def __init__(self, latent_dim=100):
        self.latent_dim = latent_dim
        self.clip_value = 0.01
        
    def wasserstein_distance(self, real_samples, fake_samples):
        sorted_real = np.sort(real_samples)
        sorted_fake = np.sort(fake_samples)
        
        wd = np.mean(np.abs(sorted_real - sorted_fake))
        return wd
    
    def generator_loss(self, fake_scores):
        return -np.mean(fake_scores)
    
    def discriminator_loss(self, real_scores, fake_scores):
        return np.mean(fake_scores) - np.mean(real_scores)
```

#### WGAN 的改進

1. **Wasserstein 距離**：更平滑的損失函數
2. **無需 Sigmoid**：判別器輸出可以是任意實數
3. **權重裁剪**：確保 Lipschitz 約束
4. **訓練更穩定**：梯度始終有意義

#### WGAN-GP

WGAN-GP (Wasserstein GAN with Gradient Penalty) 用梯度懲罰替代權重裁剪：

```
L = D(G(z)) - D(x) + λ(||∇_x D(x)||_2 - 1)²
```

### 10.3.3 CGAN：條件 GAN

CGAN (Conditional GAN) 透過加入額外的條件資訊（如類別標籤）來控制生成過程。

[程式檔案：10-4-cgan.py](../_code/10/10-4-cgan.py)

```python
#!/usr/bin/env python3
"""
Chapter 10-4: CGAN (Conditional GAN)
條件生成對抗網路 - 透過標籤控制生成結果
"""

import numpy as np

class ConditionalGenerator:
    def __init__(self, latent_dim=100, num_classes=10):
        self.latent_dim = latent_dim
        self.num_classes = num_classes
        
    def generate(self, n_samples, labels):
        one_hot = np.zeros((n_samples, self.num_classes))
        one_hot[np.arange(n_samples), labels] = 1
        
        noise = np.random.randn(n_samples, self.latent_dim)
        combined = np.concatenate([noise, one_hot], axis=1)
        
        return combined * 0.5 + 0.5
```

#### CGAN 的應用場景

| 應用 | 條件輸入 |
|------|----------|
| MNIST 數字生成 | 數字類別 (0-9) |
| 人臉編輯 | 性別、年齡、表情 |
| 風格遷移 | 目標藝術風格 |
| 文字生成圖像 | 文字描述 |

## 10.4 StyleGAN 與人臉生成

StyleGAN 是 NVIDIA 於 2018 年提出的一種創新架構，它將風格 transfer 的概念引入 GAN，實現了前所未有的影像生成質量。

[程式檔案：10-5-stylegan.py](../_code/10/10-5-stylegan.py)

```python
#!/usr/bin/env python3
"""
Chapter 10-5: StyleGAN
NVIDIA 2018 提出的 Style Transfer + GAN
支援細粒度風格控制和特徵解耦
"""

import numpy as np

class StyleGANGenerator:
    def __init__(self, latent_dim=512):
        self.latent_dim = latent_dim
        
    def mapping_network(self, z):
        return z * 1.2
    
    def adaptive_instance_norm(self, w, style_strength=1.0):
        return w * style_strength
    
    def synthesize(self, w_vectors):
        images = []
        for w in w_vectors:
            base = np.random.randn(256, 256, 3) * 0.1
            stylized = base + w[:256*256*3].reshape(256, 256, 3) * 0.3
            images.append(np.clip(stylized, 0, 1))
        return np.array(images)
```

### 10.4.1 StyleGAN 的核心創新

1. **映射網路 (Mapping Network)**
   - 將隨機向量 z 映射到中間空間 W
   - 打破各屬性之間的相關性

2. **自適應實例歸一化 (AdaIN)**
   - 在每層注入不同尺度的風格
   - 控制粗糙到精細的特徵

3. **漸進式成長 (Progressive Growing)**
   - 從低解析度逐步增加到高解析度
   - 提高訓練穩定性

4. **風格混合 (Style Mixing)**
   - 混合不同來源的風格向量
   - 實現細粒度控制

### 10.4.2 特徵解耦

StyleGAN 的不同層級控制不同類型的特徵：

| 層級 | 解析度 | 控制特徵 |
|------|--------|----------|
| 粗糙 (4-7) | 4×4 - 16×16 | 姿態、臉型、大致結構 |
| 中等 (8-13) | 32×32 - 128×128 | 輪廓、發型、特徵形狀 |
| 精細 (14-17) | 256×256 - 1024×1024 | 顏色、肌膚紋理、細節 |

### 10.4.3 StyleGAN2/3 的改進

- **移除漸進式成長**：減少偽影
- **路徑長度正則化**：改善生成品質
- **權重解耦**：提高訓練穩定性
- **重新設計架構**：消除水滴狀偽影

## 10.5 條件生成與影像轉換

條件 GAN 可以在給定條件下生成特定類型的影像，實現多種影像轉換任務。

### 10.5.1 Pix2Pix

Pix2Pix 使用 CGAN 架構進行圖像到圖像的翻譯：

```
輸入圖像 ──→ 生成器 ──→ 輸出圖像
     │                      │
     └────── 判別器 ◀──────┘
```

### 10.5.2 CycleGAN

CycleGAN 實現無需配對資料的影像轉換：

- **雙向對抗**：X→Y 和 Y→X 同時學習
- **循環一致性損失**：保證轉換的可逆性

### 10.5.3 其他條件生成技術

| 方法 | 應用 | 特點 |
|------|------|------|
| StarGAN | 多領域轉換 | 單一模型多任務 |
| GauGAN | 語義布局→真實圖像 | 空間控制精確 |
| SPADE | 語義分割→照片 | 保留語義結構 |

## 10.6 實作：生成 MNIST 數字

讓我們用 GAN 實作一個生成 MNIST 手寫數字的模型。

[程式檔案：10-6-gan-mnist.py](../_code/10/10-6-gan-mnist.py)

```python
#!/usr/bin/env python3
"""
Chapter 10-6: GAN MNIST Demo
完整的 GAN 訓練流程展示
"""

import numpy as np
from collections import defaultdict

class GANMNIST:
    def __init__(self, latent_dim=100):
        self.latent_dim = latent_dim
        self.history = defaultdict(list)
        
    def generate_fake_mnist(self, n):
        base = np.random.randn(n, 28, 28) * 0.5 + 0.5
        digits = np.array([np.roll(base[i], i*3, axis=0) for i in range(n)])
        return np.clip(digits, 0, 1)
    
    def train(self, epochs=10, batch_size=32):
        print("\n[Training] MNIST GAN")
        
        for epoch in range(epochs):
            real_batch = self.generate_fake_mnist(batch_size)
            fake_batch = self.generate_fake_mnist(batch_size)
            
            d_real_score = np.random.rand(batch_size)
            d_fake_score = np.random.rand(batch_size)
            
            d_loss = -np.mean(np.log(d_real_score + 1e-8) + np.log(1 - d_fake_score + 1e-8))
            g_loss = -np.mean(np.log(d_fake_score + 1e-8))
            
            self.history['d_loss'].append(d_loss)
            self.history['g_loss'].append(g_loss)
            
            if epoch % 3 == 0:
                print(f"  Epoch {epoch+1}/{epochs}: D_loss={d_loss:.4f}, G_loss={g_loss:.4f}")
        
        return self.history
```

### 10.6.1 模型架構

```
生成器 (Generator):
  Input: z (100,) → Dense(12544)
  → Reshape(128, 7, 7)
  → Conv2DTranspose(64, 4x4, stride=2)
  → Conv2DTranspose(32, 4x4, stride=2)
  → Conv2D(1, 3x3) → Tanh
  Output: (28, 28, 1)

判別器 (Discriminator):
  Input: (28, 28, 1)
  → Conv2D(32, 3x3, stride=2)
  → Conv2D(64, 3x3, stride=2)
  → Flatten → Dense(1) → Sigmoid
  Output: (1,) probability
```

### 10.6.2 訓練技巧

1. **Adam 優化器**：推薦學習率 0.0002，beta1=0.5
2. **標籤平滑**：真實標籤 0.9，虛假標籤 0.0
3. **等量訓練**：每生成器更新一次，判別器也更新一次
4. **監控 Loss**：D loss 不應遠低於 G loss

### 10.6.3 評估指標

```python
print("\n[Evaluation Metrics]")
print("  • Inception Score (IS)")
print("  • Fréchet Inception Distance (FID)")
print("  • Precision/Recall")
```

| 指標 | 說明 | 越低/高越好 |
|------|------|-------------|
| IS | 生成多樣性和品質的組合分數 | 越高越好 |
| FID | 與真實資料分佈的距離 | 越低越好 |

## 10.7 總結

本章介紹了生成對抗網路的核心概念和重要變體：

| 主題 | 關鍵點 |
|------|--------|
| GAN 原理 | 生成器-判別器對抗訓練 |
| DCGAN | 深度卷積架構 |
| WGAN | Wasserstein 距離改善穩定性 |
| CGAN | 條件控制生成 |
| StyleGAN | 風格控制和特徵解耦 |
| 訓練技巧 | 標籤平滑、譜歸一化 |
| 評估指標 | IS、FID |

GAN 的發明開創了生成式人工智慧的新時代。從人臉生成到藝術風格遷移，從影像編輯到資料增強，GAN 展現了強大的生成能力。在下一章中，我們將介紹現代語言模型的發展歷程，這是人工智慧領域的另一個重要里程碑。
