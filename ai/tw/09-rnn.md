# 第 9 章：循環神經網路 (RNN)

循環神經網路 (Recurrent Neural Network, RNN) 是一類專門用於處理序列資料的神經網路。與前饋神經網路不同，RNN 具有「記憶」能力，能夠利用之前的資訊來影響當前的輸出。這使得 RNN 特別適合處理文字、語音、影片等具有時間依賴性的資料。

## 9.1 RNN 基本原理與時間序列

RNN 的核心思想是在網路中引入循環連接，使得資訊可以在時間步之間傳遞。每個時間步的隱藏狀態不僅取決於當前輸入，還取決於上一個時間步的隱藏狀態。

[程式檔案：09-1-rnn-basic.py](../_code/09/09-1-rnn-basic.py)

```python
import torch
import torch.nn as nn

print("=" * 60)
print("09-1: RNN Basic Operations")
print("=" * 60)

batch_size = 2
seq_len = 5
input_size = 10
hidden_size = 8
num_layers = 1

rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True)

input_seq = torch.randn(batch_size, seq_len, input_size)
h_0 = torch.zeros(num_layers, batch_size, hidden_size)

output, h_n = rnn(input_seq, h_0)

print(f"\nInput shape: {input_seq.shape}")
print(f"Hidden state shape: {h_0.shape}")
print(f"Output shape: {output.shape}")
print(f"Final hidden state shape: {h_n.shape}")
```

### 9.1.1 RNN 的數學模型

RNN 的前向傳播可以表示為：

```
h_t = tanh(W_ih · x_t + W_hh · h_{t-1} + b_h)
y_t = W_oh · h_t + b_o
```

其中：
- x_t 是時間步 t 的輸入
- h_t 是時間步 t 的隱藏狀態
- h_{t-1} 是上一個時間步的隱藏狀態
- W_ih, W_hh, W_oh 是權重矩陣
- b_h, b_o 是偏置項

### 9.1.2 手動實現 RNN 細胞

讓我們用 NumPy 手動實現一個簡單的 RNN 細胞：

```python
print("\n--- Manual RNN Cell ---")

def rnn_cell(input_t, h_prev, W_xh, W_hh, b_h):
    h_current = torch.tanh(torch.matmul(input_t, W_xh.T) + 
                          torch.matmul(h_prev, W_hh.T) + b_h)
    return h_current

torch.manual_seed(42)
W_xh = torch.randn(hidden_size, input_size)
W_hh = torch.randn(hidden_size, hidden_size)
b_h = torch.randn(hidden_size)

input_t = input_seq[0, 0]
h_prev = torch.zeros(hidden_size)
h_t = rnn_cell(input_t, h_prev, W_xh, W_hh, b_h)

print(f"Single time step input: {input_t.shape}")
print(f"Hidden state output: {h_t.shape}")
```

### 9.1.3 雙向 RNN

雙向 RNN (Bidirectional RNN) 同時考慮序列的正向和反向資訊：

```python
print("\n--- Bidirectional RNN ---")
bi_rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True, bidirectional=True)
output_bi, h_n_bi = bi_rnn(input_seq, h_0)

print(f"Bidirectional output shape: {output_bi.shape}")
print(f"Bidirectional final hidden states: {h_n_bi.shape}")
```

雙向 RNN 適合需要完整上下文資訊的任務，如自然語言處理中的情感分析。

### 9.1.4 多層 RNN

深層 RNN (Stacked RNN) 透過堆疊多個 RNN 層來增加模型的表示能力：

```python
print("\n--- Multi-layer RNN ---")
num_layers = 3
ml_rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True)
output_ml, h_n_ml = ml_rnn(input_seq, h_0)

print(f"Multi-layer output shape: {output_ml.shape}")
print(f"Multi-layer final hidden states: {h_n_ml.shape}")
```

### 9.1.5 RNN 的梯度問題

RNN 面臨的主要挑戰是梯度消失和梯度爆炸問題：

