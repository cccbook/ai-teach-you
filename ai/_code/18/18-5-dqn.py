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
