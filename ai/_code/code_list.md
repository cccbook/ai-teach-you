# 程式碼範例清單

本書籍所有程式碼範例按照章節分類，每章有對應的程式碼目錄。

---

## 第一部分：簡介

### 第 1 章：AI 的歷史
- `01-1-eliza.py` - ELIZA 聊天機器人 (1966)
- `01-2-simple-rules.py` - 簡單的規則式系統
- `01-3-prolog-family.py` - Prolog 家族關係推論 (1972)
- `01-4-lisp-symbolic.py` - Lisp 符號處理：代數簡化
- `01-5-expert-system.py` - 簡化版 MYCIN 專家系統 (1976)

### 第 2 章：傳統 AI 技術
- `02-1-hill-climbing.py` - 爬山演算法：f(x) = (x-1)² 找最低點
- `02-2-hill-climbing-tsp.py` - 爬山演算法解決 TSP 旅行推銷員問題
- `02-3-grid-search.py` - 網格搜尋演算法
- `02-4-dfs.py` - 深度優先搜尋 (DFS)
- `02-5-bfs.py` - 廣度優先搜尋 (BFS)
- `02-6-astar.py` - A* 搜尋演算法
- `02-7-decision-tree.py` - 決策樹實作
- `02-8-naive-bayes.py` - 貝葉斯分類器
- `02-9-svm.py` - 支持向量機 (SVM)

### 第 3 章：現代 AI 技術
*（本章無獨立程式碼範例，相關範例分散在第 5-6 章）*

---

## 第二部分：神經網路

### 第 4 章：機器學習與 Scikit-Learn
- `04-1-linear-regression.py` - 線性迴歸
- `04-2-logistic-regression.py` - 邏輯迴歸
- `04-3-decision-tree.py` - 決策樹
- `04-4-random-forest.py` - 隨機森林
- `04-5-svm.py` - 支持向量機
- `04-6-knn.py` - K-Nearest Neighbors
- `04-7-kmeans.py` - K-Means 聚類

### 第 5 章：神經網路與 PyTorch
- `05-1-tensor-basics.py` - PyTorch 張量基礎操作
- `05-2-autograd.py` - 自動微分機制
- `05-3-nn-module.py` - nn.Module 建構神經網路
- `05-4-dataloader.py` - 資料集與 DataLoader
- `05-5-training-loop.py` - 完整訓練迴圈

### 第 6 章：梯度下降法與反傳遞
- `06-1-gradient-descent.py` - 梯度下降法視覺化
- `06-2-sgd-momentum.py` - SGD 與動量
- `06-3-optimizer.py` - Adam、RMSprop 優化器
- `06-4-backprop.py` - 反傳遞演算法
- `06-5-numerical-gradient.py` - 數值梯度範例：(x-1)² + (y-2)² + (z-3)²
- `06-6-micrograd.py` - 手刻神經網路（參考 micrograd 架構）

### 第 7 章：感知器到多層感知器
- `07-1-perceptron.py` - 單層感知器
- `07-2-mlp.py` - 多層感知器 (MLP)
- `07-3-activation.py` - 各種激活函數比較
- `07-4-regularization.py` - Dropout、L1/L2 正則化
- `07-5-batchnorm.py` - Batch Normalization
- `07-6-mnist-mlp.py` - 實作：MNIST 手寫數字分類

### 第 8 章：卷積神經網路 (CNN)
- `08-1-convolution.py` - 卷積層運算
- `08-2-pooling.py` - 池化層運算
- `08-3-lenet.py` - LeNet-5 架構
- `08-4-alexnet.py` - AlexNet 架構
- `08-5-resnet.py` - ResNet 架構
- `08-6-transfer-learning.py` - 遷移學習與微調
- `08-7-cifar10-cnn.py` - 實作：CIFAR-10 影像分類

### 第 9 章：循環神經網路 (RNN)
- `09-1-rnn-basic.py` - RNN 基本運算
- `09-2-lstm.py` - LSTM 結構
- `09-3-gru.py` - GRU 結構
- `09-4-seq2seq.py` - Seq2Seq 模型
- `09-5-text-generation.py` - 實作：文字生成
- `09-6-sentiment.py` - 實作：情感分類

### 第 10 章：生成對抗網路 (GAN)
- `10-1-gan-basic.py` - GAN 基本概念
- `10-2-dcgan.py` - DCGAN 架構
- `10-3-wgan.py` - WGAN 改進
- `10-4-cgan.py` - 條件 GAN
- `10-5-stylegan.py` - StyleGAN 簡介
- `10-6-gan-mnist.py` - 實作：生成 MNIST 數字

---

## 第三部分：現代語言模型與 Transformer

### 第 11 章：現代語言模型
- `11-1-ngram.py` - N-gram 語言模型
- `11-2-word2vec.py` - Word2Vec 訓練
- `11-3-glove.py` - GloVe 使用
- `11-4-bert.py` - BERT 使用與微調
- `11-5-gpt-api.py` - GPT API 呼叫範例

