import numpy as np

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

class MiniTransformer:
    def __init__(self, vocab_size, d_model, num_heads, num_layers):
        self.vocab_size = vocab_size
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        self.embedding = np.random.randn(vocab_size, d_model) * 0.1
        self.W_Q = [np.random.randn(d_model, d_model) * 0.1 for _ in range(num_layers)]
        self.W_K = [np.random.randn(d_model, d_model) * 0.1 for _ in range(num_layers)]
        self.W_V = [np.random.randn(d_model, d_model) * 0.1 for _ in range(num_layers)]
        self.W_O = np.random.randn(d_model, d_model) * 0.1
        self.W1 = [np.random.randn(d_model, d_model * 4) * 0.1 for _ in range(num_layers)]
        self.W2 = [np.random.randn(d_model * 4, d_model) * 0.1 for _ in range(num_layers)]
        self.lm_head = np.random.randn(d_model, vocab_size) * 0.1
        
    def positional_encoding(self, seq_len):
        pe = np.zeros((seq_len, self.d_model))
        position = np.arange(seq_len).reshape(-1, 1)
        div_term = np.exp(np.arange(0, self.d_model, 2) * -(np.log(10000.0) / self.d_model))
        pe[:, 0::2] = np.sin(position * div_term)
        pe[:, 1::2] = np.cos(position * div_term)
        return pe
    
    def forward(self, token_ids):
        x = self.embedding[token_ids] + self.positional_encoding(len(token_ids))
        
        for i in range(len(self.W_Q)):
            Q = x @ self.W_Q[i]
            K = x @ self.W_K[i]
            V = x @ self.W_K[i]
            scores = Q @ K.T / np.sqrt(self.d_k)
            weights = softmax(scores)
            x = weights @ V @ self.W_O
            x = np.maximum(0, x @ self.W1[i]) @ self.W2[i]
            
        logits = x @ self.lm_head
        return logits
    
    def generate(self, token_ids, max_new_tokens):
        for _ in range(max_new_tokens):
            logits = self.forward(token_ids)
            next_token = np.argmax(logits[-1])
            token_ids = np.append(token_ids, next_token)
        return token_ids

vocab_size = 50
d_model = 16
num_heads = 2
num_layers = 2

model = MiniTransformer(vocab_size, d_model, num_heads, num_layers)

seed = [1, 2, 3, 4, 5]
output = model.forward(seed)

print("=" * 60)
print("Mini Transformer Demo")
print("=" * 60)
print(f"Vocab size: {vocab_size}")
print(f"d_model: {d_model}")
print(f"num_heads: {num_heads}")
print(f"num_layers: {num_layers}")
print(f"Input length: {len(seed)}")
print(f"Output logits shape: {output.shape}")

generated = model.generate(np.array(seed), 3)
print(f"\nGenerated token IDs: {generated.tolist()}")
print("\n✓ Mini Transformer demonstrates core architecture:")
print("  embedding + positional encoding + stacked self-attention")
print("  + feed-forward layers + language model head")