| 問題 | 原因 | 解決方案 |
|------|------|----------|
| 梯度消失 | 長時間序列的反向傳播 | LSTM, GRU |
| 梯度爆炸 | 權重累積效應 | 梯度裁剪 |

## 9.2 長短期記憶網路 (LSTM)

LSTM (Long Short-Term Memory) 由 Sepp Hochreiter 和 Jürgen Schmidhuber 於 1997 年提出，是為了解決標準 RNN 的長期依賴問題而設計的。

[程式檔案：09-2-lstm.py](../_code/09/09-2-lstm.py)

```python
import torch
import torch.nn as nn

print("=" * 60)
print("09-2: LSTM Structure")
print("=" * 60)

batch_size = 2
seq_len = 5
input_size = 10
hidden_size = 8
num_layers = 1

lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)

input_seq = torch.randn(batch_size, seq_len, input_size)
h_0 = torch.zeros(num_layers, batch_size, hidden_size)
c_0 = torch.zeros(num_layers, batch_size, hidden_size)

output, (h_n, c_n) = lstm(input_seq, (h_0, c_0))

print(f"\nInput shape: {input_seq.shape}")
print(f"Hidden state shape: {h_0.shape}")
print(f"Cell state shape: {c_0.shape}")
print(f"Output shape: {output.shape}")
print(f"Final hidden state: {h_n.shape}")
print(f"Final cell state: {c_n.shape}")
```

### 9.2.1 LSTM 的核心組件：門控機制

LSTM 透過三個門控來控制資訊的流動：

1. **遺忘門 (Forget Gate)**：決定哪些資訊從細胞狀態中丟棄
2. **輸入門 (Input Gate)**：決定哪些新資訊存入細胞狀態
3. **輸出門 (Output Gate)**：決定輸出什麼資訊

```
遺忘門：f_t = σ(W_f · [h_{t-1}, x_t] + b_f)
輸入門：i_t = σ(W_i · [h_{t-1}, x_t] + b_i)
候選值：Ĉ_t = tanh(W_C · [h_{t-1}, x_t] + b_C)
細胞更新：C_t = f_t * C_{t-1} + i_t * Ĉ_t
輸出門：o_t = σ(W_o · [h_{t-1}, x_t] + b_o)
隱藏狀態：h_t = o_t * tanh(C_t)
```

### 9.2.2 手動實現 LSTM 細胞

```python
print("\n--- Manual LSTM Cell ---")

def lstm_cell_manual(input_t, h_prev, c_prev, W_ih, W_hh, b_ih, b_hh):
    gates = torch.matmul(input_t, W_ih.T) + torch.matmul(h_prev, W_hh.T)
    gates = gates + b_ih + b_hh
    
    i, f, g, o = gates.chunk(4, dim=1)
    
    i = torch.sigmoid(i)
    f = torch.sigmoid(f)
    g = torch.tanh(g)
    o = torch.sigmoid(o)
    
    c_current = f * c_prev + i * g
    h_current = o * torch.tanh(c_current)
    
    return h_current, c_current
```

### 9.2.3 LSTM 的優勢

| 特性 | 說明 |
|------|------|
| 長期記憶 | 細胞狀態可以長時間保存資訊 |
| 梯度流動 | 細胞狀態的殘差連接緩解梯度消失 |
| 選擇性 | 門控機制允許網路學習何時忘記/記憶 |

## 9.3 閘門循環單元 (GRU)

GRU (Gated Recurrent Unit) 由 Cho 等人於 2014 年提出，是 LSTM 的簡化版本，參數更少但效果相當。

[程式檔案：09-3-gru.py](../_code/09/09-3-gru.py)

