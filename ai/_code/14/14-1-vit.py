import numpy as np

class PatchEmbedding:
    def __init__(self, img_size=224, patch_size=16, in_channels=3, d_model=768):
        self.img_size = img_size
        self.patch_size = patch_size
        self.num_patches = (img_size // patch_size) ** 2
        self.d_model = d_model
        
        self.proj = np.random.randn(self.num_patches, in_channels * patch_size ** 2, d_model) * 0.02
        
    def forward(self, x):
        batch_size = x.shape[0]
        x = x.reshape(batch_size, self.num_patches, -1)
        return x @ self.proj

class ViT:
    def __init__(self, img_size=224, patch_size=16, in_channels=3, d_model=768, num_heads=12, num_layers=12):
        self.patch_embed = PatchEmbedding(img_size, patch_size, in_channels, d_model)
        self.num_patches = self.patch_embed.num_patches
        
        self.cls_token = np.random.randn(1, 1, d_model) * 0.02
        self.pos_embed = np.random.randn(1, self.num_patches + 1, d_model) * 0.02
        
        self.transformer_blocks = num_layers
        
    def forward(self, x):
        batch_size = x.shape[0]
        
        x = self.patch_embed.forward(x)
        
        cls_tokens = np.tile(self.cls_token, (batch_size, 1, 1))
        x = np.concatenate([cls_tokens, x], axis=1)
        
        x = x + self.pos_embed
        
        return x

img_size = 224
patch_size = 16
in_channels = 3
d_model = 768
num_layers = 12

vit = ViT(img_size, patch_size, in_channels, d_model, num_layers=num_layers)

batch_size = 2
x = np.random.randn(batch_size, in_channels, img_size, img_size)

output = vit.forward(x)

print("=" * 60)
print("ViT (Vision Transformer) Demo")
print("=" * 60)
print(f"Image size: {img_size}x{img_size}")
print(f"Patch size: {patch_size}x{patch_size}")
print(f"Number of patches: {vit.num_patches}")
print(f"d_model: {d_model}")
print(f"Input shape: {x.shape}")
print(f"Output shape: {output.shape}")
print("\n✓ ViT treats images as sequences of patches,")
print("  applying transformer architecture to vision tasks")
