"""
Support Vector Machine (SVM) Implementation
Simple linear SVM using gradient descent
"""

import numpy as np


class SimpleSVM:
    def __init__(self, learning_rate=0.01, lambda_param=0.01, n_iters=1000):
        self.lr = learning_rate
        self.lambda_param = lambda_param
        self.n_iters = n_iters
        self.weights = None
        self.bias = None
    
    def fit(self, X, y):
        """Train SVM using gradient descent"""
        n_samples, n_features = X.shape
        y_ = np.where(y <= 0, -1, 1)
        
        self.weights = np.zeros(n_features)
        self.bias = 0
        
        for _ in range(self.n_iters):
            for idx, x_i in enumerate(X):
                condition = y_[idx] * (np.dot(x_i, self.weights) + self.bias) >= 1
                
                if condition:
                    self.weights -= self.lr * (2 * self.lambda_param * self.weights)
                else:
                    self.weights -= self.lr * (
                        2 * self.lambda_param * self.weights -
                        np.dot(x_i, y_[idx])
                    )
                    self.bias -= self.lr * y_[idx]
    
    def predict(self, X):
        """Predict class labels for samples"""
        linear_output = np.dot(X, self.weights) + self.bias
        return np.sign(linear_output)


def accuracy(y_true, y_pred):
    """Calculate classification accuracy"""
    return np.mean(y_true == y_pred)


if __name__ == "__main__":
    np.random.seed(42)
    
    X1 = np.random.randn(50, 2) + np.array([2, 2])
    X2 = np.random.randn(50, 2) + np.array([-2, -2])
    X = np.vstack((X1, X2))
    y = np.hstack((np.ones(50), -np.ones(50)))
    
    print("=== Support Vector Machine (Linear) ===")
    print(f"Training samples: {len(X)}")
    print(f"Features: 2D points")
    print(f"Classes: +1 (blue), -1 (red)\n")
    
    svm = SimpleSVM(learning_rate=0.01, lambda_param=0.01, n_iters=1000)
    svm.fit(X, y)
    
    predictions = svm.predict(X)
    acc = accuracy(y, predictions)
    print(f"Training accuracy: {acc * 100:.2f}%")
    
    test_points = [
        [3, 3],    # should be +1
        [-3, -3],  # should be -1
        [0, 0],    # near boundary
        [2, -2],   # should be -1
    ]
    
    print("\nTest predictions:")
    for point in test_points:
        pred = svm.predict(np.array([point]))[0]
        label = "+1" if pred == 1 else "-1"
        print(f"  Point {point} -> Class {label}")
    
    print(f"\nLearned weights: {svm.weights}")
    print(f"Learned bias: {svm.bias:.4f}")
