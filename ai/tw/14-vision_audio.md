# 第 14 章：視覺與聽覺模型

Transformer 架構不僅在自然語言處理領域取得巨大成功，還徹底改變了電腦視覺和語音處理領域。本章將介紹 Vision Transformer (ViT)、CLIP、Whisper、TTS 等視覺與聽覺模型的核心原理與應用。

## 14.1 Vision Transformer (ViT)

Vision Transformer (ViT) 將 Transformer 架構應用於影像分類任務，打破了 CNN 在視覺領域的長期主導地位。

[程式檔案：14-1-vit.py](../_code/14/14-1-vit.py)

```python
import numpy as np

class PatchEmbedding:
    def __init__(self, img_size=224, patch_size=16, in_channels=3, d_model=768):
        self.img_size = img_size
        self.patch_size = patch_size
        self.num_patches = (img_size // patch_size) ** 2
        self.d_model = d_model
        
        self.proj = np.random.randn(self.num_patches, in_channels * patch_size ** 2, d_model) * 0.02
        
    def forward(self, x):
        batch_size = x.shape[0]
        x = x.reshape(batch_size, self.num_patches, -1)
        return x @ self.proj

class ViT:
    def __init__(self, img_size=224, patch_size=16, in_channels=3, d_model=768, num_heads=12, num_layers=12):
        self.patch_embed = PatchEmbedding(img_size, patch_size, in_channels, d_model)
        self.num_patches = self.patch_embed.num_patches
        
        self.cls_token = np.random.randn(1, 1, d_model) * 0.02
        self.pos_embed = np.random.randn(1, self.num_patches + 1, d_model) * 0.02
        
        self.transformer_blocks = num_layers
        
    def forward(self, x):
        batch_size = x.shape[0]
        
        x = self.patch_embed.forward(x)
        
        cls_tokens = np.tile(self.cls_token, (batch_size, 1, 1))
        x = np.concatenate([cls_tokens, x], axis=1)
        
        x = x + self.pos_embed
        
        return x

img_size = 224
patch_size = 16
in_channels = 3
d_model = 768
num_layers = 12

vit = ViT(img_size, patch_size, in_channels, d_model, num_layers=num_layers)

batch_size = 2
x = np.random.randn(batch_size, in_channels, img_size, img_size)

output = vit.forward(x)

print("=" * 60)
print("ViT (Vision Transformer) Demo")
print("=" * 60)
print(f"Image size: {img_size}x{img_size}")
print(f"Patch size: {patch_size}x{patch_size}")
print(f"Number of patches: {vit.num_patches}")
print(f"d_model: {d_model}")
print(f"Input shape: {x.shape}")
print(f"Output shape: {output.shape}")
print("\n✓ ViT treats images as sequences of patches,")
print("  applying transformer architecture to vision tasks")
```

### 14.1.1 ViT 的核心思想

ViT 將影像視為一序列的 Patch，類似於文字序列中的 Token：

```
ViT 處理流程：

┌─────────────────────────────────────────────┐
│                                             │
│   輸入影像 (224×224×3)                       │
│        ↓                                    │
│   分割成 14×14 = 196 個 Patch (16×16×3)    │
│        ↓                                    │
│   每個 Patch 線性投影為 d_model 維向量       │
│        ↓                                    │
│   添加 [CLS] token 和位置編碼               │
│        ↓                                    │
│   標準 Transformer Encoder                   │
│        ↓                                    │
│   [CLS] token 的輸出作為分類結果            │
│                                             │
└─────────────────────────────────────────────┘
```

### 14.1.2 Patch Embedding 原理

```python
class PatchEmbedding:
    def __init__(self, img_size, patch_size, in_channels, d_model):
        self.num_patches = (img_size // patch_size) ** 2
        self.projection = nn.Linear(patch_size * patch_size * in_channels, d_model)
    
    def forward(self, x):
        x = x.unfold(2, self.patch_size, self.patch_size)  # 分割 Patch
        x = x.unfold(3, self.patch_size, self.patch_size)
        x = x.flatten(2, 3)  # 展平每個 Patch
        x = self.projection(x)  # 線性投影
        return x
```

### 14.1.3 ViT vs CNN

| 特性 | ViT | CNN |
|------|-----|-----|
| 架構 | Transformer | 卷積網路 |
| 歸納偏置 | 少，依賴大量資料 | 多 (局部性、平移不變性) |
| 大規模訓練 | 更有效 | 需要更多資料 |
| 計算複雜度 | O(n²) | O(n) |
| 可解釋性 | 注意力可視化 | 特徵圖可視化 |

### 14.1.4 ViT 變體

