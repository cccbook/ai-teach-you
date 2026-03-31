# 第 13 章：最新語言模型的進展

本章將介紹自 Transformer 問世以來語言模型的重要進展，包括大語言模型 (LLM) 的縮放定律、人類回饋強化學習 (RLHF)、各種開源模型的崛起，以及重要的微調技術如 LoRA 和 QLoRA。這些技術共同推動了生成式 AI 的快速發展。

## 13.1 LLM 縮放定律與 GPT-4

大語言模型的發展遵循著獨特的縮放定律 (Scaling Laws)。研究發現，模型效能與模型參數量、訓練資料量、計算量之間存在可預測的關係。

### 13.1.1 縮放定律的基本原理

神經網路的縮放定律表明，當我們適當增加模型規模、資料量和計算資源時，模型效能會穩步提升：

| 因素 | 影響 |
|------|------|
| 模型參數 | 更大的模型有更強的表達能力 |
| 訓練資料 | 更多的資料提供更豐富的知識 |
| 計算量 | 更多的訓練計算提升泛化能力 |

### 13.1.2 GPT-4 的突破

GPT-4 是 OpenAI 發布的最新大型語言模型，雖然具體架構細節未公開，但已知它帶來了以下突破：

- **多模態能力**：支援文字和圖像輸入
- **推理能力提升**：在各種基準測試中展現更強的推理能力
- **更長的上下文**：支援更長的上下文窗口
- **安全性提升**：透過 RLHF 減少有害輸出

## 13.2 RLHF 與人類回饋學習

人類回饋強化學習 (Reinforcement Learning from Human Feedback, RLHF) 是讓語言模型與人類偏好對齊的關鍵技術。

[程式檔案：13-1-rlhf.py](../_code/13/13-1-rlhf.py)

```python
import numpy as np

class SimpleRLHF:
    def __init__(self):
        self.rewards = []
        self.responses = []
        
    def step(self, response, reward):
        self.responses.append(response)
        self.rewards.append(reward)
        
    def get_preferred_response(self):
        if not self.rewards:
            return None
        best_idx = np.argmax(self.rewards)
        return self.responses[best_idx]

class PPOTrainer:
    def __init__(self, policy_lr=0.001):
        self.policy = np.random.randn(10) * 0.1
        self.value = np.random.randn(1) * 0.1
        self.policy_lr = policy_lr
        
    def compute_loss(self, log_probs, old_log_probs, rewards, values, old_values):
        advantage = rewards - old_values
        policy_loss = -np.mean(log_probs - old_log_probs) * advantage
        value_loss = np.mean((rewards - values) ** 2)
        return policy_loss + 0.5 * value_loss
    
    def update(self, responses, rewards):
        log_probs = np.sum(responses * self.policy)
        old_log_probs = log_probs
        values = np.sum(responses * self.value)
        old_values = values
        
        loss = self.compute_loss(log_probs, old_log_probs, rewards, values, old_values)
        self.policy += self.policy_lr * loss * np.sign(np.random.randn(10))
        
        return loss

rlhf = SimpleRLHF()
rlhf.step("Hello! How can I help?", 0.8)
rlhf.step("Hi there!", 0.5)
rlhf.step("Greetings, human.", 0.9)

ppot = PPOTrainer()
loss = ppot.update(np.random.randn(10), 0.7)

print("=" * 60)
print("RLHF (Reinforcement Learning from Human Feedback) Demo")
print("=" * 60)
print("\nResponses collected:")
for i, (r, rew) in enumerate(zip(rlhf.responses, rlhf.rewards)):
    print(f"  {i+1}. '{r}' -> reward: {rew}")
    
best = rlhf.get_preferred_response()
print(f"\nPreferred response: '{best}'")
print(f"\nPPO update loss: {loss:.4f}")
print("\n✓ RLHF uses human feedback to train a reward model,")
print("  then optimizes policy via PPO to maximize rewards")
```

### 13.2.1 RLHF 的三個階段

```
RLHF 流程：

階段 1：監督式微調 (SFT)
┌─────────────┐     ┌─────────────┐
│  精選人類回饋  │ ──→ │   SFT 模型   │
└─────────────┘     └─────────────┘

階段 2：獎勵模型訓練
┌─────────────┐     ┌─────────────┐
│  回應對比    │ ──→ │  獎勵模型    │
└─────────────┘     └─────────────┘

階段 3：強化學習優化
┌─────────────┐     ┌─────────────┐
│   SFT 模型   │ ──→ │  PPO 優化    │ ←── 獎勵信號
└─────────────┘     └─────────────┘
```

