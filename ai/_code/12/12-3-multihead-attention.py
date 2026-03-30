import numpy as np

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

class MultiHeadAttention:
    def __init__(self, d_model, num_heads):
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
    def split_heads(self, x):
        x = x.reshape(x.shape[0], self.num_heads, self.d_k)
        return np.transpose(x, (1, 0, 2))
    
    def attention(self, Q, K, V):
        scores = np.matmul(Q, np.transpose(K, (0, 2, 1))) / np.sqrt(self.d_k)
        weights = softmax(scores)
        return np.matmul(weights, V)
    
    def forward(self, Q, K, V):
        Q = self.split_heads(Q)
        K = self.split_heads(K)
        V = self.split_heads(V)
        
        attn = self.attention(Q, K, V)
        attn = np.transpose(attn, (1, 0, 2))
        return attn.reshape(attn.shape[0], -1)

d_model = 8
num_heads = 2
seq_len = 4

mha = MultiHeadAttention(d_model, num_heads)
Q = np.random.randn(seq_len, d_model)
K = np.random.randn(seq_len, d_model)
V = np.random.randn(seq_len, d_model)

output = mha.forward(Q, K, V)

print("=" * 60)
print("Multi-Head Attention Demo")
print("=" * 60)
print(f"d_model: {d_model}")
print(f"num_heads: {num_heads}")
print(f"d_k per head: {d_model // num_heads}")
print(f"Input shape: {Q.shape}")
print(f"Output shape: {output.shape}")
print("\n✓ Multi-head attention allows model to attend to")
print("  information from different representation subspaces")
