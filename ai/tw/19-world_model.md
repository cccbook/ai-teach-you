# 第 19 章：世界模型

世界模型 (World Model) 是人工智慧研究的前沿方向，旨在讓 AI 系統能夠構建和理解其所處環境的內部表示。本章將介紹世界模型的概念、蒙地卡羅樹搜尋、AlphaGo 原理、Foundation World Model，以及模擬環境和 AGI 的展望。

## 19.1 世界模型概念

世界模型是一種能夠預測環境動態變化的神經網路模型，類似於人類認知中的「心理模型」。

[程式檔案：19-1-world-model.py](../_code/19/19-1-world-model.py)

```python
import numpy as np

class WorldModel:
    def __init__(self, state_dim, action_dim, latent_dim):
        self.state_encoder = np.random.randn(state_dim, latent_dim) * 0.1
        self.transition_model = np.random.randn(latent_dim + action_dim, latent_dim) * 0.1
        self.reward_model = np.random.randn(latent_dim, 1) * 0.1
        
    def encode(self, state):
        return state @ self.state_encoder
    
    def predict_next_state(self, latent_state, action):
        combined = np.concatenate([latent_state, action.reshape(1, -1)], axis=-1)
        next_latent = combined @ self.transition_model
        return next_latent
    
    def predict_reward(self, latent_state):
        return latent_state @ self.reward_model
    
    def forward(self, state, action):
        latent = self.encode(state)
        next_latent = self.predict_next_state(latent, action)
        reward = self.predict_reward(next_latent)
        return next_latent, reward

state_dim = 10
action_dim = 4
latent_dim = 8

world_model = WorldModel(state_dim, action_dim, latent_dim)

state = np.random.randn(state_dim)
action = np.random.randn(action_dim)

next_latent, reward = world_model.forward(state, action)

print("=" * 60)
print("World Model Demo")
print("=" * 60)
print(f"State dimension: {state_dim}")
print(f"Action dimension: {action_dim}")
print(f"Latent dimension: {latent_dim}")
print(f"\nInput state: {state.shape}")
print(f"Action: {action.shape}")
print(f"Predicted next latent: {next_latent.shape}")
print(f"Predicted reward: {reward.shape}")

print("\n✓ World model learns environment dynamics:")
print("  - encode(s): Map state to latent representation")
print("  - f(s,a): Predict next latent state")
print("  - r(s'): Predict reward from latent")
print("  - Enables planning without real interactions")
```

### 19.1.1 世界模型的定義

世界模型的核心思想是學習環境的壓縮表示和動態規律：

```
世界模型架構：

┌─────────────────────────────────────────────────────────────┐
│                      World Model                            │
│                                                             │
│   輸入：狀態 s, 動作 a                                     │
│                                                             │
│   ┌───────────────┐                                        │
│   │ State Encoder │ ←── 將狀態編碼為潛在表示              │
│   └───────┬───────┘                                        │
│           ↓                                                │
│   ┌───────────────┐                                        │
│   │  Transition   │ ←── 預測下一狀態                       │
│   │    Model      │     f(s, a) → s'                       │
│   └───────┬───────┘                                        │
│           ↓                                                │
│   ┌───────────────┐                                        │
│   │Reward Model   │ ←── 預測獎勵                           │
│   └───────────────┘                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 19.1.2 世界模型的優勢

| 優勢 | 說明 |
|------|------|
| 樣本效率 | 在想像中學習，減少真實互動 |
| 安全探索 | 避免危險的真實環境探索 |
| 規劃能力 | 模擬未來並選擇最佳動作 |
| 泛化能力 | 學習環境規律，應對新情境 |

### 19.1.3 世界模型 vs 環境模型

| 特性 | 世界模型 | 環境模型 |
|------|----------|----------|
| 目標 | 壓縮表示 + 預測 | 精確模擬 |
| 應用 | 規劃、想像 | 仿真、測試 |
| 學習 | 表示學習 | 物理模擬 |
| 尺度 | 可擴展到大規模 | 受限於計算 |

## 19.2 蒙地卡羅樹搜尋 (MCTS)

MCTS 是一種在不完全資訊環境下進行決策的強大算法。

[程式檔案：19-2-mcts.py](../_code/19/19-2-mcts.py)

```python
import numpy as np

