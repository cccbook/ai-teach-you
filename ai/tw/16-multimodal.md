# 第 16 章：多模態模型

多模態學習是人工智慧領域的重要研究方向，旨在讓 AI 系統能夠理解和生成來自多種模態（如文字、圖像、音頻、影片）的資訊。本章將介紹 GPT-4V、Flamingo、BLIP 等多模態模型的核心原理，以及如何建構圖文對話系統。

## 16.1 多模態學習概述

多模態學習的核心挑戰是如何有效融合不同來源的資訊，並建立跨模態的統一表示。

### 16.1.1 模態的定義

| 模態 | 說明 | 範例 |
|------|------|------|
| 文字 | 自然語言符號 | 句子、段落 |
| 圖像 | 視覺像素陣列 | 照片、圖表 |
| 音頻 | 聲波信號 | 語音、音樂 |
| 影片 | 時空像素序列 | 電影、動畫 |
| 觸覺 | 接觸感測 | 壓力、温度 |

### 16.1.2 多模態任務分類

| 任務類型 | 說明 | 範例 |
|----------|------|------|
| 跨模態理解 | 從一種模態理解另一種 | 圖像描述、VQA |
| 跨模態生成 | 從一種模態生成另一種 | 文字生成圖像 |
| 多模態對話 | 多種模態的交互 | 圖文對話 |
| 模態轉換 | 模態之間的翻譯 | 語音辨識、TTS |

## 16.2 GPT-4V 與視覺理解

GPT-4V 是 OpenAI 發布的多模態大語言模型，能夠同時處理文字和圖像輸入。

[程式檔案：16-1-gpt4v.py](../_code/16/16-1-gpt4v.py)

```python
import numpy as np

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

class GPT4V:
    def __init__(self, image_channels=3, text_dim=512, vision_dim=768):
        self.image_encoder = np.random.randn(image_channels * 224 * 224, vision_dim) * 0.02
        self.text_encoder = np.random.randn(10000, text_dim) * 0.02
        self.fusion = np.random.randn(vision_dim + text_dim, 512) * 0.02
        self.lm_head = np.random.randn(512, 10000) * 0.02
        
    def encode_image(self, image):
        return image.reshape(image.shape[0], -1) @ self.image_encoder
    
    def encode_text(self, text_tokens):
        return self.text_encoder[text_tokens]
    
    def forward(self, image, text_tokens):
        img_emb = self.encode_image(image)
        text_emb = self.encode_text(text_tokens)
        combined = np.concatenate([img_emb, text_emb], axis=-1)
        fused = combined @ self.fusion
        logits = fused @ self.lm_head
        return logits

model = GPT4V()

batch_size = 1
image = np.random.randn(batch_size, 3, 224, 224)
text_tokens = np.array([[101, 202, 303, 404, 105]])

logits = model.forward(image, text_tokens)

print("=" * 60)
print("GPT-4V (Vision) Demo")
print("=" * 60)
print(f"Image shape: {image.shape}")
print(f"Text tokens: {text_tokens.shape}")
print(f"Output logits: {logits.shape}")
print("\n✓ GPT-4V processes both images and text:")
print("  - Visual understanding & reasoning")
print("  - Image description & captioning")
print("  - Multi-modal conversation")
print("  - Charts & document understanding")
```

### 16.2.1 GPT-4V 的能力

| 能力 | 說明 |
|------|------|
| 視覺理解 | 分析圖像中的物體、場景、動作 |
| 文字識別 | 讀取圖像中的文字 (OCR) |
| 空間推理 | 理解物體之間的空間關係 |
| 图表理解 | 分析圖表、圖形的含義 |
| 文件處理 | 處理截圖、表格、發票等 |
| 多輪對話 | 基於圖像進行對話 |

### 16.2.2 GPT-4V 架構特點

GPT-4V 的架構設計通常包含以下組件：

```
GPT-4V 處理流程：

圖像輸入
    ↓
┌─────────────────────────────────────────┐
│           Vision Encoder                 │
│   (可能使用 ViT 或 custom 架構)         │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│         Vision-Language Fusion           │
│   (將視覺特徵對齊到語言模型空間)         │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│           Language Model                 │
│   (處理文字和視覺資訊的混合輸入)         │
└─────────────────────────────────────────┘
                    ↓
文字輸出
```

### 16.2.3 GPT-4V 的應用場景

```python
# 圖像描述
response = gpt4v.chat([
    {"type": "image", "content": image},
    {"type": "text", "content": "描述這張圖片"}
])

# 視覺問答
response = gpt4v.chat([
    {"type": "image", "content": chart_image},
    {"type": "text", "content": "這張圖表的趨勢是什麼？"}
])

# 文件理解
response = gpt4v.chat([
    {"type": "image", "content": invoice},
    {"type": "text", "content": "這張發票的總金額是多少？"}
])
```

