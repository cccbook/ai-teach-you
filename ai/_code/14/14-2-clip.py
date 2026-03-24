import numpy as np

class CLIPTextEncoder:
    def __init__(self, vocab_size, d_model):
        self.embedding = np.random.randn(vocab_size, d_model) * 0.02
        
    def forward(self, token_ids):
        return self.embedding[token_ids]

class CLIPImageEncoder:
    def __init__(self, img_channels, d_model):
        self.proj = np.random.randn(img_channels, d_model) * 0.02
        
    def forward(self, images):
        batch_size = images.shape[0]
        return images.reshape(batch_size, -1) @ self.proj

class CLIP:
    def __init__(self, vocab_size, d_model, img_channels):
        self.text_encoder = CLIPTextEncoder(vocab_size, d_model)
        self.image_encoder = CLIPImageEncoder(img_channels, d_model)
        self.d_model = d_model
        
        self.text_proj = np.random.randn(d_model, d_model) * 0.02
        self.image_proj = np.random.randn(d_model, d_model) * 0.02
        
    def get_text_features(self, token_ids):
        text_embeds = self.text_encoder.forward(token_ids)
        text_embeds = text_embeds @ self.text_proj
        return text_embeds / np.linalg.norm(text_embeds, axis=-1, keepdims=True)
    
    def get_image_features(self, images):
        image_embeds = self.image_encoder.forward(images)
        image_embeds = image_embeds @ self.image_proj
        return image_embeds / np.linalg.norm(image_embeds, axis=-1, keepdims=True)
    
    def contrastive_loss(self, text_features, image_features):
        logits = text_features @ image_features.T
        labels = np.arange(text_features.shape[0])
        loss = np.mean(np.diag(logits) - np.log(np.sum(np.exp(logits), axis=-1) + 1e-8))
        return loss

vocab_size = 50000
d_model = 512
img_channels = 3 * 224 * 224

clip = CLIP(vocab_size, d_model, img_channels)

batch_size = 4
token_ids = np.random.randint(0, vocab_size, (batch_size, 77))
images = np.random.randn(batch_size, 3, 224, 224)

text_features = clip.get_text_features(token_ids)
image_features = clip.get_image_features(images)

loss = clip.contrastive_loss(text_features, image_features)

print("=" * 60)
print("CLIP (Contrastive Language-Image Pre-training) Demo")
print("=" * 60)
print(f"Vocab size: {vocab_size:,}")
print(f"d_model: {d_model}")
print(f"Image channels: {img_channels:,}")
print(f"Text features shape: {text_features.shape}")
print(f"Image features shape: {image_features.shape}")
print(f"\nContrastive loss: {loss:.4f}")
print("\n✓ CLIP learns to align image and text in shared embedding space,")
print("  enabling zero-shot image classification via text queries")
