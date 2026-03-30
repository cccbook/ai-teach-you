# 第 12 章：注意力機制、Transformer 與 GPT

Transformer 是 2017 年由 Google 在經典論文《Attention Is All You Need》中提出的革命性架構。它完全基於注意力機制，拋棄了傳統的循環結構，徹底改變了自然語言處理的面貌。本章將深入介紹注意力機制的原理、Transformer 的架構，以及 GPT 模型的實現。

## 12.1 注意力機制 (Attention) 原理

注意力機制模擬了人類視覺注意力——當我們觀看一個場景時，會自然地關注某些重要的區域而忽略其他部分。在神經網路中，注意力機制允許模型動態地聚焦於輸入的相關部分。

[程式檔案：12-1-attention.py](../_code/12/12-1-attention.py)

```python
import numpy as np

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

def attention_score(query, key):
    return np.dot(query, key.T) / np.sqrt(key.shape[-1])

def attention(query, key, value):
    scores = attention_score(query, key)
    weights = softmax(scores)
    return np.dot(weights, value)

d_k = 64
d_v = 64
seq_len = 5

np.random.seed(42)
Q = np.random.randn(seq_len, d_k)
K = np.random.randn(seq_len, d_k)
V = np.random.randn(seq_len, d_v)

output = attention(Q, K, V)

print("=" * 60)
print("Attention Mechanism Demo")
print("=" * 60)
print(f"Query shape: {Q.shape}")
print(f"Key shape: {K.shape}")
print(f"Value shape: {V.shape}")
print(f"Output shape: {output.shape}")
```

### 12.1.1 注意力的數學原理

注意力機制的核心是計算查詢 (Query) 與鍵 (Key) 的相似度，然後用這個注意力權重對值 (Value) 進行加權求和：

```
Attention(Q, K, V) = softmax(QK^T / √d_k) × V
```

其中：
- **Q (Query)**：當前要查詢的向量
- **K (Key)**：資料庫中每個位置的鍵
- **V (Value)**：與鍵對應的值

### 12.1.2 注意力分數與權重

```python
print("\nSample attention scores (first query):")
scores = attention_score(Q, K)
print(scores[0])
print("\nAttention weights (first query):")
weights = softmax(scores)
print(weights[0])
```

注意力權重表示每個位置對當前查詢的重要程度：

```
        注意力權重
            │
    1.0 ──┤              ★ (高權重：聚焦區域)
        │  │
    0.5 ──┤  │
        │  │    │
    0.0 ──┴──┼────┼──────→ 位置
             │    │
             相對重要性
```

### 12.1.3 縮放點積注意力

```python
print("\n✓ Attention mechanism computes weighted sum of values")
print("  based on query-key compatibility")
```

使用 √d_k 進行縮放的原因：
1. 當 d_k 較大時，點積的結果可能很大
2. 大的點積值會使 softmax 進入梯度很小的區域
3. 縮放可以保持梯度的穩定性

### 12.1.4 注意力的優勢

| 特性 | 說明 |
|------|------|
| 平行計算 | 不同位置的注意力可以同時計算 |
| 路徑長度 | 任意兩位置之間只需 O(1) 步 |
| 可解釋性 | 注意力權重可視化 |

## 12.2 自注意力 (Self-Attention) 與 Multi-Head Attention

自注意力是注意力的特例，它允許序列中的每個位置關注序列中的所有其他位置，捕捉長距離依賴關係。

[程式檔案：12-2-self-attention.py](../_code/12/12-2-self-attention.py)

```python
import numpy as np

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

def self_attention(x, d_k=64):
    seq_len = x.shape[0]
    Q = x @ np.random.randn(d_k, d_k).T
    K = x @ np.random.randn(d_k, d_k).T
    V = x @ np.random.randn(d_k, d_k).T
    
    scores = Q @ K.T / np.sqrt(d_k)
    weights = softmax(scores)
    return weights @ V

seq_len = 4
d_model = 8

np.random.seed(42)
x = np.random.randn(seq_len, d_model)

output = self_attention(x, d_model)

print("=" * 60)
print("Self-Attention Demo")
print("=" * 60)
print(f"Input shape: {x.shape}")
print(f"Output shape: {output.shape}")
print("\nInput sequence:")
print(x)
print("\nSelf-attention output:")
print(output)
```

### 12.2.1 自注意力的原理

在自注意力中，Q、K、V 都來自同一輸入：

```
輸入 X ──→ 線性變換 W_Q ──→ Q
       └──→ 線性變換 W_K ──→ K  
       └──→ 線性變換 W_V ──→ V

輸出 = Attention(Q, K, V)
```

