# 第 18 章：強化學習

強化學習 (Reinforcement Learning, RL) 是機器學習的一個重要分支，專注於智慧體 (Agent) 通過與環境的互動來學習最優決策策略。本章將介紹強化學習的基本概念、馬爾可夫決策過程、Q-Learning、深度 Q 網路 (DQN)、策略梯度方法，以及 AlphaGo 等經典應用。

## 18.1 強化學習基本概念

強化學習的核心理念是讓 Agent 通過「試錯」來學習，透過與環境的互動獲得獎勵或懲罰，從而逐步優化決策策略。

### 18.1.1 強化學習基本要素

```
強化學習框架：

    ┌─────────────────────────────────────────────┐
    │                                             │
    │   Agent (智慧體)                           │
    │                                             │
    │   觀測 Oₜ ──→ 策略 π(a│o) ──→ 動作 Aₜ   │
    │                                             │
    └────────────────┬────────────────────────────┘
                     │
                     │ 動作 Aₜ
                     ↓
    ┌────────────────┬────────────────────────────┐
    │                │                            │
    │   環境 (Environment)                       │
    │                                             │
    │   状態 Sₜ ──→ 獎勵 Rₜ+1 ──→ 新狀態 Sₜ+1  │
    │                                             │
    └─────────────────────────────────────────────┘
```

| 要素 | 說明 |
|------|------|
| Agent | 學習者和決策者 |
| Environment | Agent 互動的外部系統 |
| State (s) | 環境的當前描述 |
| Action (a) | Agent 可以執行的動作 |
| Reward (r) | 環境對動作的反饋 |
| Policy (π) | 從狀態到動作的映射 |
| Value (V) | 未來累積獎勵的期望 |

### 18.1.2 強化學習 vs 監督學習

| 特性 | 監督學習 | 強化學習 |
|------|----------|----------|
| 資料 | 標註數據 | 互動產生 |
| 目標 | 預測標籤 | 最大化長期獎勵 |
| 反饋 | 直接標籤 | 延遲獎勵 |
| 探索 | 無需探索 | 需要探索 |

## 18.2 馬爾可夫決策過程 (MDP)

MDP 是強化學習的數學基礎，提供了一個描述序貫決策問題的框架。

[程式檔案：18-1-grid-world.py](../_code/18/18-1-grid-world.py)

```python
import numpy as np

class GridWorld:
    def __init__(self, width=4, height=4, start=(0, 0), goal=(3, 3)):
        self.width = width
        self.height = height
        self.start = start
        self.goal = goal
        self.state = start
        
    def reset(self):
        self.state = self.start
        return self.state
    
    def step(self, action):
        x, y = self.state
        if action == 0:
            y = max(0, y - 1)
        elif action == 1:
            y = min(self.height - 1, y + 1)
        elif action == 2:
            x = max(0, x - 1)
        elif action == 3:
            x = min(self.width - 1, x + 1)
            
        self.state = (x, y)
        
        if self.state == self.goal:
            return self.state, 1.0, True
        return self.state, -0.1, False
    
    def render(self):
        grid = [["." for _ in range(self.width)] for _ in range(self.height)]
        gx, gy = self.goal
        grid[gy][gx] = "G"
        sx, sy = self.state
        grid[sy][sx] = "A"
        return "\n".join([" ".join(row) for row in grid])

env = GridWorld()
state = env.reset()

print("=" * 60)
print("Grid World Environment Demo")
print("=" * 60)
print(f"Grid size: {env.width}x{env.height}")
print(f"Start: {env.start}, Goal: {env.goal}")
print("\nInitial state:")
print(env.render())

actions = [1, 1, 3, 3, 1, 1, 3]
for a in actions:
    state, reward, done = env.step(a)
    print(f"\nAction {a}, Reward: {reward:.1f}")
    print(env.render())
    if done:
        print("Goal reached!")
        break
```

### 18.2.1 MDP 定義

MDP 由五元組 (S, A, P, R, γ) 定義：

