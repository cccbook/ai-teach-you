import torch
import torch.nn as nn


def main():
    print("=" * 50)
    print("Building Neural Networks with nn.Module")
    print("=" * 50)

    print("\n1. Simple MLP (Multi-Layer Perceptron)")
    print("-" * 30)

    class SimpleNet(nn.Module):
        def __init__(self, input_dim=4, hidden_dim=8, output_dim=2):
            super().__init__()
            self.fc1 = nn.Linear(input_dim, hidden_dim)
            self.relu = nn.ReLU()
            self.fc2 = nn.Linear(hidden_dim, output_dim)

        def forward(self, x):
            x = self.fc1(x)
            x = self.relu(x)
            x = self.fc2(x)
            return x

    model = SimpleNet()
    print(model)
    print(f"\nTotal parameters: {sum(p.numel() for p in model.parameters())}")

    print("\n2. Forward Pass Demo")
    print("-" * 30)
    x = torch.randn(2, 4)
    output = model(x)
    print(f"Input shape: {x.shape}")
    print(f"Output shape: {output.shape}")
    print(f"Output: \n{output}")

    print("\n3. More Complex Network with Dropout & BatchNorm")
    print("-" * 30)

    class DeepNet(nn.Module):
        def __init__(self):
            super().__init__()
            self.layers = nn.Sequential(
                nn.Linear(10, 64),
                nn.BatchNorm1d(64),
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.Linear(64, 32),
                nn.ReLU(),
                nn.Linear(32, 5)
            )

        def forward(self, x):
            return self.layers(x)

    model2 = DeepNet()
    print(model2)

    print("\n4. Accessing Parameters")
    print("-" * 30)
    for name, param in model.named_parameters():
        print(f"{name}: shape {param.shape}")

    print("\n5. Training vs Eval Mode")
    print("-" * 30)
    model.eval()
    print("model.training:", model.training)
    print("After model.eval():", not model.training)

    print("\n6. Custom Activation Function")
    print("-" * 30)

    class Swish(nn.Module):
        def forward(self, x):
            return x * torch.sigmoid(x)

    custom_net = nn.Sequential(
        nn.Linear(3, 5),
        Swish(),
        nn.Linear(5, 1)
    )
    x = torch.randn(1, 3)
    out = custom_net(x)
    print(f"Custom Swish activation: {out}")

    print("\n7. Initialize Weights")
    print("-" * 30)
    print("Default weights sample (first layer):")
    print(model.fc1.weight[0, :5])


if __name__ == "__main__":
    main()