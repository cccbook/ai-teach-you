import numpy as np

try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Note: matplotlib not available, skipping visualization")

class SGD:
    def __init__(self, params, lr=0.01, momentum=0.0):
        self.lr = lr
        self.momentum = momentum
        self.velocity = {k: np.zeros_like(v) for k, v in params.items()}
    
    def step(self, params, gradients):
        for k in params:
            if self.momentum > 0:
                self.velocity[k] = self.momentum * self.velocity[k] - self.lr * gradients[k]
                params[k] = params[k] + self.velocity[k]
            else:
                params[k] = params[k] - self.lr * gradients[k]
        return params


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
print("SGD with Momentum Visualization")
print("=" * 60)

def optimize(f, grad_f, x0, optimizer, max_iter=100, tolerance=1e-6):
    x = np.array(x0, dtype=float)
    path = [x.copy()]
    
    params = {'x': x}
    gradients = {'x': np.zeros_like(x)}
    
    for i in range(max_iter):
        gradients['x'] = grad_f(x)
        params = optimizer.step(params, gradients)
        x = params['x']
        path.append(x.copy())
        
        if np.linalg.norm(gradients['x']) < tolerance:
            break
    
    return x, np.array(path)

x0 = [3.0, 3.0]
lr = 0.01

results = {}
optimizers = {
    'SGD': SGD({'x': np.array(x0)}, lr=lr, momentum=0.0),
    'SGD (m=0.5)': SGD({'x': np.array(x0)}, lr=lr, momentum=0.5),
    'SGD (m=0.9)': SGD({'x': np.array(x0)}, lr=lr, momentum=0.9),
    'SGD (m=0.99)': SGD({'x': np.array(x0)}, lr=lr, momentum=0.99),
}

print("\nTest Function: f(x,y) = x² + 10y² (elongated valley)")
print(f"Starting point: {x0}")
print(f"Learning rate: {lr}")
print("-" * 60)
print(f"{'Optimizer':<20} | {'Steps':>6} | {'Final Position':>20}")
print("-" * 60)

for name, opt in optimizers.items():
    opt_copy = SGD({'x': np.array(x0)}, lr=lr, momentum=opt.momentum)
    final, path = optimize(f, grad_f, x0, opt_copy)
    steps = len(path) - 1
    results[name] = (final, path)
    print(f"{name:<20} | {steps:>6} | ({final[0]:8.4f}, {final[1]:8.4f})")

if HAS_MATPLOTLIB:
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    xx, yy = np.meshgrid(np.linspace(-4, 4, 50), np.linspace(-4, 4, 50))
    zz = np.array([[f([x, y]) for x, y in zip(xx_row, yy_row)] 
                   for xx_row, yy_row in zip(xx, yy)])

    for idx, (name, (final, path)) in enumerate(results.items()):
        ax = axes[idx // 2, idx % 2]
        ax.contour(xx, yy, zz, levels=20, cmap='viridis')
        ax.contour(xx, yy, zz, levels=[1, 5, 10, 20], colors='white', linewidths=0.5, alpha=0.5)
        
        path = np.array(path)
        ax.plot(path[:, 0], path[:, 1], 'r.-', markersize=6, linewidth=1.5)
        ax.plot(path[0, 0], path[0, 1], 'go', markersize=10, label='Start')
        ax.plot(path[-1, 0], path[-1, 1], 'r*', markersize=12, label='End')
        
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title(f'{name}')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/Users/Shared/ccc/mybook/ai-teach-you/ai/_code/06/sgd_momentum_viz.png', dpi=150)
    plt.close()
    print("\n[Visualization saved to sgd_momentum_viz.png]")
else:
    print("\n[Skipping visualization - matplotlib not available]")

print("\n" + "=" * 60)
print("Momentum Comparison (Rosenbrock)")
print("=" * 60)

print("\nRosenbrock function: f(x,y) = (1-x)² + 100(y-x²)²")
print("Known minimum at (1, 1)")
print("-" * 60)

x0_rosen = [0.0, 0.0]
lr_rosen = 0.001

momentum_values = [0.0, 0.5, 0.9, 0.95]
print(f"{'Momentum':>12} | {'Steps':>6} | {'Final (x,y)':>22}")
print("-" * 50)

for m in momentum_values:
    opt = SGD({'x': np.array(x0_rosen)}, lr=lr_rosen, momentum=m)
    final, path = optimize(rosenbrock, grad_rosenbrock, x0_rosen, opt, max_iter=5000)
    steps = len(path) - 1
    print(f"{m:>12.2f} | {steps:>6} | ({final[0]:10.4f}, {final[1]:10.4f})")

print("\n" + "=" * 60)
print("Momentum Physics Explanation")
print("=" * 60)
print("""
Momentum acts like a ball rolling down a hill:
- velocity accumulates over time
- helps escape local minima and saddle points
- overshoots minimum then comes back (oscillation)
- effective for ill-conditioned (elongated) landscapes

Formula: v_t = β*v_{t-1} + (1-β)*∇L
         θ_t = θ_{t-1} - lr * v_t
         
where β (momentum) is typically 0.9
""")

print("=" * 60)
print("SGD with Momentum Demo Complete")
print("=" * 60)
