# 第 15 章：生成式 AI

生成式 AI 是近年來最令人興奮的人工智慧領域之一。從文字到圖像，從音頻到影片，生成式模型正在改變我們創造和消費數位內容的方式。本章將深入介紹 VAE、Diffusion Model、Stable Diffusion、Sora 等生成式 AI 技術的核心原理。

## 15.1 生成式 AI 概述

生成式 AI 指的是能夠創造新內容的人工智慧系統，而非僅僅分析或分類現有內容。

### 15.1.1 生成式模型的類型

| 類型 | 代表模型 | 應用 |
|------|----------|------|
| VAE | VAE, VQ-VAE | 影像生成、壓縮 |
| GAN | StyleGAN, BigGAN | 人臉生成、影像轉換 |
| 自回歸 | GPT, PixelCNN | 文字生成、影像生成 |
| Diffusion | Stable Diffusion, DALL-E 3 | 文字生成圖像 |
| Flow | Glow, RealNVP | 影像生成 |

### 15.1.2 生成式模型的評估指標

| 指標 | 說明 |
|------|------|
| FID | Fréchet Inception Distance，衡量生成品質 |
| IS | Inception Score，衡量多樣性和品質 |
| BLEU | 文字生成品質評估 |
| Perplexity | 語言模型困惑度 |

## 15.2 VAE 變分自編碼器

變分自編碼器 (Variational Autoencoder, VAE) 是一種結合了自編碼器和機率模型的生成式模型。

[程式檔案：15-1-vae.py](../_code/15/15-1-vae.py)

```python
import numpy as np

class Encoder:
    def __init__(self, input_dim, latent_dim):
        self.mu = np.random.randn(input_dim, latent_dim) * 0.1
        self.logvar = np.random.randn(input_dim, latent_dim) * 0.1
        
    def forward(self, x):
        mean = x @ self.mu
        logvar = x @ self.logvar
        std = np.exp(0.5 * logvar)
        eps = np.random.randn(*std.shape)
        z = mean + eps * std
        return z, mean, logvar

class Decoder:
    def __init__(self, latent_dim, output_dim):
        self.W = np.random.randn(latent_dim, output_dim) * 0.1
        
    def forward(self, z):
        return z @ self.W

class VAE:
    def __init__(self, input_dim, latent_dim):
        self.encoder = Encoder(input_dim, latent_dim)
        self.decoder = Decoder(latent_dim, input_dim)
        
    def forward(self, x):
        z, mean, logvar = self.encoder.forward(x)
        recon = self.decoder.forward(z)
        return recon, z, mean, logvar
    
    def reconstruction_loss(self, x, recon):
        return np.mean((x - recon) ** 2)
    
    def kl_loss(self, mean, logvar):
        return -0.5 * np.mean(1 + logvar - mean ** 2 - np.exp(logvar))

input_dim = 784
latent_dim = 16

vae = VAE(input_dim, latent_dim)

x = np.random.randn(4, input_dim)
recon, z, mean, logvar = vae.forward(x)

recon_loss = vae.reconstruction_loss(x, recon)
kl = vae.kl_loss(mean, logvar)

print("=" * 60)
print("VAE (Variational Autoencoder) Demo")
print("=" * 60)
print(f"Input dimension: {input_dim}")
print(f"Latent dimension: {latent_dim}")
print(f"Input shape: {x.shape}")
print(f"Latent representation shape: {z.shape}")
print(f"Reconstructed shape: {recon.shape}")
print(f"\nReconstruction loss: {recon_loss:.4f}")
print(f"KL divergence: {kl:.4f}")
print("\n✓ VAE learns a structured latent space for generation")
print("  by combining encoder, reparameterization, and decoder")
```

### 15.2.1 VAE 原理

VAE 的核心思想是學習一個潛在空間，使得從中採樣可以生成新數據：

```
VAE 架構：

輸入 x ──→ Encoder ──→ μ, log σ²
                      │
                      ↓
              z = μ + σ × ε (重參數化)
                      │
                      ↓
Decoder ──→ 重構輸出 x̂
     │
     └──→ 與輸入 x 比較
```

### 15.2.2 VAE 的損失函數

VAE 的損失函數由兩部分組成：