| 模型 | 發布者 | 特點 |
|------|--------|------|
| ViT | Google | 原始 ViT 架構 |
| DeiT | Meta | 蒸餾訓練，數據高效 |
| Swin Transformer | Microsoft | 階層式結構 |
| BEiT | Microsoft | 影像重建預訓練 |

## 14.2 CLIP 與對比學習

CLIP (Contrastive Language-Image Pre-training) 開創了用自然語言監督學習視覺表示的新範式。

[程式檔案：14-2-clip.py](../_code/14/14-2-clip.py)

```python
import numpy as np

class CLIPTextEncoder:
    def __init__(self, vocab_size, d_model):
        self.embedding = np.random.randn(vocab_size, d_model) * 0.02
        
    def forward(self, token_ids):
        return self.embedding[token_ids]

class CLIPImageEncoder:
    def __init__(self, img_channels, d_model):
        self.proj = np.random.randn(img_channels, d_model) * 0.02
        
    def forward(self, images):
        batch_size = images.shape[0]
        return images.reshape(batch_size, -1) @ self.proj

class CLIP:
    def __init__(self, vocab_size, d_model, img_channels):
        self.text_encoder = CLIPTextEncoder(vocab_size, d_model)
        self.image_encoder = CLIPImageEncoder(img_channels, d_model)
        self.d_model = d_model
        
        self.text_proj = np.random.randn(d_model, d_model) * 0.02
        self.image_proj = np.random.randn(d_model, d_model) * 0.02
        
    def get_text_features(self, token_ids):
        text_embeds = self.text_encoder.forward(token_ids)
        text_embeds = text_embeds @ self.text_proj
        return text_embeds / np.linalg.norm(text_embeds, axis=-1, keepdims=True)
    
    def get_image_features(self, images):
        image_embeds = self.image_encoder.forward(images)
        image_embeds = image_embeds @ self.image_proj
        return image_embeds / np.linalg.norm(image_embeds, axis=-1, keepdims=True)
    
    def contrastive_loss(self, text_features, image_features):
        logits = text_features @ image_features.T
        labels = np.arange(text_features.shape[0])
        loss = np.mean(np.diag(logits) - np.log(np.sum(np.exp(logits), axis=-1) + 1e-8))
        return loss

vocab_size = 50000
d_model = 512
img_channels = 3 * 224 * 224

clip = CLIP(vocab_size, d_model, img_channels)

batch_size = 4
token_ids = np.random.randint(0, vocab_size, (batch_size, 77))
images = np.random.randn(batch_size, 3, 224, 224)

text_features = clip.get_text_features(token_ids)
image_features = clip.get_image_features(images)

loss = clip.contrastive_loss(text_features, image_features)

print("=" * 60)
print("CLIP (Contrastive Language-Image Pre-training) Demo")
print("=" * 60)
print(f"Vocab size: {vocab_size:,}")
print(f"d_model: {d_model}")
print(f"Image channels: {img_channels:,}")
print(f"Text features shape: {text_features.shape}")
print(f"Image features shape: {image_features.shape}")
print(f"\nContrastive loss: {loss:.4f}")
print("\n✓ CLIP learns to align image and text in shared embedding space,")
print("  enabling zero-shot image classification via text queries")
```

### 14.2.1 CLIP 的訓練方式

CLIP 使用對比學習目標，同時訓練圖像編碼器和文字編碼器：

```
CLIP 訓練目標：

┌──────────┐         ┌──────────┐
│ Image 1  │         │ "a cat"  │
└────┬─────┘         └────┬─────┘
     ↓                    ↓
┌──────────┐         ┌──────────┐
│  Image   │         │  Text    │
│ Encoder  │         │ Encoder  │
└────┬─────┘         └────┬─────┘
     ↓                    ↓
┌──────────┐         ┌──────────┐
│   I1     │         │   T1     │
└────┬─────┘         └────┬─────┘
     └──────────┬──────────┘
                ↓
        最大化對角線相似度
```

### 14.2.2 對比損失函數

```python
def contrastive_loss(text_features, image_features, temperature=0.07):
    logits = text_features @ image_features.T / temperature
    labels = np.arange(len(text_features))
    
    loss_i = cross_entropy(logits, labels)  # 圖像→文字
    loss_t = cross_entropy(logits.T, labels)  # 文字→圖像
    
    return (loss_i + loss_t) / 2
```

### 14.2.3 CLIP 的應用

| 應用 | 說明 |
|------|------|
| 零樣本分類 | 用文字描述查詢圖像 |
| 影像檢索 | 文字搜尋圖像庫 |
| 風格遷移 | CLIP 引導的圖像生成 |
| 文字生成圖像 | 與生成模型結合 |

