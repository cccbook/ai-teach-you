import numpy as np

class ValueFunction:
    def __init__(self, num_states):
        self.num_states = num_states
        self.values = np.zeros(num_states)
        
    def update(self, state, reward, gamma=0.9, next_value=0):
        self.values[state] = reward + gamma * next_value
        
    def get_value(self, state):
        return self.values[state]

class QFunction:
    def __init__(self, num_states, num_actions):
        self.num_states = num_states
        self.num_actions = num_actions
        self.q_table = np.zeros((num_states, num_actions))
        
    def update(self, state, action, reward, gamma=0.9, max_next_q=0):
        self.q_table[state, action] = reward + gamma * max_next_q
        
    def get_q(self, state, action):
        return self.q_table[state, action]
    
    def get_best_action(self, state):
        return np.argmax(self.q_table[state])

num_states = 5
num_actions = 2

V = ValueFunction(num_states)
Q = QFunction(num_states, num_actions)

V.update(0, reward=1.0, next_value=V.get_value(1))
V.update(1, reward=2.0, next_value=V.get_value(2))
V.update(2, reward=0.5, next_value=0)

Q.update(0, 0, reward=1.0, max_next_q=Q.get_q(1, 1))
Q.update(0, 1, reward=0.5, max_next_q=Q.get_q(1, 0))
Q.update(1, 0, reward=2.0, max_next_q=0)

print("=" * 60)
print("Value Function Demo")
print("=" * 60)
print(f"Number of states: {num_states}")
print(f"Number of actions: {num_actions}")
print("\nState Value Function V(s):")
for s in range(num_states):
    print(f"  V({s}) = {V.get_value(s):.2f}")

print("\nQ-Function Q(s,a):")
for s in range(num_states):
    for a in range(num_actions):
        print(f"  Q({s},{a}) = {Q.get_q(s, a):.2f}")

print("\n✓ Value functions estimate expected future rewards:")
print("  - V(s): Expected return from state s")
print("  - Q(s,a): Expected return from state s, taking action a")
print("  - Used in policy extraction: π(s) = argmax_a Q(s,a)")
