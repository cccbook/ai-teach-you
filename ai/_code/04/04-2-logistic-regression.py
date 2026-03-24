import numpy as np

try:
    from sklearn.linear_model import LogisticRegression
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
    USE_SKLEARN = True
except ImportError:
    USE_SKLEARN = False


def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -500, 500)))


def gradient_descent(X, y, lr=0.1, epochs=1000):
    m, n = X.shape
    weights = np.zeros(n)
    bias = 0

    for _ in range(epochs):
        z = X @ weights + bias
        a = sigmoid(z)
        dw = (1/m) * X.T @ (a - y)
        db = (1/m) * np.sum(a - y)
        weights -= lr * dw
        bias -= lr * db

    return weights, bias


def predict_proba_gd(X, weights, bias):
    return sigmoid(X @ weights + bias)


def predict_gd(X, weights, bias):
    return (predict_proba_gd(X, weights, bias) >= 0.5).astype(int)


def main():
    np.random.seed(42)
    X, y = make_classification(n_samples=100, n_features=2, n_informative=2,
                               n_redundant=0, n_clusters_per_class=1, random_state=42)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    if USE_SKLEARN:
        print("Using sklearn LogisticRegression")
        model = LogisticRegression(random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        print(f"Coefficients: {model.coef_[0]}")
        print(f"Intercept: {model.intercept_[0]}")
    else:
        print("Using pure Python gradient descent")
        weights, bias = gradient_descent(X_train, y_train, lr=0.1, epochs=1000)
        y_pred = predict_gd(X_test, weights, bias)
        print(f"Weights: {weights}")
        print(f"Bias: {bias}")

    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {acc:.4f}")

    print("\nDemo: Predicting new values")
    X_new = np.array([[0, 0], [2, 2], [-1, 1]])
    if USE_SKLEARN:
        print(f"Input: {X_new}")
        print(f"Predictions: {model.predict(X_new)}")
        print(f"Probabilities: {model.predict_proba(X_new)}")
    else:
        print(f"Input: {X_new}")
        print(f"Predictions: {predict_gd(X_new, weights, bias)}")
        print(f"Probabilities: {predict_proba_gd(X_new, weights, bias)}")


if __name__ == "__main__":
    main()
