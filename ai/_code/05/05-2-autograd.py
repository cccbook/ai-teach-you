import torch


def main():
    print("=" * 50)
    print("PyTorch Autograd - Automatic Differentiation")
    print("=" * 50)

    print("\n1. Creating Tensors with requires_grad")
    print("-" * 30)
    x = torch.tensor(2.0, requires_grad=True)
    y = torch.tensor(3.0, requires_grad=True)
    print(f"x = {x}, y = {y}")
    print(f"x.requires_grad = {x.requires_grad}")

    print("\n2. Building Computation Graph")
    print("-" * 30)
    z = x * x + y * 3 + 1
    print(f"z = x² + 3y + 1 = {z}")
    print(f"z.grad_fn: {z.grad_fn}")

    print("\n3. Backward Pass (Compute Gradients)")
    print("-" * 30)
    z.backward()
    print(f"dz/dx = {x.grad}")
    print(f"dz/dy = {y.grad}")

    print("\n4. Manual Verification")
    print("-" * 30)
    print(f"dz/dx = 2x = {2 * x.item()}")
    print(f"dz/dy = 3")

    print("\n5. Gradient Accumulation (multiple backward)")
    print("-" * 30)
    a = torch.tensor(1.0, requires_grad=True)
    b = a * 2
    b.backward()
    print(f"First backward - grad: {a.grad}")
    a.grad = None
    b = a * 2
    b.backward()
    print(f"Second backward - grad: {a.grad}")

    print("\n6. Gradients with Multi-output")
    print("-" * 30)
    x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
    y = x * 2
    y.sum().backward()
    print(f"x = {x}")
    print(f"gradients: {x.grad}")

    print("\n7. Using torch.no_grad() for Inference")
    print("-" * 30)
    w = torch.tensor([1.0, 2.0], requires_grad=True)
    with torch.no_grad():
        prediction = w[0] * 5 + w[1] * 3
        print(f"Prediction (no grad): {prediction}")
    print(f"w.requires_grad: {w.requires_grad}")

    print("\n8. Using .detach() to Get Plain Tensor")
    print("-" * 30)
    x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
    y = x * 2
    y_detached = y.detach()
    print(f"Detached: {y_detached.requires_grad}")


if __name__ == "__main__":
    main()