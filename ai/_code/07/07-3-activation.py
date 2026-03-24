import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import numpy as np

print("=" * 50)
print("Comparison of Activation Functions")
print("=" * 50)

x = torch.linspace(-5, 5, 100)

activations = {
    'Sigmoid': torch.sigmoid,
    'Tanh': torch.tanh,
    'ReLU': torch.relu,
    'Leaky ReLU': lambda x: torch.where(x > 0, x, 0.01 * x),
    'ELU': torch.nn.ELU(),
    'Swish': lambda x: x * torch.sigmoid(x),
    'Softmax': lambda x: torch.softmax(x, dim=0),
}

print("\nFunction formulas and characteristics:")
print("- Sigmoid: 1/(1+e^-x) - gradient vanishes for large |x|")
print("- Tanh: (e^x-e^-x)/(e^x+e^-x) - zero-centered")
print("- ReLU: max(0,x) - vanishing gradient solved, dying ReLU problem")
print("- Leaky ReLU: max(0.01x,x) -解决了dying ReLU")
print("- ELU: x if x>0, (e^x-1) if x<0 - smooth everywhere")
print("- Swish: x*sigmoid(x) - learnable, self-gated")
print("- Softmax: e^x_i/sum(e^x_j) - multi-class output")

print("\n--- Activation Comparison ---")
for name, func in activations.items():
    y = func(x)
    print(f"{name:15} range: [{y.min().item():.3f}, {y.max().item():.3f}]")

print("\n--- Gradient Comparison ---")
x.requires_grad = True
for name, func in activations.items():
    if name == 'Softmax':
        continue
    y = func(x)
    y.sum().backward()
    grad = x.grad.clone()
    x.grad.zero_()
    print(f"{name:15} mean grad: {grad.abs().mean().item():.3f}")

print("\n--- Derivatives ---")
def sigmoid_deriv(x):
    s = torch.sigmoid(x)
    return s * (1 - s)

def tanh_deriv(x):
    return 1 - torch.tanh(x) ** 2

def relu_deriv(x):
    return (x > 0).float()

x_test = torch.tensor([2.0], requires_grad=True)
print(f"d/dx(sigmoid) at x=2: {sigmoid_deriv(x_test).item():.4f}")
print(f"d/dx(tanh)    at x=2: {tanh_deriv(x_test).item():.4f}")
print(f"d/dx(ReLU)    at x=2: {relu_deriv(x_test).item():.4f}")