class MCTSNode:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.children = {}
        self.visits = 0
        self.value = 0.0
        
    def is_expanded(self):
        return len(self.children) > 0
    
    def best_child(self, c_param=1.4):
        best_score = float('-inf')
        best_child = None
        for action, child in self.children.items():
            exploitation = child.value / (child.visits + 1)
            exploration = c_param * np.sqrt(np.log(self.visits + 1) / (child.visits + 1))
            score = exploitation + exploration
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

class MCTS:
    def __init__(self, num_actions):
        self.num_actions = num_actions
        self.root = None
        
    def select(self, node):
        while node.is_expanded():
            node = node.best_child()
        return node
    
    def expand(self, node, action, next_state):
        child = MCTSNode(next_state, node, action)
        node.children[action] = child
        return child
    
    def backpropagate(self, node, reward):
        while node is not None:
            node.visits += 1
            node.value += reward
            node = node.parent

def simulate(env_state):
    return np.random.randn()

mcts = MCTS(num_actions=4)
mcts.root = MCTSNode(state=np.array([0, 0]))

for i in range(3):
    node = mcts.select(mcts.root)
    action = i
    next_state = np.array([i+1, i+1])
    child = mcts.expand(node, action, next_state)
    reward = simulate(next_state)
    mcts.backpropagate(child, reward)

best = mcts.root.best_child()

print("=" * 60)
print("MCTS (Monte Carlo Tree Search) Demo")
print("=" * 60)
print(f"Number of actions: 4")
print(f"Root visits: {mcts.root.visits}")
print(f"Root value: {mcts.root.value:.4f}")

print("\nChildren:")
for action, child in mcts.root.children.items():
    print(f"  Action {action}: visits={child.visits}, value={child.value:.4f}")

print("\n✓ MCTS combines tree search with Monte Carlo simulation:")
print("  - Selection: traverse tree using UCB")
print("  - Expansion: add new child node")
print("  - Simulation: rollout random policy")
print("  - Backpropagation: update statistics")
```

### 19.2.1 MCTS 四個步驟

```
MCTS 四個步驟：

1. Selection (選擇)
   從根節點出發，使用 UCB 選擇最佳子節點
   直到到達葉節點

2. Expansion (擴展)
   如果節點未完全擴展，添加新子節點

3. Simulation (模擬)
   從新節點出發，隨機 rollout 直到遊戲結束

4. Backpropagation (回傳)
   將模擬結果回傳更新路徑上所有節點的統計
```

### 19.2.2 UCB 公式

Upper Confidence Bound (UCB) 平衡探索與利用：

$$UCB = \frac{w_i}{n_i} + c \sqrt{\frac{\ln N}{n_i}}$$

其中：
- $w_i$：節點 i 的總獎勵
- $n_i$：節點 i 的訪問次數
- $N$：父節點的訪問次數
- $c$：探索常數

### 19.2.3 MCTS 的變體

| 變體 | 說明 |
|------|------|
| UCT | 標準 UCB 選擇 |
| RAVE | Rapid Action Value Estimation |
| MCTS-Solver | 處理失敗節點 |
| AlphaZero | 深度學習 + MCTS |

## 19.3 RL 與 AlphaGo 原理

AlphaGo 結合了深度學習、強化學習和 MCTS，是世界模型思想的典型應用。

[程式檔案：19-3-alphago.py](../_code/19/19-3-alphago.py)

```python
import numpy as np

class AlphaGo:
    def __init__(self):
        self.policy_net = np.random.randn(361, 361) * 0.1
        self.value_net = np.random.randn(361, 1) * 0.1
        
        self.sl_policy_loss = 0.0
        self.value_loss = 0.0
        self.mcts_iters = 0
        
    def policy_head(self, state):
        logits = state @ self.policy_net
        probs = np.exp(logits) / np.sum(np.exp(logits))
        return probs
    
    def value_head(self, state):
        return (state @ self.value_net)
    
    def mcts_search(self, state, num_iters=100):
        self.mcts_iters = num_iters
        return np.random.randint(361)
    
    def self_play(self):
        states = []
        mcts_probs = []
        rewards = []
        
        for _ in range(10):
            state = np.random.randn(361)
            states.append(state)
            
            pi = self.mcts_search(state)
            mcts_probs.append(pi)
            
            reward = 1.0 if np.random.random() > 0.5 else -1.0
            rewards.append(reward)
        
        return states, mcts_probs, rewards
    
    def train(self):
        states, mcts_probs, rewards = self.self_play()
        
        for s, pi, r in zip(states, mcts_probs, rewards):
            policy = self.policy_head(s)
            self.sl_policy_loss += -np.log(policy[pi] + 1e-8)
            self.value_loss += (self.value_head(s) - r) ** 2
            
        return self.sl_policy_loss, self.value_loss

