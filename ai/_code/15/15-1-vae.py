import numpy as np

class Encoder:
    def __init__(self, input_dim, latent_dim):
        self.mu = np.random.randn(input_dim, latent_dim) * 0.1
        self.logvar = np.random.randn(input_dim, latent_dim) * 0.1
        
    def forward(self, x):
        mean = x @ self.mu
        logvar = x @ self.logvar
        std = np.exp(0.5 * logvar)
        eps = np.random.randn(*std.shape)
        z = mean + eps * std
        return z, mean, logvar

class Decoder:
    def __init__(self, latent_dim, output_dim):
        self.W = np.random.randn(latent_dim, output_dim) * 0.1
        
    def forward(self, z):
        return z @ self.W

class VAE:
    def __init__(self, input_dim, latent_dim):
        self.encoder = Encoder(input_dim, latent_dim)
        self.decoder = Decoder(latent_dim, input_dim)
        
    def forward(self, x):
        z, mean, logvar = self.encoder.forward(x)
        recon = self.decoder.forward(z)
        return recon, z, mean, logvar
    
    def reconstruction_loss(self, x, recon):
        return np.mean((x - recon) ** 2)
    
    def kl_loss(self, mean, logvar):
        return -0.5 * np.mean(1 + logvar - mean ** 2 - np.exp(logvar))

input_dim = 784
latent_dim = 16

vae = VAE(input_dim, latent_dim)

x = np.random.randn(4, input_dim)
recon, z, mean, logvar = vae.forward(x)

recon_loss = vae.reconstruction_loss(x, recon)
kl = vae.kl_loss(mean, logvar)

print("=" * 60)
print("VAE (Variational Autoencoder) Demo")
print("=" * 60)
print(f"Input dimension: {input_dim}")
print(f"Latent dimension: {latent_dim}")
print(f"Input shape: {x.shape}")
print(f"Latent representation shape: {z.shape}")
print(f"Reconstructed shape: {recon.shape}")
print(f"\nReconstruction loss: {recon_loss:.4f}")
print(f"KL divergence: {kl:.4f}")
print("\n✓ VAE learns a structured latent space for generation")
print("  by combining encoder, reparameterization, and decoder")
