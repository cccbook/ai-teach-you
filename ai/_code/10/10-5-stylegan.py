#!/usr/bin/env python3
"""
Chapter 10-5: StyleGAN
NVIDIA 2018 提出的 Style Transfer + GAN
支援細粒度風格控制和特徵解耦
"""

import numpy as np

class StyleGANGenerator:
    def __init__(self, latent_dim=512):
        self.latent_dim = latent_dim
        
    def mapping_network(self, z):
        return z * 1.2
    
    def adaptive_instance_norm(self, w, style_strength=1.0):
        return w * style_strength
    
    def synthesize(self, w_vectors):
        images = []
        for w in w_vectors:
            base = np.random.randn(256, 256, 3) * 0.1
            stylized = base + w[:256*256*3].reshape(256, 256, 3) * 0.3
            images.append(np.clip(stylized, 0, 1))
        return np.array(images)
    
    def generate(self, z, truncation_psi=0.7):
        w = self.mapping_network(z)
        
        if truncation_psi < 1.0:
            w = 0.7 * w + 0.3 * np.mean(w, axis=0)
        
        for layer in range(18):
            w = self.adaptive_instance_norm(w)
        
        images = self.synthesize([w] * len(z))
        return images

class StyleGANDiscriminator:
    def __init__(self):
        pass
    
    def discriminate(self, images):
        scores = np.random.rand(len(images))
        return scores

def demo():
    print("=" * 60)
    print("Chapter 10-5: StyleGAN")
    print("=" * 60)
    
    print("\n[Concept] StyleGAN 創新:")
    print("  1. Mapping Network: z → w 空間")
    print("  2. AdaIN (Adaptive Instance Normalization)")
    print("  3. 漸進式成長 (Progressive Growing)")
    print("  4. 風格混合 (Style Mixing)")
    print("  5. 截斷技巧 (Truncation Trick)")
    
    print("\n[Architecture Details]")
    print("  Mapping Network: 8層 MLP (512 → 512)")
    print("  Synthesis Network: 18 layers (1024x1024)")
    print("  每層有 AdaIN + Noise input")
    
    print("\n[Generation]")
    gen = StyleGANGenerator(latent_dim=512)
    
    z = np.random.randn(4, 512)
    images = gen.generate(z, truncation_psi=0.7)
    
    print(f"  Input latent z: {z.shape}")
    print(f"  Generated images: {images.shape}")
    print(f"  Value range: [{images.min():.2f}, {images.max():.2f}]")
    
    print("\n[Style Mixing]")
    z1 = np.random.randn(1, 512)
    z2 = np.random.randn(1, 512)
    
    w1 = gen.mapping_network(z1)
    w2 = gen.mapping_network(z2)
    
    print(f"  z1 → w1: {w1.shape}")
    print(f"  z2 → w2: {w2.shape}")
    print("  Style mixing: 交叉不同w向量的中間層")
    
    print("\n[Feature Disentanglement]")
    print("  • Coarse styles (4-7): 姿態、臉型")
    print("  • Middle styles (8-13): 輪廓、特徵")  
    print("  • Fine styles (14-17): 顏色、質地")
    
    print("\n[StyleGAN2/3 Improvements]")
    print("  • 移除 progressive growing")
    print("  • 更好的正則化 (R1, Path Length)")
    print("  • 減少偽影 (blob artifacts)")
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    print("=" * 60)

if __name__ == "__main__":
    demo()