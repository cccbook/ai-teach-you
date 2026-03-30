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
