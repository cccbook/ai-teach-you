# 第 11 章：現代語言模型簡介

語言模型是自然語言處理的核心技術，它的目標是學習語言的機率分佈，預測下一個詞或評估句子的合理性。從早期的統計方法到現代的深度學習，語言模型經歷了巨大的演進。本章將介紹語言模型的發展歷程和關鍵技術。

## 11.1 語言模型的發展歷程

語言模型的發展可以分為幾個重要階段：

```
┌──────────────────────────────────────────────────────────────┐
│                      語言模型演進                             │
├──────────────────────────────────────────────────────────────┤
│  1950s-1990s    │  傳統統計方法：N-gram, HMM                 │
│  2000-2013      │  神經網路興起：NNLM, Word2Vec              │
│  2013-2017      │  RNN/LSTM 序列建模                         │
│  2017-         │  Transformer 時代：BERT, GPT               │
│  2020-         │  大語言模型：GPT-4, Claude, LLaMA           │
└──────────────────────────────────────────────────────────────┘
```

### 11.1.1 語言模型的任務

語言模型的核心任務是計算句子的機率：

```
P(w_1, w_2, ..., w_n) = P(w_1) × P(w_2|w_1) × ... × P(w_n|w_1,...,w_{n-1})
```

### 11.1.2 語言模型的評估指標

| 指標 | 說明 | 應用場景 |
|------|------|----------|
| Perplexity | 衡量模型預測能力 | 語言建模 |
| BLEU | 翻譯品質評估 | 機器翻譯 |
| ROUGE | 生成品質評估 | 文字摘要 |
| GLUE/SuperGLUE | 綜合 NLP 任務 | 模型評測 |

## 11.2 N-gram 與神經語言模型

N-gram 是最傳統的統計語言模型，而神經語言模型則開啟了深度學習在 NLP 應用的先河。

[程式檔案：11-1-ngram.py](../_code/11/11-1-ngram.py)

```python
#!/usr/bin/env python3
"""
Chapter 11-1: N-gram Language Model
基礎的統計語言模型
"""

import numpy as np
from collections import defaultdict, Counter
import re

class NGramModel:
    def __init__(self, n=2):
        self.n = n
        self.ngram_counts = defaultdict(Counter)
        self.context_counts = defaultdict(int)
        self.vocabulary = set()
        
    def tokenize(self, text):
        return ['<s>'] * (self.n - 1) + text.lower().split() + ['</s>']
    
    def train(self, corpus):
        sentences = corpus.split('.')
        for sentence in sentences:
            if sentence.strip():
                tokens = self.tokenize(sentence)
                self.vocabulary.update(tokens)
                
                for i in range(len(tokens) - self.n + 1):
                    ngram = tuple(tokens[i:i+self.n])
                    context = ngram[:-1]
                    next_word = ngram[-1]
                    
                    self.ngram_counts[context][next_word] += 1
                    self.context_counts[context] += 1
    
    def predict(self, context):
        context = tuple(context[-(self.n-1):])
        if context not in self.ngram_counts:
            return '<unk>'
        
        candidates = self.ngram_counts[context]
        total = self.context_counts[context]
        
        probs = {word: count/total for word, count in candidates.items()}
        return max(probs, key=probs.get)
    
    def probability(self, word, context):
        context = tuple(context[-(self.n-1):])
        if context not in self.ngram_counts:
            return 1/len(self.vocabulary)
        
        count = self.ngram_counts[context].get(word, 0)
        total = self.context_counts[context]
        return (count + 1) / (total + len(self.vocabulary))
```

### 11.2.1 N-gram 的原理

N-gram 模型假設第 n 個詞只與前 n-1 個詞相關：

```
P(w_n | w_1, ..., w_{n-1}) ≈ P(w_n | w_{n-N+1}, ..., w_{n-1})
```

| N 值 | 名稱 | 優點 | 缺點 |
|------|------|------|------|
| 1 | Unigram | 簡單 | 無上下文 |
| 2 | Bigram | 簡單上下文 | 稀疏性高 |
| 3 | Trigram | 較好上下文 | 稀疏性高 |
| N | N-gram | 更豐富上下文 | 計算爆炸 |

### 11.2.2 平滑技術

為了解決零機率問題，使用平滑技術：

```python
print("\n[Smoothing]")
print("  Add-k smoothing: P(w|c) = (count + k) / (total + k*|V|)")
print("  Good-Turing: 重新分配概率給低頻詞")
```

