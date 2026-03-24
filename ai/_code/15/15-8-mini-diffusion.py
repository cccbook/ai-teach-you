import numpy as np

class SimpleDiffusion:
    def __init__(self, latent_shape=(4, 8, 8)):
        self.latent_shape = latent_shape
        self.num_steps = 20
        
    def forward_process(self, x0, t):
        noise = np.random.randn(*x0.shape)
        alpha = np.cos((t + 1) / (self.num_steps + 1) * np.pi / 2) ** 2
        return np.sqrt(alpha) * x0 + np.sqrt(1 - alpha) * noise
    
    def reverse_process(self, xT, num_steps=None):
        if num_steps is None:
            num_steps = self.num_steps
        x = xT
        for step in range(num_steps):
            t = num_steps - step - 1
            noise_pred = np.random.randn(*x.shape) * 0.1
            alpha = np.cos((t + 1) / (num_steps + 1) * np.pi / 2) ** 2
            x = (x - np.sqrt(1 - alpha) * noise_pred) / np.sqrt(alpha)
        return x
    
    def generate(self, batch_size=1):
        xT = np.random.randn(batch_size, *self.latent_shape)
        return self.reverse_process(xT)

diffusion = SimpleDiffusion(latent_shape=(4, 8, 8))

x0 = np.random.randn(1, 4, 8, 8)
noised = diffusion.forward_process(x0, t=10)
generated = diffusion.generate(batch_size=1)

print("=" * 60)
print("Mini Diffusion Demo")
print("=" * 60)
print(f"Latent shape: {diffusion.latent_shape}")
print(f"Number of steps: {diffusion.num_steps}")
print(f"\nOriginal: {x0.shape}")
print(f"Forward (t=10): {noised.shape}")
print(f"Generated: {generated.shape}")
print("\n✓ Diffusion model process:")
print("  1. Forward: Add noise to data gradually")
print("  2. Reverse: Learn to denoise (generate)")
