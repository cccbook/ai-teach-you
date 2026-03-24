import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms

print("=" * 60)
print("08-7: CIFAR-10 Classification")
print("=" * 60)

class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super(SimpleCNN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(32, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Dropout(0.25),
            
            nn.Conv2d(32, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Conv2d(64, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Dropout(0.25),
            
            nn.Conv2d(64, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Conv2d(128, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Dropout(0.25),
        )
        
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 4 * 4, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

model = SimpleCNN()
print(f"\nSimple CNN for CIFAR-10:")
print(model)

total_params = sum(p.numel() for p in model.parameters())
print(f"\nTotal parameters: {total_params:,}")

print("\n--- Data Transforms ---")
train_transform = transforms.Compose([
    transforms.RandomCrop(32, padding=4),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2470, 0.2435, 0.2616))
])

test_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2470, 0.2435, 0.2616))
])

print("Train: RandomCrop(32, pad=4), RandomHorizontalFlip, Normalize")
print("Test: Normalize only")

print("\n--- Training Configuration ---")
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.5)

print(f"Optimizer: Adam(lr=0.001)")
print(f"Scheduler: StepLR(step_size=10, gamma=0.5)")
print(f"Criterion: CrossEntropyLoss")

print("\n--- Simulated Training Loop (1 epoch) ---")
x = torch.randn(4, 3, 32, 32)
y = torch.randint(0, 10, (4,))

optimizer.zero_grad()
outputs = model(x)
loss = criterion(outputs, y)
loss.backward()
optimizer.step()

print(f"Batch input: {x.shape}")
print(f"Batch output: {outputs.shape}")
print(f"Loss: {loss.item():.4f}")

print("\n--- CIFAR-10 Classes ---")
classes = ['plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
print(classes)

print("\n--- Testing on batch ---")
model.eval()
with torch.no_grad():
    x_test = torch.randn(2, 3, 32, 32)
    output = model(x_test)
    probs = torch.softmax(output, dim=1)
    preds = output.argmax(dim=1)
    print(f"Predictions: {preds.tolist()}")
    print(f"Probabilities: {probs[0].tolist()[:3]}...")

print("\n--- Save/Load Model ---")
torch.save(model.state_dict(), 'cifar10_cnn.pth')
print("Model saved to 'cifar10_cnn.pth'")

state_dict = torch.load('cifar10_cnn.pth')
model.load_state_dict(state_dict)
print("Model loaded from 'cifar10_cnn.pth'")

import os
os.remove('cifar10_cnn.pth')
print("Cleaned up test file")