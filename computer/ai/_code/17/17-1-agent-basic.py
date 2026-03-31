import numpy as np

class SimpleAgent:
    def __init__(self, state_dim, action_dim):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.policy = np.random.randn(state_dim, action_dim) * 0.1
        
    def perceive(self, observation):
        return observation @ self.policy
    
    def decide(self, perception):
        return np.argmax(perception)
    
    def act(self, action):
        return f"Action {action} executed"
    
    def run(self, observation):
        perception = self.perceive(observation)
        action = self.decide(perception)
        result = self.act(action)
        return result

agent = SimpleAgent(state_dim=10, action_dim=4)

observation = np.random.randn(10)
result = agent.run(observation)

print("=" * 60)
print("Basic Agent Demo")
print("=" * 60)
print(f"State dimension: 10")
print(f"Action dimension: 4")
print(f"\nObservation: {observation[:5]}...")
print(f"Result: {result}")
print("\n✓ Simple agent architecture:")
print("  1. Perceive: Process observation")
print("  2. Decide: Choose action based on perception")
print("  3. Act: Execute the chosen action")
