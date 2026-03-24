import numpy as np

class DDIMScheduler:
    def __init__(self, num_timesteps=50, eta=0.0):
        self.num_timesteps = num_timesteps
        self.eta = eta
        
    def get_schedule(self):
        timesteps = np.linspace(self.num_timesteps - 1, 0, self.num_timesteps)
        return timesteps.astype(int)
    
    def step(self, x_t, noise_pred, t, t_prev):
        alpha_t = self.get_alpha(t)
        alpha_t_prev = self.get_alpha(t_prev)
        
        pred_x0 = (x_t - np.sqrt(1 - alpha_t) * noise_pred) / np.sqrt(alpha_t)
        
        if self.eta == 0:
            x_t_prev = np.sqrt(alpha_t_prev) * pred_x0 + np.sqrt(1 - alpha_t_prev) * noise_pred
        else:
            sigma_t = self.eta * np.sqrt((1 - alpha_t_prev) / (1 - alpha_t)) * np.sqrt(1 - alpha_t / alpha_t_prev)
            x_t_prev = np.sqrt(alpha_t_prev) * pred_x0 + sigma_t * np.random.randn(*x_t.shape) + np.sqrt(1 - alpha_t_prev - sigma_t**2) * noise_pred
            
        return x_t_prev
    
    def get_alpha(self, t):
        return np.cos((t / self.num_timesteps + 0.008) * np.pi / 2) ** 2

class DDIM:
    def __init__(self, num_steps=50, eta=0.0):
        self.scheduler = DDIMScheduler(num_steps, eta)
        self.model = np.random.randn(512, 512) * 0.1
        
    def sample(self, num_images=1):
        x_t = np.random.randn(num_images, 4, 32, 32)
        
        timesteps = self.scheduler.get_schedule()
        
        for i in range(len(timesteps) - 1):
            noise_pred = x_t @ self.model
            x_t = self.scheduler.step(x_t, noise_pred, timesteps[i], timesteps[i+1])
            
        return x_t

ddim = DDIM(num_steps=50, eta=0.0)

samples = ddim.sample(num_images=1)

print("=" * 60)
print("DDIM (Denoising Diffusion Implicit Models) Demo")
print("=" * 60)
print(f"Number of sampling steps: {ddim.scheduler.num_timesteps}")
print(f"DDIM eta (randomness): {ddim.scheduler.eta}")
print(f"Initial noise shape: (1, 4, 32, 32)")
print(f"Final latent shape: {samples.shape}")
print("\n✓ DDIM enables faster sampling than standard DDPM")
print("  by using a non-Markovian forward process")
print("  eta=0 gives deterministic sampling")
