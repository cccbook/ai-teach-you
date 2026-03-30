import numpy as np

try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Note: matplotlib not available, skipping visualization")

def gradient_descent(f, grad_f, x0, learning_rate=0.1, max_iter=50, tolerance=1e-6):
    x = np.array(x0, dtype=float)
    path = [x.copy()]
    
    for i in range(max_iter):
        gradient = grad_f(x)
        x = x - learning_rate * gradient
        path.append(x.copy())
        
        if np.linalg.norm(gradient) < tolerance:
            break
    
    return x, np.array(path)

def f(x):
    return x[0]**2 + x[1]**2

def grad_f(x):
    return np.array([2*x[0], 2*x[1]])

def f_elliptic(x):
    return x[0]**2 + 10*x[1]**2

def grad_f_elliptic(x):
    return np.array([2*x[0], 20*x[1]])

def f_saddle(x):
    return x[0]**2 - x[1]**2

def grad_f_saddle(x):
    return np.array([2*x[0], -2*x[1]])

x0 = [4.0, 3.0]
learning_rate = 0.1

print("=" * 60)
print("Gradient Descent Visualization")
print("=" * 60)

print("\n1. Simple Quadratic: f(x,y) = x² + y²")
print(f"   Starting point: {x0}")
optimum, path = gradient_descent(f, grad_f, x0, learning_rate)
print(f"   Found optimum at: {optimum}")
print(f"   Steps taken: {len(path)-1}")
print(f"   Path: {path[:5].tolist()}...")

print("\n2. Elliptic Quadratic: f(x,y) = x² + 10y²")
print(f"   Starting point: {x0}")
optimum, path = gradient_descent(f_elliptic, grad_f_elliptic, x0, learning_rate)
print(f"   Found optimum at: {optimum}")
print(f"   Steps taken: {len(path)-1}")

print("\n3. Saddle Point: f(x,y) = x² - y²")
print(f"   Starting point: {x0}")
optimum, path = gradient_descent(f_saddle, grad_f_saddle, x0, learning_rate, max_iter=20)
print(f"   Steps taken: {len(path)-1}")
print(f"   Final point: {optimum} (saddle point behavior)")

if HAS_MATPLOTLIB:
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    def plot_contour(ax, f, path, title, xlim=(-5, 5), ylim=(-5, 5)):
        xx, yy = np.meshgrid(np.linspace(*xlim, 50), np.linspace(*ylim, 50))
        zz = np.array([[f([x, y]) for x, y in zip(xx_row, yy_row)] 
                       for xx_row, yy_row in zip(xx, yy)])
        
        ax.contour(xx, yy, zz, levels=20, cmap='viridis')
        ax.contour(xx, yy, zz, levels=[1, 5, 10, 20], colors='white', linewidths=0.5, alpha=0.5)
        
        path = np.array(path)
        ax.plot(path[:, 0], path[:, 1], 'r.-', markersize=8, linewidth=2, label='Gradient descent')
        ax.plot(path[0, 0], path[0, 1], 'go', markersize=12, label='Start', zorder=5)
        ax.plot(path[-1, 0], path[-1, 1], 'r*', markersize=15, label='End', zorder=5)
        
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title(title)
        ax.legend(loc='upper right', fontsize=8)
        ax.grid(True, alpha=0.3)

    x0 = [4.0, 3.0]
    lr = 0.1

    _, path1 = gradient_descent(f, grad_f, x0, lr)
    _, path2 = gradient_descent(f_elliptic, grad_f_elliptic, x0, lr)
    _, path3 = gradient_descent(f_saddle, grad_f_saddle, x0, lr, max_iter=15)

    plot_contour(axes[0], f, path1, 'f(x,y) = x² + y²')
    plot_contour(axes[1], f_elliptic, path2, 'f(x,y) = x² + 10y²')
    plot_contour(axes[2], f_saddle, path3, 'f(x,y) = x² - y² (saddle)', ylim=(-5, 5))

    plt.tight_layout()
    plt.savefig('/Users/Shared/ccc/mybook/ai-teach-you/ai/_code/06/gradient_descent_viz.png', dpi=150)
    plt.close()

    print("\n[Visualization saved to gradient_descent_viz.png]")
else:
    print("\n[Skipping visualization - matplotlib not available]")

print("\n" + "=" * 60)
print("Learning Rate Effects")
print("=" * 60)

lr_test = [0.001, 0.01, 0.1, 0.5, 0.9, 1.1]
print("\nLearning rate | Steps to converge | Final position")
print("-" * 55)

for lr in lr_test:
    _, path = gradient_descent(f, grad_f, x0, lr, max_iter=100)
    final = path[-1]
    steps = len(path) - 1
    print(f"     {lr:5.3f}    |        {steps:3d}        | {final}")

print("\n" + "=" * 60)
print("Convergence Analysis Complete")
print("=" * 60)
