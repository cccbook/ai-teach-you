import numpy as np

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

class AutoregressiveModel:
    def __init__(self, vocab_size, d_model):
        self.embedding = np.random.randn(vocab_size, d_model) * 0.1
        self.lm_head = np.random.randn(d_model, vocab_size) * 0.1
        
    def forward(self, token_ids):
        x = self.embedding[token_ids]
        return x @ self.lm_head
    
    def generate(self, seed_ids, max_new_tokens):
        generated = list(seed_ids)
        for _ in range(max_new_tokens):
            logits = self.forward(np.array(generated))
            next_token = np.argmax(logits[-1])
            generated.append(next_token)
        return generated

vocab_size = 100
d_model = 32

model = AutoregressiveModel(vocab_size, d_model)

seed = [1, 2, 3, 4, 5]
generated = model.generate(seed, 10)

print("=" * 60)
print("Autoregressive Generation Demo")
print("=" * 60)
print(f"Vocab size: {vocab_size}")
print(f"d_model: {d_model}")
print(f"Seed token IDs: {seed}")
print(f"Generated token IDs ({len(generated)} total):")
print(f"  {generated}")
print("\n✓ Autoregressive models generate one token at a time")
print("  using previously generated tokens as context")
print("  (used in GPT, LLM generation)")