$$L = L_{reconstruction} + L_{KL}$$

- **重構損失**：衡量解碼器輸出與輸入的相似度
- **KL 散度**：強制潛在分佈趨近於標準正態分佈

```python
def vae_loss(x, recon_x, mean, logvar):
    # 重構損失 (二元交叉熵或 MSE)
    recon_loss = nn.functional.binary_cross_entropy(recon_x, x)
    
    # KL 散度
    kl_loss = -0.5 * torch.sum(1 + logvar - mean.pow(2) - logvar.exp())
    
    return recon_loss + kl_loss
```

### 15.2.3 重參數化技巧

重參數化是 VAE 的關鍵技術，使梯度能夠流動：

```python
def reparameterize(mean, logvar):
    std = torch.exp(0.5 * logvar)
    eps = torch.randn_like(std)  # 隨機種子
    return mean + std * eps
```

## 15.3 自回歸生成與採樣策略

自回歸模型逐個 token 生成內容，是語言模型的基礎。

[程式檔案：15-2-autoregressive.py](../_code/15/15-2-autoregressive.py)

```python
import numpy as np

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

class AutoregressiveModel:
    def __init__(self, vocab_size, d_model):
        self.embedding = np.random.randn(vocab_size, d_model) * 0.1
        self.lm_head = np.random.randn(d_model, vocab_size) * 0.1
        
    def forward(self, token_ids):
        x = self.embedding[token_ids]
        return x @ self.lm_head
    
    def generate(self, seed_ids, max_new_tokens):
        generated = list(seed_ids)
        for _ in range(max_new_tokens):
            logits = self.forward(np.array(generated))
            next_token = np.argmax(logits[-1])
            generated.append(next_token)
        return generated

vocab_size = 100
d_model = 32

model = AutoregressiveModel(vocab_size, d_model)

seed = [1, 2, 3, 4, 5]
generated = model.generate(seed, 10)

print("=" * 60)
print("Autoregressive Generation Demo")
print("=" * 60)
print(f"Vocab size: {vocab_size}")
print(f"d_model: {d_model}")
print(f"Seed token IDs: {seed}")
print(f"Generated token IDs ({len(generated)} total):")
print(f"  {generated}")
print("\n✓ Autoregressive models generate one token at a time")
print("  using previously generated tokens as context")
print("  (used in GPT, LLM generation)")
```

### 15.3.1 自回歸生成過程

```python
def generate(model, seed_tokens, max_length, temperature=1.0):
    tokens = seed_tokens.copy()
    
    for _ in range(max_length):
        logits = model.forward(tokens)
        logits = logits[-1] / temperature  # 溫度縮放
        
        probs = softmax(logits)
        next_token = np.random.choice(len(probs), p=probs)
        
        tokens.append(next_token)
        
        if next_token == EOS_TOKEN:
            break
    
    return tokens
```

### 15.3.2 採樣策略

| 策略 | 說明 | 特點 |
|------|------|------|
| Greedy | 選擇最高概率 | 確定性，可能重複 |
| Temperature | 調整概率分佈 | 控制隨機性 |
| Top-k | 只從前 k 高概率採樣 | 平衡多樣性和品質 |
| Top-p (Nucleus) | 從累積概率 > p 的 tokens 採樣 | 自適應截斷 |

```python
def top_k_sample(logits, k=50, temperature=1.0):
    logits = logits / temperature
    indices = np.argsort(logits)[-k:]
    probs = softmax(logits[indices])
    return indices[np.random.choice(k, p=probs)]

def top_p_sample(logits, p=0.9, temperature=1.0):
    logits = logits / temperature
    sorted_indices = np.argsort(logits)[::-1]
    sorted_probs = softmax(logits[sorted_indices])
    cumsum = np.cumsum(sorted_probs)
    
    cutoff = np.searchsorted(cumsum, p)
    selected = sorted_indices[:cutoff+1]
    selected_probs = sorted_probs[:cutoff+1]
    
    return selected[np.random.choice(len(selected), p=selected_probs)]
```

## 15.4 Diffusion 擴散模型原理

Diffusion Model 是近年來最受矚目的生成式模型之一，特別是在影像生成領域。

[程式檔案：15-3-diffusion.py](../_code/15/15-3-diffusion.py)

