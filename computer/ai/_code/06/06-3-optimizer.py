import numpy as np

try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Note: matplotlib not available, skipping visualization")


class Optimizer:
    def __init__(self, params, lr=0.001):
        self.lr = lr
        self.params = {k: v for k, v in params.items()}
        self.state = {}
    
    def step(self, gradients):
        pass


class SGD(Optimizer):
    def __init__(self, params, lr=0.01, momentum=0.0, nesterov=False):
        super().__init__(params, lr)
        self.momentum = momentum
        self.nesterov = nesterov
        self.velocity = {k: np.zeros_like(v) for k, v in params.items()}
    
    def step(self, gradients):
        for k in self.params:
            if self.momentum > 0:
                if self.nesterov:
                    grad = gradients[k] + self.momentum * self.velocity[k]
                else:
                    grad = self.momentum * self.velocity[k] - self.lr * gradients[k]
                    self.velocity[k] = grad
                    self.params[k] = self.params[k] + grad
            else:
                self.params[k] = self.params[k] - self.lr * gradients[k]
        return self.params


class RMSprop(Optimizer):
    def __init__(self, params, lr=0.001, alpha=0.99, epsilon=1e-8):
        super().__init__(params, lr)
        self.alpha = alpha
        self.epsilon = epsilon
        self.square_grads = {k: np.zeros_like(v) for k, v in params.items()}
    
    def step(self, gradients):
        for k in self.params:
            self.square_grads[k] = self.alpha * self.square_grads[k] + \
                (1 - self.alpha) * (gradients[k] ** 2)
            self.params[k] = self.params[k] - self.lr * gradients[k] / \
                (np.sqrt(self.square_grads[k]) + self.epsilon)
        return self.params


class Adam(Optimizer):
    def __init__(self, params, lr=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8):
        super().__init__(params, lr)
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.m = {k: np.zeros_like(v) for k, v in params.items()}
        self.v = {k: np.zeros_like(v) for k, v in params.items()}
        self.t = 0
    
    def step(self, gradients):
        self.t += 1
        for k in self.params:
            self.m[k] = self.beta1 * self.m[k] + (1 - self.beta1) * gradients[k]
            self.v[k] = self.beta2 * self.v[k] + (1 - self.beta2) * (gradients[k] ** 2)
            
            m_hat = self.m[k] / (1 - self.beta1 ** self.t)
            v_hat = self.v[k] / (1 - self.beta2 ** self.t)
            
            self.params[k] = self.params[k] - self.lr * m_hat / (np.sqrt(v_hat) + self.epsilon)
        return self.params


class AdaGrad(Optimizer):
    def __init__(self, params, lr=0.01, epsilon=1e-10):
        super().__init__(params, lr)
        self.epsilon = epsilon
        self.grad_sum = {k: np.zeros_like(v) for k, v in params.items()}
    
    def step(self, gradients):
        for k in self.params:
            self.grad_sum[k] += gradients[k] ** 2
            self.params[k] = self.params[k] - self.lr * gradients[k] / \
                (np.sqrt(self.grad_sum[k]) + self.epsilon)
        return self.params


def f(xy):
    x, y = xy
    return x**2 + 10*y**2

def grad_f(xy):
    x, y = xy
    return np.array([2*x, 20*y])

def rosenbrock(xy):
    x, y = xy
    return (1 - x)**2 + 100*(y - x**2)**2

def grad_rosenbrock(xy):
    x, y = xy
    dx = -2*(1 - x) - 400*x*(y - x**2)
    dy = 200*(y - x**2)
    return np.array([dx, dy])


print("=" * 60)
print("Optimizer Comparison: Adam, RMSprop, AdaGrad, SGD")
print("=" * 60)

def optimize(f, grad_f, x0, optimizer, name, max_iter=500, tolerance=1e-6):
    x = np.array(x0, dtype=float)
    path = [x.copy()]
    
    params = {'x': x}
    opt = type(optimizer)({'x': x}, lr=optimizer.lr)
    
    for i in range(max_iter):
        gradients = {'x': grad_f(x)}
        params = opt.step(gradients)
        x = params['x']
        path.append(x.copy())
        
        if np.linalg.norm(gradients['x']) < tolerance:
            break
    
    return x, np.array(path), len(path) - 1

