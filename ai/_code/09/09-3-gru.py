import torch
import torch.nn as nn

print("=" * 60)
print("09-3: GRU Structure")
print("=" * 60)

batch_size = 2
seq_len = 5
input_size = 10
hidden_size = 8
num_layers = 1

gru = nn.GRU(input_size, hidden_size, num_layers, batch_first=True)

input_seq = torch.randn(batch_size, seq_len, input_size)
h_0 = torch.zeros(num_layers, batch_size, hidden_size)

output, h_n = gru(input_seq, h_0)

print(f"\nInput shape: {input_seq.shape}")
print(f"Hidden state shape: {h_0.shape}")
print(f"Output shape: {output.shape}")
print(f"Final hidden state shape: {h_n.shape}")

print("\n--- GRU Gates ---")
gru_cell = nn.GRUCell(input_size, hidden_size)

h = torch.zeros(batch_size, hidden_size)

for t in range(seq_len):
    input_t = input_seq[:, t, :]
    h = gru_cell(input_t, h)
    print(f"Time step {t}: h.shape={h.shape}")

print("\n--- Manual GRU Cell ---")

def gru_cell_manual(input_t, h_prev, W_iz, W_iz_rev, W_hz, W_hz_rev, b_z, W_ir, W_hr, b_r, W_ih, W_hh, b_h):
    z = torch.sigmoid(torch.matmul(input_t, W_iz.T) + torch.matmul(h_prev, W_hz.T) + b_z)
    r = torch.sigmoid(torch.matmul(input_t, W_ir.T) + torch.matmul(h_prev, W_hr.T) + b_r)
    
    h_tilde = torch.tanh(torch.matmul(input_t, W_ih.T) + torch.matmul(r * h_prev, W_hh.T) + b_h)
    
    h_current = (1 - z) * h_prev + z * h_tilde
    
    return h_current

torch.manual_seed(42)
W_ir = torch.randn(hidden_size, input_size)
W_hr = torch.randn(hidden_size, hidden_size)
b_r = torch.randn(hidden_size)

W_iz = torch.randn(hidden_size, input_size)
W_hz = torch.randn(hidden_size, hidden_size)
b_z = torch.randn(hidden_size)

W_ih = torch.randn(hidden_size, input_size)
W_hh = torch.randn(hidden_size, hidden_size)
b_h = torch.randn(hidden_size)

input_t = input_seq[0, 0]
h_prev = torch.zeros(hidden_size)

h_t = gru_cell_manual(input_t, h_prev, W_iz, None, W_hz, None, b_z, 
                       W_ir, W_hr, b_r, W_ih, W_hh, b_h)

print(f"Single GRU cell input: {input_t.shape}")
print(f"Hidden state: {h_t.shape}")
print(f"Hidden state values:\n{h_t}")

print("\n--- Bidirectional GRU ---")
bi_gru = nn.GRU(input_size, hidden_size, num_layers, batch_first=True, bidirectional=True)
output_bi, h_n_bi = bi_gru(input_seq, h_0)

print(f"Bidirectional output shape: {output_bi.shape}")
print(f"Bidirectional hidden states: {h_n_bi.shape}")

print("\n--- Multi-layer GRU ---")
num_layers = 2
ml_gru = nn.GRU(input_size, hidden_size, num_layers, batch_first=True)
output_ml, h_n_ml = ml_gru(input_seq, h_0)

print(f"Multi-layer output shape: {output_ml.shape}")
print(f"Multi-layer hidden states: {h_n_ml.shape}")

print("\n--- GRU vs LSTM Parameters ---")
lstm = nn.LSTM(input_size, hidden_size, num_layers)
gru = nn.GRU(input_size, hidden_size, num_layers)

lstm_params = sum(p.numel() for p in lstm.parameters())
gru_params = sum(p.numel() for p in gru.parameters())

print(f"LSTM parameters: {lstm_params}")
print(f"GRU parameters: {gru_params}")
print(f"GRU has fewer parameters because it combines gates")