- **S**: 狀態空間
- **A**: 動作空間  
- **P**: 轉移概率 P(s'|s, a)
- **R**: 獎勵函數 R(s, a, s')
- **γ**: 折扣因子 (0 ≤ γ < 1)

### 18.2.2 價值函數與 Q 函數

```python
# 狀態價值函數 V(s)
def compute_value(state, policy, env, gamma=0.9, theta=0.001):
    V = {s: 0 for s in range(env.width * env.height)}
    
    while True:
        delta = 0
        for s in range(env.width * env.height):
            v = V[s]
            action = policy(s)
            # 計算新價值
            V[s] = sum(
                prob * (reward + gamma * V[next_state])
                for prob, next_state, reward in env.transitions[s][action]
            )
            delta = max(delta, abs(v - V[s]))
        
        if delta < theta:
            break
    
    return V
```

[程式檔案：18-2-mdp.py](../_code/18/18-2-mdp.py)

```python
import numpy as np

class MDP:
    def __init__(self, states, actions, transitions, rewards, gamma=0.9):
        self.states = states
        self.actions = actions
        self.transitions = transitions
        self.rewards = rewards
        self.gamma = gamma
        
    def transition_prob(self, s, a, s_next):
        return self.transitions.get((s, a, s_next), 0.0)
    
    def reward(self, s, a, s_next):
        return self.rewards.get((s, a, s_next), 0.0)
    
    def value_iteration(self, threshold=0.001, max_iter=100):
        V = {s: 0.0 for s in self.states}
        
        for _ in range(max_iter):
            delta = 0
            new_V = {}
            
            for s in self.states:
                max_value = float('-inf')
                for a in self.actions:
                    value = 0
                    for s_next in self.states:
                        p = self.transition_prob(s, a, s_next)
                        r = self.reward(s, a, s_next)
                        value += p * (r + self.gamma * V[s_next])
                    max_value = max(max_value, value)
                new_V[s] = max_value
                delta = max(delta, abs(new_V[s] - V[s]))
                
            V = new_V
            
            if delta < threshold:
                break
                
        return V

states = [0, 1, 2]
actions = [0, 1]
transitions = {
    (0, 0, 0): 0.8, (0, 0, 1): 0.2,
    (0, 1, 1): 0.9, (0, 1, 2): 0.1,
    (1, 0, 0): 0.5, (1, 0, 1): 0.5,
    (1, 1, 2): 1.0,
    (2, 0, 2): 1.0, (2, 1, 2): 1.0,
}
rewards = {
    (0, 1, 1): 1.0,
    (1, 1, 2): 10.0,
}

mdp = MDP(states, actions, transitions, rewards)
V = mdp.value_iteration()

print("=" * 60)
print("MDP (Markov Decision Process) Demo")
print("=" * 60)
print(f"States: {states}")
print(f"Actions: {actions}")
print(f"Discount factor: {mdp.gamma}")
print("\nOptimal Value Function:")
for s, v in V.items():
    print(f"  V(s={s}) = {v:.4f}")
print("\n✓ MDP components:")
print("  - States: possible environmental states")
print("  - Actions: agent's choices")
print("  - Transitions: P(s'|s,a)")
print("  - Rewards: R(s,a,s')")
print("  - Discount: importance of future rewards")
```

## 18.3 Q-Learning 與深度 Q 網路

Q-Learning 是一種經典的無模型強化學習算法。

[程式檔案：18-4-q-learning.py](../_code/18/18-4-q-learning.py)

```python
import numpy as np

class QLearning:
    def __init__(self, num_states, num_actions, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.num_states = num_states
        self.num_actions = num_actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = np.zeros((num_states, num_actions))
        
    def choose_action(self, state):
        if np.random.random() < self.epsilon:
            return np.random.randint(self.num_actions)
        return np.argmax(self.q_table[state])
    
    def update(self, state, action, reward, next_state):
        current_q = self.q_table[state, action]
        max_next_q = np.max(self.q_table[next_state])
        target = reward + self.gamma * max_next_q
        self.q_table[state, action] = current_q + self.alpha * (target - current_q)
        
    def decay_epsilon(self):
        self.epsilon = max(0.01, self.epsilon * 0.99)

num_states = 16
num_actions = 4

agent = QLearning(num_states, num_actions)

episodes = [
    [(0, 1, 0, 1), (1, 1, 0, 2), (2, 1, 0, 3)],
    [(0, 0, 0, 4), (4, 2, 1, 8)],
]

print("=" * 60)
print("Q-Learning Demo")
print("=" * 60)
print(f"States: {num_states}, Actions: {num_actions}")
print(f"Alpha: {agent.alpha}, Gamma: {agent.gamma}, Epsilon: {agent.epsilon}")

for ep, episode in enumerate(episodes):
    for state, action, reward, next_state in episode:
        agent.update(state, action, reward, next_state)
    agent.decay_epsilon()
    
print("\nQ-table after training:")
print(f"Q(0,0) = {agent.q_table[0,0]:.2f}, Q(0,1) = {agent.q_table[0,1]:.2f}")
print(f"Q(0,2) = {agent.q_table[0,2]:.2f}, Q(0,3) = {agent.q_table[0,3]:.2f}")
print(f"\nEpsilon after decay: {agent.epsilon:.4f}")

print("\n✓ Q-Learning algorithm:")
print("  - Off-policy TD control")
print("  - Q(s,a) ← Q(s,a) + α[r + γmax_a' Q(s',a') - Q(s,a)]")
print("  - Explores with ε-greedy, decays over time")
```

### 18.3.1 Q-Learning 更新規則

Q-Learning 使用時序差分 (TD) 更新：

$$Q(s, a) \leftarrow Q(s, a) + \alpha [r + \gamma \max_{a'} Q(s', a') - Q(s, a)]$$

```
Q-Learning 流程：

初始化 Q(s, a) 為任意值
REPEAT (對每個episode):
    初始化狀態 s
    REPEAT (對episode中的每步):
        使用 ε-greedy 選擇動作 a
        執行動作 a，觀察 r 和 s'
        Q(s, a) ← Q(s, a) + α[r + γmax_a' Q(s', a') - Q(s, a)]
        s ← s'
    直到 s 是終止狀態
```

### 18.3.2 深度 Q 網路 (DQN)

DQN 將 Q-Learning 與深度神經網路結合，處理高維度狀態空間。

[程式檔案：18-5-dqn.py](../_code/18/18-5-dqn.py)

```python
import numpy as np

class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = []
        self.capacity = capacity
        
    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))
        if len(self.buffer) > self.capacity:
            self.buffer.pop(0)
            
    def sample(self, batch_size):
        indices = np.random.choice(len(self.buffer), batch_size, replace=False)
        return [self.buffer[i] for i in indices]

class DQN:
    def __init__(self, state_dim, action_dim, hidden_dim=64):
        self.action_dim = action_dim
        self.q_network = np.random.randn(state_dim, hidden_dim) * 0.1
        self.q_target = np.random.randn(state_dim, hidden_dim) * 0.1
        self.q_head = np.random.randn(hidden_dim, action_dim) * 0.1
        
    def forward(self, state, target=False):
        net = self.q_target if target else self.q_network
        hidden = state @ net
        return hidden @ self.q_head
    
    def update_target(self):
        self.q_target = self.q_network.copy()

state_dim = 4
action_dim = 2

dqn = DQN(state_dim, action_dim)
buffer = ReplayBuffer(capacity=1000)

for i in range(100):
    state = np.random.randn(state_dim)
    action = np.random.randint(action_dim)
    reward = np.random.randn()
    next_state = np.random.randn(state_dim)
    done = False
    buffer.push(state, action, reward, next_state, done)

batch = buffer.sample(batch_size=32)

print("=" * 60)
print("DQN (Deep Q-Network) Demo")
print("=" * 60)
print(f"State dimension: {state_dim}")
print(f"Action dimension: {action_dim}")
print(f"Replay buffer capacity: 1000")
print(f"Batch size: {len(batch)}")
print(f"\nQ-network output shape: {dqn.forward(batch[0][0]).shape}")

dqn.update_target()

print("\n✓ DQN combines Q-learning with deep neural networks:")
print("  - Experience replay buffer")
print("  - Target network for stability")
print("  - Epsilon-greedy exploration")
print("  - Q(s,a) approximation via neural net")
```

### 18.3.3 DQN 的關鍵技術

| 技術 | 說明 | 作用 |
|------|------|------|
| Experience Replay | 存儲並隨機採樣經驗 | 打破樣本相關性 |
| Target Network | 固定目標網路 | 提高訓練穩定性 |
| Epsilon-Greedy | 隨機探索 | 確保探索 |
| Double DQN | 雙網路減少過估計 | 提升性能 |

## 18.4 Policy Gradient 與 Actor-Critic

策略梯度方法直接優化策略網路，適合連續動作空間。

[程式檔案：18-6-policy-gradient.py](../_code/18/18-6-policy-gradient.py)

```python
import numpy as np

class PolicyNetwork:
    def __init__(self, state_dim, action_dim, hidden_dim=32):
        self.W1 = np.random.randn(state_dim, hidden_dim) * 0.1
        self.W2 = np.random.randn(hidden_dim, action_dim) * 0.1
        
    def forward(self, state):
        hidden = np.maximum(0, state @ self.W1)
        logits = hidden @ self.W2
        probs = self.softmax(logits)
        return probs
    
    def softmax(self, x):
        exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=-1, keepdims=True)
    
    def get_action(self, state):
        probs = self.forward(state)
        return np.random.choice(len(probs), p=probs)
    
    def update(self, states, actions, advantages, lr=0.01):
        for s, a, adv in zip(states, actions, advantages):
            probs = self.forward(s)
            log_prob = np.log(probs[a] + 1e-8)
            grad = -adv * log_prob
            
            hidden = np.maximum(0, s @ self.W1)
            self.W2 += lr * grad * hidden
            self.W1 += lr * grad * np.where(hidden > 0, s, 0)

policy = PolicyNetwork(state_dim=4, action_dim=2)

state = np.random.randn(4)
probs = policy.forward(state)
action = policy.get_action(state)

print("=" * 60)
print("Policy Gradient Demo")
print("=" * 60)
print(f"State dimension: 4")
print(f"Action dimension: 2")
print(f"\nState: {state}")
print(f"Action probabilities: {probs}")
print(f"Sampled action: {action}")
print("\n✓ Policy Gradient methods:")
print("  - Directly optimize policy π(a|s)")
print("  - REINFORCE: ∇J = E[∇log π(a|s) * Gt]")
print("  - Stochastic policy, good for continuous actions")
print("  - Can have high variance, use baseline to reduce")
```

### 18.4.1 REINFORCE 算法

REINFORCE 是最基礎的策略梯度算法：

$$\nabla_\theta J(\theta) = \mathbb{E}[\nabla_\theta \log \pi_\theta(a|s) \cdot G_t]$$

其中 $G_t$ 是從時間 t 開始的累積折扣獎勵。

### 18.4.2 Actor-Critic 架構

[程式檔案：18-7-actor-critic.py](../_code/18/18-7-actor-critic.py)

```python
import numpy as np

class Actor:
    def __init__(self, state_dim, action_dim, hidden_dim=32):
        self.W = np.random.randn(state_dim, hidden_dim) * 0.1
        self.head = np.random.randn(hidden_dim, action_dim) * 0.1
        
    def forward(self, state):
        hidden = np.maximum(0, state @ self.W)
        logits = hidden @ self.head
        probs = np.exp(logits) / np.sum(np.exp(logits))
        return probs
    
    def get_action(self, state):
        probs = self.forward(state)
        return np.random.choice(len(probs), p=probs)

class Critic:
    def __init__(self, state_dim, hidden_dim=32):
        self.W = np.random.randn(state_dim, hidden_dim) * 0.1
        self.head = np.random.randn(hidden_dim, 1) * 0.1
        
    def forward(self, state):
        hidden = np.maximum(0, state @ self.W)
        return (hidden @ self.head).flatten()

class ActorCritic:
    def __init__(self, state_dim, action_dim):
        self.actor = Actor(state_dim, action_dim)
        self.critic = Critic(state_dim)
        
    def update(self, state, action, reward, next_state, gamma=0.9, lr=0.01):
        value = self.critic.forward(state)
        next_value = self.critic.forward(next_state)
        
        advantage = reward + gamma * next_value - value
        
        probs = self.actor.forward(state)
        log_prob = np.log(probs[action] + 1e-8)
        
        self.critic.W += lr * advantage * state
        self.actor.W += lr * advantage * log_prob * state

actor_critic = ActorCritic(state_dim=4, action_dim=2)

state = np.random.randn(4)
action = actor_critic.actor.get_action(state)
value = actor_critic.critic.forward(state)
next_state = np.random.randn(4)

actor_critic.update(state, action, 1.0, next_state)

print("=" * 60)
print("Actor-Critic Demo")
print("=" * 60)
print(f"State dimension: 4")
print(f"Action dimension: 2")
print(f"\nState: {state}")
print(f"Action chosen: {action}")
print(f"Value estimate: {value[0]:.4f}")

print("\n✓ Actor-Critic combines policy gradient with value function:")
print("  - Actor: policy π(a|s) - learns which action to take")
print("  - Critic: V(s) - estimates state value")
print("  - Advantage = r + γV(s') - V(s)")
print("  - Lower variance than REINFORCE alone")
```

### 18.4.3 Actor-Critic 優勢

| 組件 | 功能 | 優勢 |
|------|------|------|
| Actor | 學習策略 | 直接優化目標 |
| Critic | 估計價值 | 降低方差 |
| Advantage | A = r + γV(s') - V(s) | 優勢估計 |

## 18.5 AlphaGo 與自我對弈

AlphaGo 是 DeepMind 開發的圍棋 AI，結合了深度學習、強化學習和蒙地卡羅樹搜尋。

[程式檔案：18-3-value-function.py](未找到，18-3文件不存在)

[程式檔案：18-8-tictactoe.py](../_code/18/18-8-tictactoe.py)

```python
import numpy as np

class TicTacToe:
    def __init__(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.player = 1
        
    def reset(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.player = 1
        return self.board.flatten()
    
    def get_empty_cells(self):
        return list(zip(*np.where(self.board == 0)))
    
    def check_winner(self):
        for i in range(3):
            if np.all(self.board[i, :] == self.player):
                return True
            if np.all(self.board[:, i] == self.player):
                return True
        if np.all(np.diag(self.board) == self.player):
            return True
        if np.all(np.diag(np.fliplr(self.board)) == self.player):
            return True
        return False
    
    def step(self, action):
        row, col = action // 3, action % 3
        
        if self.board[row, col] != 0:
            return self.board.flatten(), -1.0, True
            
        self.board[row, col] = self.player
        
        if self.check_winner():
            return self.board.flatten(), 1.0, True
            
        if len(self.get_empty_cells()) == 0:
            return self.board.flatten(), 0.0, True
            
        self.player = -self.player
        return self.board.flatten(), 0.0, False

class TictactoeRL:
    def __init__(self):
        self.q_table = {}
        
    def get_state_key(self, board):
        return tuple(board)
    
    def get_q(self, state, action):
        key = (self.get_state_key(state), action)
        return self.q_table.get(key, 0.0)
    
    def update(self, state, action, reward):
        key = (self.get_state_key(state), action)
        self.q_table[key] = reward

game = TicTacToe()
agent = TictactoeRL()

print("=" * 60)
print("Tic-Tac-Toe RL Demo")
print("=" * 60)

state = game.reset()
print("Initial board:")
print(np.array([' ' if x == 0 else ('X' if x == 1 else 'O') for x in state]).reshape(3,3))

actions = [4, 0, 1, 2]
for a in actions:
    state, reward, done = game.step(a)
    agent.update(state, a, reward)
    board_display = np.array([' ' if x == 0 else ('X' if x == 1 else 'O') for x in state]).reshape(3,3)
    print(f"\nAfter move {a}:")
    print(board_display)
    if done:
        print(f"Game over! Reward: {reward}")
        break

print("\n✓ Tic-Tac-Toe RL demonstrates:")
print("  - Discrete action space (9 positions)")
print("  - Perfect information game")
print("  - Can be solved with Q-learning / search")
print("  - Good baseline for game-playing RL")
```

### 18.5.1 AlphaGo 的核心技術

| 技術 | 說明 |
|------|------|
| 監督學習策略網路 | 從人類高手棋譜學習 |
| 強化學習策略網路 | 自我對弈提升 |
| 價值網路 | 評估局勢 |
| MCTS | 蒙地卡羅樹搜尋 |
| 深度學習 | 特徵提取和模式識別 |

### 18.5.2 AlphaGo 訓練流程

```
AlphaGo 訓練流程：

階段 1：監督學習
人類棋譜 ──→ Policy Network (SL) ──→ 預測人類落子

階段 2：自我對弈
SL Policy Network ──→ RL Policy Network ──→ 更高勝率

階段 3：價值學習
自我對弈棋局 ──→ Value Network ──→ 預測勝率

階段 4：MCTS 搜尋
Policy Network + Value Network ──→ 蒙地卡羅樹搜尋 ──→ 選擇落子
```

## 18.6 強化學習的應用場景

| 領域 | 應用 | 說明 |
|------|------|------|
| 遊戲 | AlphaGo, OpenAI Five | 超越人類水平 |
| 機器人 | 運動控制 | 學習複雜動作 |
| 推薦系統 | 廣告推薦 | 優化長期收益 |
| 自動駕駛 | 決策規劃 | 路徑規劃 |
| 金融 | 投資組合 | 資產配置 |

## 18.7 總結

本章介紹了強化學習的核心概念和算法：

| 算法 | 類型 | 特點 |
|------|------|------|
| Q-Learning | 值函數 | 離策略 TD 控制 |
| DQN | 值函數 | 深度學習 + Q-Learning |
| Policy Gradient | 策略梯度 | 直接優化策略 |
| Actor-Critic | 混合 | 結合值函數和策略梯度 |
| AlphaGo | 整合 | MCTS + 深度學習 |

強化學習是人工智慧領域最具挑戰性的方向之一，它使機器能夠通過與環境的互動自主學習複雜的決策策略。從遊戲到機器人，從推薦系統到自動駕駛，強化學習正在展現出巨大的應用潛力。