x0 = [3.0, 3.0]

print("\n1. Elliptic Function: f(x,y) = x² + 10y²")
print(f"   Starting point: {x0}")
print("-" * 60)

optimizers = {
    'SGD (lr=0.1)': SGD({'x': np.array(x0)}, lr=0.1),
    'SGD + Momentum': SGD({'x': np.array(x0)}, lr=0.1, momentum=0.9),
    'RMSprop': RMSprop({'x': np.array(x0)}, lr=0.1),
    'AdaGrad': AdaGrad({'x': np.array(x0)}, lr=0.5),
    'Adam': Adam({'x': np.array(x0)}, lr=0.5),
}

print(f"{'Optimizer':<20} | {'Steps':>6} | {'Final (x,y)':>20}")
print("-" * 60)

results = {}
for name, opt in optimizers.items():
    final, path, steps = optimize(f, grad_f, x0, opt, name)
    results[name] = (final, path)
    print(f"{name:<20} | {steps:>6} | ({final[0]:8.4f}, {final[1]:8.4f})")

if HAS_MATPLOTLIB:
    fig, axes = plt.subplots(2, 3, figsize=(14, 9))

    xx, yy = np.meshgrid(np.linspace(-4, 4, 50), np.linspace(-4, 4, 50))
    zz = np.array([[f([x, y]) for x, y in zip(xx_row, yy_row)] 
                   for xx_row, yy_row in zip(xx, yy)])

    for idx, (name, (final, path)) in enumerate(results.items()):
        ax = axes[idx // 3, idx % 3]
        ax.contour(xx, yy, zz, levels=15, cmap='viridis')
        path = np.array(path)
        ax.plot(path[:, 0], path[:, 1], 'r.-', markersize=5, linewidth=1.5)
        ax.plot(path[0, 0], path[0, 1], 'go', markersize=10, label='Start')
        ax.plot(path[-1, 0], path[-1, 1], 'r*', markersize=12, label='End')
        ax.set_title(name)
        ax.grid(True, alpha=0.3)

    axes[1, 2].axis('off')
    plt.tight_layout()
    plt.savefig('/Users/Shared/ccc/mybook/ai-teach-you/ai/_code/06/optimizer_viz.png', dpi=150)
    plt.close()
    print("\n[Visualization saved to optimizer_viz.png]")
else:
    print("\n[Skipping visualization - matplotlib not available]")

print("\n" + "=" * 60)
print("Rosenbrock Function Test (more challenging)")
print("=" * 60)
print("\nRosenbrock: f(x,y) = (1-x)² + 100(y-x²)²")
print("Global minimum at (1, 1)")
print("-" * 60)

x0_rosen = [0.0, 0.0]

optimizers_rosen = {
    'SGD (lr=0.001)': SGD({'x': np.array(x0_rosen)}, lr=0.001),
    'SGD + Momentum': SGD({'x': np.array(x0_rosen)}, lr=0.001, momentum=0.9),
    'RMSprop': RMSprop({'x': np.array(x0_rosen)}, lr=0.01),
    'Adam': Adam({'x': np.array(x0_rosen)}, lr=0.01),
}

print(f"{'Optimizer':<20} | {'Steps':>6} | {'Final (x,y)':>22}")
print("-" * 60)

for name, opt in optimizers_rosen.items():
    final, path, steps = optimize(rosenbrock, grad_rosenbrock, x0_rosen, opt, name, max_iter=5000)
    print(f"{name:<20} | {steps:>6} | ({final[0]:10.4f}, {final[1]:10.4f})")

print("\n" + "=" * 60)
print("Optimizer Summary")
print("=" * 60)
print("""
Adam (Adaptive Moment Estimation):
  - Combines Momentum + RMSprop
  - Maintains first moment (m) and second moment (v) estimates
  - Bias-corrected estimates
  - Best general-purpose optimizer
  
RMSprop:
  - Divides gradient by running average of gradient magnitudes
  - Effective for non-stationary objectives
  
AdaGrad:
  - Adapts learning rate based on past gradients
  - Good for sparse gradients, but learning rate can become too small
  
SGD + Momentum:
  - Classic approach with momentum
  - Requires careful learning rate tuning
  - Good baseline
""")

print("=" * 60)
print("Optimizer Demo Complete")
print("=" * 60)
