import numpy as np

class SDXL:
    def __init__(self):
        self.text_encoder = np.random.randn(77, 2048) * 0.1
        self.text_encoder_2 = np.random.randn(77, 1024) * 0.1
        
        self.unet_main = np.random.randn(2048, 2048) * 0.1
        self.unet_refiner = np.random.randn(2048, 2048) * 0.1
        
        self.vae = np.random.randn(3 * 64 * 64, 4 * 32 * 32) * 0.1
        
    def generate(self, prompt, num_steps=30):
        text_embeds = self.text_encoder[:len(prompt.split())] @ np.eye(2048)[:len(prompt.split())]
        
        latents = np.random.randn(1, 4, 128, 128)
        
        for step in range(num_steps):
            latents = latents @ self.unet_main
            
        refined = latents @ self.unet_refiner
        
        image = refined @ self.vae
        return image.reshape(1, 3, 256, 256)

prompt = "a majestic castle at sunset"
sdxl = SDXL()

image = sdxl.generate(prompt)

print("=" * 60)
print("SDXL (Stable Diffusion XL) Demo")
print("=" * 60)
print(f"Prompt: '{prompt}'")
print(f"Text encoder dimensions: 2048, 1024")
print(f"UNet main: 2048 dim")
print(f"UNet refiner: 2048 dim")
print(f"VAE latent: 4x128x128 -> image: 3x256x256")
print(f"Number of steps: 30")
print(f"\nGenerated image shape: {image.shape}")
print("\n✓ SDXL improvements over SD:")
print("  - Larger text encoders (OpenCLIP + BERT)")
print("  - Larger resolution (1024x1024)")
print("  - Refiner module for quality")
print("  - Better prompt following")
