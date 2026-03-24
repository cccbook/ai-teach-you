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