1. **監督式微調 (SFT)**：使用人類撰寫的優質回應微調模型
2. **獎勵模型訓練**：訓練一個模型來預測人類偏好
3. **PPO 強化學習**：使用獎勵模型提供的信號優化策略

### 13.2.2 PPO 演算法核心

近端策略優化 (Proximal Policy Optimization, PPO) 是 RLHF 的核心優化演算法：

```python
# PPO 損失函數的核心概念
def compute_ppo_loss(log_probs, old_log_probs, advantages):
    ratio = np.exp(log_probs - old_log_probs)
    clipped_ratio = np.clip(ratio, 1 - epsilon, 1 + epsilon)
    return -np.min(ratio * advantages, clipped_ratio * advantages)
```

### 13.2.3 RLHF 的影響

| 應用 | 說明 |
|------|------|
| ChatGPT | 對話更加自然、安全 |
| Claude | 強調無害性和幫助性 |
| InstructGPT | 更好地遵循指令 |

## 13.3 InstructGPT 與 ChatGPT 原理

InstructGPT 是 OpenAI 將 RLHF 技術應用於語言模型的開創性工作，也是 ChatGPT 的技術基礎。

### 13.3.1 InstructGPT 的核心思想

InstructGPT 的目標是讓語言模型生成的回應符合人類意圖。主要步驟包括：

1. 收集人類偏好的對比數據
2. 訓練獎勵模型預測人類偏好
3. 使用 PPO 優化語言模型

### 13.3.2 ChatGPT 的架構

ChatGPT 是 InstructGPT 技術在對話場景的應用：

```
ChatGPT 架構：

使用者輸入 → 上下文處理 → 語言模型 + RLHF → 安全過濾 → 回應輸出
                         ↑
                    人類回饋訓練
```

## 13.4 開源模型的崛起：LLaMA、Mistral、Claude

開源大型語言模型的發展極大地推動了 AI 民主化。

### 13.4.1 LLaMA 系列

Meta 的 LLaMA (Large Language Model Meta AI) 系列是重要的開源模型：

| 版本 | 參數量 | 特色 |
|------|--------|------|
| LLaMA 1 | 7B-65B | 首次開源大型模型 |
| LLaMA 2 | 7B-70B | 開源可商用許可 |
| LLaMA 3 | 8B-70B | 更強效能，支援長上下文 |

### 13.4.2 Mistral 模型

Mistral AI 發布的 Mistral 模型以其高效能和開源許可受到廣泛關注：

- **Mistral 7B**：在多項基準測試中超越 LLaMA 2 13B
- **Mixtral 8x7B**：專家混合模型 (MoE)，每token僅啟用2個專家

### 13.4.3 Claude 與 Anthropic 模型

Anthropic 的 Claude 系列強調安全性和有用性：

- Constitutional AI：透過內在原則引導模型行為
- RLHF + AI Feedback：結合人類和 AI 回饋

## 13.5 提示工程 (Prompt Engineering)

提示工程是最大化 LLM 效能的關鍵技術。

[程式檔案：13-2-prompt-engineering.py](../_code/13/13-2-prompt-engineering.py)

```python
import numpy as np

class PromptEngineer:
    def __init__(self):
        self.templates = {
            "zero_shot": "Task: {task}\nInput: {input}\nOutput:",
            "few_shot": "Task: {task}\nExamples:\n{examples}\nInput: {input}\nOutput:",
            "cot": "Task: {task}\nInput: {input}\nLet's think step by step.\nOutput:",
            "style": "Task: {task}\nStyle: {style}\nInput: {input}\nOutput:",
        }
        
    def format_prompt(self, template, **kwargs):
        return self.templates[template].format(**kwargs)
    
    def zero_shot(self, task, input_text):
        return self.format_prompt("zero_shot", task=task, input=input_text)
    
    def few_shot(self, task, examples, input_text):
        ex_str = "\n".join([f"Input: {e['input']} -> Output: {e['output']}" for e in examples])
        return self.format_prompt("few_shot", task=task, examples=ex_str, input=input_text)
    
    def chain_of_thought(self, task, input_text):
        return self.format_prompt("cot", task=task, input=input_text)

pe = PromptEngineer()

zero_shot_prompt = pe.zero_shot("Sentiment analysis", "I love this product!")
few_shot_prompt = pe.few_shot(
    "Translation",
    [{"input": "hello", "output": "hola"}, {"input": "goodbye", "output": "adios"}],
    "thank you"
)
cot_prompt = pe.chain_of_thought("Math problem", "What is 23 * 17?")

print("=" * 60)
print("Prompt Engineering Demo")
print("=" * 60)

print("\n[Zero-Shot Prompting]")
print(zero_shot_prompt)

print("\n[Few-Shot Prompting]")
print(few_shot_prompt)

print("\n[Chain-of-Thought Prompting]")
print(cot_prompt)

print("\n✓ Prompt engineering techniques:")
print("  - Zero-shot: Direct task description")
print("  - Few-shot: Include examples")
print("  - Chain-of-thought: Encourage reasoning")
print("  - Style control: Specify output format/tone")
```