alphago = AlphaGo()

policy_loss, value_loss = alphago.train()

print("=" * 60)
print("AlphaGo Demo")
print("=" * 60)
print(f"MCTS iterations: {alphago.mcts_iters}")
print(f"Policy loss: {policy_loss:.4f}")
print(f"Value loss: {value_loss:.4f}")

print("\n✓ AlphaGo combines:")
print("  - Supervised learning on expert moves")
print("  - Reinforcement learning (self-play)")
print("  - MCTS tree search with policy/value heads")
print("  - Beat human champion in Go (2016)")
```

### 19.3.1 AlphaGo 網路架構

```
AlphaGo 網路架構：

┌─────────────────────────────────────────────────────────────┐
│                    Input: 19×19 Board                        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Convolutional Layers                      │
│                    (類似 VGG 的特徵提取)                     │
└─────────────────────────────────────────────────────────────┘
                              ↓
              ┌───────────────┴───────────────┐
              ↓                               ↓
┌─────────────────────────┐     ┌─────────────────────────────┐
│    Policy Head          │     │      Value Head            │
│    (下一手預測)         │     │    (勝率預測)             │
│    Output: 19×19=361   │     │    Output: [-1, 1]         │
└─────────────────────────┘     └─────────────────────────────┘
```

### 19.3.2 AlphaGo 的訓練流程

| 階段 | 數據來源 | 目標 |
|------|----------|------|
| SL Policy | 人類棋譜 | 預測人類落子 |
| RL Policy | 自我對弈 | 提升勝率 |
| Value | 自我對弈 | 評估局面 |

### 19.3.3 AlphaGo Zero 的改進

AlphaGo Zero 拋棄了人類棋譜，完全從自我對弈中學習：

| 特性 | AlphaGo | AlphaGo Zero |
|------|---------|--------------|
| 人類數據 | 需要 | 不需要 |
| 特徵工程 | 手動設計 | 端到端 |
| 網路共享 | 獨立網路 | 共享骨幹 |
| 訓練方式 | 監督+強化 | 純強化 |

## 19.4 Foundation Model as World Model

Foundation Model 的出現為世界模型帶來了新的可能性。

[程式檔案：19-4-foundation-world.py](../_code/19/19-4-foundation-world.py)

```python
import numpy as np

class FoundationWorldModel:
    def __init__(self, obs_dim, action_dim, hidden_dim=256):
        self.encoder = np.random.randn(obs_dim, hidden_dim) * 0.1
        self.transition = np.random.randn(hidden_dim + action_dim, hidden_dim) * 0.1
        self.reward_head = np.random.randn(hidden_dim, 1) * 0.1
        self.discount_head = np.random.randn(hidden_dim, 1) * 0.1
        
    def encode(self, obs):
        return obs @ self.encoder
    
    def predict(self, latent_state, action):
        combined = np.concatenate([latent_state, action.reshape(1, -1)], axis=-1)
        next_latent = combined @ self.transition
        
        reward = (next_latent @ self.reward_head).flatten()
        discount = np.sigmoid(next_latent @ self.discount_head).flatten()
        
        return next_latent, reward, discount
    
    def rollout(self, obs, actions):
        latent = self.encode(obs)
        rewards = []
        discounts = []
        
        for action in actions:
            latent, reward, discount = self.predict(latent, action)
            rewards.append(reward)
            discounts.append(discount)
            
        return rewards, discounts

class Imagine:
    def __init__(self, foundation_model):
        self.model = foundation_model
        
    def plan(self, obs, num_steps=10):
        action_dim = 4
        imagined_actions = [np.random.randn(action_dim) for _ in range(num_steps)]
        
        rewards, discounts = self.model.rollout(obs, imagined_actions)
        
        returns = []
        R = 0
        for r, d in zip(rewards, discounts):
            R = r + d * R
            returns.append(R)
            
        return imagined_actions, returns