```python
import numpy as np

class UNet:
    def __init__(self, channels):
        self.down_blocks = []
        self.up_blocks = []
        
        for i in range(len(channels) - 1):
            self.down_blocks.append({
                'conv': np.random.randn(channels[i+1], channels[i], 3, 3) * 0.1,
                'downsample': np.random.randn(channels[i+1], channels[i+1], 2, 2) * 0.1
            })
        
        for i in range(len(channels) - 1, 0, -1):
            self.up_blocks.append({
                'conv': np.random.randn(channels[i-1], channels[i], 3, 3) * 0.1,
                'upsample': np.random.randn(channels[i-1], channels[i-1], 2, 2) * 0.1
            })

class DiffusionScheduler:
    def __init__(self, num_timesteps=1000):
        self.num_timesteps = num_timesteps
        
    def get_alpha_bar(self, t):
        return np.cos((t / self.num_timesteps + 0.008) * np.pi / 2) ** 2
    
    def add_noise(self, x_start, noise, t):
        alpha_bar = self.get_alpha_bar(t)
        sqrt_alpha_bar = np.sqrt(alpha_bar)
        sqrt_one_minus_alpha_bar = np.sqrt(1 - alpha_bar)
        return sqrt_alpha_bar * x_start + sqrt_one_minus_alpha_bar * noise

class DiffusionModel:
    def __init__(self, in_channels, hidden_dims):
        self.unet = UNet([in_channels] + hidden_dims)
        self.scheduler = DiffusionScheduler()
        
    def forward(self, x, t):
        return self.unet.down_blocks[0]['conv'][:1, :1] @ x.flatten()

in_channels = 3
hidden_dims = [64, 128, 256]

diffusion = DiffusionModel(in_channels, hidden_dims)

x = np.random.randn(1, in_channels, 32, 32)
t = np.array([100])

output = diffusion.forward(x, t)

print("=" * 60)
print("Diffusion Model Demo")
print("=" * 60)
print(f"Input channels: {in_channels}")
print(f"UNet hidden dimensions: {hidden_dims}")
print(f"Number of timesteps: {diffusion.scheduler.num_timesteps}")
print(f"Input shape: {x.shape}")
print(f"timestep: {t[0]}")

x_noisy = diffusion.scheduler.add_noise(x, np.random.randn(*x.shape), t)
print(f"Noised image shape: {x_noisy.shape}")
print("\n✓ Diffusion models learn to reverse the noising process")
print("  to generate images from random noise")
```

### 15.4.1 Diffusion 雙向過程

```
Diffusion Model 的雙向過程：

前向過程 (Forward Process)：
x₀ ──→ x₁ ──→ x₂ ──→ ... ──→ xₜ ──→ ... ──→ xT
  ↓      ↓      ↓                ↓
添加噪音，逐漸變為純噪音 (通常 T = 1000)

反向過程 (Reverse Process)：
xT ──→ xₜ₋₁ ──→ xₜ₋₂ ──→ ... ──→ x₀
  ↓      ↓        ↓
學習去噪，從噪音恢復為圖像
```

### 15.4.2 前向過程 (Forward Process)

前向過程是固定的，只需使用閉式解：

$$q(x_t | x_0) = \mathcal{N}(x_t; \sqrt{\bar{\alpha}_t} x_0, (1-\bar{\alpha}_t)I)$$

```python
def forward_process(x0, t, alphas_cumprod):
    sqrt_alpha_bar = np.sqrt(alphas_cumprod[t])
    sqrt_one_minus_alpha = np.sqrt(1 - alphas_cumprod[t])
    
    noise = np.random.randn_like(x0)
    return sqrt_alpha_bar * x0 + sqrt_one_minus_alpha * noise
```

### 15.4.3 反向過程 (Reverse Process)

反向過程由神經網路學習：

$$p_\theta(x_{t-1} | x_t) = \mathcal{N}(x_{t-1}; \mu_\theta(x_t, t), \Sigma_\theta(x_t, t))$$

U-Net 是 Diffusion Model 中常用的骨幹網路：

```
U-Net 架構：

輸入 xₜ ──→ 下採樣 ──→ Bottleneck ──→ 上採樣 ──→ 輸出
              ↓              ↑              ↓
           Skip         跳層連接        噪聲預測
           連接
```

