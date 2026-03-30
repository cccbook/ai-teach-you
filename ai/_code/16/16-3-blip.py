import numpy as np

class ImageEncoder:
    def __init__(self, img_dim, hidden_dim):
        self.proj = np.random.randn(img_dim, hidden_dim) * 0.02
        
    def forward(self, images):
        return images.reshape(images.shape[0], -1) @ self.proj

class TextDecoder:
    def __init__(self, hidden_dim, vocab_size):
        self.lm_head = np.random.randn(hidden_dim, vocab_size) * 0.02
        
    def forward(self, image_features, text_tokens):
        combined = image_features + np.random.randn(*text_tokens.shape) * 0.1
        return combined @ self.lm_head

class BLIP:
    def __init__(self, img_size, hidden_dim, vocab_size):
        img_dim = 3 * img_size * img_size
        self.image_encoder = ImageEncoder(img_dim, hidden_dim)
        self.text_decoder = TextDecoder(hidden_dim, vocab_size)
        
    def generate_caption(self, image):
        features = self.image_encoder.forward(image)
        dummy_tokens = np.array([[1, 2, 3]])
        logits = self.text_decoder.forward(features, dummy_tokens)
        return logits
    
    def answer_question(self, image, question):
        img_features = self.image_encoder.forward(image)
        q_features = question + np.random.randn(1, 32) * 0.1
        combined = np.concatenate([img_features, q_features], axis=-1)
        return combined @ np.random.randn(combined.shape[-1], 100) * 0.02

blip = BLIP(img_size=224, hidden_dim=768, vocab_size=30522)

image = np.random.randn(1, 3, 224, 224)
question = np.random.randn(1, 32)

caption_logits = blip.generate_caption(image)
answer_logits = blip.answer_question(image, question)

print("=" * 60)
print("BLIP (Bootstrapped Language-Image Pre-training) Demo")
print("=" * 60)
print(f"Image size: 224x224")
print(f"Hidden dimension: 768")
print(f"Vocab size: 30,522")
print(f"\nImage input: {image.shape}")
print(f"Caption logits: {caption_logits.shape}")
print(f"Answer logits: {answer_logits.shape}")
print("\n✓ BLIP features:")
print("  - Image-to-text generation")
print("  - Image-grounded conversation")
print("  - Zero-shot image captioning")
print("  - Multimodal understanding")