## 16.3 Flamingo 模型架構

Flamingo 是 DeepMind 開發的少樣本學習多模態模型，展示了出色的零樣本和少樣本能力。

[程式檔案：16-2-flamingo.py](../_code/16/16-2-flamingo.py)

```python
import numpy as np

class PerceiverResampler:
    def __init__(self, input_dim, output_dim, num_queries):
        self.query_tokens = np.random.randn(num_queries, input_dim) * 0.02
        self.cross_attention = np.random.randn(input_dim, input_dim) * 0.02
        
    def forward(self, x):
        queries = self.query_tokens[:1] @ np.ones((1, x.shape[1]))
        combined = np.concatenate([queries, x], axis=0)
        return combined @ self.cross_attention

class Flamingo:
    def __init__(self, vision_dim=768, text_dim=512, num_queries=64):
        self.vision_encoder = np.random.randn(224 * 224 * 3, vision_dim) * 0.02
        self.perceiver = PerceiverResampler(vision_dim, text_dim, num_queries)
        self.text_decoder = np.random.randn(text_dim, 32000) * 0.02
        
    def forward(self, image, text_tokens):
        vision_features = image.reshape(image.shape[0], -1) @ self.vision_encoder
        vision_features = self.perceiver.forward(vision_features)
        text_logits = text_tokens @ self.text_decoder
        return text_logits

flamingo = Flamingo()

image = np.random.randn(1, 3, 224, 224)
text_tokens = np.array([[101, 202, 303]])

output = flamingo.forward(image, text_tokens)

print("=" * 60)
print("Flamingo Demo")
print("=" * 60)
print(f"Vision encoder dim: 768")
print(f"Text decoder vocab: 32000")
print(f"Perceiver queries: 64")
print(f"\nImage shape: {image.shape}")
print(f"Text tokens: {text_tokens.shape}")
print(f"Output logits: {output.shape}")
print("\n✓ Flamingo architecture:")
print("  - Vision encoder (CLIP ViT)")
print("  - Perceiver Resampler (cross-modal)")
print("  - Text decoder (GPT-style)")
print("  - Few-shot learning capability")
```

### 16.3.1 Flamingo 架構詳解

```
Flamingo 架構：

圖像輸入
    ↓
┌─────────────────────────────────────────┐
│        Vision Encoder (Frozen)           │
│   使用預訓練的 CLIP ViT                  │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│        Perceiver Resampler               │
│   • 學習固定數量的查詢 tokens            │
│   • Cross-attention 融合視覺特徵          │
│   • 輸出：64 個條件化視覺 tokens         │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│     GATED XATTN-DENSE Layers             │
│   • 插入在語言模型層之間                  │
│   • 門控機制控制視覺資訊流動              │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│     Large Language Model (Frozen)        │
│   使用預訓練 的 LM (如 Chinchilla)       │
└─────────────────────────────────────────┘
                    ↓
文字輸出
```

### 16.3.2 Perceiver Resampler

Perceiver Resampler 是 Flamingo 的關鍵創新：

```python
class PerceiverResampler(nn.Module):
    def __init__(self, vision_dim, num_queries=64):
        self.num_queries = num_queries
        self.query_tokens = nn.Parameter(torch.randn(num_queries, vision_dim))
        
    def forward(self, vision_features):
        # vision_features: [B, seq_len, vision_dim]
        # query_tokens: [num_queries, vision_dim]
        
        # Cross-attention: queries 關注 vision features
        attn_output = self.cross_attention(
            self.query_tokens,
            vision_features
        )
        return attn_output
```

### 16.3.3 少樣本學習能力

Flamingo 的核心優勢是少樣本學習：

```python
# 少樣本分類示例
prompt = [
    {"type": "image", "content": cat_img},
    {"type": "text", "content": "This is a cat. "},
    {"type": "image", "content": dog_img},
    {"type": "text", "content": "This is a dog. "},
    {"type": "image", "content": bird_img},
    {"type": "text", "content": "This is a"}  # 模型預測
]
```

## 16.4 BLIP 系列模型

BLIP (Bootstrapped Language-Image Pre-training) 是 Salesforce 開發的多模態模型系列，特別擅長視覺語言任務。

[程式檔案：16-3-blip.py](../_code/16/16-3-blip.py)

