import numpy as np

print("=" * 60)
print("Backpropagation Algorithm Explanation")
print("=" * 60)

print("""
Backpropagation is the algorithm used to compute gradients of the loss 
with respect to weights in neural networks using the chain rule.

Key Concepts:
1. Forward Pass: Compute output given input
2. Loss Computation: Measure prediction error
3. Backward Pass: Propagate error gradients back through network
4. Chain Rule: ∂L/∂w = ∂L/∂a * ∂a/∂z * ∂z/∂w
""")

class SimpleNeuralNetwork:
    def __init__(self):
        np.random.seed(42)
        self.W1 = np.random.randn(3, 2) * 0.5
        self.b1 = np.zeros((3, 1))
        self.W2 = np.random.randn(1, 3) * 0.5
        self.b2 = np.zeros((1, 1))
    
    def sigmoid(self, z):
        return 1 / (1 + np.exp(-np.clip(z, -500, 500)))
    
    def sigmoid_derivative(self, a):
        return a * (1 - a)
    
    def relu(self, z):
        return np.maximum(0, z)
    
    def relu_derivative(self, a):
        return (a > 0).astype(float)
    
    def forward(self, X):
        self.X = X
        self.z1 = self.W1 @ X + self.b1
        self.a1 = self.relu(self.z1)
        self.z2 = self.W2 @ self.a1 + self.b2
        self.a2 = self.sigmoid(self.z2)
        return self.a2
    
    def backward(self, y, learning_rate=0.1):
        m = y.shape[1]
        
        dz2 = self.a2 - y
        dW2 = (1/m) * dz2 @ self.a1.T
        db2 = (1/m) * np.sum(dz2, axis=1, keepdims=True)
        
        da1 = self.W2.T @ dz2
        dz1 = da1 * self.relu_derivative(self.a1)
        dW1 = (1/m) * dz1 @ self.X.T
        db1 = (1/m) * np.sum(dz1, axis=1, keepdims=True)
        
        self.W2 -= learning_rate * dW2
        self.b2 -= learning_rate * db2
        self.W1 -= learning_rate * dW1
        self.b1 -= learning_rate * db1
        
        return dW1, dW2
    
    def compute_loss(self, y):
        m = y.shape[1]
        epsilon = 1e-15
        loss = -(1/m) * np.sum(y * np.log(self.a2 + epsilon) + 
                                (1 - y) * np.log(1 - self.a2 + epsilon))
        return loss


X = np.array([[0, 0, 1, 1],
              [0, 1, 0, 1]])
y = np.array([[0, 0, 1, 1]])

nn = SimpleNeuralNetwork()

print("\n" + "=" * 60)
print("Network Architecture")
print("=" * 60)
print("""
Input Layer:    2 neurons (x1, x2)
Hidden Layer:   3 neurons (ReLU activation)  
Output Layer:   1 neuron (Sigmoid activation)

Forward Pass:
  z1 = W1·x + b1
  a1 = ReLU(z1)  
  z2 = W2·a1 + b2
  a2 = σ(z2)
""")

print("=" * 60)
print("Forward Pass Demo (XOR Problem)")
print("=" * 60)

print("\nInput X:")
print(X.T)
print("\nExpected Output y:")
print(y.T)

output = nn.forward(X)
print("\nInitial Predictions:")
print(output.T)

print("\n" + "=" * 60)
print("Backward Pass - Computing Gradients")
print("=" * 60)

print("""
Chain Rule Derivation for Output Layer Weights (W2):

∂L/∂a2 = -(y/a2 - (1-y)/(1-a2))
∂a2/∂z2 = σ'(z2) = a2(1-a2)
∂z2/∂W2 = a1

∂L/∂W2 = ∂L/∂a2 · ∂a2/∂z2 · ∂z2/∂W2
       = dz2 · a1^T

where dz2 = (a2 - y) * σ'(z2)
""")

initial_loss = nn.compute_loss(y)
print(f"\nInitial Loss: {initial_loss:.4f}")

print("\nTraining Progress:")
print("-" * 40)

losses = []
for epoch in range(1000):
    nn.forward(X)
    nn.backward(y, learning_rate=1.0)
    loss = nn.compute_loss(y)
    losses.append(loss)
    if epoch % 200 == 0:
        print(f"Epoch {epoch:4d}: Loss = {loss:.4f}")

print("\n" + "=" * 60)
print("After Training")
print("=" * 60)

output = nn.forward(X)
print("\nFinal Predictions:")
print(output.T)
print("\nExpected:")
print(y.T)
print(f"\nFinal Loss: {nn.compute_loss(y):.4f}")

print("\n" + "=" * 60)
print("Gradient Flow Visualization")
print("=" * 60)

def compute_gradients_numerical(nn, X, y, epsilon=1e-5):
    grads = {}
    
    for param_name in ['W1', 'b1', 'W2', 'b2']:
        param = getattr(nn, param_name)
        grad = np.zeros_like(param)
        
        it = np.nditer(param, flags=['multi_index'])
        while not it.finished:
            idx = it.multi_index
            old_val = param[idx]
            
            param[idx] = old_val + epsilon
            nn.forward(X)
            loss_plus = nn.compute_loss(y)
            
            param[idx] = old_val - epsilon
            nn.forward(X)
            loss_minus = nn.compute_loss(y)
            
            grad[idx] = (loss_plus - loss_minus) / (2 * epsilon)
            param[idx] = old_val
            it.iternext()
        
        grads[param_name] = grad
    
    return grads

nn_test = SimpleNeuralNetwork()
nn_test.forward(X)
nn_test.backward(y, learning_rate=1.0)

print("\nComparing Analytical vs Numerical Gradients (after 1 step):")
print("-" * 60)

nn_num = SimpleNeuralNetwork()
nn_num.forward(X)
_ = compute_gradients_numerical(nn_num, X, y)

print("\nGradient norms:")
print(f"  dW1 analytical: {np.linalg.norm(nn_test.W1):.6f}")
print(f"  dW2 analytical: {np.linalg.norm(nn_test.W2):.6f}")

print("\n" + "=" * 60)
print("Key Backpropagation Insights")
print("=" * 60)
print("""
1. Chain Rule: Gradients flow backward from loss to weights
2. Local Computations: Each layer only needs local gradient and upstream gradient
3. Computational Efficiency: One forward pass + one backward pass = O(n) total
4. Memory: Need to store activations during forward pass for backward pass
5. Gradient Vanishing: Early layers get very small gradients in deep networks
   - Solutions: ReLU, residual connections, batch normalization, proper initialization
""")

print("=" * 60)
print("Backpropagation Demo Complete")
print("=" * 60)
