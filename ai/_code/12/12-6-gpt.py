import numpy as np

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

vocab_size = 100
d_model = 16
seq_len = 5

embedding = np.random.randn(vocab_size, d_model) * 0.1
W_Q = np.random.randn(d_model, d_model) * 0.1
W_K = np.random.randn(d_model, d_model) * 0.1
W_V = np.random.randn(d_model, d_model) * 0.1
W_O = np.random.randn(d_model, d_model) * 0.1

token_ids = [45, 23, 78, 12, 56]
x = embedding[token_ids]

def self_attention(x, mask=None):
    Q = x @ W_Q
    K = x @ W_K
    V = x @ W_V
    scores = Q @ K.T / np.sqrt(d_model)
    if mask is not None:
        scores = scores + np.where(mask, -1e9, 0)
    weights = softmax(scores)
    return weights @ V

def causal_mask(seq_len):
    mask = np.ones((seq_len, seq_len))
    return np.tril(mask)

mask = causal_mask(seq_len)
output = self_attention(x, mask)
output = output @ W_O

print("=" * 60)
print("GPT-style Decoder Demo")
print("=" * 60)
print(f"Vocab size: {vocab_size}")
print(f"d_model: {d_model}")
print(f"Sequence length: {seq_len}")
print(f"Output shape: {output.shape}")
print("\nToken embeddings shape:", x.shape)
print("Causal mask (prevents attending to future):")
print(mask.astype(int))
print("\n✓ GPT uses causal (unidirectional) self-attention")
print("  where each position can only attend to previous positions")
