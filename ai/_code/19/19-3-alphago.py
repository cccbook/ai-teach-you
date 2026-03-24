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