| 方法 | 公式 | 特點 |
|------|------|------|
| Add-k | (c + k) / (N + k|V|) | 簡單直觀 |
| Good-Turing | 重新估計稀疏計數 | 理論嚴謹 |
| Kneser-Ney | 基於上下文平滑 | 效果較好 |

### 11.2.3 N-gram 的局限

```
[Limitations]
  • 稀疏性問題
  • 無法捕捉長距離依賴
  • 沒有語義理解
```

## 11.3 Word2Vec, GloVe, FastText

詞向量是將詞映射到稠密向量空間的技術，使得語義相似的詞在向量空間中距離相近。

### 11.3.1 Word2Vec

Word2Vec 由 Mikolov 等人於 2013 年提出，是第一個成功將詞向量用於大規模語言建模的方法。

[程式檔案：11-2-word2vec.py](../_code/11/11-2-word2vec.py)

```python
#!/usr/bin/env python3
"""
Chapter 11-2: Word2Vec
Mikolov 2013 提出的詞向量模型
Skip-gram 與 CBOW
"""

import numpy as np

class Word2Vec:
    def __init__(self, vocab_size=10000, embedding_dim=100):
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        
        np.random.seed(42)
        self.target_embeddings = np.random.randn(vocab_size, embedding_dim) * 0.1
        self.context_embeddings = np.random.randn(vocab_size, embedding_dim) * 0.1
        
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def skip_gram(self, center_word, context_word):
        center_idx = hash(center_word) % self.vocab_size
        context_idx = hash(context_word) % self.vocab_size
        
        center_emb = self.target_embeddings[center_idx]
        context_emb = self.context_embeddings[context_idx]
        
        score = np.dot(center_emb, context_emb)
        prob = self.sigmoid(score)
        
        return prob
    
    def cbow(self, context_words, target_word):
        context_embs = []
        for word in context_words:
            idx = hash(word) % self.vocab_size
            context_embs.append(self.context_embeddings[idx])
        
        avg_emb = np.mean(context_embs, axis=0)
        target_idx = hash(target_word) % self.vocab_size
        target_emb = self.target_embeddings[target_idx]
        
        score = np.dot(avg_emb, target_emb)
        prob = self.sigmoid(score)
        
        return prob
```

#### Word2Vec 的兩種架構

| 架構 | 輸入 | 輸出 | 適用場景 |
|------|------|------|----------|
| Skip-gram | 中心詞 | 預測上下文詞 | 小語料庫、高頻詞 |
| CBOW | 上下文詞 | 預測中心詞 | 大語料庫、訓練速度快 |

#### 詞類比推理

Word2Vec 的一個驚人特性是可以進行詞類比推理：

```
vec("king") - vec("man") + vec("woman") ≈ vec("queen")
vec("Paris") - vec("France") + vec("Germany") ≈ vec("Berlin")
```

### 11.3.2 負採樣

負採樣 (Negative Sampling) 是用於加速 Word2Vec 訓練的技術：

```python
print("\n[Negative Sampling]")
print("  減少 softmax 計算量")
print("  每個正樣本配 K 個負樣本")
print("  目標: 最大化正樣本，最小化負樣本")
```

### 11.3.3 GloVe

GloVe (Global Vectors) 由斯坦福大學於 2014 年提出，結合了全局共現統計資訊和局部上下文。

[程式檔案：11-3-glove.py](../_code/11/11-3-glove.py)

```python
#!/usr/bin/env python3
"""
Chapter 11-3: GloVe
Global Vectors for Word Representation
結合全局統計與局部上下文
"""

import numpy as np

class GloVe:
    def __init__(self, vocab_size=10000, embedding_dim=100):
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        
        np.random.seed(42)
        self.W = np.random.randn(vocab_size, embedding_dim) * 0.1
        self.W_tilde = np.random.randn(vocab_size, embedding_dim) * 0.1
        self.b = np.random.randn(vocab_size) * 0.1
        self.b_tilde = np.random.randn(vocab_size) * 0.1
        
        self.word_to_idx = {}
        self.co_occurrence = {}
        
    def build_vocab(self, corpus):
        words = corpus.lower().split()
        unique_words = list(set(words))
        
        for idx, word in enumerate(unique_words):
            self.word_to_idx[word] = idx
        
        for i in range(len(words) - 1):
            w1, w2 = words[i], words[i+1]
            if w1 in self.word_to_idx and w2 in self.word_to_idx:
                key = (self.word_to_idx[w1], self.word_to_idx[w2])
                self.co_occurrence[key] = self.co_occurrence.get(key, 0) + 1
    
    def weighting_function(self, x):
        if x < 100:
            return (x / 100) ** 0.75
        return 1.0
    
    def loss(self, i, j, x_ij):
        w_i = self.W[i]
        w_j = self.W_tilde[j]
        b_i = self.b[i]
        b_j = self.b_tilde[j]
        
        pred = np.dot(w_i, w_j) + b_i + b_j
        weight = self.weighting_function(x_ij)
        
        diff = pred - np.log(x_ij + 1e-8)
        return weight * diff * diff
```

