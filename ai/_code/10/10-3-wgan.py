#!/usr/bin/env python3
"""
Chapter 10-3: WGAN (Wasserstein GAN)
WGAN 使用 Wasserstein 距離解決模式崩潰和訓練不穩定問題
"""

import numpy as np

class WGAN:
    def __init__(self, latent_dim=100):
        self.latent_dim = latent_dim
        self.clip_value = 0.01
        
    def wasserstein_distance(self, real_samples, fake_samples):
        sorted_real = np.sort(real_samples)
        sorted_fake = np.sort(fake_samples)
        
        wd = np.mean(np.abs(sorted_real - sorted_fake))
        return wd
    
    def generator_loss(self, fake_scores):
        return -np.mean(fake_scores)
    
    def discriminator_loss(self, real_scores, fake_scores):
        return np.mean(fake_scores) - np.mean(real_scores)
    
    def clip_weights(self, weights):
        clipped = {}
        for k, v in weights.items():
            clipped[k] = np.clip(v, -self.clip_value, self.clip_value)
        return clipped
    
    def train_step(self, real_images, fake_images, n_critic=5):
        real_scores = np.random.rand(len(real_images)) * 2 - 1
        fake_scores = np.random.rand(len(fake_images)) * 2 - 1
        
        d_loss = self.discriminator_loss(real_scores, fake_scores)
        g_loss = self.generator_loss(fake_scores)
        
        wd = self.wasserstein_distance(real_images, fake_images)
        
        return d_loss, g_loss, wd

def demo():
    print("=" * 60)
    print("Chapter 10-3: WGAN - Wasserstein GAN")
    print("=" * 60)
    
    print("\n[Concept] WGAN 的改進:")
    print("  1. 使用 Earth Mover (Wasserstein) 距離")
    print("  2. 判別器不使用 Sigmoid (critic 而非 discriminator)")
    print("  3. 權重裁剪確保 Lipschitz 約束")
    print("  4. 訓練更穩定，收斂更快")
    
    print("\n[Mathematical Formulation]")
    print("  W(Pr, Pg) = inf_γ∈Π(Pr, Pg) E_{(x,y)∼γ}[||x-y||]")
    print("  這是兩分佈之間的最小transportation cost")
    
    print("\n[Training]")
    wgan = WGAN(latent_dim=100)
    
    real_images = np.random.randn(32, 28, 28, 1)
    fake_images = np.random.randn(32, 28, 28, 1)
    
    d_loss, g_loss, wd = wgan.train_step(real_images, fake_images)
    
    print(f"  Discriminator loss: {d_loss:.4f}")
    print(f"  Generator loss: {g_loss:.4f}")
    print(f"  Wasserstein distance: {wd:.4f}")
    
    print("\n[WGAN-GP (Improved)]")
    print("  Gradient Penalty 取代權重裁剪:")
    print("  L = D(G(z)) - D(x) + λ(||∇_x D(x)||_2 - 1)²")
    
    print("\n[Comparison: GAN vs WGAN]")
    print("  ┌────────────┬────────────┬────────────┐")
    print("  │   Aspect   │    GAN     │    WGAN    │")
    print("  ├────────────┼────────────┼────────────┤")
    print("  │ Loss       │ JS Div     │ Wasserstein│")
    print("  │ Stability  │ Unstable   │ More stable│")
    print("  │ Mode Coll. │ Common     │ Less common│")
    print("  │ Gradient   │ Vanishing  │ Meaningful │")
    print("  └────────────┴────────────┴────────────┘")
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    print("=" * 60)

if __name__ == "__main__":
    demo()