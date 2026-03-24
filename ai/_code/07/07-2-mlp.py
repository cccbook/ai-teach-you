import torch
import torch.nn as nn

print("=" * 50)
print("Multi-Layer Perceptron (MLP)")
print("=" * 50)

class MLP(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(MLP, self).__init__()
        self.layer1 = nn.Linear(input_dim, hidden_dim)
        self.layer2 = nn.Linear(hidden_dim, hidden_dim)
        self.output = nn.Linear(hidden_dim, output_dim)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        x = self.relu(self.layer1(x))
        x = self.relu(self.layer2(x))
        return self.output(x)

model = MLP(784, 256, 10)
print(f"\nMLP Architecture:")
print(model)

print(f"\nTotal parameters: {sum(p.numel() for p in model.parameters()):,}")

x = torch.randn(32, 784)
y = model(x)
print(f"\nInput shape: {x.shape}")
print(f"Output shape: {y.shape}")

print("\n--- Training Example (XOR) ---")
class XORMLP(nn.Module):
    def __init__(self):
        super(XORMLP, self).__init__()
        self.fc1 = nn.Linear(2, 4)
        self.fc2 = nn.Linear(4, 1)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        return self.fc2(x)

model = XORMLP()
optimizer = torch.optim.Adam(model.parameters(), lr=0.1)
criterion = nn.MSELoss()

x_train = torch.tensor([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
y_train = torch.tensor([[0.], [1.], [1.], [0.]])

for epoch in range(2000):
    optimizer.zero_grad()
    outputs = model(x_train)
    loss = criterion(outputs, y_train)
    loss.backward()
    optimizer.step()

print(f"Final loss: {loss.item():.4f}")
with torch.no_grad():
    preds = model(x_train).squeeze()
    print(f"Predictions: {[f'{p:.2f}' for p in preds.tolist()]}")
    print(f"Expected:   {[f'{y:.0f}' for y in y_train.squeeze().tolist()]}")