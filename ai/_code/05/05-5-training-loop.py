import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader


def main():
    print("=" * 50)
    print("Complete Training Loop in PyTorch")
    print("=" * 50)

    torch.manual_seed(42)

    print("\n1. Prepare Data")
    print("-" * 30)
    n_samples = 200
    X = torch.randn(n_samples, 1) * 5
    y = 3 * X + 5 + torch.randn(n_samples, 1) * 2

    train_size = int(0.8 * n_samples)
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    train_ds = TensorDataset(X_train, y_train)
    test_ds = TensorDataset(X_test, y_test)

    train_loader = DataLoader(train_ds, batch_size=16, shuffle=True)
    test_loader = DataLoader(test_ds, batch_size=16)

    print(f"Training samples: {len(train_ds)}")
    print(f"Test samples: {len(test_ds)}")

    print("\n2. Define Model")
    print("-" * 30)

    class LinearRegression(nn.Module):
        def __init__(self):
            super().__init__()
            self.linear = nn.Linear(1, 1)

        def forward(self, x):
            return self.linear(x)

    model = LinearRegression()
    print(model)
    print(f"Initial weights: weight={model.linear.weight.item():.4f}, bias={model.linear.bias.item():.4f}")

    print("\n3. Define Loss and Optimizer")
    print("-" * 30)
    criterion = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01)
    print(f"Loss: MSE")
    print(f"Optimizer: SGD, lr=0.01")

    print("\n4. Training Loop")
    print("-" * 30)
    n_epochs = 20

    for epoch in range(n_epochs):
        model.train()
        train_loss = 0.0
        for batch_x, batch_y in train_loader:
            optimizer.zero_grad()
            predictions = model(batch_x)
            loss = criterion(predictions, batch_y)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()

        train_loss /= len(train_loader)

        if (epoch + 1) % 5 == 0:
            model.eval()
            with torch.no_grad():
                test_pred = model(X_test)
                test_loss = criterion(test_pred, y_test).item()
            print(f"Epoch {epoch+1}/{n_epochs} - Train Loss: {train_loss:.4f} - Test Loss: {test_loss:.4f}")

    print("\n5. Final Results")
    print("-" * 30)
    model.eval()
    with torch.no_grad():
        train_pred = model(X_train)
        test_pred = model(X_test)
        train_mse = criterion(train_pred, y_train).item()
        test_mse = criterion(test_pred, y_test).item()

    print(f"Final weight: {model.linear.weight.item():.4f}")
    print(f"Final bias: {model.linear.bias.item():.4f}")
    print(f"Train MSE: {train_mse:.4f}")
    print(f"Test MSE: {test_mse:.4f}")

    print("\n6. Save and Load Model")
    print("-" * 30)
    torch.save(model.state_dict(), "model.pth")
    print("Saved model.state_dict() to 'model.pth'")

    model2 = LinearRegression()
    model2.load_state_dict(torch.load("model.pth"))
    model2.eval()
    print("Loaded model from 'model.pth'")

    with torch.no_grad():
        pred = model2(torch.tensor([[5.0]]))
    print(f"Prediction for x=5: {pred.item():.4f}")


if __name__ == "__main__":
    main()