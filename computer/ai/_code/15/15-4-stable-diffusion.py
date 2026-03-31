import numpy as np

class VAEEncoder:
    def __init__(self, in_channels, latent_dim):
        self.conv = np.random.randn(latent_dim, in_channels, 3, 3) * 0.1
        
    def forward(self, x):
        return x @ self.conv.flatten()[:16].reshape(4, 4)

class StableDiffusion:
    def __init__(self, latent_dim=4, hidden_dim=512):
        self.vae_enc = VAEEncoder(3, latent_dim)
        self.vae_dec = np.random.randn(latent_dim * 32 * 32, hidden_dim) * 0.1
        
        self.text_encoder = np.random.randn(77, hidden_dim) * 0.1
        self.unet = np.random.randn(hidden_dim, hidden_dim) * 0.1
        self.scheduler_steps = 50
        
    def text_to_image(self, prompt_embedding):
        latents = np.random.randn(1, 4, 32, 32)
        
        for step in range(self.scheduler_steps):
            noise_pred = latents @ self.unet
            latents = latents - 0.01 * noise_pred
        
        image = latents.reshape(1, -1) @ self.vae_dec
        return image.reshape(1, 3, 64, 64)

prompt = "a photo of an astronaut riding a horse"
prompt_tokens = np.array([len(prompt.split())])

sd = StableDiffusion()

result = sd.text_to_image(prompt_tokens)

print("=" * 60)
print("Stable Diffusion Demo")
print("=" * 60)
print(f"Prompt: '{prompt}'")
print(f"Latent dimension: 4 x 32 x 32")
print(f"UNet hidden dimension: 512")
print(f"Sampling steps: {sd.scheduler_steps}")
print(f"\nGenerated image shape: {result.shape}")
print("\n✓ Stable Diffusion uses:")
print("  - VAE for latent space encoding")
print("  - CLIP text encoder for conditioning")
print("  - U-Net for noise prediction")
print("  - Cross-attention for text-image alignment")
