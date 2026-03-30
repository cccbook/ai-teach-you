import numpy as np

try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Note: matplotlib not available, skipping visualization")

print("=" * 60)
print("Numerical Gradient Computation")
print("=" * 60)

print("""
Numerical Gradient is a method to compute gradients without using
the analytical derivatives. It uses the definition of derivative:

f'(x) = lim[h→0] (f(x+h) - f(x-h)) / 2h

This is called the "central difference" method.
""")

def f(x, y, z):
    return (x - 1)**2 + (y - 2)**2 + (z - 3)**2

def analytical_gradient(x, y, z):
    df_dx = 2 * (x - 1)
    df_dy = 2 * (y - 2)
    df_dz = 2 * (z - 3)
    return np.array([df_dx, df_dy, df_dz])

def numerical_gradient(f, x, y, z, h=1e-5):
    grad = np.zeros(3)
    
    grad[0] = (f(x + h, y, z) - f(x - h, y, z)) / (2 * h)
    grad[1] = (f(x, y + h, z) - f(x, y - h, z)) / (2 * h)
    grad[2] = (f(x, y, z + h) - f(x, y, z - h)) / (2 * h)
    
    return grad

print("=" * 60)
print("Test Function: f(x,y,z) = (x-1)² + (y-2)² + (z-3)²")
print("=" * 60)

print("\nThis function has its minimum at (1, 2, 3)")
print("The gradient points toward this minimum.")

test_points = [
    (0.0, 0.0, 0.0, "origin"),
    (5.0, 5.0, 5.0, "far point"),
    (1.0, 2.0, 3.0, "minimum"),
    (2.0, 3.0, 4.0, "near minimum"),
]

print("\n" + "-" * 70)
print(f"{'Point':<25} | {'Analytical':<20} | {'Numerical':<20}")
print("-" * 70)

for x, y, z, label in test_points:
    analytic = analytical_gradient(x, y, z)
    numeric = numerical_gradient(f, x, y, z)
    
    print(f"{label:<25} | [{analytic[0]:7.3f}, {analytic[1]:7.3f}, {analytic[2]:7.3f}] | [{numeric[0]:7.3f}, {numeric[1]:7.3f}, {numeric[2]:7.3f}]")

print("\n" + "=" * 60)
print("Error Analysis: Effect of Step Size h")
print("=" * 60)

x, y, z = 3.0, 4.0, 5.0
true_grad = analytical_gradient(x, y, z)

print(f"\nTest point: ({x}, {y}, {z})")
print(f"True gradient: {true_grad}")
print("\n" + "-" * 50)
print(f"{'h':<15} | {'Error':<15} | {'Error (log10)'}")
print("-" * 50)

h_values = [1.0, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-9, 1e-10]

errors = []
for h in h_values:
    num_grad = numerical_gradient(f, x, y, z, h)
    error = np.linalg.norm(num_grad - true_grad)
    errors.append(error)
    print(f"{h:<15.1e} | {error:<15.10f} | {np.log10(error + 1e-15):.1f}")

if HAS_MATPLOTLIB:
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].semilogx(h_values, errors, 'bo-', linewidth=2, markersize=8)
    axes[0].axvline(x=1e-5, color='r', linestyle='--', label='Optimal h ≈ 1e-5')
    axes[0].set_xlabel('Step size h', fontsize=12)
    axes[0].set_ylabel('Absolute Error', fontsize=12)
    axes[0].set_title('Numerical Gradient Error vs Step Size', fontsize=14)
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    axes[1].plot([0, 1, 2, 3], [0, 2, 4, 6], 'b-', linewidth=2, label='Analytical: 2(x-1)')
    axes[1].plot([0, 1, 2, 3], [0, 2.002, 4.004, 6.006], 'r--', linewidth=2, label='Numerical (h=0.01)')
    axes[1].set_xlabel('x (y=z=0)', fontsize=12)
    axes[1].set_ylabel('df/dx', fontsize=12)
    axes[1].set_title('Gradient Comparison (1D slice)', fontsize=14)
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/Users/Shared/ccc/mybook/ai-teach-you/ai/_code/06/numerical_gradient_viz.png', dpi=150)
    plt.close()
    print("\n[Visualization saved to numerical_gradient_viz.png]")
else:
    print("\n[Skipping visualization - matplotlib not available]")

print("\n" + "=" * 60)
print("Why Numerical Gradient?")
print("=" * 60)
print("""
1. Verification: Check if analytical gradients are correct
2. Debugging: Find bugs in gradient computation
3. Automatic Differentiation: Foundation for modern frameworks

Limitations:
- O(2n) function evaluations for n parameters (slow for large networks)
- Numerical precision issues with very small h
- Cannot compute second-order derivatives efficiently
""")

print("\n" + "=" * 60)
print("Gradient Descent using Numerical Gradients")
print("=" * 60)

def gradient_descent_numerical(f, x0, y0, z0, lr=0.1, max_iter=50):
    x, y, z = x0, y0, z0
    path = [(x, y, z)]
    
    for i in range(max_iter):
        grad = numerical_gradient(f, x, y, z)
        x = x - lr * grad[0]
        y = y - lr * grad[1]
        z = z - lr * grad[2]
        path.append((x, y, z))
    
    return (x, y, z), path

x0, y0, z0 = 0.0, 0.0, 0.0
optimum, path = gradient_descent_numerical(f, x0, y0, z0, lr=0.1)

print(f"\nStarting point: ({x0}, {y0}, {z0})")
print(f"Found minimum: ({optimum[0]:.4f}, {optimum[1]:.4f}, {optimum[2]:.4f})")
print(f"Expected: (1.0, 2.0, 3.0)")
print(f"Function value at minimum: {f(*optimum):.6f}")

print("\nOptimization path (first 10 steps):")
for i, (x, y, z) in enumerate(path[:10]):
    print(f"  Step {i}: ({x:.3f}, {y:.3f}, {z:.3f})")

print("\n" + "=" * 60)
print("Numerical Gradient Demo Complete")
print("=" * 60)
