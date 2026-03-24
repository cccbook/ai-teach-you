import numpy as np

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

def self_attention(x, d_k=64):
    seq_len = x.shape[0]
    Q = x @ np.random.randn(d_k, d_k).T
    K = x @ np.random.randn(d_k, d_k).T
    V = x @ np.random.randn(d_k, d_k).T
    
    scores = Q @ K.T / np.sqrt(d_k)
    weights = softmax(scores)
    return weights @ V

seq_len = 4
d_model = 8

np.random.seed(42)
x = np.random.randn(seq_len, d_model)

output = self_attention(x, d_model)

print("=" * 60)
print("Self-Attention Demo")
print("=" * 60)
print(f"Input shape: {x.shape}")
print(f"Output shape: {output.shape}")
print("\nInput sequence:")
print(x)
print("\nSelf-attention output:")
print(output)
print("\n✓ Self-attention allows each position to attend to all")
print("  positions in the previous layer")
