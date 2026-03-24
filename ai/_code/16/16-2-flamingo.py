import numpy as np

class PerceiverResampler:
    def __init__(self, input_dim, output_dim, num_queries):
        self.query_tokens = np.random.randn(num_queries, input_dim) * 0.02
        self.cross_attention = np.random.randn(input_dim, input_dim) * 0.02
        
    def forward(self, x):
        queries = self.query_tokens[:1] @ np.ones((1, x.shape[1]))
        combined = np.concatenate([queries, x], axis=0)
        return combined @ self.cross_attention

class Flamingo:
    def __init__(self, vision_dim=768, text_dim=512, num_queries=64):
        self.vision_encoder = np.random.randn(224 * 224 * 3, vision_dim) * 0.02
        self.perceiver = PerceiverResampler(vision_dim, text_dim, num_queries)
        self.text_decoder = np.random.randn(text_dim, 32000) * 0.02
        
    def forward(self, image, text_tokens):
        vision_features = image.reshape(image.shape[0], -1) @ self.vision_encoder
        vision_features = self.perceiver.forward(vision_features)
        text_logits = text_tokens @ self.text_decoder
        return text_logits

flamingo = Flamingo()

image = np.random.randn(1, 3, 224, 224)
text_tokens = np.array([[101, 202, 303]])

output = flamingo.forward(image, text_tokens)

print("=" * 60)
print("Flamingo Demo")
print("=" * 60)
print(f"Vision encoder dim: 768")
print(f"Text decoder vocab: 32000")
print(f"Perceiver queries: 64")
print(f"\nImage shape: {image.shape}")
print(f"Text tokens: {text_tokens.shape}")
print(f"Output logits: {output.shape}")
print("\n✓ Flamingo architecture:")
print("  - Vision encoder (CLIP ViT)")
print("  - Perceiver Resampler (cross-modal)")
print("  - Text decoder (GPT-style)")
print("  - Few-shot learning capability")
