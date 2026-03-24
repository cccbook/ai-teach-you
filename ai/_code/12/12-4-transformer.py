import numpy as np

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

class FeedForward:
    def __init__(self, d_model, d_ff):
        self.W1 = np.random.randn(d_model, d_ff) * 0.1
        self.W2 = np.random.randn(d_ff, d_model) * 0.1
        
    def forward(self, x):
        return (np.maximum(0, x @ self.W1) @ self.W2)

class TransformerBlock:
    def __init__(self, d_model, num_heads, d_ff):
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        self.ff = FeedForward(d_model, d_ff)
        
    def self_attention(self, x):
        Q = x @ np.random.randn(self.d_model, self.d_model) * 0.1
        K = x @ np.random.randn(self.d_model, self.d_model) * 0.1
        V = x @ np.random.randn(self.d_model, self.d_model) * 0.1
        
        scores = Q @ K.T / np.sqrt(self.d_k)
        weights = softmax(scores)
        return weights @ V
    
    def forward(self, x):
        attn = self.self_attention(x)
        x = x + attn
        ff_out = self.ff.forward(x)
        return x + ff_out

d_model = 8
num_heads = 2
d_ff = 16
seq_len = 4

transformer = TransformerBlock(d_model, num_heads, d_ff)
x = np.random.randn(seq_len, d_model)

output = transformer.forward(x)

print("=" * 60)
print("Transformer Block Demo")
print("=" * 60)
print(f"d_model: {d_model}, num_heads: {num_heads}, d_ff: {d_ff}")
print(f"Input shape: {x.shape}")
print(f"Output shape: {output.shape}")
print("\n✓ Transformer block combines self-attention with")
print("  position-wise feed-forward network")
