import math
from collections import defaultdict

print("=" * 60)
print("Micrograd: Hand-crafted Neural Network")
print("=" * 60)

print("""
Micrograd is a tiny autograd engine that demonstrates the core ideas
behind automatic differentiation. It builds a computational graph
and computes gradients using the chain rule.

Key Components:
1. Value: A scalar with gradients
2. Operators: +, -, *, /, exp, log, relu, sigmoid, tanh
3. Backward: Computes gradients using chain rule
""")

class Value:
    def __init__(self, data, _children=(), _op=''):
        self.data = float(data)
        self.grad = 0.0
        self._backward = lambda: None
        self._prev = set(_children)
        self._op = _op
    
    def __repr__(self):
        return f"Value(data={self.data:.4f}, grad={self.grad:.4f})"
    
    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), '+')
        
        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward
        return out
    
    def __radd__(self, other):
        return self + other
    
    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), '*')
        
        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward
        return out
    
    def __rmul__(self, other):
        return self * other
    
    def __sub__(self, other):
        return self + (-other)
    
    def __rsub__(self, other):
        return other + (-self)
    
    def __neg__(self):
        return self * -1
    
    def __truediv__(self, other):
        return self * (other ** -1)
    
    def __rtruediv__(self, other):
        return other * (self ** -1)
    
    def __pow__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError("Only int/float powers supported")
        out = Value(self.data ** other, (self,), f'**{other}')
        
        def _backward():
            self.grad += other * (self.data ** (other - 1)) * out.grad
        out._backward = _backward
        return out
    
    def exp(self):
        out = Value(math.exp(self.data), (self,), 'exp')
        
        def _backward():
            self.grad += out.data * out.grad
        out._backward = _backward
        return out
    
    def log(self):
        out = Value(math.log(self.data), (self,), 'log')
        
        def _backward():
            self.grad += out.grad / self.data
        out._backward = _backward
        return out
    
    def relu(self):
        out = Value(max(0, self.data), (self,), 'ReLU')
        
        def _backward():
            self.grad += (self.data > 0) * out.grad
        out._backward = _backward
        return out
    
    def sigmoid(self):
        s = 1 / (1 + math.exp(-self.data))
        out = Value(s, (self,), 'σ')
        
        def _backward():
            self.grad += s * (1 - s) * out.grad
        out._backward = _backward
        return out
    
    def tanh(self):
        t = math.tanh(self.data)
        out = Value(t, (self,), 'tanh')
        
        def _backward():
            self.grad += (1 - t * t) * out.grad
        out._backward = _backward
        return out
    
    def backward(self):
        topo = []
        visited = set()
        
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)
        
        build_topo(self)
        self.grad = 1.0
        
        for v in reversed(topo):
            v._backward()


class Neuron:
    def __init__(self, nin):
        self.w = [Value(random.uniform(-1, 1)) for _ in range(nin)]
        self.b = Value(random.uniform(-1, 1))
    
    def __call__(self, x):
        return sum((wi * xi for wi, xi in zip(self.w, x)), self.b).relu()
    
    def parameters(self):
        return self.w + [self.b]


class Layer:
    def __init__(self, nin, nout):
        self.neurons = [Neuron(nin) for _ in range(nout)]
    
    def __call__(self, x):
        return [n(x) for n in self.neurons]
    
    def parameters(self):
        return [p for n in self.neurons for p in n.parameters()]


class MLP:
    def __init__(self, nin, nouts):
        sz = [nin] + nouts
        self.layers = [Layer(sz[i], sz[i+1]) for i in range(len(nouts))]
    
    def __call__(self, x):
        for layer in self.layers:
            x = layer(x)
        return x
    
    def parameters(self):
        return [p for layer in self.layers for p in layer.parameters()]


import random

print("\n" + "=" * 60)
print("1. Basic Operations Demo")
print("=" * 60)

a = Value(2.0)
b = Value(3.0)
c = a * b
d = c + a
e = d.relu()

print(f"\na = Value(2.0)")
print(f"b = Value(3.0)")
print(f"c = a * b = {c}")
print(f"d = c + a = {d}")
print(f"e = d.relu() = {e}")

e.backward()
print(f"\nAfter backward():")
print(f"  a.grad = {a.grad}")
print(f"  b.grad = {b.grad}")
print(f"  c.grad = {c.grad}")
print(f"  d.grad = {d.grad}")
print(f"  e.grad = {e.grad}")