## 15.5 Stable Diffusion 與影像生成

Stable Diffusion 是一種基於 Latent Diffusion 的文字生成圖像模型，結合了 CLIP 和 Diffusion 技術。

[程式檔案：15-4-stable-diffusion.py](../_code/15/15-4-stable-diffusion.py)

```python
import numpy as np

class VAEEncoder:
    def __init__(self, in_channels, latent_dim):
        self.conv = np.random.randn(latent_dim, in_channels, 3, 3) * 0.1
        
    def forward(self, x):
        return x @ self.conv.flatten()[:16].reshape(4, 4)

class StableDiffusion:
    def __init__(self, latent_dim=4, hidden_dim=512):
        self.vae_enc = VAEEncoder(3, latent_dim)
        self.vae_dec = np.random.randn(latent_dim * 32 * 32, hidden_dim) * 0.1
        
        self.text_encoder = np.random.randn(77, hidden_dim) * 0.1
        self.unet = np.random.randn(hidden_dim, hidden_dim) * 0.1
        self.scheduler_steps = 50
        
    def text_to_image(self, prompt_embedding):
        latents = np.random.randn(1, 4, 32, 32)
        
        for step in range(self.scheduler_steps):
            noise_pred = latents @ self.unet
            latents = latents - 0.01 * noise_pred
        
        image = latents.reshape(1, -1) @ self.vae_dec
        return image.reshape(1, 3, 64, 64)

prompt = "a photo of an astronaut riding a horse"
prompt_tokens = np.array([len(prompt.split())])

sd = StableDiffusion()

result = sd.text_to_image(prompt_tokens)

print("=" * 60)
print("Stable Diffusion Demo")
print("=" * 60)
print(f"Prompt: '{prompt}'")
print(f"Latent dimension: 4 x 32 x 32")
print(f"UNet hidden dimension: 512")
print(f"Sampling steps: {sd.scheduler_steps}")
print(f"\nGenerated image shape: {result.shape}")
print("\n✓ Stable Diffusion uses:")
print("  - VAE for latent space encoding")
print("  - CLIP text encoder for conditioning")
print("  - U-Net for noise prediction")
print("  - Cross-attention for text-image alignment")
```

### 15.5.1 Stable Diffusion 架構

```
Stable Diffusion 架構：

文字輸入
    ↓
┌─────────────────────────────────────────────┐
│          CLIP Text Encoder                  │
│   將文字轉換為條件向量 (77×768)             │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│          Latent Diffusion                   │
│                                             │
│   噪聲 ──→ UNet + 文字條件 ──→ 預測噪聲     │
│     ↓                    ↑                  │
│   迭代去噪            Cross-Attention      │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│              VAE Decoder                    │
│   將潛在表示解碼為圖像                      │
└─────────────────────────────────────────────┘
```

### 15.5.2 潛在空間擴散

Stable Diffusion 的關鍵創新是在壓縮的潛在空間中進行擴散：

| 空間 | 維度 | 說明 |
|------|------|------|
| 像素空間 | 512×512×3 | 原始圖像空間 |
| 潛在空間 | 64×64×4 | 壓縮 48 倍 |

### 15.5.3 Cross-Attention

文字條件透過 Cross-Attention 機制注入：

```python
def cross_attention(query, context):
    # query: 來自 U-Net 的特徵
    # context: 來自 CLIP 的文字嵌入
    
    attention_scores = query @ context.T / np.sqrt(query.shape[-1])
    attention_weights = softmax(attention_scores)
    return attention_weights @ context
```

## 15.6 DDIM 加速採樣

DDIM (Denoising Diffusion Implicit Models) 是一種加速 Diffusion 採樣的技術。

[程式檔案：15-5-ddim.py](../_code/15/15-5-ddim.py)