### 12.2.2 自注意力的應用場景

| 應用 | 說明 |
|------|------|
| 機器翻譯 | 源語言和目標語言的對齊 |
| 文字分類 | 捕捉詞與詞之間的關係 |
| 問答系統 | 問題與文本的匹配 |
| 影像處理 | 像素之間的長距離依賴 |

### 12.2.3 多頭注意力 (Multi-Head Attention)

多頭注意力將 Q、K、V 投影到多個子空間，每個頭專注於不同的表示子空間。

[程式檔案：12-3-multihead-attention.py](../_code/12/12-3-multihead-attention.py)

```python
import numpy as np

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

class MultiHeadAttention:
    def __init__(self, d_model, num_heads):
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
    def split_heads(self, x):
        x = x.reshape(x.shape[0], self.num_heads, self.d_k)
        return np.transpose(x, (1, 0, 2))
    
    def attention(self, Q, K, V):
        scores = np.matmul(Q, np.transpose(K, (0, 2, 1))) / np.sqrt(self.d_k)
        weights = softmax(scores)
        return np.matmul(weights, V)
    
    def forward(self, Q, K, V):
        Q = self.split_heads(Q)
        K = self.split_heads(K)
        V = self.split_heads(V)
        
        attn = self.attention(Q, K, V)
        attn = np.transpose(attn, (1, 0, 2))
        return attn.reshape(attn.shape[0], -1)

d_model = 8
num_heads = 2
seq_len = 4

mha = MultiHeadAttention(d_model, num_heads)
Q = np.random.randn(seq_len, d_model)
K = np.random.randn(seq_len, d_model)
V = np.random.randn(seq_len, d_model)

output = mha.forward(Q, K, V)

print("=" * 60)
print("Multi-Head Attention Demo")
print("=" * 60)
print(f"d_model: {d_model}")
print(f"num_heads: {num_heads}")
print(f"d_k per head: {d_model // num_heads}")
```

### 12.2.4 多頭注意力的優勢

```
多頭注意力示意圖：

  輸入 ──→ 頭1 ──┐
       ──→ 頭2 ──┼──→ 拼接 ──→ 線性變換 ──→ 輸出
       ──→ 頭3 ──┤
       ──→ 頭4 ──┘
```

每個頭可以學習不同的注意力模式：
- 頭1：語法關係（主語、動詞）
- 頭2：語義關係（同義詞）
- 頭3：指代消解（代詞指向）
- 頭4：長距離依賴

## 12.3 Transformer 架構：Encoder 與 Decoder

Transformer採用 Encoder-Decoder 架構， Encoder 處理輸入序列，Decoder 生成輸出序列。

[程式檔案：12-4-transformer.py](../_code/12/12-4-transformer.py)

```python
import numpy as np

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

class FeedForward:
    def __init__(self, d_model, d_ff):
        self.W1 = np.random.randn(d_model, d_ff) * 0.1
        self.W2 = np.random.randn(d_ff, d_model) * 0.1
        
    def forward(self, x):
        return (np.maximum(0, x @ self.W1) @ self.W2)

class TransformerBlock:
    def __init__(self, d_model, num_heads, d_ff):
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        self.ff = FeedForward(d_model, d_ff)
        
    def self_attention(self, x):
        Q = x @ np.random.randn(self.d_model, self.d_model) * 0.1
        K = x @ np.random.randn(self.d_model, self.d_model) * 0.1
        V = x @ np.random.randn(self.d_model, self.d_model) * 0.1
        
        scores = Q @ K.T / np.sqrt(self.d_k)
        weights = softmax(scores)
        return weights @ V
    
    def forward(self, x):
        attn = self.self_attention(x)
        x = x + attn
        ff_out = self.ff.forward(x)
        return x + ff_out

d_model = 8
num_heads = 2
d_ff = 16
seq_len = 4

transformer = TransformerBlock(d_model, num_heads, d_ff)
x = np.random.randn(seq_len, d_model)

output = transformer.forward(x)

print("=" * 60)
print("Transformer Block Demo")
print("=" * 60)
print(f"d_model: {d_model}, num_heads: {num_heads}, d_ff: {d_ff}")
print(f"Input shape: {x.shape}")
print(f"Output shape: {output.shape}")
```

### 12.3.1 Transformer 整體架構

