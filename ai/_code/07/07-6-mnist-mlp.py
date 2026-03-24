import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

print("=" * 50)
print("MNIST Digit Classification with MLP")
print("=" * 50)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"\nUsing device: {device}")

class MNISTMLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(784, 256)
        self.bn1 = nn.BatchNorm1d(256)
        self.fc2 = nn.Linear(256, 128)
        self.bn2 = nn.BatchNorm1d(128)
        self.fc3 = nn.Linear(128, 10)
        self.dropout = nn.Dropout(0.3)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        x = self.flatten(x)
        x = self.relu(self.bn1(self.fc1(x)))
        x = self.dropout(x)
        x = self.relu(self.bn2(self.fc2(x)))
        x = self.dropout(x)
        return self.fc3(x)

print("\n--- Loading MNIST (simulated) ---")
X_train = torch.randn(60000, 1, 28, 28)
y_train = torch.randint(0, 10, (60000,))
X_test = torch.randn(10000, 1, 28, 28)
y_test = torch.randint(0, 10, (10000,))

train_dataset = TensorDataset(X_train, y_train)
test_dataset = TensorDataset(X_test, y_test)
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

model = MNISTMLP().to(device)
print(f"\nModel:\n{model}")
print(f"\nTotal parameters: {sum(p.numel() for p in model.parameters()):,}")

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)

print("\n--- Training ---")
model.train()
for epoch in range(3):
    total_loss = 0
    correct = 0
    total = 0
    for batch_x, batch_y in train_loader:
        batch_x, batch_y = batch_x.to(device), batch_y.to(device)
        optimizer.zero_grad()
        outputs = model(batch_x)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
        _, predicted = outputs.max(1)
        total += batch_y.size(0)
        correct += predicted.eq(batch_y).sum().item()
    print(f"Epoch {epoch+1}: Loss={total_loss/len(train_loader):.4f}, Acc={100*correct/total:.2f}%")

print("\n--- Evaluation ---")
model.eval()
correct = 0
total = 0
with torch.no_grad():
    for batch_x, batch_y in test_loader:
        batch_x, batch_y = batch_x.to(device), batch_y.to(device)
        outputs = model(batch_x)
        _, predicted = outputs.max(1)
        total += batch_y.size(0)
        correct += predicted.eq(batch_y).sum().item()

print(f"Test Accuracy: {100 * correct / total:.2f}%")

print("\n--- Sample Predictions ---")
model.eval()
with torch.no_grad():
    sample = X_test[:5].to(device)
    outputs = model(sample)
    probs = torch.softmax(outputs, dim=1)
    preds = outputs.argmax(dim=1)
    print("Predictions:", preds.tolist())
    print("Confidence:", [f"{p.max().item()*100:.1f}%" for p in probs])