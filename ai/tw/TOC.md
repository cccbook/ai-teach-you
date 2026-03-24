# 讓 AI 教你人工智慧 -- 以 PyTorch 實作

## 詳細目錄

### 第一部分：簡介

#### 第 1 章：AI 的歷史
- 1.1 人工智慧的起源 (1956年達特茅斯會議)
- 1.2 第一次 AI 熱潮：符號主義與專家系統
- 1.3 AI 寒冬與復甦
- 1.4 深度學習的興起 (2012年 AlexNet)
- 1.5 大語言模型時代 (2017年 Transformer, 2022年 ChatGPT)

#### 第 2 章：傳統 AI 技術 (1950-2010) 簡介
- 2.1 爬山演算法：f(x) = (x-1)² 找最低點
- 2.2 爬山演算法解決 TSP 旅行推銷員問題
- 2.3 搜尋演算法：A*, DFS, BFS
- 2.4 邏輯與推論：命題邏輯、一階邏輯
- 2.5 專家系統 MYCIN
- 2.6 知識表示與本體論
- 2.7 早期機器學習：決策樹、貝葉斯分類器、SVM

#### 第 3 章：現代 AI 技術 (2010-現在) 簡介
- 3.1 現代 AI 技術源自神經網路
- 3.2 梯度下降算法
- 3.3 反傳遞算法
- 3.4 Hinton 等人 1986 在語音辨識上的成功
- 3.5 卷積神經網路 (CNN) 的突破
- 3.6 深度學習框架：Theano, TensorFlow, PyTorch
- 3.7 自然語言處理的演進：Word2Vec, LSTM, Transformer
- 3.8 生成式 AI：GAN, Diffusion, GPT
- 3.9 多模態 AI 與世界模型

---

### 第二部分：神經網路

#### 第 4 章：機器學習與 Scikit-Learn 套件
- 4.1 監督式學習與非監督式學習
- 4.2 線性迴歸與邏輯迴歸
- 4.3 決策樹與隨機森林
- 4.4 支持向量機 (SVM)
- 4.5 K-Nearest Neighbors 與 clustering
- 4.6 Scikit-Learn 教學：實作經典機器學習演算法

#### 第 5 章：神經網路與 PyTorch 套件
- 5.1 神經網路基本概念：神經元、權重、偏置
- 5.2 PyTorch 張量 (Tensor) 操作
- 5.3 autograd 自動微分機制
- 5.4 建構第一個神經網路：nn.Module
- 5.5 資料集與 DataLoader
- 5.6 訓練迴圈與反向傳播

#### 第 6 章：梯度下降法與反傳遞演算法
- 6.1 優化問題與損失函數
- 6.2 梯度下降法 (Gradient Descent)
- 6.3 隨機梯度下降法 (SGD) 與動量
- 6.4 Adam、RMSprop 等優化器
- 6.5 反傳遞演算法 (Backpropagation) 原理解說
- 6.6 數值梯度範例：(x-1)² + (y-2)² + (z-3)² 找最低點
- 6.7 手刻神經網路範例：參考 micrograd/microgpt 架構

#### 第 7 章：從感知器到多層感知器
- 7.1 單層感知器 (Perceptron)
- 7.2 多層感知器 (MLP) 架構
- 7.3 激活函數：Sigmoid, Tanh, ReLU, Leaky ReLU
- 7.4 過擬合與正則化：Dropout, L1/L2
- 7.5 Batch Normalization 與層標準化
- 7.6 實作：MNIST 手寫數字分類

#### 第 8 章：卷積神經網路 (CNN)
- 8.1 卷積層與卷積運算
- 8.2 池化層 (Pooling)：Max Pooling, Average Pooling
- 8.3 經典 CNN 架構：LeNet, AlexNet, VGG, ResNet
- 8.4 遷移學習 (Transfer Learning) 與微調
- 8.5 目標檢測：YOLO, R-CNN 系列
- 8.6 實作：CIFAR-10 影像分類

#### 第 9 章：循環神經網路 (RNN)
- 9.1 RNN 基本原理與時間序列
- 9.2 長短期記憶網路 (LSTM)
- 9.3 閘門循環單元 (GRU)
- 9.4 雙向 RNN 與深層 RNN
- 9.5 序列到序列 (Seq2Seq) 模型
- 9.6 實作：文字生成與情感分類

