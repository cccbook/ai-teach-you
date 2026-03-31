import numpy as np

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

class PositionalEncoding:
    def __init__(self, d_model, max_len=100):
        self.d_model = d_model
        
    def get_positional_encoding(self, seq_len):
        pe = np.zeros((seq_len, self.d_model))
        position = np.arange(seq_len).reshape(-1, 1)
        div_term = np.exp(np.arange(0, self.d_model, 2) * -(np.log(10000.0) / self.d_model))
        pe[:, 0::2] = np.sin(position * div_term)
        pe[:, 1::2] = np.cos(position * div_term)
        return pe

d_model = 8
seq_len = 10

pe = PositionalEncoding(d_model)
pos_enc = pe.get_positional_encoding(seq_len)

print("=" * 60)
print("Positional Encoding Demo")
print("=" * 60)
print(f"d_model: {d_model}")
print(f"sequence length: {seq_len}")
print(f"Positional encoding shape: {pos_enc.shape}")
print("\nPositional encoding for first 3 positions:")
print(pos_enc[:3])
print("\n✓ Positional encoding encodes position information")
print("  using sine and cosine functions of different frequencies")
