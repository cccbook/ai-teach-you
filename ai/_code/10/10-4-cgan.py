#!/usr/bin/env python3
"""
Chapter 10-4: CGAN (Conditional GAN)
條件生成對抗網路 - 透過標籤控制生成結果
"""

import numpy as np

class ConditionalGenerator:
    def __init__(self, latent_dim=100, num_classes=10):
        self.latent_dim = latent_dim
        self.num_classes = num_classes
        
    def generate(self, n_samples, labels):
        one_hot = np.zeros((n_samples, self.num_classes))
        one_hot[np.arange(n_samples), labels] = 1
        
        noise = np.random.randn(n_samples, self.latent_dim)
        combined = np.concatenate([noise, one_hot], axis=1)
        
        return combined * 0.5 + 0.5

class ConditionalDiscriminator:
    def __init__(self, num_classes=10):
        self.num_classes = num_classes
        
    def discriminate(self, images, labels):
        one_hot = np.zeros((len(labels), self.num_classes))
        one_hot[np.arange(len(labels)), labels] = 1
        
        scores = np.random.rand(len(images))
        return scores

class CGAN:
    def __init__(self, latent_dim=100, num_classes=10):
        self.latent_dim = latent_dim
        self.num_classes = num_classes
        self.generator = ConditionalGenerator(latent_dim, num_classes)
        self.discriminator = ConditionalDiscriminator(num_classes)
        
    def train_step(self, real_images, labels):
        batch_size = len(real_images)
        
        fake_images = self.generator.generate(batch_size, labels)
        
        real_scores = self.discriminator.discriminate(real_images, labels)
        fake_scores = self.discriminator.discriminate(fake_images, labels)
        
        d_loss = -np.mean(np.log(real_scores + 1e-8) + np.log(1 - fake_scores + 1e-8))
        g_loss = -np.mean(np.log(fake_scores + 1e-8))
        
        return d_loss, g_loss

def demo():
    print("=" * 60)
    print("Chapter 10-4: CGAN - Conditional GAN")
    print("=" * 60)
    
    print("\n[Concept] Conditional GAN:")
    print("  透過額外的標籤資訊(條件)來控制生成過程")
    print("  P(x|y) - 在給定條件y下生成x")
    
    print("\n[Architecture]")
    print("  Generator: G(z, y) → x")
    print("  Discriminator: D(x, y) → [0,1]")
    
    print("\n[Training]")
    cgan = CGAN(latent_dim=100, num_classes=10)
    
    labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(f"  Available classes: {labels}")
    
    fake_samples = cgan.generator.generate(10, labels)
    print(f"  Generated samples shape: {fake_samples.shape}")
    
    real_images = np.random.randn(10, 28, 28, 1)
    d_loss, g_loss = cgan.train_step(real_images, labels)
    
    print(f"  D loss: {d_loss:.4f}")
    print(f"  G loss: {g_loss:.4f}")
    
    print("\n[Example: Generate specific digits]")
    test_labels = [5, 3, 8, 2, 7]
    for label in test_labels:
        sample = cgan.generator.generate(1, [label])
        print(f"  Label {label}: mean={sample.mean():.4f}, std={sample.std():.4f}")
    
    print("\n[Applications]")
    print("  • MNIST: 指定數字生成")
    print("  • Face Generation: 指定性別/年齡")
    print("  • Image-to-Image: 指定風格轉換")
    print("  • Text-to-Image: 指定描述生成")
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    print("=" * 60)

if __name__ == "__main__":
    demo()