print("\n" + "=" * 60)
print("2. Chain Rule Visualization")
print("=" * 60)

x = Value(2.0)
y = x * 3 + 1
z = y ** 2

print(f"\nx = Value(2.0)")
print(f"y = x * 3 + 1 = {y}")
print(f"z = y² = {z}")

print(f"\nAnalytical: dz/dx = 2y * dy/dx = 2*7 * 3 = 42")

z.backward()
print(f"Computed: x.grad = {x.grad}")

print("\n" + "=" * 60)
print("3. Neural Network Forward Pass")
print("=" * 60)

nn = MLP(2, [4, 1])

print("\nMLP(2, [4, 1]) - 2 inputs, 4 hidden neurons, 1 output")
print("Architecture: 2 -> 4 (ReLU) -> 1 (identity)")

x = [Value(0.5), Value(0.3)]
output = nn(x)

print(f"\nInput: [{x[0].data}, {x[1].data}]")
print(f"Output: [{output[0].data:.4f}]")

print("\nNetwork weights:")
for i, layer in enumerate(nn.layers):
    print(f"\nLayer {i+1}:")
    for j, neuron in enumerate(layer.neurons):
        w_str = ", ".join([f"{w.data:.3f}" for w in neuron.w])
        print(f"  Neuron {j}: w=[{w_str}], b={neuron.b.data:.3f}")

print("\n" + "=" * 60)
print("4. Training a Simple Network (XOR)")
print("=" * 60)

nn = MLP(2, [4, 1])

def train_step(nn, x_data, y_val, lr=0.1):
    x = [Value(v) for v in x_data]
    y = Value(y_val)
    pred = nn(x)[0]
    loss = (pred - y) ** 2
    loss.backward()
    
    for p in nn.parameters():
        p.data -= lr * p.grad
        p.grad = 0.0
    
    return loss.data

X_xor = [
    ([0, 0], 0),
    ([0, 1], 1),
    ([1, 0], 1),
    ([1, 1], 0),
]

random.seed(42)
nn = MLP(2, [4, 1])

print("\n" + "=" * 60)
print("4. Training a Simple Network (XOR)")
print("=" * 60)

print("\nTraining XOR on MLP(2, [4, 1])...")
print("-" * 50)

for epoch in range(100):
    total_loss = 0
    for x, y in X_xor:
        loss = train_step(nn, x, y, lr=0.5)
        total_loss += loss
    
    if epoch % 20 == 0:
        print(f"Epoch {epoch:3d}: Loss = {total_loss:.4f}")

print("\n" + "=" * 60)
print("5. Results")
print("=" * 60)

print("\nPredictions after training:")
for x, y in X_xor:
    pred = nn([Value(v) for v in x])[0].data
    print(f"  ({x[0]}, {x[1]}) -> {pred:.4f} (expected {y})")

print("\n" + "=" * 60)
print("6. Gradient Flow Analysis")
print("=" * 60)

nn = MLP(2, [4, 1])
x = [Value(1.0), Value(0.5)]
y = Value(1.0)

pred = nn(x)[0]
loss = (pred - y) ** 2

print(f"\nInput: {x[0].data}, {x[1].data}")
print(f"Target: {y.data}")
print(f"Initial prediction: {pred.data:.4f}")

loss.backward()

grad_norms = []
for i, layer in enumerate(nn.layers):
    layer_grads = [p.grad for p in layer.parameters()]
    grad_norms.append((i, [abs(g) for g in layer_grads]))

print("\nGradient magnitudes by layer:")
for layer_idx, grads in grad_norms:
    avg_grad = sum(grads) / len(grads)
    max_grad = max(grads) if grads else 0
    print(f"  Layer {layer_idx+1}: avg |grad| = {avg_grad:.6f}, max = {max_grad:.6f}")

print("\n" + "=" * 60)
print("Micrograd Architecture Summary")
print("=" * 60)
print("""
Micrograd Core Ideas:
1. Build computational graph dynamically (forward pass)
2. Store gradient function for each operation (_backward)
3. Topological sort for backward pass
4. Chain rule applied automatically

This is the foundation used by PyTorch, JAX, etc.
The same principle scales to billions of parameters.
""")

print("=" * 60)
print("Micrograd Demo Complete")
print("=" * 60)
