import torch
import torch.nn as nn

print("=" * 60)
print("09-2: LSTM Structure")
print("=" * 60)

batch_size = 2
seq_len = 5
input_size = 10
hidden_size = 8
num_layers = 1

lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)

input_seq = torch.randn(batch_size, seq_len, input_size)
h_0 = torch.zeros(num_layers, batch_size, hidden_size)
c_0 = torch.zeros(num_layers, batch_size, hidden_size)

output, (h_n, c_n) = lstm(input_seq, (h_0, c_0))

print(f"\nInput shape: {input_seq.shape}")
print(f"Hidden state shape: {h_0.shape}")
print(f"Cell state shape: {c_0.shape}")
print(f"Output shape: {output.shape}")
print(f"Final hidden state: {h_n.shape}")
print(f"Final cell state: {c_n.shape}")

print("\n--- LSTM Gates ---")
lstm_cell = nn.LSTMCell(input_size, hidden_size)

h = torch.zeros(batch_size, hidden_size)
c = torch.zeros(batch_size, hidden_size)

for t in range(seq_len):
    input_t = input_seq[:, t, :]
    h, c = lstm_cell(input_t, (h, c))
    print(f"Time step {t}: h.shape={h.shape}, c.shape={c.shape}")

print("\n--- Manual LSTM Cell ---")

def lstm_cell_manual(input_t, h_prev, c_prev, W_ih, W_hh, b_ih, b_hh):
    gates = torch.matmul(input_t, W_ih.T) + torch.matmul(h_prev, W_hh.T)
    gates = gates + b_ih + b_hh
    
    i, f, g, o = gates.chunk(4, dim=1)
    
    i = torch.sigmoid(i)
    f = torch.sigmoid(f)
    g = torch.tanh(g)
    o = torch.sigmoid(o)
    
    c_current = f * c_prev + i * g
    h_current = o * torch.tanh(c_current)
    
    return h_current, c_current

torch.manual_seed(42)
W_ih = torch.randn(4 * hidden_size, input_size)
W_hh = torch.randn(4 * hidden_size, hidden_size)
b_ih = torch.randn(4 * hidden_size)
b_hh = torch.randn(4 * hidden_size)

input_t = input_seq[0, 0]
h_t, c_t = lstm_cell_manual(input_t, h[0], c[0], W_ih, W_hh, b_ih, b_hh)

print(f"Single LSTM cell input: {input_t.shape}")
print(f"Hidden state: {h_t.shape}")
print(f"Cell state: {c_t.shape}")

print("\n--- Bidirectional LSTM ---")
bi_lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, bidirectional=True)
output_bi, (h_n_bi, c_n_bi) = bi_lstm(input_seq, (h_0, c_0))

print(f"Bidirectional output shape: {output_bi.shape}")
print(f"Bidirectional hidden states: {h_n_bi.shape}")

print("\n--- Multi-layer LSTM ---")
num_layers = 2
ml_lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
output_ml, (h_n_ml, c_n_ml) = ml_lstm(input_seq, (h_0, c_0))

print(f"Multi-layer output shape: {output_ml.shape}")
print(f"Multi-layer hidden states: {h_n_ml.shape}")

print("\n--- LSTM Parameters ---")
lstm_params = sum(p.numel() for p in lstm.parameters())
print(f"Total parameters in LSTM: {lstm_params}")
print(f"  - LSTM has 4 gates (input, forget, cell, output)")
print(f"  - Each gate: W_ih ({input_size}), W_hh ({hidden_size}), bias")
