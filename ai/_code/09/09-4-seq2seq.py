import torch
import torch.nn as nn
import torch.nn.functional as F

print("=" * 60)
print("09-4: Seq2Seq Model")
print("=" * 60)

class Encoder(nn.Module):
    def __init__(self, input_dim, embed_dim, hidden_dim, n_layers=1):
        super().__init__()
        self.embedding = nn.Embedding(input_dim, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, n_layers, batch_first=True)
        
    def forward(self, x):
        embedded = self.embedding(x)
        outputs, (hidden, cell) = self.lstm(embedded)
        return hidden, cell

class Decoder(nn.Module):
    def __init__(self, output_dim, embed_dim, hidden_dim, n_layers=1):
        super().__init__()
        self.embedding = nn.Embedding(output_dim, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, n_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)
        
    def forward(self, x, hidden, cell):
        x = x.unsqueeze(1)
        embedded = self.embedding(x)
        output, (hidden, cell) = self.lstm(embedded, (hidden, cell))
        prediction = self.fc(output.squeeze(1))
        return prediction, hidden, cell

class Seq2Seq(nn.Module):
    def __init__(self, encoder, decoder):
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
        
    def forward(self, src, tgt, teacher_forcing_ratio=0.5):
        batch_size = tgt.shape[0]
        tgt_len = tgt.shape[1]
        tgt_vocab_size = self.decoder.fc.out_features
        
        outputs = torch.zeros(batch_size, tgt_len, tgt_vocab_size)
        
        hidden, cell = self.encoder(src)
        
        dec_input = tgt[:, 0]
        
        for t in range(1, tgt_len):
            output, hidden, cell = self.decoder(dec_input, hidden, cell)
            outputs[:, t] = output
            
            teacher_force = torch.rand(1).item() < teacher_forcing_ratio
            top1 = output.argmax(1)
            dec_input = tgt[:, t] if teacher_force else top1
            
        return outputs

vocab_size = 100
embed_dim = 64
hidden_dim = 128
src_len = 10
tgt_len = 12
batch_size = 4

encoder = Encoder(vocab_size, embed_dim, hidden_dim)
decoder = Decoder(vocab_size, embed_dim, hidden_dim)
model = Seq2Seq(encoder, decoder)

src = torch.randint(0, vocab_size, (batch_size, src_len))
tgt = torch.randint(0, vocab_size, (batch_size, tgt_len))

output = model(src, tgt)

print(f"\nSource shape: {src.shape}")
print(f"Target shape: {tgt.shape}")
print(f"Output shape: {output.shape}")

print("\n--- Training Step ---")
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

model.train()
optimizer.zero_grad()

output = model(src, tgt)
output = output.view(-1, vocab_size)
target = tgt.view(-1)

loss = criterion(output, target)
print(f"Loss: {loss.item():.4f}")

loss.backward()
optimizer.step()

print("\n--- Inference (Greedy Decoding) ---")
model.eval()

def translate(src, model, max_len=15):
    model.eval()
    with torch.no_grad():
        hidden, cell = model.encoder(src)
        
        dec_input = torch.tensor([2])
        results = []
        
        for _ in range(max_len):
            output, hidden, cell = model.decoder(dec_input, hidden, cell)
            top1 = output.argmax(1)
            results.append(top1.item())
            
            if top1.item() == 3:
                break
            dec_input = top1
            
        return results

src_sample = torch.tensor([[5, 12, 8, 1, 9, 2, 7, 4]])
translation = translate(src_sample, model)
print(f"Input: {src_sample.tolist()}")
print(f"Output tokens: {translation}")

print("\n--- Seq2Seq with Attention ---")

class Attention(nn.Module):
    def __init__(self, hidden_dim):
        super().__init__()
        self.attn = nn.Linear(hidden_dim * 2, hidden_dim)
        self.v = nn.Linear(hidden_dim, 1, bias=False)
        
    def forward(self, hidden, encoder_outputs):
        batch_size = encoder_outputs.shape[0]
        src_len = encoder_outputs.shape[1]
        
        hidden = hidden.repeat(1, src_len, 1)
        
        energy = torch.tanh(self.attn(torch.cat((hidden, encoder_outputs), dim=2)))
        attention = self.v(energy).squeeze(2)
        
        return F.softmax(attention, dim=1)

print("Seq2Seq with attention mechanism defined")
