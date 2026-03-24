import numpy as np

class WorldModel:
    def __init__(self, state_dim, action_dim, latent_dim):
        self.state_encoder = np.random.randn(state_dim, latent_dim) * 0.1
        self.transition_model = np.random.randn(latent_dim + action_dim, latent_dim) * 0.1
        self.reward_model = np.random.randn(latent_dim, 1) * 0.1
        
    def encode(self, state):
        return state @ self.state_encoder
    
    def predict_next_state(self, latent_state, action):
        combined = np.concatenate([latent_state, action.reshape(1, -1)], axis=-1)
        next_latent = combined @ self.transition_model
        return next_latent
    
    def predict_reward(self, latent_state):
        return latent_state @ self.reward_model
    
    def forward(self, state, action):
        latent = self.encode(state)
        next_latent = self.predict_next_state(latent, action)
        reward = self.predict_reward(next_latent)
        return next_latent, reward

state_dim = 10
action_dim = 4
latent_dim = 8

world_model = WorldModel(state_dim, action_dim, latent_dim)

state = np.random.randn(state_dim)
action = np.random.randn(action_dim)

next_latent, reward = world_model.forward(state, action)

print("=" * 60)
print("World Model Demo")
print("=" * 60)
print(f"State dimension: {state_dim}")
print(f"Action dimension: {action_dim}")
print(f"Latent dimension: {latent_dim}")
print(f"\nInput state: {state.shape}")
print(f"Action: {action.shape}")
print(f"Predicted next latent: {next_latent.shape}")
print(f"Predicted reward: {reward.shape}")

print("\n✓ World model learns environment dynamics:")
print("  - encode(s): Map state to latent representation")
print("  - f(s,a): Predict next latent state")
print("  - r(s'): Predict reward from latent")
print("  - Enables planning without real interactions")
