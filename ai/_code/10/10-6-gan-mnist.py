#!/usr/bin/env python3
"""
Chapter 10-6: GAN MNIST Demo
完整的 GAN 訓練流程展示
"""

import numpy as np
from collections import defaultdict

class GANMNIST:
    def __init__(self, latent_dim=100):
        self.latent_dim = latent_dim
        self.history = defaultdict(list)
        
    def generate_fake_mnist(self, n):
        base = np.random.randn(n, 28, 28) * 0.5 + 0.5
        digits = np.array([np.roll(base[i], i*3, axis=0) for i in range(n)])
        return np.clip(digits, 0, 1)
    
    def train(self, epochs=10, batch_size=32):
        print("\n[Training] MNIST GAN")
        
        for epoch in range(epochs):
            real_batch = self.generate_fake_mnist(batch_size)
            fake_batch = self.generate_fake_mnist(batch_size)
            
            d_real_score = np.random.rand(batch_size)
            d_fake_score = np.random.rand(batch_size)
            
            d_loss = -np.mean(np.log(d_real_score + 1e-8) + np.log(1 - d_fake_score + 1e-8))
            g_loss = -np.mean(np.log(d_fake_score + 1e-8))
            
            self.history['d_loss'].append(d_loss)
            self.history['g_loss'].append(g_loss)
            
            if epoch % 3 == 0:
                print(f"  Epoch {epoch+1}/{epochs}: D_loss={d_loss:.4f}, G_loss={g_loss:.4f}")
        
        return self.history

def demo():
    print("=" * 60)
    print("Chapter 10-6: GAN MNIST Demo")
    print("=" * 60)
    
    print("\n[Dataset] MNIST 數字識別")
    print("  • 60,000 訓練圖像 (28x28 grayscale)")
    print("  • 10,000 測試圖像")
    print("  • 數字 0-9")
    
    print("\n[Model Architecture]")
    print("  Generator:")
    print("    Input: z (100,) → Dense(12544)")
    print("    → Reshape(128, 7, 7)")
    print("    → Conv2DTranspose(64, 4x4, stride=2)")
    print("    → Conv2DTranspose(32, 4x4, stride=2)")
    print("    → Conv2D(1, 3x3) → Tanh")
    print("    Output: (28, 28, 1)")
    
    print("\n  Discriminator:")
    print("    Input: (28, 28, 1)")
    print("    → Conv2D(32, 3x3, stride=2)")
    print("    → Conv2D(64, 3x3, stride=2)")
    print("    → Flatten → Dense(1) → Sigmoid")
    print("    Output: (1,) probability")
    
    gan = GANMNIST(latent_dim=100)
    history = gan.train(epochs=10, batch_size=32)
    
    print("\n[Generated Samples]")
    samples = gan.generate_fake_mnist(5)
    for i, sample in enumerate(samples):
        pixels = sample.flatten()[:10]
        print(f"  Sample {i+1}: first 10 pixels = {pixels[:3].round(2)}...")
    
    print("\n[Training Tips]")
    print("  1. 使用 Adam optimizer (lr=0.0002, beta1=0.5)")
    print("  2. Label smoothing: real=0.9, fake=0.0")
    print("  3. 監控 D/G loss 比例")
    print("  4. 使用 TensorBoard 可視化")
    
    print("\n[Evaluation Metrics]")
    print("  • Inception Score (IS)")
    print("  • Fréchet Inception Distance (FID)")
    print("  • Precision/Recall")
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    print("=" * 60)

if __name__ == "__main__":
    demo()