### 14.2.4 Zero-Shot 分類範例

```python
# CLIP 零樣本分類
classes = ["cat", "dog", "bird"]
text_prompts = [f"a photo of a {c}" for c in classes]

text_features = clip.encode_text(text_prompts)
image_features = clip.encode_image(image)

similarities = text_features @ image_features.T
predicted_class = classes[similarities.argmax()]
```

## 14.3 語音辨識模型：Whisper

Whisper 是 OpenAI 開發的大規模語音辨識模型，在多語言語音辨識任務上展現了卓越效能。

[程式檔案：14-3-whisper.py](../_code/14/14-3-whisper.py)

```python
import numpy as np

class WhisperEncoder:
    def __init__(self, n_mels=80, d_model=512):
        self.conv1 = np.random.randn(3* n_mels, d_model) * 0.02
        self.conv2 = np.random.randn(3* n_mels, d_model) * 0.02
        
    def forward(self, mel_spec):
        x = mel_spec.reshape(mel_spec.shape[0], -1)
        x = np.maximum(0, x @ self.conv1)
        x = np.maximum(0, x @ self.conv2)
        return x

class WhisperDecoder:
    def __init__(self, vocab_size, d_model, max_len=448):
        self.embedding = np.random.randn(vocab_size, d_model) * 0.02
        self.pos_embed = np.random.randn(max_len, d_model) * 0.02
        self.lm_head = np.random.randn(d_model, vocab_size) * 0.02
        
    def forward(self, token_ids, encoder_output):
        x = self.embedding[token_ids]
        x = x + self.pos_embed[:x.shape[0]]
        x = x + encoder_output
        return x @ self.lm_head

class Whisper:
    def __init__(self, vocab_size=51865, n_mels=80, d_model=512):
        self.encoder = WhisperEncoder(n_mels, d_model)
        self.decoder = WhisperDecoder(vocab_size, d_model)
        self.vocab_size = vocab_size
        
    def forward(self, mel_spec, token_ids):
        encoder_out = self.encoder.forward(mel_spec)
        logits = self.decoder.forward(token_ids, encoder_out)
        return logits

vocab_size = 51865
n_mels = 80
d_model = 512

whisper = Whisper(vocab_size, n_mels, d_model)

batch_size = 2
mel_spec = np.random.randn(batch_size, n_mels, 3000)
token_ids = np.array([50257, 50359, 41420, 2117])

logits = whisper.forward(mel_spec, token_ids)

print("=" * 60)
print("Whisper (Speech Recognition) Demo")
print("=" * 60)
print(f"Vocab size: {vocab_size:,}")
print(f"Mel spectrogram bins: {n_mels}")
print(f"d_model: {d_model}")
print(f"Input mel shape: {mel_spec.shape}")
print(f"Token IDs: {token_ids}")
print(f"Output logits shape: {logits.shape}")
print("\n✓ Whisper is a speech recognition model that processes")
print("  mel spectrograms to generate text transcriptions")
```

### 14.3.1 Whisper 架構特點

Whisper 採用 Encoder-Decoder 架構：

```
Whisper 架構：

音頻輸入
    ↓
Mel Spectrogram (80 mel bins)
    ↓
┌─────────────────────────────────┐
│          Encoder               │
│   • 2層 Conv + GELU            │
│   • 位置編碼                     │
│   • 36層 Transformer Block      │
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│          Decoder               │
│   • 位置嵌入                     │
│   • Cross Attention (←Encoder) │
│   • 12 層 Transformer Block    │
└────────────┬────────────────────┘
             ↓
文字輸出 (Tokenizer)
```

### 14.3.2 語音處理流程

```python
def process_audio(audio):
    # 1. 預強調
    audio = np.append(audio[0], audio[1:] - 0.97 * audio[:-1])
    
    # 2. 短時傅立葉變換
    stft = librosa.stft(audio, n_fft=400, hop_length=160)
    
    # 3. Mel 頻譜圖
    mel_spec = librosa.feature.melspectrogram(S=np.abs(stft)**2, n_mels=80)
    mel_spec = np.log(mel_spec + 1e-9)
    
    return mel_spec
```

### 14.3.3 Whisper 的優勢

| 特性 | 說明 |
|------|------|
| 多語言支援 | 支援 99 種語言 |
| 強健性 | 對噪音和口音有較好適應性 |
| 端到端 | 直接輸出文字，無需獨立解碼 |
| 時間戳記 | 可輸出單詞級時間戳記 |

### 14.3.4 Wav2Vec 2.0