```python
import numpy as np

class DDIMScheduler:
    def __init__(self, num_timesteps=50, eta=0.0):
        self.num_timesteps = num_timesteps
        self.eta = eta
        
    def get_schedule(self):
        timesteps = np.linspace(self.num_timesteps - 1, 0, self.num_timesteps)
        return timesteps.astype(int)
    
    def step(self, x_t, noise_pred, t, t_prev):
        alpha_t = self.get_alpha(t)
        alpha_t_prev = self.get_alpha(t_prev)
        
        pred_x0 = (x_t - np.sqrt(1 - alpha_t) * noise_pred) / np.sqrt(alpha_t)
        
        if self.eta == 0:
            x_t_prev = np.sqrt(alpha_t_prev) * pred_x0 + np.sqrt(1 - alpha_t_prev) * noise_pred
        else:
            sigma_t = self.eta * np.sqrt((1 - alpha_t_prev) / (1 - alpha_t)) * np.sqrt(1 - alpha_t / alpha_t_prev)
            x_t_prev = np.sqrt(alpha_t_prev) * pred_x0 + sigma_t * np.random.randn(*x_t.shape) + np.sqrt(1 - alpha_t_prev - sigma_t**2) * noise_pred
            
        return x_t_prev
    
    def get_alpha(self, t):
        return np.cos((t / self.num_timesteps + 0.008) * np.pi / 2) ** 2

class DDIM:
    def __init__(self, num_steps=50, eta=0.0):
        self.scheduler = DDIMScheduler(num_steps, eta)
        self.model = np.random.randn(512, 512) * 0.1
        
    def sample(self, num_images=1):
        x_t = np.random.randn(num_images, 4, 32, 32)
        
        timesteps = self.scheduler.get_schedule()
        
        for i in range(len(timesteps) - 1):
            noise_pred = x_t @ self.model
            x_t = self.scheduler.step(x_t, noise_pred, timesteps[i], timesteps[i+1])
            
        return x_t

ddim = DDIM(num_steps=50, eta=0.0)

samples = ddim.sample(num_images=1)

print("=" * 60)
print("DDIM (Denoising Diffusion Implicit Models) Demo")
print("=" * 60)
print(f"Number of sampling steps: {ddim.scheduler.num_timesteps}")
print(f"DDIM eta (randomness): {ddim.scheduler.eta}")
print(f"Initial noise shape: (1, 4, 32, 32)")
print(f"Final latent shape: {samples.shape}")
print("\n✓ DDIM enables faster sampling than standard DDPM")
print("  by using a non-Markovian forward process")
print("  eta=0 gives deterministic sampling")
```

### 15.6.1 DDIM vs DDPM

| 特性 | DDPM | DDIM |
|------|------|------|
| 採樣步數 | 1000 | 20-50 |
| 採樣時間 | 幾分鐘 | 幾秒 |
| 確定性 | 隨機 | 可確定性 (η=0) |
| 品質 | 最高 | 接近 DDPM |

### 15.6.2 DDIM 採樣公式

```python
def ddim_step(x_t, noise_pred, alpha_t, alpha_t_prev, eta=0):
    pred_x0 = (x_t - np.sqrt(1 - alpha_t) * noise_pred) / np.sqrt(alpha_t)
    
    if eta == 0:  # 確定性
        x_t_prev = np.sqrt(alpha_t_prev) * pred_x0
    else:  # 隨機性
        sigma = eta * np.sqrt((1 - alpha_t_prev) / (1 - alpha_t)) * np.sqrt(1 - alpha_t / alpha_t_prev)
        x_t_prev = np.sqrt(alpha_t_prev) * pred_x0 + sigma * noise
    
    return x_t_prev
```

## 15.7 SDXL 與更高品質生成

SDXL (Stable Diffusion XL) 是 Stable Diffusion 的升級版本，提供更高品質和更大分辨率的圖像生成能力。

[程式檔案：15-6-sdxl.py](../_code/15/15-6-sdxl.py)

