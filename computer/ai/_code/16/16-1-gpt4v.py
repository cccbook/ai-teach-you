import numpy as np

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

class GPT4V:
    def __init__(self, image_channels=3, text_dim=512, vision_dim=768):
        self.image_encoder = np.random.randn(image_channels * 224 * 224, vision_dim) * 0.02
        self.text_encoder = np.random.randn(10000, text_dim) * 0.02
        self.fusion = np.random.randn(vision_dim + text_dim, 512) * 0.02
        self.lm_head = np.random.randn(512, 10000) * 0.02
        
    def encode_image(self, image):
        return image.reshape(image.shape[0], -1) @ self.image_encoder
    
    def encode_text(self, text_tokens):
        return self.text_encoder[text_tokens]
    
    def forward(self, image, text_tokens):
        img_emb = self.encode_image(image)
        text_emb = self.encode_text(text_tokens)
        combined = np.concatenate([img_emb, text_emb], axis=-1)
        fused = combined @ self.fusion
        logits = fused @ self.lm_head
        return logits

model = GPT4V()

batch_size = 1
image = np.random.randn(batch_size, 3, 224, 224)
text_tokens = np.array([[101, 202, 303, 404, 105]])

logits = model.forward(image, text_tokens)

print("=" * 60)
print("GPT-4V (Vision) Demo")
print("=" * 60)
print(f"Image shape: {image.shape}")
print(f"Text tokens: {text_tokens.shape}")
print(f"Output logits: {logits.shape}")
print("\n✓ GPT-4V processes both images and text:")
print("  - Visual understanding & reasoning")
print("  - Image description & captioning")
print("  - Multi-modal conversation")
print("  - Charts & document understanding")
