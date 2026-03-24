import numpy as np

class ImageEncoder:
    def __init__(self, img_size, d_model):
        self.proj = np.random.randn(img_size * img_size * 3, d_model) * 0.02
        
    def forward(self, images):
        x = images.reshape(images.shape[0], -1)
        return x @ self.proj

class CaptionDecoder:
    def __init__(self, vocab_size, d_model):
        self.embedding = np.random.randn(vocab_size, d_model) * 0.02
        self.lm_head = np.random.randn(d_model, vocab_size) * 0.02
        
    def forward(self, image_features, token_ids):
        x = self.embedding[token_ids]
        x = x + image_features
        return x @ self.lm_head

class ImageCaptioningModel:
    def __init__(self, vocab_size, img_size, d_model):
        self.encoder = ImageEncoder(img_size, d_model)
        self.decoder = CaptionDecoder(vocab_size, d_model)
        
    def forward(self, images, token_ids):
        image_features = self.encoder.forward(images)
        logits = self.decoder.forward(image_features, token_ids)
        return logits

vocab_size = 50000
img_size = 224
d_model = 512

model = ImageCaptioningModel(vocab_size, img_size, d_model)

batch_size = 2
images = np.random.randn(batch_size, 3, img_size, img_size)
token_ids = np.array([[101, 202, 303, 404, 105]])

logits = model.forward(images, token_ids)

print("=" * 60)
print("Image Captioning Demo")
print("=" * 60)
print(f"Vocab size: {vocab_size:,}")
print(f"Image size: {img_size}x{img_size}")
print(f"d_model: {d_model}")
print(f"Input image shape: {images.shape}")
print(f"Input token IDs shape: {token_ids.shape}")
print(f"Output logits shape: {logits.shape}")
print("\n✓ Image captioning models (like BLIP, CLIP):")
print("  - Encode images to feature representations")
print("  - Generate descriptive text captions")
print("  - Enable multimodal understanding")