```python
import torch
import torch.nn as nn

print("=" * 60)
print("09-3: GRU Structure")
print("=" * 60)

batch_size = 2
seq_len = 5
input_size = 10
hidden_size = 8
num_layers = 1

gru = nn.GRU(input_size, hidden_size, num_layers, batch_first=True)

input_seq = torch.randn(batch_size, seq_len, input_size)
h_0 = torch.zeros(num_layers, batch_size, hidden_size)

output, h_n = gru(input_seq, h_0)

print(f"\nInput shape: {input_seq.shape}")
print(f"Hidden state shape: {h_0.shape}")
print(f"Output shape: {output.shape}")
print(f"Final hidden state shape: {h_n.shape}")
```

### 9.3.1 GRU 的數學模型

GRU 將 LSTM 的三個門簡化為兩個：

```
更新門：z_t = σ(W_z · [h_{t-1}, x_t])
重置門：r_t = σ(W_r · [h_{t-1}, x_t])
候選值：h̃_t = tanh(W_h · [r_t * h_{t-1}, x_t])
隱藏狀態：h_t = (1 - z_t) * h_{t-1} + z_t * h̃_t
```

### 9.3.2 GRU vs LSTM 比較

```python
print("\n--- GRU vs LSTM Parameters ---")
lstm = nn.LSTM(input_size, hidden_size, num_layers)
gru = nn.GRU(input_size, hidden_size, num_layers)

lstm_params = sum(p.numel() for p in lstm.parameters())
gru_params = sum(p.numel() for p in gru.parameters())

print(f"LSTM parameters: {lstm_params}")
print(f"GRU parameters: {gru_params}")
print(f"GRU has fewer parameters because it combines gates")
```

| 特性 | LSTM | GRU |
|------|------|-----|
| 門數量 | 3 個門 + 細胞狀態 | 2 個門 |
| 參數數量 | 較多 | 較少 |
| 計算量 | 較大 | 較小 |
| 記憶能力 | 強 | 強（多數任務相當） |
| 適用場景 | 長序列複雜任務 | 一般序列任務 |

### 9.3.3 選擇建議

- **使用 GRU**：當計算資源有限，或序列相對較短
- **使用 LSTM**：當任務需要更精細的長期依賴控制

## 9.4 雙向 RNN 與深層 RNN

現代 RNN 架構通常結合雙向處理和多層堆疊，以獲得更強的表示能力。

### 9.4.1 雙向 RNN 的應用

雙向 RNN 同時處理正向和反向的序列資訊：

```python
print("\n--- Bidirectional LSTM ---")
bi_lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, bidirectional=True)
output_bi, (h_n_bi, c_n_bi) = bi_lstm(input_seq, (h_0, c_0))

print(f"Bidirectional output shape: {output_bi.shape}")
print(f"Bidirectional hidden states: {h_n_bi.shape}")
```

適合的任務：
- 語音辨識
- 命名實體識別
- 機器翻譯
- 情感分析

### 9.4.2 深層 RNN

深層 RNN (Stacked RNN) 透過堆疊多個循環層來增加模型深度：

```python
print("\n--- Multi-layer LSTM ---")
num_layers = 2
ml_lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
output_ml, (h_n_ml, c_n_ml) = ml_lstm(input_seq, (h_0, c_0))

print(f"Multi-layer output shape: {output_ml.shape}")
print(f"Multi-layer hidden states: {h_n_ml.shape}")
```

## 9.5 序列到序列 (Seq2Seq) 模型

Seq2Seq 模型是將一個序列轉換為另一個序列的架構，廣泛應用於機器翻譯、文字摘要、對話系統等任務。

[程式檔案：09-4-seq2seq.py](../_code/09/09-4-seq2seq.py)

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

print("=" * 60)
print("09-4: Seq2Seq Model")
print("=" * 60)

class Encoder(nn.Module):
    def __init__(self, input_dim, embed_dim, hidden_dim, n_layers=1):
        super().__init__()
        self.embedding = nn.Embedding(input_dim, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, n_layers, batch_first=True)
        
    def forward(self, x):
        embedded = self.embedding(x)
        outputs, (hidden, cell) = self.lstm(embedded)
        return hidden, cell