#### GloVe 的目標函數

```
J = Σ f(X_ij)(w_i^T w_j + b_i + b_j - log(X_ij))²
```

其中 f(x) 是加權函數：
```
f(x) = (x/x_max)^α  if x < x_max
     = 1            otherwise
```

#### Word2Vec vs GloVe

| 特性 | Word2Vec | GloVe |
|------|----------|-------|
| 方法 | 預測式 | 統計式 |
| 上下文 | 局部 | 全局 |
| 訓練速度 | 快 | 更快 |
| 記憶體需求 | 低 | 高 |
| 詞類比任務 | 好 | 更好 |

## 11.4 ELMO 與情境化詞向量

傳統的詞向量（如 Word2Vec、GloVe）是靜態的，每個詞只有一個固定的向量表示。然而，同一個詞在不同的上下文中有不同的含義。ELMo 和 BERT 解決了這個問題。

### 11.4.1 ELMo：情境化詞向量

ELMo (Embeddings from Language Models) 由 AllenNLP 團隊於 2018 年提出，使用雙向 LSTM 產生情境化詞向量。

ELMo 的創新之處：
1. **雙向語言模型**：同時考慮左右上下文
2. **多層表示**：不同層捕捉不同層次的語言特徵
3. **情境相關**：同一詞在不同句子中有不同表示

### 11.4.2 層級表示

ELMo 的多層雙向 LSTM 捕捉不同類型的資訊：

| 層級 | 捕捉的特徵 |
|------|-----------|
| 底層 LSTM | 句法資訊（詞性、句法關係） |
| 高層 LSTM | 語義資訊（詞義消歧、情緒） |

### 11.4.3 BERT：雙向 Transformer

BERT (Bidirectional Encoder Representations from Transformers) 是 Google 於 2018 年提出的革命性模型。

[程式檔案：11-4-bert.py](../_code/11/11-4-bert.py)

```python
#!/usr/bin/env python3
"""
Chapter 11-4: BERT
Bidirectional Encoder Representations from Transformers
"""

import numpy as np

class BERT:
    def __init__(self, vocab_size=30522, hidden_dim=768, num_layers=12):
        self.vocab_size = vocab_size
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        
        np.random.seed(42)
        
        self.token_embedding = np.random.randn(vocab_size, hidden_dim) * 0.02
        self.position_embedding = np.random.randn(512, hidden_dim) * 0.02
        self.segment_embedding = np.random.randn(2, hidden_dim) * 0.02
        
        self.transformer_layers = [
            {
                'attention': np.random.randn(hidden_dim, hidden_dim) * 0.02,
                'ffn': np.random.randn(hidden_dim, hidden_dim * 4) * 0.02,
                'layer_norm_1': np.ones(hidden_dim),
                'layer_norm_2': np.ones(hidden_dim),
            }
            for _ in range(num_layers)
        ]
```

#### BERT 的預訓練任務

1. **遮罩語言模型 (MLM)**
   - 隨機遮罩 15% 的 token
   - 預測被遮罩的詞
   - 雙向上下文建模

2. **下一句預測 (NSP)**
   - 判斷句子 B 是否是句子 A 的下一句
   - 學習句子間關係

#### BERT 的架構規模

| 配置 | 層數 | 隱藏維度 | 注意力頭 | 參數量 |
|------|------|----------|----------|--------|
| BERT-Tiny | 2 | 128 | 2 | 4M |
| BERT-Mini | 4 | 256 | 4 | 11M |
| BERT-Small | 4 | 512 | 8 | 44M |
| BERT-Base | 12 | 768 | 12 | 110M |
| BERT-Large | 24 | 1024 | 16 | 340M |

### 11.4.4 BERT 的下游應用

BERT 可以透過微調應用於各種 NLP 任務：

```python
print("\n[Fine-tuning Tasks]")
print("  • 文本分類 (Classification)")
print("  • 命名實體識別 (NER)")
print("  • 問答 (Question Answering)")
print("  • 句子對分類 (Sentence Pair)")
```

## 11.5 GPT 系列的演進

