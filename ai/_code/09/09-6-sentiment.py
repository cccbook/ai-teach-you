import torch
import torch.nn as nn
import torch.nn.functional as F
from collections import Counter

print("=" * 60)
print("09-6: Sentiment Classification")
print("=" * 60)

class SentimentRNN(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_layers, output_dim, dropout=0.3):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, num_layers, 
                           batch_first=True, bidirectional=True, dropout=dropout if num_layers > 1 else 0)
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_dim * 2, output_dim)
        
    def forward(self, x):
        embedded = self.dropout(self.embedding(x))
        output, (hidden, cell) = self.lstm(embedded)
        
        hidden = torch.cat((hidden[-2,:,:], hidden[-1,:,:]), dim=1)
        hidden = self.dropout(hidden)
        
        return self.fc(hidden)

def tokenize(text):
    return text.lower().split()

def build_vocab(texts, min_freq=1):
    counter = Counter()
    for text in texts:
        counter.update(tokenize(text))
    
    vocab = {'<PAD>': 0, '<UNK>': 1}
    for word, count in counter.items():
        if count >= min_freq:
            vocab[word] = len(vocab)
    return vocab

def encode_text(text, vocab):
    tokens = tokenize(text)
    return torch.tensor([vocab.get(token, vocab['<UNK>']) for token in tokens])

vocab_size = 1000
embed_dim = 100
hidden_dim = 128
num_layers = 2
output_dim = 2

model = SentimentRNN(vocab_size, embed_dim, hidden_dim, num_layers, output_dim)

print(f"\nModel parameters: {sum(p.numel() for p in model.parameters())}")

sample_texts = [
    "this movie is amazing and i loved it",
    "terrible film waste of time",
    "great acting and wonderful story",
    "boring and awful experience",
    "best movie i have ever seen",
    "horrible acting bad plot"
]

labels = torch.tensor([1, 0, 1, 0, 1, 0])

vocab = build_vocab(sample_texts)
print(f"Vocabulary size: {len(vocab)}")

encoded_texts = [encode_text(text, vocab) for text in sample_texts]

max_len = max(len(e) for e in encoded_texts)

padded_texts = []
for enc in encoded_texts:
    if len(enc) < max_len:
        padded = F.pad(enc, (0, max_len - len(enc)), value=0)
    else:
        padded = enc
    padded_texts.append(padded)

X = torch.stack(padded_texts)
y = labels

print(f"\nInput shape: {X.shape}")
print(f"Labels shape: {y.shape}")

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

model.train()

for epoch in range(50):
    optimizer.zero_grad()
    output = model(X)
    loss = criterion(output, y)
    loss.backward()
    optimizer.step()
    
    if (epoch + 1) % 10 == 0:
        _, predicted = output.max(1)
        accuracy = (predicted == y).float().mean()
        print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}, Acc: {accuracy.item():.4f}")

print("\n--- Inference ---")
model.eval()

def predict(text, model, vocab, max_len):
    model.eval()
    encoded = encode_text(text, vocab)
    
    if len(encoded) < max_len:
        padded = F.pad(encoded, (0, max_len - len(encoded)), value=0)
    else:
        padded = encoded[:max_len]
    
    x = padded.unsqueeze(0)
    
    with torch.no_grad():
        output = model(x)
        probs = F.softmax(output, dim=1)
        pred = output.argmax(1).item()
        
    return pred, probs[0]

test_reviews = [
    "i really enjoyed this movie",
    "worst movie ever terrible",
    "amazing film highly recommend"
]

for review in test_reviews:
    pred, probs = predict(review, model, vocab, max_len)
    sentiment = "Positive" if pred == 1 else "Negative"
    print(f"Review: '{review}'")
    print(f"Sentiment: {sentiment}, Confidence: {probs[pred].item():.4f}\n")

print("\n--- Different Architectures ---")

class SentimentCNN(nn.Module):
    def __init__(self, vocab_size, embed_dim, num_filters, filter_sizes, output_dim, dropout=0.3):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.convs = nn.ModuleList([
            nn.Conv1d(embed_dim, num_filters, fs) for fs in filter_sizes
        ])
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(len(filter_sizes) * num_filters, output_dim)
        
    def forward(self, x):
        embedded = self.embedding(x)
        embedded = embedded.permute(0, 2, 1)
        
        conv_outputs = [F.relu(conv(embedded)) for conv in self.convs]
        pooled = [F.max_pool1d(conv_out, conv_out.shape[2]).squeeze(2) for conv_out in conv_outputs]
        
        cat = self.dropout(torch.cat(pooled, dim=1))
        return self.fc(cat)

cnn_model = SentimentCNN(vocab_size, embed_dim, 100, [2, 3, 4], output_dim)
print(f"CNN model parameters: {sum(p.numel() for p in cnn_model.parameters())}")

output = cnn_model(X)
loss = criterion(output, y)
print(f"CNN initial loss: {loss.item():.4f}")

print("\n--- Sentiment with Attention ---")

class AttentionLayer(nn.Module):
    def __init__(self, hidden_dim):
        super().__init__()
        self.attention = nn.Linear(hidden_dim * 2, 1)
        
    def forward(self, lstm_output):
        attention_weights = F.softmax(self.attention(lstm_output), dim=1)
        weighted_output = torch.sum(attention_weights * lstm_output, dim=1)
        return weighted_output

class SentimentLSTMAttention(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, output_dim, dropout=0.3):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True, bidirectional=True)
        self.attention = AttentionLayer(hidden_dim)
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_dim * 2, output_dim)
        
    def forward(self, x):
        embedded = self.dropout(self.embedding(x))
        lstm_out, _ = self.lstm(embedded)
        attended = self.attention(lstm_out)
        return self.fc(attended)

attn_model = SentimentLSTMAttention(vocab_size, embed_dim, hidden_dim, output_dim)
print(f"LSTM+Attention model parameters: {sum(p.numel() for p in attn_model.parameters())}")