```python
import numpy as np

class SDXL:
    def __init__(self):
        self.text_encoder = np.random.randn(77, 2048) * 0.1
        self.text_encoder_2 = np.random.randn(77, 1024) * 0.1
        
        self.unet_main = np.random.randn(2048, 2048) * 0.1
        self.unet_refiner = np.random.randn(2048, 2048) * 0.1
        
        self.vae = np.random.randn(3 * 64 * 64, 4 * 32 * 32) * 0.1
        
    def generate(self, prompt, num_steps=30):
        text_embeds = self.text_encoder[:len(prompt.split())] @ np.eye(2048)[:len(prompt.split())]
        
        latents = np.random.randn(1, 4, 128, 128)
        
        for step in range(num_steps):
            latents = latents @ self.unet_main
            
        refined = latents @ self.unet_refiner
        
        image = refined @ self.vae
        return image.reshape(1, 3, 256, 256)

prompt = "a majestic castle at sunset"
sdxl = SDXL()

image = sdxl.generate(prompt)

print("=" * 60)
print("SDXL (Stable Diffusion XL) Demo")
print("=" * 60)
print(f"Prompt: '{prompt}'")
print(f"Text encoder dimensions: 2048, 1024")
print(f"UNet main: 2048 dim")
print(f"UNet refiner: 2048 dim")
print(f"VAE latent: 4x128x128 -> image: 3x256x256")
print(f"Number of steps: 30")
print(f"\nGenerated image shape: {image.shape}")
print("\n✓ SDXL improvements over SD:")
print("  - Larger text encoders (OpenCLIP + BERT)")
print("  - Larger resolution (1024x1024)")
print("  - Refiner module for quality")
print("  - Better prompt following")
```

### 15.7.1 SDXL 的改進

| 特性 | Stable Diffusion | SDXL |
|------|-----------------|------|
| 文字編碼器 | CLIP | OpenCLIP + BERT |
| 分辨率 | 512×512 | 1024×1024 |
| U-Net 維度 | 768 | 2048 |
| Refiner | 無 | 有 |
| 文字嵌入維度 | 768 | 2048 |

### 15.7.2 Refiner 模組

SDXL 引入了專門的 Refiner 模組來提升圖像品質：

```python
def refinement(image, refiner):
    # 兩階段生成
    base_image = base_unet(image)
    refined_image = refiner(base_image)
    return refined_image
```

## 15.8 文字生成影片：Sora

Sora 是 OpenAI 發布的影片生成模型，能夠根據文字描述生成高質量影片。

[程式檔案：15-7-sora.py](../_code/15/15-7-sora.py)

```python
import numpy as np

class SpatioTemporalAttention:
    def __init__(self, d_model):
        self.d_model = d_model
        
    def forward(self, x):
        b, t, h, w, c = x.shape
        x_flat = x.reshape(b, t * h * w, c)
        attn = x_flat @ x_flat.T / np.sqrt(self.d_model)
        attn = np.softmax(attn, axis=-1)
        return (attn @ x_flat).reshape(b, t, h, w, c)

class VideoDiffusion:
    def __init__(self, num_frames=60, resolution=(64, 64)):
        self.num_frames = num_frames
        self.resolution = resolution
        self.d_model = 512
        
        self.attention = SpatioTemporalAttention(self.d_model)
        self.temporal_attention = np.random.randn(self.d_model, self.d_model) * 0.1
        
    def generate(self, prompt_embedding):
        video = np.random.randn(1, self.num_frames, *self.resolution, 3)
        
        for frame in range(self.num_frames):
            frame_latent = video[0, frame]
            frame_latent = frame_latent @ self.temporal_attention
            
        return video

prompt = "a drone flying through a scenic mountain landscape at golden hour"
video_diffusion = VideoDiffusion(num_frames=60, resolution=(64, 64))

video = video_diffusion.generate(prompt)

print("=" * 60)
print("Sora (Video Generation) Demo")
print("=" * 60)
print(f"Prompt: '{prompt}'")
print(f"Number of frames: {video_diffusion.num_frames}")
print(f"Resolution: {video_diffusion.resolution}")
print(f"Video shape: {video.shape}")
print("\n✓ Sora capabilities:")
print("  - Text-to-video generation")
print("  - Image-to-video generation")
print("  - Video extension")
print("  - Spatio-temporal attention")
print("  - Variable resolution & duration")
```

### 15.8.1 影片生成的挑戰

| 挑戰 | 說明 |
|------|------|
| 時序一致性 | 物體運動和場景變化的連貫性 |
| 長影片生成 | 維持遠距離幀的一致性 |
| 計算成本 | 影片數據量遠大於圖像 |
| 物理規律 | 模擬重力、光影等物理現象 |

### 15.8.2 時空注意力

Sora 採用時空注意力機制，同時建模時間和空間維度：