### 13.5.1 Zero-Shot Prompting

零樣本提示是最簡單的方式，直接描述任務：

```
任務：情感分析
輸入：我愛這個產品！
輸出：
```

### 13.5.2 Few-Shot Prompting

少樣本提示提供幾個範例：

```
任務：翻譯
範例：
輸入：hello → 輸出：hola
輸入：goodbye → 輸出：adios
輸入：thank you → 輸出：
```

### 13.5.3 Chain-of-Thought Prompting

鏈式思考提示鼓勵模型逐步推理：

```
任務：數學問題
輸入：23 × 17 = ?
讓我們一步一步思考：
```

## 13.6 微調技術：LoRA、QLoRA、Adapter

随着模型規模增大，全參數微調的成本越來越高。低秩適配 (LoRA) 等技術提供了高效的微調方案。

[程式檔案：13-3-lora.py](../_code/13/13-3-lora.py)

```python
import numpy as np

class LoRALayer:
    def __init__(self, d_model, d_ff, rank=4):
        self.d_model = d_model
        self.d_ff = d_ff
        self.rank = rank
        
        self.W = np.random.randn(d_model, d_ff) * 0.1
        self.A = np.random.randn(rank, d_model) * 0.1
        self.B = np.random.randn(d_ff, rank) * 0.1
        
    def forward(self, x):
        base_out = x @ self.W
        lora_out = x @ self.A.T @ self.B.T
        return base_out + lora_out
    
    def get_trainable_params(self):
        return self.A.size + self.B.size
    
    def get_original_params(self):
        return self.W.size

class LoRA:
    def __init__(self, d_model, d_ff, num_layers, rank=4):
        self.layers = [LoRALayer(d_model, d_ff, rank) for _ in range(num_layers)]
        
    def forward(self, x):
        for layer in self.layers:
            x = layer.forward(x)
        return x
    
    def summary_params(self):
        total_trainable = sum(l.get_trainable_params() for l in self.layers)
        total_original = sum(l.get_original_params() for l in self.layers)
        reduction = (1 - total_trainable / total_original) * 100
        return total_trainable, total_original, reduction

d_model = 512
d_ff = 2048
num_layers = 12
rank = 8

lora = LoRA(d_model, d_ff, num_layers, rank)
x = np.random.randn(2, d_model)

output = lora.forward(x)
trainable, original, reduction = lora.summary_params()

print("=" * 60)
print("LoRA (Low-Rank Adaptation) Demo")
print("=" * 60)
print(f"d_model: {d_model}, d_ff: {d_ff}, num_layers: {num_layers}, rank: {rank}")
print(f"Input shape: {x.shape}")
print(f"Output shape: {output.shape}")
print(f"\nTrainable parameters: {trainable:,}")
print(f"Original parameters: {original:,}")
print(f"Parameter reduction: {reduction:.1f}%")
print("\n✓ LoRA adds low-rank matrices to attention/FFN weights")
print("  allowing efficient fine-tuning with minimal parameter changes")
```

### 13.6.1 LoRA 原理

LoRA 的核心思想是假設權重更新矩陣是低秩的：

```
原始權重：W ∈ R^(d×k)
LoRA 更新：ΔW = B × A，其中 A ∈ R^(r×k), B ∈ R^(d×r), r << min(d,k)

新權重：W' = W + ΔW = W + B × A
```

| 優勢 | 說明 |
|------|------|
| 參數效率 | 僅訓練 r×(d+k) 個參數 |
| 記憶體節省 | 無需儲存梯度和中間狀態 |
| 可組合 | 多個 LoRA 適配器可快速切換 |

### 13.6.2 QLoRA：量化 + LoRA

[程式檔案：13-4-qlora.py](../_code/13/13-4-qlora.py)