Wav2Vec 2.0 是另一個重要的自監督語音辨識模型：

```python
class Wav2Vec2:
    def __init__(self):
        self.feature_encoder = ConvFeatureEncoder()
        self.transformer = TransformerEncoder()
        self.quantizer = VectorQuantizer()
        
    def contrastive_loss(self, true_ids, pred_ids):
        # 對比學習損失
        return ...
```

## 14.4 文字轉語音 (TTS)

文字轉語音技術將文字轉換為自然語音輸出。

[程式檔案：14-4-tts.py](../_code/14/14-4-tts.py)

```python
import numpy as np

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

class Vocoder:
    def __init__(self, n_mels=80, audio_channels=1):
        self.n_mels = n_mels
        self.audio_channels = audio_channels
        
    def forward(self, mel_spec):
        audio = np.random.randn(mel_spec.shape[0], mel_spec.shape[1] * 256)
        return audio

class FastSpeech:
    def __init__(self, vocab_size, d_model=256):
        self.embedding = np.random.randn(vocab_size, d_model) * 0.02
        self.length_regulator = np.random.randn(d_model, d_model) * 0.02
        self.vocoder = Vocoder()
        
    def forward(self, token_ids, durations=None):
        x = self.embedding[token_ids]
        if durations is not None:
            x = self.expand_by_duration(x, durations)
        mel_spec = x @ self.length_regulator
        audio = self.vocoder.forward(mel_spec)
        return audio
    
    def expand_by_duration(self, x, durations):
        batch_size, seq_len, d_model = x.shape
        max_len = int(durations.sum(axis=1).max())
        output = np.zeros((batch_size, max_len, d_model))
        
        for b in range(batch_size):
            pos = 0
            for i, d in enumerate(durations[b]):
                output[b, pos:pos+int(d)] = x[b, i]
                pos += int(d)
        return output

class VALL_E:
    def __init__(self, vocab_size, d_model=512):
        self.embedding = np.random.randn(vocab_size, d_model) * 0.02
        self.codec_embed = np.random.randn(1024, d_model) * 0.02
        
    def forward(self, text_tokens, acoustic_tokens=None):
        x = self.embedding[text_tokens]
        if acoustic_tokens is not None:
            x = x + self.codec_embed[acoustic_tokens]
        return x

vocab_size = 500

fastspeech = FastSpeech(vocab_size)
token_ids = np.array([[1, 2, 3, 4, 5]])
durations = np.array([[1, 2, 1, 3, 1]])

audio = fastspeech.forward(token_ids, durations)

print("=" * 60)
print("TTS (Text-to-Speech) Demo")
print("=" * 60)
print(f"Vocab size: {vocab_size}")
print(f"Input tokens: {token_ids}")
print(f"Durations: {durations}")
print(f"Output audio shape: {audio.shape}")
print("\n✓ TTS models convert text to speech audio:")
print("  - FastSpeech: Duration-controlled neural TTS")
print("  - VALL-E: Neural codec language model for TTS")
```

### 14.4.1 FastSpeech 架構

FastSpeech 是 Transformer 基礎的 TTS 模型，支援可控的語速和韻律：

```
FastSpeech 架構：

輸入文字
    ↓
詞嵌入 + 位置編碼
    ↓
┌──────────────────────────┐
│   編碼器 (FFT 塊)        │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│  Duration Predictor     │ ← 預測每個音素的持續時間
│  (長度調節器)            │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│   解碼器 (FFT 塊)        │
└────────────┬─────────────┘
             ↓
Mel 頻譜圖
    ↓
Vocoder (神經聲碼器)
    ↓
語音輸出
```

### 14.4.2 VALL-E 語音克隆

VALL-E 是一個神經音頻編解碼語言模型，支援高質量語音克隆：

```python
class VALL_E:
    def __init__(self):
        self.text_encoder = Transformer()
        self.audio_decoder = ARDecoder()
        self.codec = NeuralCodec()
    
    def generate(self, text, reference_audio):
        # 1. 提取參考音頻的聲學特徵
        ref_features = self.codec.encode(reference_audio)
        
        # 2. 編碼文字
        text_features = self.text_encoder(text)
        
        # 3. 自回歸生成音頻 tokens
        audio_tokens = self.audio_decoder(text_features, ref_features)
        
        # 4. 解碼為音頻波形
        return self.codec.decode(audio_tokens)
```

### 14.4.3 主流 TTS 模型比較

| 模型 | 機構 | 特點 |
|------|------|------|
| FastSpeech | Microsoft | 並行生成，可控時長 |
| Tacotron 2 | Google | 端到端合成 |
| VALL-E | Microsoft | 3秒音頻即可克隆 |
| Bark | Suno | 多語言開源 |

