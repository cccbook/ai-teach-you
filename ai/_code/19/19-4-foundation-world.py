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
