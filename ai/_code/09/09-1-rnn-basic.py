import torch
import torch.nn as nn

print("=" * 60)
print("09-1: RNN Basic Operations")
print("=" * 60)

batch_size = 2
seq_len = 5
input_size = 10
hidden_size = 8
num_layers = 1

rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True)

input_seq = torch.randn(batch_size, seq_len, input_size)
h_0 = torch.zeros(num_layers, batch_size, hidden_size)

output, h_n = rnn(input_seq, h_0)

print(f"\nInput shape: {input_seq.shape}")
print(f"Hidden state shape: {h_0.shape}")
print(f"Output shape: {output.shape}")
print(f"Final hidden state shape: {h_n.shape}")

print("\n--- Manual RNN Cell ---")

def rnn_cell(input_t, h_prev, W_xh, W_hh, b_h):
    h_current = torch.tanh(torch.matmul(input_t, W_xh.T) + 
                          torch.matmul(h_prev, W_hh.T) + b_h)
    return h_current

torch.manual_seed(42)
W_xh = torch.randn(hidden_size, input_size)
W_hh = torch.randn(hidden_size, hidden_size)
b_h = torch.randn(hidden_size)

input_t = input_seq[0, 0]
h_prev = torch.zeros(hidden_size)
h_t = rnn_cell(input_t, h_prev, W_xh, W_hh, b_h)

print(f"Single time step input: {input_t.shape}")
print(f"Hidden state output: {h_t.shape}")
print(f"Hidden state values:\n{h_t}")

print("\n--- Bidirectional RNN ---")
bi_rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True, bidirectional=True)
output_bi, h_n_bi = bi_rnn(input_seq, h_0)

print(f"Bidirectional output shape: {output_bi.shape}")
print(f"Bidirectional final hidden states: {h_n_bi.shape}")

print("\n--- Multi-layer RNN ---")
num_layers = 3
ml_rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True)
output_ml, h_n_ml = ml_rnn(input_seq, h_0)

print(f"Multi-layer output shape: {output_ml.shape}")
print(f"Multi-layer final hidden states: {h_n_ml.shape}")

print("\n--- RNN Parameters ---")
total_params = sum(p.numel() for p in rnn.parameters())
print(f"Total parameters in RNN: {total_params}")
print(f"  - W_xh: {input_size * hidden_size}")
print(f"  - W_hh: {hidden_size * hidden_size}")
print(f"  - b_h: {hidden_size}")