```
Transformer 架構圖：

         Encoder                              Decoder
    ┌─────────────────┐                ┌─────────────────┐
    │  輸入嵌入        │                │  輸出嵌入        │
    │    + 位置編碼    │                │    + 位置編碼    │
    ├─────────────────┤                ├─────────────────┤
    │                 │                │                 │
    │  N × Encoder     │──────┐        │  N × Decoder    │
    │    Block        │      │        │    Block         │
    │                 │      ↓        │                 │
    │  • Multi-Head    │  Cross        │  • Masked MHA   │
    │    Self-Attn    │  Attention    │  • Self-Attn    │
    │  • Feed Forward │      │        │  • Feed Forward │
    │  • Add & Norm   │      │        │  • Add & Norm   │
    │                 │      │        │                 │
    ├─────────────────┤      │        ├─────────────────┤
    │                 │      │        │  Linear + Softmax│
    │  N × Encoder     │      │        │                 │
    │    Block        │      │        │  輸出概率        │
    │                 │      │        │                 │
    └─────────────────┘      │        └─────────────────┘
                              │
                              ↓
                    ┌─────────────────┐
                    │                 │
                    │  Linear + Softmax│
                    │                 │
                    │  輸出序列        │
                    └─────────────────┘
```

### 12.3.2 殘差連接與層標準化

每個子層都有殘差連接和層標準化：

```
Output = LayerNorm(x + Sublayer(x))
```

這確保了：
1. 梯度能夠直接流動
2. 每層的輸入輸出分佈穩定
3. 訓練更加穩定

### 12.3.3 Feed-Forward 網路

每個 Encoder/Decoder Block 中都包含一個 Position-wise Feed-Forward 網路：

```python
class FeedForward:
    def __init__(self, d_model, d_ff):
        self.W1 = np.random.randn(d_model, d_ff) * 0.1
        self.W2 = np.random.randn(d_ff, d_model) * 0.1
        
    def forward(self, x):
        return (np.maximum(0, x @ self.W1) @ self.W2)
```

這是一個兩層的全連接網路：
- 內部維度通常是模型維度的 4 倍
- 使用 ReLU 激活函數
- 對每個位置獨立應用

## 12.4 位置編碼 (Positional Encoding)

由於 Transformer 沒有循環結構，無法直接捕捉序列的位置資訊。位置編碼透過向輸入嵌入添加位置資訊來解決這個問題。

[程式檔案：12-5-positional-encoding.py](../_code/12/12-5-positional-encoding.py)

```python
import numpy as np

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

class PositionalEncoding:
    def __init__(self, d_model, max_len=100):
        self.d_model = d_model
        
    def get_positional_encoding(self, seq_len):
        pe = np.zeros((seq_len, self.d_model))
        position = np.arange(seq_len).reshape(-1, 1)
        div_term = np.exp(np.arange(0, self.d_model, 2) * -(np.log(10000.0) / self.d_model))
        pe[:, 0::2] = np.sin(position * div_term)
        pe[:, 1::2] = np.cos(position * div_term)
        return pe

d_model = 8
seq_len = 10

pe = PositionalEncoding(d_model)
pos_enc = pe.get_positional_encoding(seq_len)

print("=" * 60)
print("Positional Encoding Demo")
print("=" * 60)
print(f"d_model: {d_model}")
print(f"sequence length: {seq_len}")
print(f"Positional encoding shape: {pos_enc.shape}")
print("\nPositional encoding for first 3 positions:")
print(pos_enc[:3])
```

### 12.4.1 正弦/餘弦位置編碼

Transformer 使用正弦和餘弦函數生成位置編碼：

```
PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
```

其中：
- pos 是位置 (0, 1, 2, ...)
- i 是維度索引 (0, 1, 2, ..., d_model/2)

### 12.4.2 位置編碼的特性

| 特性 | 說明 |
|------|------|
| 週期性 | 不同頻率的正弦波捕捉不同尺度的位置關係 |
| 相對位置 | 任意兩個位置的差可以用線性組合表示 |
| 無需學習 | 固定公式生成，可推廣到任意長度 |

### 12.4.3 位置編碼的可視化

```
位置編碼熱力圖：

         維度 →
     0   1   2   3   4   5   6   7
  ┌──────────────────────────────────┐
0 │ ■  □  ■  □  ■  □  ■  □ │
1 │ □  ■  □  ■  □  ■  □  ■ │
2 │ ■  □  □  ■  ■  □  □  ■ │
3 │ □  ■  ■  □  □  ■  ■  □ │
  └──────────────────────────────────┘
  │
  └─ 位置 (行)
```

## 12.5 GPT-1/2/3/4 演進

GPT (Generative Pre-trained Transformer) 系列是 OpenAI 開發的自回歸語言模型，採用純 Decoder 架構。

[程式檔案：12-6-gpt.py](../_code/12/12-6-gpt.py)