```python
class SpatioTemporalAttention(nn.Module):
    def forward(self, x):
        # x: [B, T, H, W, C]
        b, t, h, w, c = x.shape
        
        # 展平為時空序列
        x = x.reshape(b, t * h * w, c)
        
        # 計算注意力
        attn = x @ x.transpose(-2, -1)
        attn = F.softmax(attn, dim=-1)
        
        return (attn @ x).reshape(b, t, h, w, c)
```

## 15.9 實作：建構簡單的 Diffusion 模型

讓我們實現一個簡化的 Diffusion 模型來理解其核心原理。

[程式檔案：15-8-mini-diffusion.py](../_code/15/15-8-mini-diffusion.py)

```python
import numpy as np

class SimpleDiffusion:
    def __init__(self, latent_shape=(4, 8, 8)):
        self.latent_shape = latent_shape
        self.num_steps = 20
        
    def forward_process(self, x0, t):
        noise = np.random.randn(*x0.shape)
        alpha = np.cos((t + 1) / (self.num_steps + 1) * np.pi / 2) ** 2
        return np.sqrt(alpha) * x0 + np.sqrt(1 - alpha) * noise
    
    def reverse_process(self, xT, num_steps=None):
        if num_steps is None:
            num_steps = self.num_steps
        x = xT
        for step in range(num_steps):
            t = num_steps - step - 1
            noise_pred = np.random.randn(*x.shape) * 0.1
            alpha = np.cos((t + 1) / (num_steps + 1) * np.pi / 2) ** 2
            x = (x - np.sqrt(1 - alpha) * noise_pred) / np.sqrt(alpha)
        return x
    
    def generate(self, batch_size=1):
        xT = np.random.randn(batch_size, *self.latent_shape)
        return self.reverse_process(xT)

diffusion = SimpleDiffusion(latent_shape=(4, 8, 8))

x0 = np.random.randn(1, 4, 8, 8)
noised = diffusion.forward_process(x0, t=10)
generated = diffusion.generate(batch_size=1)

print("=" * 60)
print("Mini Diffusion Demo")
print("=" * 60)
print(f"Latent shape: {diffusion.latent_shape}")
print(f"Number of steps: {diffusion.num_steps}")
print(f"\nOriginal: {x0.shape}")
print(f"Forward (t=10): {noised.shape}")
print(f"Generated: {generated.shape}")
print("\n✓ Diffusion model process:")
print("  1. Forward: Add noise to data gradually")
print("  2. Reverse: Learn to denoise (generate)")
```

### 15.9.1 完整訓練流程

```python
class DiffusionModel(nn.Module):
    def __init__(self, unet, scheduler):
        super().__init__()
        self.unet = unet
        self.scheduler = scheduler
    
    def training_step(self, x0):
        batch_size = x0.shape[0]
        
        # 隨機採樣時間步
        t = torch.randint(0, self.num_steps, (batch_size,))
        
        # 添加噪音
        noise = torch.randn_like(x0)
        noisy_x = self.scheduler.add_noise(x0, t, noise)
        
        # 預測噪音
        noise_pred = self.unet(noisy_x, t)
        
        # 計算損失
        return F.mse_loss(noise_pred, noise)
    
    @torch.no_grad()
    def generate(self, num_images=1):
        xT = torch.randn(num_images, *self.latent_shape)
        
        for t in reversed(range(self.num_steps)):
            noise_pred = self.unet(xT, t)
            xT = self.scheduler.step(xT, noise_pred, t)
        
        return xT
```

## 15.10 總結

本章系統介紹了生成式 AI 的核心技術：

| 技術 | 核心原理 | 應用場景 |
|------|----------|----------|
| VAE | 潛在變數模型 | 壓縮、生成 |
| 自回歸 | 順序生成 | 文字、音頻 |
| Diffusion | 去噪生成 | 圖像、影片 |
| Stable Diffusion | Latent Diffusion | 文字生成圖像 |
| DDIM | 非馬爾可夫採樣 | 加速生成 |
| Sora | 時空Diffusion | 文字生成影片 |

生成式 AI 正處於快速發展階段，從靜態圖像到動態影片，從二維到三維，AI 的創造力正在不斷突破想像。掌握這些核心技術，將幫助我們更好地理解和應用未來的 AI 系統。
