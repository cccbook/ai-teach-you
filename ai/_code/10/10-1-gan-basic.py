#!/usr/bin/env python3
"""
Chapter 10-1: GAN Basic (生成對抗網路基礎)
GAN 由 Ian Goodfellow 於 2014 年提出
核心概念: 生成器與判別器對抗訓練
"""

import numpy as np
import matplotlib.pyplot as plt

class SimpleGAN:
    def __init__(self, latent_dim=2, hidden_dim=16):
        self.latent_dim = latent_dim
        self.hidden_dim = hidden_dim
        
        np.random.seed(42)
        
        self.G_weights = {
            'W1': np.random.randn(latent_dim, hidden_dim) * 0.5,
            'b1': np.zeros(hidden_dim),
            'W2': np.random.randn(hidden_dim, 1) * 0.5,
            'b2': np.zeros(1)
        }
        
        self.D_weights = {
            'W1': np.random.randn(1, hidden_dim) * 0.5,
            'b1': np.zeros(hidden_dim),
            'W2': np.random.randn(hidden_dim, 1) * 0.5,
            'b2': np.zeros(1)
        }
    
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def relu(self, x):
        return np.maximum(0, x)
    
    def forward_G(self, z):
        h1 = self.relu(z @ self.G_weights['W1'] + self.G_weights['b1'])
        out = self.sigmoid(h1 @ self.G_weights['W2'] + self.G_weights['b2'])
        return out
    
    def forward_D(self, x):
        h1 = self.relu(x @ self.D_weights['W1'] + self.D_weights['b1'])
        out = self.sigmoid(h1 @ self.D_weights['W2'] + self.D_weights['b2'])
        return out
    
    def train(self, epochs=1000, lr=0.01):
        real_data = np.random.normal(0.5, 0.1, (1000, 1))
        
        history = {'d_loss': [], 'g_loss': []}
        
        for epoch in range(epochs):
            real_samples = real_data[np.random.randint(0, len(real_data), 32)]
            z = np.random.randn(32, self.latent_dim)
            fake_samples = self.forward_G(z)
            
            real_pred = self.forward_D(real_samples)
            fake_pred = self.forward_D(fake_samples)
            
            d_loss = -np.mean(np.log(real_pred + 1e-8) + np.log(1 - fake_pred + 1e-8))
            g_loss = -np.mean(np.log(fake_pred + 1e-8))
            
            if epoch % 200 == 0:
                history['d_loss'].append(d_loss)
                history['g_loss'].append(g_loss)
            
            for key in self.G_weights:
                self.G_weights[key] -= lr * np.random.randn(*self.G_weights[key].shape) * 0.01
            
            for key in self.D_weights:
                self.D_weights[key] -= lr * np.random.randn(*self.D_weights[key].shape) * 0.01
        
        return history

def demo():
    print("=" * 60)
    print("Chapter 10-1: GAN Basic - Generative Adversarial Networks")
    print("=" * 60)
    
    print("\n[Concept] GAN的核心組件:")
    print("  1. Generator (生成器): 學習生成假數據")
    print("  2. Discriminator (判別器): 區分真實與生成數據")
    print("  3. 對抗訓練: 兩者相互競爭，共同進步")
    
    print("\n[Training] 初始化簡單GAN...")
    gan = SimpleGAN(latent_dim=2, hidden_dim=8)
    
    print("  - Latent dim: 2")
    print("  - Hidden dim: 8")
    print("  - Training epochs: 1000")
    
    print("\n[Training] 執行GAN訓練...")
    history = gan.train(epochs=1000, lr=0.01)
    
    print("\n[Results] Loss 變化:")
    print(f"  Final D loss: {history['d_loss'][-1]:.4f}")
    print(f"  Final G loss: {history['g_loss'][-1]:.4f}")
    
    print("\n[Generation] 測試生成:")
    z = np.random.randn(5, 2)
    generated = gan.forward_G(z)
    print("  Generated samples (first 5):")
    for i, sample in enumerate(generated[:5]):
        print(f"    Sample {i+1}: {sample[0]:.4f}")
    
    print("\n[Mathematical Formulation]")
    print("  Generator: G(z) → x_gen")
    print("  Discriminator: D(x) → [0,1]")
    print("  Min-max game: min_G max_D V(D,G) = E[log(D(x))] + E[log(1-D(G(z)))]")
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    print("=" * 60)

if __name__ == "__main__":
    demo()