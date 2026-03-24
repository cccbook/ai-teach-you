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
