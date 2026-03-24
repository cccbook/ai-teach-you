import torch
import torch.nn as nn

print("=" * 50)
print("Regularization: Dropout, L1/L2")
print("=" * 50)

print("\n--- Dropout ---")
class NetWithDropout(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 256)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(256, 10)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        return self.fc2(x)

model = NetWithDropout()
model.train()
x = torch.randn(32, 784)
y = model(x)
print(f"Training mode - output mean: {y.mean().item():.4f}")

model.eval()
with torch.no_grad():
    y = model(x)
    print(f"Eval mode - output mean: {y.mean().item():.4f}")

print("\n--- L2 Regularization (Weight Decay) ---")
model_l2 = nn.Linear(10, 10)
optimizer = torch.optim.SGD(model_l2.parameters(), lr=0.01, weight_decay=0.01)
print(f"Optimizer weight_decay: {optimizer.param_groups[0]['weight_decay']}")

print("\n--- L1 Regularization (Manual) ---")
def l1_regularization(model, lambda_l1=0.01):
    l1_loss = 0
    for param in model.parameters():
        l1_loss += torch.sum(torch.abs(param))
    return lambda_l1 * l1_loss

model = nn.Linear(10, 10)
criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

x = torch.randn(5, 10)
y = torch.randn(5, 10)

optimizer.zero_grad()
output = model(x)
loss = criterion(output, y)
l1_loss = l1_regularization(model, lambda_l1=0.01)
total_loss = loss + l1_loss
total_loss.backward()
optimizer.step()

print(f"MSELoss: {loss.item():.4f}")
print(f"L1 Loss: {l1_loss.item():.4f}")
print(f"Total Loss: {total_loss.item():.4f}")

print("\n--- Comparison of Regularization Effects ---")
class SimpleNet(nn.Module):
    def __init__(self, use_dropout=False):
        super().__init__()
        self.fc = nn.Linear(10, 10)
        self.dropout = nn.Dropout(0.5) if use_dropout else nn.Identity()
    
    def forward(self, x):
        return self.dropout(self.fc(x))

torch.manual_seed(42)
net_no_reg = SimpleNet(False)
torch.manual_seed(42)
net_dropout = SimpleNet(True)

print(f"No dropout weights: {net_no_reg.fc.weight[0, :3]}")
net_dropout.train()
with torch.no_grad():
    _ = net_dropout(torch.randn(1, 10))
print(f"With dropout weights: {net_dropout.fc.weight[0, :3]}")

print("\n--- Weight Decay Effect ---")
model1 = nn.Linear(10, 10)
model2 = nn.Linear(10, 10)
opt1 = torch.optim.SGD(model1.parameters(), lr=0.01, weight_decay=0.0)
opt2 = torch.optim.SGD(model2.parameters(), lr=0.01, weight_decay=0.1)

x = torch.randn(32, 10)
y = torch.randn(32, 10)

for _ in range(100):
    opt1.zero_grad(); loss = ((model1(x) - y) ** 2).mean(); loss.backward(); opt1.step()
    opt2.zero_grad(); loss = ((model2(x) - y) ** 2).mean(); loss.backward(); opt2.step()

print(f"Without weight decay - weight norm: {model1.weight.norm().item():.4f}")
print(f"With weight decay    - weight norm: {model2.weight.norm().item():.4f}")