```python
import numpy as np

def quantize(w, bits=4):
    n = 2 ** bits
    w_min, w_max = w.min(), w.max()
    scale = (w_max - w_min) / n
    quantized = np.round((w - w_min) / scale).astype(int)
    quantized = np.clip(quantized, 0, n - 1)
    return quantized, scale, w_min

def dequantize(quantized, scale, w_min, bits=4):
    n = 2 ** bits
    return (quantized * scale + w_min).astype(np.float32)

class QLoRA:
    def __init__(self, d_model, d_ff, num_layers, rank=4, quant_bits=4):
        self.quant_bits = quant_bits
        self.layers = []
        
        for _ in range(num_layers):
            W = np.random.randn(d_model, d_ff) * 0.1
            q, scale, zero = quantize(W, quant_bits)
            
            A = np.random.randn(rank, d_model) * 0.1
            B = np.random.randn(d_ff, rank) * 0.1
            
            self.layers.append({
                'W_quantized': q,
                'W_scale': scale,
                'W_zero': zero,
                'A': A,
                'B': B
            })
    
    def forward(self, x):
        for layer in self.layers:
            W = dequantize(layer['W_quantized'], layer['W_scale'], layer['W_zero'], self.quant_bits)
            base_out = x @ W
            lora_out = x @ layer['A'].T @ layer['B'].T
            x = base_out + lora_out
        return x
    
    def summary_params(self):
        d_model, d_ff = 512, 2048
        num_layers = len(self.layers)
        
        original = d_model * d_ff * num_layers
        quant_params = original * self.quant_bits // 8
        lora_params = rank * d_model * 2 * num_layers
        rank = self.layers[0]['A'].shape[0]
        
        return quant_params, lora_params, original

d_model = 512
d_ff = 2048
num_layers = 12
rank = 8
quant_bits = 4

qlora = QLoRA(d_model, d_ff, num_layers, rank, quant_bits)
x = np.random.randn(2, d_model)

output = qlora.forward(x)
quant_params, lora_params, original = qlora.summary_params()

print("=" * 60)
print("QLoRA (Quantized LoRA) Demo")
print("=" * 60)
print(f"d_model: {d_model}, d_ff: {d_ff}, num_layers: {num_layers}")
print(f"Rank: {rank}, Quantization bits: {quant_bits}")
print(f"Input shape: {x.shape}")
print(f"Output shape: {output.shape}")
print(f"\nQuantized base weights: {quant_params:,} bytes")
print(f"LoRA adapters: {lora_params:,} params")
print(f"Original weights: {original:,} params")
print("\n✓ QLoRA combines quantization with LoRA for")
print("  even more memory-efficient fine-tuning")
```

### 13.6.3 QLoRA 的技術要點

QLoRA 結合了量化技術和 LoRA：

1. **4-bit NormalFloat 量化**：優化量化參數
2. **雙重量化**：對量化常數也進行量化
3. **分頁優化器**：處理記憶體峰值

```
QLoRA 記憶體節省：

全參數微調：需要 80GB GPU
QLoRA：僅需 24GB GPU

節省比例：~70%
```

### 13.6.4 Adapter 技術

Adapter 是另一種輕量級微調方法：

| Adapter 類型 | 說明 |
|--------------|------|
| Adapter-B | Bottleneck adapter， bottle_dim = 64 |
| Adapter-H | Parallel adapter 配置 |
| Adapter-LN | LayerNorm 後添加 adapter |

## 13.7 實作：LoRA 訓練流程

讓我們實現一個完整的 LoRA 訓練流程：

```python
class LoRATrainer:
    def __init__(self, model, rank=8, alpha=16):
        self.model = model
        self.rank = rank
        self.alpha = alpha
        self.lora_layers = {}
        
    def apply_lora(self, layer_names):
        for name in layer_names:
            original_weight = self.model.get_weight(name)
            d_out, d_in = original_weight.shape
            
            lora_A = np.random.randn(self.rank, d_in) * 0.01
            lora_B = np.zeros((d_out, self.rank))
            
            self.lora_layers[name] = {
                'A': lora_A,
                'B': lora_B,
                'original': original_weight
            }
    
    def forward(self, x):
        for name, layer in self.lora_layers.items():
            base_out = x @ layer['original']
            lora_out = x @ layer['A'].T @ layer['B'].T
            x = base_out + (self.alpha / self.rank) * lora_out
        return x
```

## 13.8 總結

本章介紹了大語言模型領域的重要進展：

| 技術 | 核心貢獻 |
|------|----------|
| RLHF | 讓模型與人類偏好對齊 |
| Prompt Engineering | 最大化模型潛力 |
| LoRA | 高效的模型微調 |
| QLoRA | 量化 + LoRA 的結合 |

這些技術共同推動了大型語言模型的快速發展，使得更強大、更安全、更易用的 AI 系統成為可能。從 GPT-4 到開源模型 LLaMA、Mistral，語言模型正在經歷前所未有的革命。
