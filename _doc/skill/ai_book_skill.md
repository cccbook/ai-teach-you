# AI 書籍寫作 Skill

> **注意**：本文件使用繁體中文撰寫。

## 概述

本 Skill 提供撰寫人工智慧（AI）相關書籍的完整工作流程，涵蓋基礎 AI 理論、深度學習、語言模型等主題的程式碼範例規劃、測試與驗證。

## 核心原則

1. **理論與實踐結合**：AI 概念需配有可執行的程式碼範例
2. **循序渐进**：從基礎概念到進階主題逐步推進
3. **經典範例**：每章包含1-2個經典實作範例
4. **測試驗證**：所有程式碼必須經過執行測試
5. **專有名詞索引**：建立統一的術語說明

## AI 書籍專有特色

### 1. 經典 AI 歷史範例

| 範例 | 年份 | 主題 |
|------|------|------|
| ELIZA | 1966 | 聊天機器人、規則式系統 |
| MYCIN | 1976 | 專家系統專家系統 |
| Prolog | 1972 | 邏輯式 AI |
| Lisp | 1958 | 函數式 AI、符號處理 |

### 2. 深度學習核心範例

- 微分與梯度下降：f(x) = (x-1)² + (y-2)² + (z-3)²
- 反傳遞演算法：micrograd 實作
- 經典模型：LeNet, AlexNet, ResNet, Transformer
- 預訓練模型：GPT, BERT, CLIP, Stable Diffusion

### 3. 語言模型範例

- micrograd/microgpt：從零建構 GPT
- LoRA/QLoRA：微調技術
- Prompt Engineering：提示工程

### 4. 強化學習範例

- Q-Learning 走迷宮
- DQN 玩 CartPole
- AlphaGo 井字棋（MCTS + 類神經網路）

## 工作流程

### 第一階段：規劃（建立 code_list.md）

在開始撰寫書籍之前，先建立完整的程式碼清單：

```markdown
# 程式碼範例清單

## 第 1 章：AI 的歷史
- `01-1-eliza.py` - ELIZA 聊天機器人
- `01-2-simple-rules.py` - 規則式系統
- ...

## 第 2 章：傳統 AI 技術
- `02-1-hill-climbing.py` - 爬山演算法
- ...
```

**建立清單的好處**：
- 先規劃所有程式碼，確保每章都有實作範例
- 確認程式碼涵蓋足夠的主題
- 方便後續追蹤進度
- 可作為書籍的附錄參考

### 第二階段：程式碼開發

#### 1. 經典 AI 範例

```python
# ELIZA 聊天機器人範例結構
class Eliza:
    def __init__(self):
        self.rules = [...]
    
    def respond(self, user_input):
        # Pattern matching
        # 回應生成
        pass
```

#### 2. 數學運算範例

```python
# 梯度下降範例
def gradient_descent(func, start, learning_rate=0.1):
    x = start
    for _ in range(1000):
        grad = numerical_gradient(func, x)
        x -= learning_rate * grad
    return x
```

#### 3. PyTorch 範例

```python
import torch
import torch.nn as nn

class SimpleNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 256)
        self.fc2 = nn.Linear(256, 10)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        return self.fc2(x)
```

### 第三階段：測試

```bash
# 測試每個檔案
python3 01-1-eliza.py
python3 02-1-hill-climbing.py
python3 05-1-tensor-basics.py
```

### 第四階段：書籍撰寫

在每個程式碼區塊前加入連結：

```markdown
[程式檔案：01-1-eliza.py](../_code/01/01-1-eliza.py)
```python
# 程式碼
```
```

## AI 書籍章節範例規劃

### 第 1 章：AI 的歷史
- ELIZA 聊天機器人
- Prolog 家族關係推論
- Lisp 符號處理
- MYCIN 專家系統

### 第 2 章：傳統 AI 技術
- 爬山演算法：f(x) = (x-1)²
- TSP 旅行推銷員問題
- DFS/BFS/A* 搜尋

### 第 6 章：梯度下降與反傳遞
- 數值梯度：(x-1)² + (y-2)² + (z-3)²
- micrograd 實作

### 第 12 章：Transformer
- 從零建構小型 Transformer
- GPT 模型實作

### 第 18 章：強化學習
- Q-Learning 走迷宮
- DQN
- AlphaGo 井字棋

## 驗收標準

1. ✅ 所有章節都有程式碼範例（至少 1-2 個/章）
2. ✅ 每個程式碼檔案可執行並有輸出
3. ✅ 程式碼包含詳細註解
4. ✅ 書籍章節與程式碼有對應連結
5. ✅ 專有名詞索引完整

## 擴展應用

本 Skill 可用於：
- 深度學習書籍
- 機器學習書籍
- 自然語言處理書籍
- 電腦視覺書籍
- 強化學習書籍

只需根據具體主題調整：
- 程式碼範例類型
- 框架選擇（PyTorch/TensorFlow）
- 資料集選擇