class Decoder(nn.Module):
    def __init__(self, output_dim, embed_dim, hidden_dim, n_layers=1):
        super().__init__()
        self.embedding = nn.Embedding(output_dim, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, n_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)
        
    def forward(self, x, hidden, cell):
        x = x.unsqueeze(1)
        embedded = self.embedding(x)
        output, (hidden, cell) = self.lstm(embedded, (hidden, cell))
        prediction = self.fc(output.squeeze(1))
        return prediction, hidden, cell
```

### 9.5.1 Seq2Seq 架構

Seq2Seq 模型由兩部分組成：
1. **編碼器 (Encoder)**：將輸入序列編碼為固定維度的上下文向量
2. **解碼器 (Decoder)**：根據上下文向量逐步生成輸出序列

### 9.5.2 Teacher Forcing

Teacher Forcing 是一種訓練技巧，在訓練時使用真實標籤而非模型預測作為解碼器的輸入：

```python
class Seq2Seq(nn.Module):
    def __init__(self, encoder, decoder):
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
        
    def forward(self, src, tgt, teacher_forcing_ratio=0.5):
        batch_size = tgt.shape[0]
        tgt_len = tgt.shape[1]
        tgt_vocab_size = self.decoder.fc.out_features
        
        outputs = torch.zeros(batch_size, tgt_len, tgt_vocab_size)
        
        hidden, cell = self.encoder(src)
        dec_input = tgt[:, 0]
        
        for t in range(1, tgt_len):
            output, hidden, cell = self.decoder(dec_input, hidden, cell)
            outputs[:, t] = output
            
            teacher_force = torch.rand(1).item() < teacher_forcing_ratio
            top1 = output.argmax(1)
            dec_input = tgt[:, t] if teacher_force else top1
            
        return outputs
```

### 9.5.3 貪心解碼與束搜索

```python
print("\n--- Inference (Greedy Decoding) ---")
model.eval()

def translate(src, model, max_len=15):
    model.eval()
    with torch.no_grad():
        hidden, cell = model.encoder(src)
        
        dec_input = torch.tensor([2])
        results = []
        
        for _ in range(max_len):
            output, hidden, cell = model.decoder(dec_input, hidden, cell)
            top1 = output.argmax(1)
            results.append(top1.item())
            
            if top1.item() == 3:
                break
            dec_input = top1
            
        return results
```

## 9.6 實作：文字生成與情感分類

### 9.6.1 文字生成

文字生成是 RNN 的經典應用，模型學習根據給定的文本片段預測下一個字符或單詞。

[程式檔案：09-5-text-generation.py](../_code/09/09-5-text-generation.py)

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

print("=" * 60)
print("09-5: Text Generation")
print("=" * 60)

class TextGenerator(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_layers=1):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, vocab_size)
        
    def forward(self, x, hidden=None):
        embedded = self.embedding(x)
        if hidden is None:
            output, hidden = self.lstm(embedded)
        else:
            output, hidden = self.lstm(embedded, hidden)
        prediction = self.fc(output)
        return prediction, hidden
```

#### 9.6.1.1 溫度採樣

溫度參數控制生成的隨機性：

```python
def generate(model, start_str, char_to_idx, idx_to_char, max_len=50, temperature=1.0):
    model.eval()
    
    input_seq = encode_text(start_str, char_to_idx).unsqueeze(0)
    generated = start_str
    
    hidden = None
    
    for _ in range(max_len):
        output, hidden = model(input_seq, hidden)
        
        output = output.squeeze(0) / temperature
        probs = F.softmax(output[-1], dim=0)
        
        next_idx = torch.multinomial(probs, 1).item()
        next_char = idx_to_char.get(next_idx, '<UNK>')
        
        if next_char == '<UNK>':
            break
            
        generated += next_char
        input_seq = torch.tensor([[next_idx]])
        
    return generated
```

