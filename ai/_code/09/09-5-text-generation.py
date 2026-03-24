import torch
import torch.nn as nn
import torch.nn.functional as F

print("=" * 60)
print("09-5: Text Generation")
print("=" * 60)

class TextGenerator(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_layers=1):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, vocab_size)
        
    def forward(self, x, hidden=None):
        embedded = self.embedding(x)
        if hidden is None:
            output, hidden = self.lstm(embedded)
        else:
            output, hidden = self.lstm(embedded, hidden)
        prediction = self.fc(output)
        return prediction, hidden

vocab_size = 256
embed_dim = 128
hidden_dim = 256
num_layers = 2

model = TextGenerator(vocab_size, embed_dim, hidden_dim, num_layers)

print(f"\nModel parameters: {sum(p.numel() for p in model.parameters())}")

sample_text = "hello world"
char_to_idx = {ch: i for i, ch in enumerate(set(sample_text))}
idx_to_char = {i: ch for ch, i in char_to_idx.items()}

char_to_idx['<UNK>'] = len(char_to_idx)
idx_to_char[len(idx_to_char)] = '<UNK>'

print(f"Vocabulary size: {len(char_to_idx)}")

def encode_text(text, char_to_idx):
    return torch.tensor([char_to_idx.get(ch, char_to_idx['<UNK>']) for ch in text])

def decode_text(tensor, idx_to_char):
    return ''.join([idx_to_char.get(idx.item(), '<UNK>') for idx in tensor])

encoded = encode_text(sample_text, char_to_idx)
print(f"Encoded: {encoded}")
print(f"Decoded: {decode_text(encoded, idx_to_char)}")

print("\n--- Training ---")

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

model.train()

sequence = "hello world"
encoded_seq = encode_text(sequence, char_to_idx)

input_seq = encoded_seq[:-1]
target_seq = encoded_seq[1:]

input_seq = input_seq.unsqueeze(0)
target_seq = target_seq.unsqueeze(0)

output, _ = model(input_seq)
output = output.squeeze(0)

loss = criterion(output, target_seq)
print(f"Initial loss: {loss.item():.4f}")

for epoch in range(100):
    optimizer.zero_grad()
    output, _ = model(input_seq)
    loss = criterion(output.squeeze(0), target_seq.squeeze(0))
    loss.backward()
    optimizer.step()
    
    if (epoch + 1) % 25 == 0:
        print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")

print("\n--- Text Generation ---")
model.eval()

def generate(model, start_str, char_to_idx, idx_to_char, max_len=50, temperature=1.0):
    model.eval()
    
    input_seq = encode_text(start_str, char_to_idx).unsqueeze(0)
    generated = start_str
    
    hidden = None
    
    for _ in range(max_len):
        output, hidden = model(input_seq, hidden)
        
        output = output.squeeze(0) / temperature
        probs = F.softmax(output[-1], dim=0)
        
        next_idx = torch.multinomial(probs, 1).item()
        next_char = idx_to_char.get(next_idx, '<UNK>')
        
        if next_char == '<UNK>':
            break
            
        generated += next_char
        input_seq = torch.tensor([[next_idx]])
        
    return generated

result = generate(model, "hello", char_to_idx, idx_to_char, max_len=20, temperature=0.8)
print(f"Generated text: {result}")

print("\n--- Sampling Methods ---")

def generate_greedy(model, start_str, char_to_idx, idx_to_char, max_len=20):
    input_seq = encode_text(start_str, char_to_idx).unsqueeze(0)
    hidden = None
    
    for _ in range(max_len):
        output, hidden = model(input_seq, hidden)
        next_idx = output.argmax(2)[0, -1].item()
        next_char = idx_to_char.get(next_idx, '<UNK>')
        
        if next_char == '<UNK>':
            break
            
        start_str += next_char
        input_seq = torch.tensor([[next_idx]])
        
    return start_str

greedy_result = generate_greedy(model, "hello", char_to_idx, idx_to_char)
print(f"Greedy: {greedy_result}")