```python
import numpy as np

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

vocab_size = 100
d_model = 16
seq_len = 5

embedding = np.random.randn(vocab_size, d_model) * 0.1
W_Q = np.random.randn(d_model, d_model) * 0.1
W_K = np.random.randn(d_model, d_model) * 0.1
W_V = np.random.randn(d_model, d_model) * 0.1
W_O = np.random.randn(d_model, d_model) * 0.1

token_ids = [45, 23, 78, 12, 56]
x = embedding[token_ids]

def self_attention(x, mask=None):
    Q = x @ W_Q
    K = x @ W_K
    V = x @ W_V
    scores = Q @ K.T / np.sqrt(d_model)
    if mask is not None:
        scores = scores + np.where(mask, -1e9, 0)
    weights = softmax(scores)
    return weights @ V

def causal_mask(seq_len):
    mask = np.ones((seq_len, seq_len))
    return np.tril(mask)

mask = causal_mask(seq_len)
output = self_attention(x, mask)
output = output @ W_O

print("=" * 60)
print("GPT-style Decoder Demo")
print("=" * 60)
print(f"Vocab size: {vocab_size}")
print(f"d_model: {d_model}")
print(f"Sequence length: {seq_len}")
print(f"Output shape: {output.shape}")
print("\nCausal mask (prevents attending to future):")
print(mask.astype(int))
```

### 12.5.1 GPT 與 BERT 的區別

| 特性 | GPT (Decoder-only) | BERT (Encoder-only) |
|------|-------------------|-------------------|
| 注意力 | 單向 (Causal) | 雙向 |
| 預訓練目標 | 標準語言模型 | MLM + NSP |
| 適用任務 | 生成任務 | 理解任務 |
| 推理方式 | 自回歸 | 雙向編碼 |

### 12.5.2 GPT 系列的演進

| 版本 | 發布年份 | 參數量 | 關鍵創新 |
|------|----------|--------|----------|
| GPT-1 | 2018 | 1.17 億 | 預訓練+微調範式 |
| GPT-2 | 2019 | 15 億 | Zero-shot 能力 |
| GPT-3 | 2020 | 1750 億 | Few-shot 學習 |
| GPT-4 | 2023 | 未公開 | 多模態、推理增強 |

### 12.5.3 因果注意力 (Causal Attention)

GPT 使用因果注意力掩碼，確保每個位置只能關注之前的位置：

```python
def causal_mask(seq_len):
    mask = np.ones((seq_len, seq_len))
    return np.tril(mask)
```

```
Causal Mask 示意圖：
         輸出位置 →
    0   1   2   3   4
  ┌─────────────────────┐
0 │ ■   ×   ×   ×   ×  │
1 │ ■   ■   ×   ×   ×  │ ← 輸入位置
2 │ ■   ■   ■   ×   ×  │   ↓
3 │ ■   ■   ■   ■   ×  │
4 │ ■   ■   ■   ■   ■  │
  └─────────────────────┘
  ■ = 可以關注, × = 不能關注
```

## 12.6 實作：從零建構小型 Transformer

讓我們用 NumPy 從頭實現一個簡化版的 Transformer，以深入理解其工作原理。

[程式檔案：12-7-mini-transformer.py](../_code/12/12-7-mini-transformer.py)

```python
import numpy as np

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

class MiniTransformer:
    def __init__(self, vocab_size, d_model, num_heads, num_layers):
        self.vocab_size = vocab_size
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        self.embedding = np.random.randn(vocab_size, d_model) * 0.1
        self.W_Q = [np.random.randn(d_model, d_model) * 0.1 for _ in range(num_layers)]
        self.W_K = [np.random.randn(d_model, d_model) * 0.1 for _ in range(num_layers)]
        self.W_V = [np.random.randn(d_model, d_model) * 0.1 for _ in range(num_layers)]
        self.W_O = np.random.randn(d_model, d_model) * 0.1
        self.W1 = [np.random.randn(d_model, d_model * 4) * 0.1 for _ in range(num_layers)]
        self.W2 = [np.random.randn(d_model * 4, d_model) * 0.1 for _ in range(num_layers)]
        self.lm_head = np.random.randn(d_model, vocab_size) * 0.1
        
    def positional_encoding(self, seq_len):
        pe = np.zeros((seq_len, self.d_model))
        position = np.arange(seq_len).reshape(-1, 1)
        div_term = np.exp(np.arange(0, self.d_model, 2) * -(np.log(10000.0) / self.d_model))
        pe[:, 0::2] = np.sin(position * div_term)
        pe[:, 1::2] = np.cos(position * div_term)
        return pe
```

### 12.6.1 前向傳播