GPT (Generative Pre-trained Transformer) 系列是 OpenAI 開發的自回歸語言模型，與 BERT 的主要區別是使用 Transformer 解碼器架構。

### 11.5.1 GPT-1：開創先河

GPT-1 (2018) 首次展示了預訓練+微調範式的強大潛力：
- 單向 Transformer 解碼器
- 預訓練：標準語言模型
- 微調：各種下游任務

### 11.5.2 GPT-2：規模突破

GPT-2 (2019) 展示了模型規模的重要性：
- 15 億參數
- 高品質文字生成
-  Zero-shot 任務執行能力

### 11.5.3 GPT-3：湧現能力

GPT-3 (2020) 是規模的質變：
- 1750 億參數
- Few-shot 學習能力
- 無需任務特定微調
- 湧現出意想不到的能力

### 11.5.4 GPT-4 與後續

GPT-4 (2023) 帶來了多模態能力：
- 文字+圖像輸入
- 更強的推理能力
- 更安全的輸出

## 11.6 使用 GPT API

現代大語言模型透過 API 提供服務，讓開發者能夠輕鬆使用強大的語言模型能力。

[程式檔案：11-5-gpt-api.py](../_code/11/11-5-gpt-api.py)

```python
#!/usr/bin/env python3
"""
Chapter 11-5: GPT API Demo
使用 OpenAI GPT API 進行文本生成
"""

import json
import time

class GPTAPI:
    def __init__(self, api_key=None):
        self.api_key = api_key or "demo-key"
        self.model = "gpt-4"
        self.max_tokens = 100
        
    def chat_completion(self, messages, temperature=0.7, top_p=1.0):
        response = {
            "id": f"chatcmpl-{hash(str(messages)) % 1000000}",
            "model": self.model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "This is a simulated response. In production, use openai.OpenAI() API."
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": sum(len(m["content"].split()) for m in messages),
                "completion_tokens": 20,
                "total_tokens": sum(len(m["content"].split()) for m in messages) + 20
            }
        }
        
        return response
    
    def generate(self, prompt, system_prompt=None):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self.chat_completion(messages)
        return response["choices"][0]["message"]["content"]
```

### 11.6.1 API 使用範例

```python
from openai import OpenAI

client = OpenAI(api_key="sk-...")
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "你是有用的助手"},
        {"role": "user", "content": "解釋什麼是深度學習"}
    ],
    temperature=0.7,
    max_tokens=500
)

print(response.choices[0].message.content)
```

### 11.6.2 關鍵參數

```python
print("\n[Parameters]")
print("  • temperature: 控制隨機性 (0=確定性, 2=創意)")
print("  • top_p: nucleus sampling 閾值")
print("  • max_tokens: 最大生成 tokens")
print("  • presence_penalty: 降低重複")
print("  • frequency_penalty: 降低高頻詞")
```

| 參數 | 範圍 | 效果 |
|------|------|------|
| temperature | 0-2 | 越低越確定，越高越隨機 |
| top_p | 0-1 | nucleus sampling 閾值 |
| max_tokens | 1-∞ | 生成最大 token 數 |
| presence_penalty | -2~2 | 降低重複提及 |
| frequency_penalty | -2~2 | 降低高頻詞 |

### 11.6.3 可用模型

```python
print("\n[Models Available]")
print("  • gpt-4-turbo: 最新 4o 模型")
print("  • gpt-4: 強大但較慢")
print("  • gpt-3.5-turbo: 快速，便宜")
print("  • gpt-3.5-turbo-instruct: 指令調優版本")
```

### 11.6.4 最佳實踐

```python
print("\n[Best Practices]")
print("  1. 使用 system prompt 定義行為")
print("  2. 提供具體上下文和範例")
print("  3. 控制 temperature 平衡確定性與創意")
print("  4. 使用 Few-shot prompting")
```

## 11.7 總結

本章介紹了現代語言模型的發展歷程：

| 階段 | 技術 | 關鍵創新 |
|------|------|----------|
| 早期 | N-gram | 統計語言模型 |
| 中期 | Word2Vec, GloVe | 詞向量表示 |
| 過渡 | ELMo | 情境化詞向量 |
| 現代 | BERT, GPT | Transformer 架構 |
| 當代 | GPT-4, Claude | 大語言模型 |

語言模型的演進展示了人工智慧在理解和使用語言方面的巨大進步。從統計方法到深度學習，從單任務模型到大語言模型，每一次突破都帶來了新的可能性。

下一章將深入介紹 Transformer 架構，這是現代語言模型的基石，我們將從注意力機制開始，逐步解構這個革命性的模型。