| 溫度 | 效果 |
|------|------|
| 0.0 | 確定性輸出，總是選擇最高概率 |
| 0.5-0.7 | 平衡隨機性和質量 |
| 1.0 | 保持原始概率分佈 |
| > 1.0 | 增加隨機性，可能產生低質量輸出 |

### 9.6.2 情感分類

情感分類是將文本分類為正面或負面的任務，RNN 能夠捕捉文本的序列特徵。

[程式檔案：09-6-sentiment.py](../_code/09/09-6-sentiment.py)

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from collections import Counter

print("=" * 60)
print("09-6: Sentiment Classification")
print("=" * 60)

class SentimentRNN(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_layers, output_dim, dropout=0.3):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, num_layers, 
                           batch_first=True, bidirectional=True, dropout=dropout if num_layers > 1 else 0)
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_dim * 2, output_dim)
        
    def forward(self, x):
        embedded = self.dropout(self.embedding(x))
        output, (hidden, cell) = self.lstm(embedded)
        
        hidden = torch.cat((hidden[-2,:,:], hidden[-1,:,:]), dim=1)
        hidden = self.dropout(hidden)
        
        return self.fc(hidden)
```

#### 9.6.2.1 雙向 LSTM 的優勢

```python
def predict(text, model, vocab, max_len):
    model.eval()
    encoded = encode_text(text, vocab)
    
    if len(encoded) < max_len:
        padded = F.pad(encoded, (0, max_len - len(encoded)), value=0)
    else:
        padded = encoded[:max_len]
    
    x = padded.unsqueeze(0)
    
    with torch.no_grad():
        output = model(x)
        probs = F.softmax(output, dim=1)
        pred = output.argmax(1).item()
        
    return pred, probs[0]
```

#### 9.6.2.2 注意力機制

在序列分類中加入注意力機制可以讓模型聚焦於最相關的單詞：

```python
print("\n--- Sentiment with Attention ---")

class AttentionLayer(nn.Module):
    def __init__(self, hidden_dim):
        super().__init__()
        self.attention = nn.Linear(hidden_dim * 2, 1)
        
    def forward(self, lstm_output):
        attention_weights = F.softmax(self.attention(lstm_output), dim=1)
        weighted_output = torch.sum(attention_weights * lstm_output, dim=1)
        return weighted_output
```

### 9.6.3 CNN 用於文字分類

除了 RNN，CNN 也可用於文字分類，稱為 TextCNN：

```python
class SentimentCNN(nn.Module):
    def __init__(self, vocab_size, embed_dim, num_filters, filter_sizes, output_dim, dropout=0.3):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.convs = nn.ModuleList([
            nn.Conv1d(embed_dim, num_filters, fs) for fs in filter_sizes
        ])
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(len(filter_sizes) * num_filters, output_dim)
        
    def forward(self, x):
        embedded = self.embedding(x)
        embedded = embedded.permute(0, 2, 1)
        
        conv_outputs = [F.relu(conv(embedded)) for conv in self.convs]
        pooled = [F.max_pool1d(conv_out, conv_out.shape[2]).squeeze(2) for conv_out in conv_outputs]
        
        cat = self.dropout(torch.cat(pooled, dim=1))
        return self.fc(cat)
```

## 9.7 總結

本章介紹了循環神經網路用於序列資料處理的各種方法：

| 主題 | 關鍵點 |
|------|--------|
| RNN 基本原理 | 隱藏狀態傳遞時間資訊 |
| LSTM | 三個門控機制，解決長期依賴 |
| GRU | LSTM 的簡化版本 |
| 雙向 RNN | 同時利用前後文資訊 |
| Seq2Seq | Encoder-Decoder 架構 |
| 文字生成 | 溫度採樣控制隨機性 |
| 情感分類 | 序列分類的典型應用 |

RNN 及其變體在自然語言處理領域有著廣泛的應用。然而，標準 RNN 架構在處理非常長的序列時仍有局限。下一章將介紹生成對抗網路 (GAN)，這是一種強大的生成模型，能夠學習生成逼真的資料。