```python
    def forward(self, token_ids):
        x = self.embedding[token_ids] + self.positional_encoding(len(token_ids))
        
        for i in range(len(self.W_Q)):
            Q = x @ self.W_Q[i]
            K = x @ self.W_K[i]
            V = x @ self.W_K[i]
            scores = Q @ K.T / np.sqrt(self.d_k)
            weights = softmax(scores)
            x = weights @ V @ self.W_O
            x = np.maximum(0, x @ self.W1[i]) @ self.W2[i]
            
        logits = x @ self.lm_head
        return logits
```

### 12.6.2 文字生成

```python
    def generate(self, token_ids, max_new_tokens):
        for _ in range(max_new_tokens):
            logits = self.forward(token_ids)
            next_token = np.argmax(logits[-1])
            token_ids = np.append(token_ids, next_token)
        return token_ids

vocab_size = 50
d_model = 16
num_heads = 2
num_layers = 2

model = MiniTransformer(vocab_size, d_model, num_heads, num_layers)

seed = [1, 2, 3, 4, 5]
output = model.forward(seed)

print("=" * 60)
print("Mini Transformer Demo")
print("=" * 60)
print(f"Vocab size: {vocab_size}")
print(f"d_model: {d_model}")
print(f"num_heads: {num_heads}")
print(f"num_layers: {num_layers}")
print(f"Input length: {len(seed)}")
print(f"Output logits shape: {output.shape}")

generated = model.generate(np.array(seed), 3)
print(f"\nGenerated token IDs: {generated.tolist()}")
```

### 12.6.3 Transformer 的訓練流程

1. **資料準備**：將文本轉換為 token 序列
2. **嵌入+位置編碼**：獲得每個 token 的表示
3. **堆疊 Transformer 層**：重複應用自注意力和前饋網路
4. **語言模型頭**：將表示映射到詞彙空間
5. **計算損失**：比較預測與真實下一個 token

### 12.6.4 PyTorch 實現要點

使用 PyTorch 實現 Transformer 時的關鍵點：

```python
import torch
import torch.nn as nn

class TransformerLM(nn.Module):
    def __init__(self, vocab_size, d_model, num_heads, num_layers):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.pos_encoding = PositionalEncoding(d_model)
        self.transformer = nn.TransformerDecoder(
            nn.TransformerDecoderLayer(d_model, num_heads),
            num_layers
        )
        self.lm_head = nn.Linear(d_model, vocab_size)
    
    def forward(self, x):
        x = self.embedding(x) + self.pos_encoding(x.shape[1])
        x = self.transformer(x, x)
        return self.lm_head(x)
```

## 12.7 Transformer 的優勢與應用

Transformer 的出現徹底改變了深度學習的多個領域。

### 12.7.1 Transformer 的核心優勢

| 優勢 | 說明 |
|------|------|
| 平行計算 | 所有位置的計算可以並行 |
| 長距離依賴 | 任意位置之間的路徑長度為 O(1) |
| 可擴展性 | 易於擴展到更大規模 |
| 通用性 | 可應用於多種任務 |

### 12.7.2 Transformer 家族

```
Transformer 家族樹：

                    Transformer
                    /         \
           Encoder              Decoder
           /    \                  \
      BERT     ViT              GPT系列
        |       |                  |
     RoBERTa  DeiT             GPT-2/3/4
     DistilBERT                ChatGPT
```

### 12.7.3 應用領域

| 領域 | 應用 |
|------|------|
| 自然語言處理 | 機器翻譯、問答、摘要、生成 |
| 電腦視覺 | 影像分類、檢測、分割 |
| 語音處理 | 語音辨識、合成 |
| 多模態 | 圖文理解、視頻分析 |
| 程式設計 | Code generation, 程式碼補全 |

## 12.8 總結

本章深入介紹了 Transformer 架構的核心原理和實現：

| 組件 | 說明 |
|------|------|
| 注意力機制 | Query-Key-Value 加權求和 |
| 自注意力 | 序列內部的長距離依賴 |
| 多頭注意力 | 多個表示子空間的並行學習 |
| 位置編碼 | 正弦/餘弦函數注入位置資訊 |
| Encoder | 雙向理解輸入序列 |
| Decoder | 自回歸生成輸出序列 |

Transformer 的發明是深度學習史上最重要的突破之一。它不僅在 NLP 領域取得了巨大成功，還擴展到電腦視覺、音頻處理等多個領域，成為現代人工智慧的基石。

從 GPT 到 BERT，從 ViT 到多模態模型，Transformer 架構展現了驚人的通用性和擴展性。隨著模型規模的不斷增大和能力的不斷增強，我們正在見證通用人工智慧 (AGI) 逐步成為現實的可能性。