obs_dim = 64
action_dim = 4

foundation = FoundationWorldModel(obs_dim, action_dim)
imagine = Imagine(foundation)

obs = np.random.randn(obs_dim)
planned_actions, returns = imagine.plan(obs, num_steps=5)

print("=" * 60)
print("Foundation World Model Demo")
print("=" * 60)
print(f"Observation dim: {obs_dim}")
print(f"Action dim: {action_dim}")
print(f"Planning steps: 5")

print(f"\nPlanned actions: {len(planned_actions)}")
print(f"Imagined returns: {[float(r[0]) for r in returns]}")

print("\n✓ Foundation World Models enable:")
print("  - Learning world dynamics from observations")
print("  - Imagining future trajectories")
print("  - Planning via model-based RL")
print("  - Efficient exploration without real interactions")
```

### 19.4.1 Foundation World Model 的特點

| 特點 | 說明 |
|------|------|
| 大規模預訓練 | 從海量視頻中學習 |
| 通用表示 | 跨任務泛化能力 |
| 想像規劃 | 在潛在空間中模擬 |
| 零樣本 | 處理新任務無需訓練 |

### 19.4.2 影片預訓練

Foundation World Model 通常在大規模影片數據上預訓練：

```python
class VideoPreTraining:
    def __init__(self):
        self.spacetime_model = SpacetimeTransformer()
        
    def pretrain(self, videos):
        # 從影片中學習：
        # 1. 視覺特徵
        # 2. 動作預測
        # 3. 物理規律
        loss = self.forward(videos)
        return loss
```

## 19.5 模擬環境與規劃

模擬環境是世界模型應用的重要場景。

[程式檔案：19-5-simulation.py](../_code/19/19-5-simulation.py)

```python
import numpy as np

class Simulator:
    def __init__(self, physics_params):
        self.params = physics_params
        self.state = np.zeros(10)
        
    def step(self, action):
        self.state += action * self.params.get('dt', 0.1)
        self.state += np.random.randn(10) * 0.01
        reward = -np.sum(self.state**2)
        done = abs(self.state).max() > 10
        return self.state, reward, done
    
    def reset(self):
        self.state = np.random.randn(10) * 0.1
        return self.state

class ModelBasedRL:
    def __init__(self, obs_dim, action_dim):
        self.world_model = np.random.randn(obs_dim + action_dim, obs_dim) * 0.1
        self.policy = np.random.randn(obs_dim, action_dim) * 0.1
        self.simulator = Simulator({'dt': 0.1})
        
    def imagine_rollout(self, initial_obs, num_steps=5):
        obs = initial_obs
        imagined_states = []
        
        for _ in range(num_steps):
            action = obs @ self.policy
            obs = obs @ self.world_model + np.random.randn(*obs.shape) * 0.1
            imagined_states.append(obs)
            
        return imagined_states
    
    def plan(self, initial_obs):
        imagined = self.imagine_rollout(initial_obs)
        return imagined

obs_dim = 10
action_dim = 4

agent = ModelBasedRL(obs_dim, action_dim)

initial_obs = np.random.randn(obs_dim)
planned = agent.plan(initial_obs)

print("=" * 60)
print("Simulation-Based Planning Demo")
print("=" * 60)
print(f"Observation dim: {obs_dim}")
print(f"Action dim: {action_dim}")
print(f"Imagination horizon: {len(planned)} steps")

print(f"\nInitial observation norm: {np.linalg.norm(initial_obs):.4f}")
print(f"First imagined state norm: {np.linalg.norm(planned[0]):.4f}")

print("\n✓ Simulation-based planning:")
print("  - Learn world model from interactions")
print("  - Imagine future trajectories in latent space")
print("  - Optimize policy using imagined rollouts")
print("  - Reduces real-world sample requirements")
```

### 19.5.1 模擬環境的優勢

| 優勢 | 說明 |
|------|------|
| 樣本效率 | 可批量生成數據 |
| 安全性 | 避免危險操作 |
| 可重複性 | 確定性實驗 |
| 成本 | 低於真實環境 |

### 19.5.2 Model-Based RL 流程

```
Model-Based RL 流程：

