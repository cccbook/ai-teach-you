import torch
import torch.nn as nn

print("=" * 50)
print("Single Layer Perceptron")
print("=" * 50)

class Perceptron(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(Perceptron, self).__init__()
        self.fc = nn.Linear(input_dim, output_dim)
    
    def forward(self, x):
        return self.fc(x)

model = Perceptron(2, 1)
print(f"\nModel Architecture:\n{model}")

x = torch.randn(4, 2)
y = model(x)
print(f"\nInput shape: {x.shape}")
print(f"Output shape: {y.shape}")

print("\n--- Training Example ---")
criterion = nn.BCEWithLogitsLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)

x_train = torch.tensor([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
y_train = torch.tensor([[0.], [1.], [1.], [0.]])

model.train()
for epoch in range(200):
    optimizer.zero_grad()
    outputs = model(x_train)
    loss = criterion(outputs, y_train)
    loss.backward()
    optimizer.step()

print(f"\nFinal loss: {loss.item():.4f}")
with torch.no_grad():
    predictions = (torch.sigmoid(model(x_train)) > 0.5).float()
    print(f"Predictions: {predictions.squeeze().tolist()}")
    print(f"Expected:   {y_train.squeeze().tolist()}")