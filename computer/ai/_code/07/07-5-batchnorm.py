import torch
import torch.nn as nn

print("=" * 50)
print("Batch Normalization")
print("=" * 50)

print("\n--- Manual Batch Norm ---")
def batch_norm_manual(x, gamma, beta, eps=1e-5):
    mean = x.mean(dim=0, keepdim=True)
    var = x.var(dim=0, keepdim=True, unbiased=False)
    x_norm = (x - mean) / torch.sqrt(var + eps)
    return gamma * x_norm + beta

x = torch.randn(32, 10)
gamma = torch.ones(10)
beta = torch.zeros(10)
y = batch_norm_manual(x, gamma, beta)
print(f"Input  mean: {x.mean(dim=0).mean().item():.4f}")
print(f"Output mean: {y.mean(dim=0).mean().item():.4f}")
print(f"Output std:  {y.std(dim=0).mean().item():.4f}")

print("\n--- PyTorch BatchNorm1d ---")
bn = nn.BatchNorm1d(10)
x = torch.randn(32, 10)
y = bn(x)
print(f"Before BN - mean: {x.mean().item():.4f}, std: {x.std().item():.4f}")
print(f"After BN  - mean: {y.mean().item():.4f}, std: {y.std().item():.4f}")
print(f"Gamma: {bn.weight[:3].tolist()}")
print(f"Beta:  {bn.bias[:3].tolist()}")

print("\n--- Training vs Eval Mode ---")
bn.eval()
with torch.no_grad():
    y_eval = bn(x)
print(f"Eval mode - running mean: {bn.running_mean[:3].tolist()}")

bn.train()
y_train = bn(x)
print(f"Train mode - output: {y_train[:3, :3]}")

print("\n--- MLP with BatchNorm ---")
class MLPWithBN(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 256)
        self.bn1 = nn.BatchNorm1d(256)
        self.fc2 = nn.Linear(256, 10)
    
    def forward(self, x):
        x = torch.relu(self.bn1(self.fc1(x)))
        return self.fc2(x)

model = MLPWithBN()
x = torch.randn(64, 784)
y = model(x)
print(f"Output shape: {y.shape}")

print("\n--- BatchNorm for Conv ---")
bn_conv = nn.BatchNorm2d(64)
x_conv = torch.randn(8, 64, 32, 32)
y_conv = bn_conv(x_conv)
print(f"Conv input shape:  {x_conv.shape}")
print(f"Conv output shape: {y_conv.shape}")

print("\n--- Momentum Effect ---")
bn_slow = nn.BatchNorm1d(10, momentum=0.1)
bn_fast = nn.BatchNorm1d(10, momentum=0.9)

for _ in range(50):
    x = torch.randn(32, 10)
    bn_slow(x)
    bn_fast(x)

print(f"Momentum=0.1 - running mean: {bn_slow.running_mean[:3].tolist()}")
print(f"Momentum=0.9 - running mean: {bn_fast.running_mean[:3].tolist()}")