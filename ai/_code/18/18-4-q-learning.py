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