```python
import numpy as np

class ImageEncoder:
    def __init__(self, img_dim, hidden_dim):
        self.proj = np.random.randn(img_dim, hidden_dim) * 0.02
        
    def forward(self, images):
        return images.reshape(images.shape[0], -1) @ self.proj

class TextDecoder:
    def __init__(self, hidden_dim, vocab_size):
        self.lm_head = np.random.randn(hidden_dim, vocab_size) * 0.02
        
    def forward(self, image_features, text_tokens):
        combined = image_features + np.random.randn(*text_tokens.shape) * 0.1
        return combined @ self.lm_head

class BLIP:
    def __init__(self, img_size, hidden_dim, vocab_size):
        img_dim = 3 * img_size * img_size
        self.image_encoder = ImageEncoder(img_dim, hidden_dim)
        self.text_decoder = TextDecoder(hidden_dim, vocab_size)
        
    def generate_caption(self, image):
        features = self.image_encoder.forward(image)
        dummy_tokens = np.array([[1, 2, 3]])
        logits = self.text_decoder.forward(features, dummy_tokens)
        return logits
    
    def answer_question(self, image, question):
        img_features = self.image_encoder.forward(image)
        q_features = question + np.random.randn(1, 32) * 0.1
        combined = np.concatenate([img_features, q_features], axis=-1)
        return combined @ np.random.randn(combined.shape[-1], 100) * 0.02

blip = BLIP(img_size=224, hidden_dim=768, vocab_size=30522)

image = np.random.randn(1, 3, 224, 224)
question = np.random.randn(1, 32)

caption_logits = blip.generate_caption(image)
answer_logits = blip.answer_question(image, question)

print("=" * 60)
print("BLIP (Bootstrapped Language-Image Pre-training) Demo")
print("=" * 60)
print(f"Image size: 224x224")
print(f"Hidden dimension: 768")
print(f"Vocab size: 30,522")
print(f"\nImage input: {image.shape}")
print(f"Caption logits: {caption_logits.shape}")
print(f"Answer logits: {answer_logits.shape}")
print("\n✓ BLIP features:")
print("  - Image-to-text generation")
print("  - Image-grounded conversation")
print("  - Zero-shot image captioning")
print("  - Multimodal understanding")
```

### 16.4.1 BLIP 的預訓練目標

BLIP 採用多任務學習，結合四個目標：

| 任務 | 說明 | 損失函數 |
|------|------|----------|
| Image-Text Contrastive (ITC) | 對比學習對齊圖像和文字 | InfoNCE |
| Image-Text Matching (ITM) | 判斷圖文是否匹配 | Binary CE |
| Language Modeling (LM) | 文字生成 | Cross-Entropy |
| Reactive Captioning (RC) | 生成描述性文字 | Cross-Entropy |

### 16.4.2 BLIP-2 的架構

BLIP-2 引入了輕量級的 Q-Former 來連接視覺和語言模態：

```
BLIP-2 架構：

┌─────────────────────────────────────────┐
│           Frozen Image Encoder           │
│   (如 ViT, CLIP)                        │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│              Q-Former                   │
│   • Query 數量：32                       │
│   • 學習提取與文字相關的視覺特徵          │
│   • Cross-attention + Self-attention     │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│         Frozen Language Model            │
│   (如 OPT, FlanT5)                      │
└─────────────────────────────────────────┘
                    ↓
文字輸出
```

### 16.4.3 Q-Former 原理

Q-Former 是 BLIP-2 的核心組件：

```python
class QFormer(nn.Module):
    def __init__(self, num_queries=32):
        self.query_tokens = nn.Parameter(torch.randn(num_queries, hidden_dim))
        self.cross_attention = CrossAttention()
        self.self_attention = SelfAttention()
        
    def forward(self, vision_features, text_embeddings):
        # 從視覺特徵中提取查詢表示
        query_output = self.cross_attention(self.query_tokens, vision_features)
        
        # 與文字交互
        combined = torch.cat([query_output, text_embeddings], dim=1)
        output = self.self_attention(combined)
        
        return output
```

## 16.5 實作：圖文對話系統

讓我們實現一個簡單的多模態對話系統。

[程式檔案：16-4-multimodal-chat.py](../_code/16/16-4-multimodal-chat.py)

