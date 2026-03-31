import numpy as np

class SimpleRLHF:
    def __init__(self):
        self.rewards = []
        self.responses = []
        
    def step(self, response, reward):
        self.responses.append(response)
        self.rewards.append(reward)
        
    def get_preferred_response(self):
        if not self.rewards:
            return None
        best_idx = np.argmax(self.rewards)
        return self.responses[best_idx]

class PPOTrainer:
    def __init__(self, policy_lr=0.001):
        self.policy = np.random.randn(10) * 0.1
        self.value = np.random.randn(1) * 0.1
        self.policy_lr = policy_lr
        
    def compute_loss(self, log_probs, old_log_probs, rewards, values, old_values):
        advantage = rewards - old_values
        policy_loss = -np.mean(log_probs - old_log_probs) * advantage
        value_loss = np.mean((rewards - values) ** 2)
        return policy_loss + 0.5 * value_loss
    
    def update(self, responses, rewards):
        log_probs = np.sum(responses * self.policy)
        old_log_probs = log_probs
        values = np.sum(responses * self.value)
        old_values = values
        
        loss = self.compute_loss(log_probs, old_log_probs, rewards, values, old_values)
        self.policy += self.policy_lr * loss * np.sign(np.random.randn(10))
        
        return loss

rlhf = SimpleRLHF()
rlhf.step("Hello! How can I help?", 0.8)
rlhf.step("Hi there!", 0.5)
rlhf.step("Greetings, human.", 0.9)

ppot = PPOTrainer()
loss = ppot.update(np.random.randn(10), 0.7)

print("=" * 60)
print("RLHF (Reinforcement Learning from Human Feedback) Demo")
print("=" * 60)
print("\nResponses collected:")
for i, (r, rew) in enumerate(zip(rlhf.responses, rlhf.rewards)):
    print(f"  {i+1}. '{r}' -> reward: {rew}")
    
best = rlhf.get_preferred_response()
print(f"\nPreferred response: '{best}'")
print(f"\nPPO update loss: {loss:.4f}")
print("\n✓ RLHF uses human feedback to train a reward model,")
print("  then optimizes policy via PPO to maximize rewards")
