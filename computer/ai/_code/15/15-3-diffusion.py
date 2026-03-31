import numpy as np

class UNet:
    def __init__(self, channels):
        self.down_blocks = []
        self.up_blocks = []
        
        for i in range(len(channels) - 1):
            self.down_blocks.append({
                'conv': np.random.randn(channels[i+1], channels[i], 3, 3) * 0.1,
                'downsample': np.random.randn(channels[i+1], channels[i+1], 2, 2) * 0.1
            })
        
        for i in range(len(channels) - 1, 0, -1):
            self.up_blocks.append({
                'conv': np.random.randn(channels[i-1], channels[i], 3, 3) * 0.1,
                'upsample': np.random.randn(channels[i-1], channels[i-1], 2, 2) * 0.1
            })

class DiffusionScheduler:
    def __init__(self, num_timesteps=1000):
        self.num_timesteps = num_timesteps
        
    def get_alpha_bar(self, t):
        return np.cos((t / self.num_timesteps + 0.008) * np.pi / 2) ** 2
    
    def add_noise(self, x_start, noise, t):
        alpha_bar = self.get_alpha_bar(t)
        sqrt_alpha_bar = np.sqrt(alpha_bar)
        sqrt_one_minus_alpha_bar = np.sqrt(1 - alpha_bar)
        return sqrt_alpha_bar * x_start + sqrt_one_minus_alpha_bar * noise

class DiffusionModel:
    def __init__(self, in_channels, hidden_dims):
        self.unet = UNet([in_channels] + hidden_dims)
        self.scheduler = DiffusionScheduler()
        
    def forward(self, x, t):
        return self.unet.down_blocks[0]['conv'][:1, :1] @ x.flatten()

in_channels = 3
hidden_dims = [64, 128, 256]

diffusion = DiffusionModel(in_channels, hidden_dims)

x = np.random.randn(1, in_channels, 32, 32)
t = np.array([100])

output = diffusion.forward(x, t)

print("=" * 60)
print("Diffusion Model Demo")
print("=" * 60)
print(f"Input channels: {in_channels}")
print(f"UNet hidden dimensions: {hidden_dims}")
print(f"Number of timesteps: {diffusion.scheduler.num_timesteps}")
print(f"Input shape: {x.shape}")
print(f"timestep: {t[0]}")

x_noisy = diffusion.scheduler.add_noise(x, np.random.randn(*x.shape), t)
print(f"Noised image shape: {x_noisy.shape}")
print("\n✓ Diffusion models learn to reverse the noising process")
print("  to generate images from random noise")
