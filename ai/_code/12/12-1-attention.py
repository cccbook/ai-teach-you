import numpy as np

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

def attention_score(query, key):
    return np.dot(query, key.T) / np.sqrt(key.shape[-1])

def attention(query, key, value):
    scores = attention_score(query, key)
    weights = softmax(scores)
    return np.dot(weights, value)

d_k = 64
d_v = 64
seq_len = 5

np.random.seed(42)
Q = np.random.randn(seq_len, d_k)
K = np.random.randn(seq_len, d_k)
V = np.random.randn(seq_len, d_v)

output = attention(Q, K, V)

print("=" * 60)
print("Attention Mechanism Demo")
print("=" * 60)
print(f"Query shape: {Q.shape}")
print(f"Key shape: {K.shape}")
print(f"Value shape: {V.shape}")
print(f"Output shape: {output.shape}")
print("\nSample attention scores (first query):")
scores = attention_score(Q, K)
print(scores[0])
print("\nAttention weights (first query):")
weights = softmax(scores)
print(weights[0])
print("\nOutput (first token):")
print(output[0][:5], "...")
print("\n✓ Attention mechanism computes weighted sum of values")
print("  based on query-key compatibility")