#### 第 10 章：生成對抗網路 (GAN)
- 10.1 GAN 基本概念：生成器與判別器
- 10.2 損失函數與訓練技巧
- 10.3 DCGAN、WGAN、CGAN
- 10.4 StyleGAN 與人臉生成
- 10.5 條件生成與影像轉換
- 10.6 實作：生成 MNIST 數字

---

### 第三部分：現代語言模型與 Transformer

#### 第 11 章：現代語言模型簡介
- 11.1 語言模型的發展歷程
- 11.2 N-gram 與神經語言模型
- 11.3 Word2Vec, GloVe, FastText
- 11.4 ELMO 與情境化詞向量
- 11.5 GPT 系列的演進
- 11.6 BERT 與遮罩語言模型

#### 第 12 章：注意力機制、Transformer 與 GPT
- 12.1 注意力機制 (Attention) 原理
- 12.2 自注意力 (Self-Attention) 與 Multi-Head Attention
- 12.3 Transformer 架構：Encoder 與 Decoder
- 12.4 位置編碼 (Positional Encoding)
- 12.5 GPT-1/2/3/4 演進
- 12.6 實作：從零建構小型 Transformer

#### 第 13 章：最新語言模型的進展 (2018-現在)
- 13.1 LLM  Scaling Laws 與 GPT-4
- 13.2 RLHF 與人類回饋學習
- 13.3 InstructGPT 與 ChatGPT 原理
- 13.4 LLaMA, Mistral, Claude 等開源模型
- 13.5 提示工程 (Prompt Engineering)
- 13.6 微調技術：LoRA, QLoRA, Adapter

---

### 第四部分：Transformer 之後與世界模型

#### 第 14 章：視覺與聽覺模型
- 14.1 Vision Transformer (ViT)
- 14.2 CLIP 與對比學習
- 14.3 語音辨識模型：Whisper, Wav2Vec
- 14.4 文字轉語音 (TTS)：WaveNet, FastSpeech
- 14.5 實作：影像描述生成

#### 第 15 章：生成式 AI (Generative AI)
- 15.1 生成式 AI 概述
- 15.2 自回歸生成與採樣策略
- 15.3 VAE 變分自編碼器
- 15.4 Diffusion 擴散模型原理
- 15.5 Stable Diffusion 與影像生成
- 15.6 文字生成圖片：DALL-E, Midjourney
- 15.7 文字生成影片：Sora, Runway
- 15.8 實作：建構簡單的 Diffusion 模型

#### 第 16 章：多模態模型
- 16.1 多模態學習概述
- 16.2 GPT-4V 與視覺理解
- 16.3 Flamingo, BLIP 系列
- 16.4 實作：圖文對話系統

#### 第 17 章：代理人技術 (Agent)
- 17.1 AI Agent 概念與架構
- 17.2 ReAct 推理與行動框架
- 17.3 Tool Use 與 function calling
- 17.4 OpenCode、Claude Code、Codex 等程式工具
- 17.5 Memory 與長期記憶機制
- 17.6 實作：建構 AI 助手
  - 參考 [mini-openclaw.py](https://gist.github.com/dabit3/86ee04a1c02c839409a02b20fe99a492)

#### 第 18 章：強化學習 (Reinforcement Learning)
- 18.1 強化學習基本概念：Agent、Environment、Reward
- 18.2 Markov Decision Process (MDP)
- 18.3 價值函數與 Q 函數
- 18.4 Q-Learning 與 DQN
- 18.5 Policy Gradient 與 Actor-Critic
- 18.6 AlphaGo 與自我對弈

#### 第 19 章：世界模型 (World Model)
- 19.1 世界模型概念
- 19.2 Monte Carlo Tree Search (MCTS)
- 19.3 RL 與 AlphaGo 原理
- 19.4 Foundation Model as World Model
- 19.5 AI Playground 與模擬環境
- 19.6 通用人工智慧 (AGI) 的展望

---

### 附錄

#### 附錄 A：PyTorch 深度學習框架詳解
- A.1 PyTorch 與 TensorFlow 比較
- A.2 張量運算與 GPU 加速
- A.3 nn.Module 與模型建構
- A.4 訓練技巧與除錯

#### 附錄 B：數學基礎
- B.1 線性代數複習：矩陣、向量、奇異值分解
- B.2 機率論與資訊理論
- B.3 微積分與梯度
- B.4 最優化理論

#### 附錄 C：專有名詞索引
- 參考 ./index/README.md

#### 附錄 D：參考資源
- D.1 經典論文清單
- D.2 線上課程與教學資源
- D.3 開源專案與工具