```python
import numpy as np

class MultimodalChat:
    def __init__(self):
        self.image_encoder = np.random.randn(224*224*3, 512) * 0.02
        self.text_encoder = np.random.randn(10000, 512) * 0.02
        self.decoder = np.random.randn(512, 10000) * 0.02
        
        self.history = []
        
    def process_image(self, image):
        return image.reshape(1, -1) @ self.image_encoder
    
    def process_text(self, text_tokens):
        return self.text_encoder[text_tokens]
    
    def generate_response(self, image, text_input):
        img_emb = self.process_image(image)
        text_emb = self.process_text(text_input)
        
        combined = (img_emb + text_emb) / 2
        
        logits = combined @ self.decoder
        response_tokens = np.argmax(logits, axis=-1)
        
        return response_tokens
    
    def chat(self, image=None, text=None):
        if image is not None:
            self.history.append({"type": "image"})
        if text is not None:
            self.history.append({"type": "text", "content": text})
        
        response = self.generate_response(image, [101, 202, 303])
        
        return {"response": response.tolist(), "history_len": len(self.history)}

chat = MultimodalChat()

image = np.random.randn(1, 3, 224, 224)

result1 = chat.chat(image=image, text="What do you see?")
result2 = chat.chat(text="Tell me more")

print("=" * 60)
print("Multimodal Chat Demo")
print("=" * 60)
print(f"\n[Turn 1] Image + Text: 'What do you see?'")
print(f"  Response tokens: {result1['response']}")
print(f"  History length: {result1['history_len']}")

print(f"\n[Turn 2] Text only: 'Tell me more'")
print(f"  Response tokens: {result2['response']}")
print(f"  History length: {result2['history_len']}")

print("\n✓ Multimodal chat capabilities:")
print("  - Image understanding + conversation")
print("  - Multi-turn dialogue")
print("  - Context preservation")
print("  - Seamless modality switching")
```

### 16.5.1 多模態對話系統架構

```
多模態對話系統架構：

┌──────────────────────────────────────────────────────────┐
│                      使用者輸入                            │
│   • 圖像 + 文字 (第一輪)                                  │
│   • 文字 (後續輪)                                         │
└──────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────┐
│                    輸入處理                               │
│   • 圖像編碼器 (ViT/CLIP)                                │
│   • 文字編碼器 (Transformer)                             │
│   • 對話歷史編碼                                          │
└──────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────┐
│                  多模態融合                               │
│   • 特徵拼接                                              │
│   • Cross-attention                                      │
│   • 門控機制                                              │
└──────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────┐
│                  回應生成                                 │
│   • 自回歸文字生成                                        │
│   • 多模態輸出                                            │
└──────────────────────────────────────────────────────────┘
                          ↓
                        回應
```

### 16.5.2 對話歷史管理

```python
class ConversationManager:
    def __init__(self, max_history=10):
        self.history = []
        self.max_history = max_history
    
    def add_turn(self, role, content, modality="text"):
        self.history.append({
            "role": role,
            "content": content,
            "modality": modality
        })
        
        # 保持歷史長度
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def format_history(self):
        formatted = []
        for turn in self.history:
            if turn["modality"] == "image":
                formatted.append("[Image]")
            else:
                formatted.append(f"{turn['role']}: {turn['content']}")
        return "\n".join(formatted)
```

### 16.5.3 多模態注意力機制

```python
class MultimodalAttention(nn.Module):
    def __init__(self, vision_dim, text_dim, hidden_dim):
        self.vision_proj = nn.Linear(vision_dim, hidden_dim)
        self.text_proj = nn.Linear(text_dim, hidden_dim)
        self.cross_attention = nn.MultiheadAttention(hidden_dim, num_heads=8)
    
    def forward(self, vision_features, text_features):
        # 投影到相同空間
        v_proj = self.vision_proj(vision_features)
        t_proj = self.text_proj(text_features)
        
        # Cross-attention
        attn_output, _ = self.cross_attention(
            t_proj, v_proj, v_proj
        )
        
        return attn_output
```

## 16.6 多模態模型的評估

多模態模型的評估需要綜合考慮多個方面。

### 16.6.1 常用評估基準

| 基準 | 任務 | 說明 |
|------|------|------|
| VQAv2 | 視覺問答 | 開放域視覺問答 |
| GQA | 視覺推理 | 結構化視覺推理 |
| COCO Caption | 圖像描述 | 生成描述性文字 |
| Flickr30k | 圖文檢索 | 圖像-文字匹配 |
| NoCaps | 開放域描述 | 未見過類別的描述 |

### 16.6.2 評估指標

| 指標 | 適用任務 | 說明 |
|------|----------|------|
| BLEU | 文字生成 | n-gram 重合度 |
| ROUGE | 摘要生成 | 召回率導向 |
| CIDEr | 圖像描述 | 人工評分的相關性 |
| SPICE | 場景理解 | 語義圖解析 |
| VQA Score | 視覺問答 | 準確率 |

## 16.7 總結

本章介紹了多模態學習的核心概念和重要模型：

| 模型 | 機構 | 核心貢獻 |
|------|------|----------|
| GPT-4V | OpenAI | 強大的視覺理解和推理 |
| Flamingo | DeepMind | 少樣本學習能力 |
| BLIP | Salesforce | 統一的視覺語言預訓練 |
| LLaVA | 開源 | GPT-4V 風格的開源方案 |

多模態 AI 代表了人工智慧的下一個發展方向，它使得 AI 系統能夠像人類一樣，綜合理解和處理來自不同感官的資訊。從 GPT-4V 的視覺理解到 Flamingo 的少樣本學習，多模態模型正在快速縮小 AI 與人類認知能力之間的差距。