## 14.5 實作：影像描述生成

影像描述 (Image Captioning) 任務結合了視覺理解和語言生成能力。

[程式檔案：14-5-image-captioning.py](../_code/14/14-5-image-captioning.py)

```python
import numpy as np

class ImageEncoder:
    def __init__(self, img_size, d_model):
        self.proj = np.random.randn(img_size * img_size * 3, d_model) * 0.02
        
    def forward(self, images):
        x = images.reshape(images.shape[0], -1)
        return x @ self.proj

class CaptionDecoder:
    def __init__(self, vocab_size, d_model):
        self.embedding = np.random.randn(vocab_size, d_model) * 0.02
        self.lm_head = np.random.randn(d_model, vocab_size) * 0.02
        
    def forward(self, image_features, token_ids):
        x = self.embedding[token_ids]
        x = x + image_features
        return x @ self.lm_head

class ImageCaptioningModel:
    def __init__(self, vocab_size, img_size, d_model):
        self.encoder = ImageEncoder(img_size, d_model)
        self.decoder = CaptionDecoder(vocab_size, d_model)
        
    def forward(self, images, token_ids):
        image_features = self.encoder.forward(images)
        logits = self.decoder.forward(image_features, token_ids)
        return logits

vocab_size = 50000
img_size = 224
d_model = 512

model = ImageCaptioningModel(vocab_size, img_size, d_model)

batch_size = 2
images = np.random.randn(batch_size, 3, img_size, img_size)
token_ids = np.array([[101, 202, 303, 404, 105]])

logits = model.forward(images, token_ids)

print("=" * 60)
print("Image Captioning Demo")
print("=" * 60)
print(f"Vocab size: {vocab_size:,}")
print(f"Image size: {img_size}x{img_size}")
print(f"d_model: {d_model}")
print(f"Input image shape: {images.shape}")
print(f"Input token IDs shape: {token_ids.shape}")
print(f"Output logits shape: {logits.shape}")
print("\n✓ Image captioning models (like BLIP, CLIP):")
print("  - Encode images to feature representations")
print("  - Generate descriptive text captions")
print("  - Enable multimodal understanding")
```

### 14.5.1 影像描述模型架構

```
影像描述模型架構：

┌─────────────┐
│   影像      │
└──────┬──────┘
       ↓
┌─────────────┐     ┌─────────────┐
│   視覺編碼器  │ ──→ │  圖像特徵    │
│  (CNN/ViT)  │     └──────┬──────┘
└─────────────┘            ↓
                    ┌─────────────┐
                    │  Cross      │
                    │  Attention  │
                    └──────┬──────┘
                           ↓
                    ┌─────────────┐
                    │   語言解碼器  │
                    │ (Transformer)│
                    └──────┬──────┘
                           ↓
                    ┌─────────────┐
                    │  描述文字    │
                    └─────────────┘
```

### 14.5.2 訓練與推理

```python
class ImageCaptioningModel(nn.Module):
    def __init__(self, encoder, decoder):
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
    
    def forward(self, images, captions):
        features = self.encoder(images)
        logits = self.decoder(features, captions[:-1])
        return logits
    
    def generate(self, image, tokenizer, max_len=50):
        features = self.encoder(image)
        tokens = [tokenizer.bos_token_id]
        
        for _ in range(max_len):
            logits = self.decoder(features, torch.tensor([tokens]))
            next_token = logits.argmax(-1, keepdim=True)
            tokens.append(next_token.item())
            if next_token == tokenizer.eos_token_id:
                break
        
        return tokenizer.decode(tokens)
```

### 14.5.3 預訓練模型

| 模型 | 說明 |
|------|------|
| BLIP | 統一視覺語言預訓練 |
| BLIP-2 | 結合 CLIP 和語言模型 |
| LLaVA | GPT-4V 風格的開源方案 |
| MiniGPT-4 | 輕量級多模態模型 |

## 14.6 總結

本章介紹了視覺和聽覺領域的重要模型：

| 模型類型 | 代表模型 | 核心技術 |
|----------|----------|----------|
| 影像分類 | ViT, DeiT | Patch + Transformer |
| 圖文理解 | CLIP | 對比學習 |
| 語音辨識 | Whisper | Encoder-Decoder |
| 語音合成 | FastSpeech, VALL-E | 自回歸 + Codec |
| 影像描述 | BLIP | 多模態 Transformer |

這些模型的共同特點是採用 Transformer 架構，並在大規模數據上進行預訓練。從視覺到聽覺，深度學習正在重塑我們與機器交互的方式。
