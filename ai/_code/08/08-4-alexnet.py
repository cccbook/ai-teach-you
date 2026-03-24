import torch
import torch.nn as nn

print("=" * 60)
print("08-4: AlexNet Architecture")
print("=" * 60)

class AlexNet(nn.Module):
    def __init__(self, num_classes=1000):
        super(AlexNet, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, 11, stride=4, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(3, stride=2),
            
            nn.Conv2d(64, 192, 5, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(3, stride=2),
            
            nn.Conv2d(192, 384, 3, padding=1),
            nn.ReLU(inplace=True),
            
            nn.Conv2d(384, 256, 3, padding=1),
            nn.ReLU(inplace=True),
            
            nn.Conv2d(256, 256, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(3, stride=2),
        )
        
        self.avgpool = nn.AdaptiveAvgPool2d((6, 6))
        
        self.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(256 * 6 * 6, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Linear(4096, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x

model = AlexNet()
print(f"\nAlexNet Architecture:")
print(model)

x = torch.randn(1, 3, 224, 224)
output = model(x)
print(f"\nInput shape: {x.shape}")
print(f"Output shape: {output.shape}")

total_params = sum(p.numel() for p in model.parameters())
print(f"\nTotal parameters: {total_params:,}")

print("\n--- Feature Map Sizes ---")
x_test = torch.randn(1, 3, 224, 224)
for i, layer in enumerate(model.features):
    x_test = layer(x_test)
    print(f"Layer {i+1}: {x_test.shape}")

print("\n--- ReLU vs Inplace ReLU ---")
relu = nn.ReLU()
relu_inplace = nn.ReLU(inplace=True)
x = torch.randn(1, 3, 4, 4)
y1 = relu(x.clone())
y2 = relu_inplace(x.clone())
print(f"Original ReLU creates new tensor: {id(y1) != id(x)}")
print(f"Inplace ReLU reuses tensor: {id(y2) == id(x)}")