1. 環境互動
   收集轉移數據 (s, a, r, s')

2. 世界模型學習
   訓練 f(s,a) → s', r(s')

3. 想像 rollout
   在模型中模擬未來

4. 策略優化
   選擇最大化想像回報的動作

5. 執行
   在真實環境中執行動作
```

## 19.6 通用人工智慧 (AGI) 的展望

AGI 是人工智慧研究的終極目標，世界模型是實現 AGI 的重要路徑之一。

[程式檔案：19-6-agi-future.py](../_code/19/19-6-agi-future.py)

```python
import numpy as np

class AGIFuture:
    def __init__(self):
        self.components = {
            "perception": "Multi-modal understanding",
            "cognition": "Reasoning & planning",
            "memory": "Long-term knowledge",
            "action": "Tool use & execution",
            "learning": "Self-improvement"
        }
        
        self.capabilities = []
        
    def add_capability(self, name, level):
        self.capabilities.append({"name": name, "level": level})
        
    def assess(self):
        scores = {
            "perception": 0.85,
            "cognition": 0.70,
            "memory": 0.90,
            "action": 0.75,
            "learning": 0.65
        }
        overall = np.mean(list(scores.values()))
        return scores, overall

agi = AGIFuture()

agi.add_capability("language", 0.9)
agi.add_capability("vision", 0.85)
agi.add_capability("reasoning", 0.7)
agi.add_capability("planning", 0.65)
agi.add_capability("creativity", 0.5)

scores, overall = agi.assess()

print("=" * 60)
print("AGI Future Demo")
print("=" * 60)

print("\nCore AGI Components:")
for comp, desc in agi.components.items():
    print(f"  - {comp}: {desc}")

print("\nCurrent Capability Levels:")
for cap, score in scores.items():
    bar = "█" * int(score * 20) + "░" * (20 - int(score * 20))
    print(f"  {cap:12s}: [{bar}] {score:.0%}")

print(f"\nOverall AGI Readiness: {overall:.0%}")

print("\n✓ Pathways to AGI:")
print("  - Foundation models as basis")
print("  - Multi-modal perception")
print("  - Autonomous agents")
print("  - Self-improvement loops")
print("  - Safe alignment throughout")
```

### 19.6.1 AGI 的關鍵要素

| 要素 | 當前水平 | 發展方向 |
|------|----------|----------|
| 感知 | 85% | 整合更多模態 |
| 認知 | 70% | 深度推理 |
| 記憶 | 90% | 長期學習 |
| 行動 | 75% | 物理交互 |
| 學習 | 65% | 自主學習 |

### 19.6.2 AGI 的可能路徑

```
AGI 發展路徑：

路徑 1：擴展 Transformer
  Transformer → 更大多模態模型 → AGI

路徑 2：世界模型
  語言模型 → 世界模型 → 想像規劃 → AGI

路徑 3：代理人系統
  LLM + Tool Use → Agent → 自主系統 → AGI

路徑 4：神經符號混合
  神經網路 + 符號推理 → 混合系統 → AGI
```

### 19.6.3 安全與對齊

AGI 的發展必須伴隨安全研究：

| 挑戰 | 說明 |
|------|------|
| 價值對齊 | 確保 AI 目標與人類一致 |
| 可解釋性 | 理解 AI 決策過程 |
| 魯棒性 | 抵禦對抗攻擊 |
| 控制 | 保持人類控制 |

## 19.7 總結

本章介紹了世界模型的核心概念和相關技術：

| 技術 | 說明 |
|------|------|
| 世界模型 | 學習環境動態的內部表示 |
| MCTS | 結合樹搜尋和模擬的決策算法 |
| AlphaGo | 深度學習 + 強化學習 + MCTS |
| Foundation World Model | 大規模預訓練的世界模型 |
| 模擬環境 | 安全高效的規劃平台 |

世界模型代表了人工智慧向更高級認知能力發展的重要方向。通過學習環境的表示和規律，AI 系統可以進行想像、規劃和推理，這些都是邁向通用人工智慧的關鍵能力。

從 AlphaGo 到 Foundation World Model，我們正在見證世界模型技術的快速發展。隨著模型規模的擴大、數據的多樣化和算法的進步，AI 系統對世界的理解將越來越深入，為實現通用人工智慧奠定基礎。
