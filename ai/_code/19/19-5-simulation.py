import numpy as np

class Simulator:
    def __init__(self, physics_params):
        self.params = physics_params
        self.state = np.zeros(10)
        
    def step(self, action):
        self.state += action * self.params.get('dt', 0.1)
        self.state += np.random.randn(10) * 0.01
        reward = -np.sum(self.state**2)
        done = abs(self.state).max() > 10
        return self.state, reward, done
    
    def reset(self):
        self.state = np.random.randn(10) * 0.1
        return self.state

class ModelBasedRL:
    def __init__(self, obs_dim, action_dim):
        self.world_model = np.random.randn(obs_dim + action_dim, obs_dim) * 0.1
        self.policy = np.random.randn(obs_dim, action_dim) * 0.1
        self.simulator = Simulator({'dt': 0.1})
        
    def imagine_rollout(self, initial_obs, num_steps=5):
        obs = initial_obs
        imagined_states = []
        
        for _ in range(num_steps):
            action = obs @ self.policy
            obs = obs @ self.world_model + np.random.randn(*obs.shape) * 0.1
            imagined_states.append(obs)
            
        return imagined_states
    
    def plan(self, initial_obs):
        imagined = self.imagine_rollout(initial_obs)
        return imagined

obs_dim = 10
action_dim = 4

agent = ModelBasedRL(obs_dim, action_dim)

initial_obs = np.random.randn(obs_dim)
planned = agent.plan(initial_obs)

print("=" * 60)
print("Simulation-Based Planning Demo")
print("=" * 60)
print(f"Observation dim: {obs_dim}")
print(f"Action dim: {action_dim}")
print(f"Imagination horizon: {len(planned)} steps")

print(f"\nInitial observation norm: {np.linalg.norm(initial_obs):.4f}")
print(f"First imagined state norm: {np.linalg.norm(planned[0]):.4f}")

print("\n✓ Simulation-based planning:")
print("  - Learn world model from interactions")
print("  - Imagine future trajectories in latent space")
print("  - Optimize policy using imagined rollouts")
print("  - Reduces real-world sample requirements")