### 第 12 章：注意力機制、Transformer 與 GPT
- `12-1-attention.py` - 注意力機制原理
- `12-2-self-attention.py` - 自注意力機制
- `12-3-multihead-attention.py` - Multi-Head Attention
- `12-4-transformer.py` - Transformer 完整架構
- `12-5-positional-encoding.py` - 位置編碼
- `12-6-gpt.py` - GPT 模型實作
- `12-7-mini-transformer.py` - 實作：從零建構小型 Transformer

### 第 13 章：最新語言模型
- `13-1-rlhf.py` - RLHF 訓練流程
- `13-2-prompt-engineering.py` - 提示工程技巧
- `13-3-lora.py` - LoRA 微調技術
- `13-4-qlora.py` - QLoRA 微調技術

---

## 第四部分：Transformer 之後與世界模型

### 第 14 章：視覺與聽覺模型
- `14-1-vit.py` - Vision Transformer (ViT)
- `14-2-clip.py` - CLIP 模型使用
- `14-3-whisper.py` - Whisper 語音辨識
- `14-4-tts.py` - 文字轉語音 (TTS)
- `14-5-image-captioning.py` - 實作：影像描述生成

### 第 15 章：生成式 AI
- `15-1-vae.py` - VAE 變分自編碼器
- `15-2-autoregressive.py` - 自回歸生成
- `15-3-diffusion.py` - Diffusion 前向與逆向過程
- `15-4-stable-diffusion.py` - Stable Diffusion 使用
- `15-5-ddim.py` - DDIM 採樣
- `15-6-sdxl.py` - SDXL 文字生成圖片
- `15-7-sora.py` - 影片生成模型簡介
- `15-8-mini-diffusion.py` - 實作：建構簡單的 Diffusion 模型

### 第 16 章：多模態模型
- `16-1-gpt4v.py` - GPT-4V 視覺理解
- `16-2-flamingo.py` - Flamingo 模型
- `16-3-blip.py` - BLIP 圖文對話
- `16-4-multimodal-chat.py` - 實作：圖文對話系統

### 第 17 章：代理人技術 (Agent)
- `17-1-agent-basic.py` - AI Agent 基本架構
- `17-2-react.py` - ReAct 推理與行動框架
- `17-3-tool-use.py` - Tool Use 實作
- `17-4-memory.py` - Memory 長期記憶
- `17-5-opencode.py` - OpenCode/Claude Code 原理
- `17-6-mini-openclaw.py` - 實作：建構 AI 助手（參考 mini-openclaw）

### 第 18 章：強化學習
- `18-1-grid-world.py` - 強化學習基本概念
- `18-2-mdp.py` - Markov Decision Process
- `18-3-value-function.py` - 價值函數與 Q 函數
- `18-4-q-learning.py` - Q-Learning 走迷宮
- `18-5-dqn.py` - DQN 玩 CartPole
- `18-6-policy-gradient.py` - Policy Gradient
- `18-7-actor-critic.py` - Actor-Critic
- `18-8-tictactoe.py` - 實作：AlphaGo 井字棋（MCTS + 類神經網路）

### 第 19 章：世界模型
- `19-1-world-model.py` - 世界模型概念
- `19-2-mcts.py` - Monte Carlo Tree Search
- `19-3-alphago.py` - AlphaGo 原理
- `19-4-foundation-world.py` - Foundation Model as World Model
- `19-5-simulation.py` - 模擬環境範例
- `19-6-agi-future.py` - AGI 展望

---

## 附錄

### 附錄 A：PyTorch 深度學習框架
- `A-1-pytorch-vs-tensorflow.py` - PyTorch 與 TensorFlow 比較
- `A-2-tensor-gpu.py` - 張量運算與 GPU 加速
- `A-3-model-building.py` - nn.Module 模型建構
- `A-4-debugging.py` - 訓練技巧與除錯

### 附錄 B：數學基礎
- `B-1-linear-algebra.py` - 矩陣、向量運算
- `B-2-probability.py` - 機率論基礎
- `B-3-calculus.py` - 微積分與梯度
- `B-4-optimization.py` - 最優化理論

---

## 程式碼目錄結構

```
ai/_code/
├── 02/                 # 第 2 章
├── 04/                 # 第 4 章
├── 05/                 # 第 5 章
├── 06/                 # 第 6 章
├── 07/                 # 第 7 章
├── 08/                 # 第 8 章
├── 09/                 # 第 9 章
├── 10/                 # 第 10 章
├── 11/                 # 第 11 章
├── 12/                 # 第 12 章
├── 13/                 # 第 13 章
├── 14/                 # 第 14 章
├── 15/                 # 第 15 章
├── 16/                 # 第 16 章
├── 17/                 # 第 17 章
├── 18/                 # 第 18 章
├── 19/                 # 第 19 章
└── A/                  # 附錄 A
```
