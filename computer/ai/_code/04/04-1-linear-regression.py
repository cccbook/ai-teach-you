import numpy as np

try:
    from sklearn.linear_model import LinearRegression
    from sklearn.datasets import make_regression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_squared_error, r2_score
    USE_SKLEARN = True
except ImportError:
    USE_SKLEARN = False


def gradient_descent(X, y, lr=0.01, epochs=1000):
    m, n = X.shape
    weights = np.zeros(n)
    bias = 0

    for _ in range(epochs):
        y_pred = X @ weights + bias
        dw = (2/m) * X.T @ (y_pred - y)
        db = (2/m) * np.sum(y_pred - y)
        weights -= lr * dw
        bias -= lr * db

    return weights, bias


def predict_gd(X, weights, bias):
    return X @ weights + bias


def main():
    np.random.seed(42)
    X, y = make_regression(n_samples=100, n_features=1, noise=10, random_state=42)
    y = y.reshape(-1, 1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    if USE_SKLEARN:
        print("Using sklearn LinearRegression")
        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        print(f"Coefficient: {model.coef_[0][0]:.4f}")
        print(f"Intercept: {model.intercept_[0]:.4f}")
    else:
        print("Using pure Python gradient descent")
        weights, bias = gradient_descent(X_train, y_train, lr=0.01, epochs=1000)
        y_pred = predict_gd(X_test, weights, bias)
        print(f"Weights: {weights.flatten()}")
        print(f"Bias: {bias}")

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"MSE: {mse:.4f}")
    print(f"R2 Score: {r2:.4f}")

    print("\nDemo: Predicting new values")
    X_new = np.array([[0], [5], [10]])
    if USE_SKLEARN:
        print(f"Input: {X_new.flatten()}")
        print(f"Predictions: {model.predict(X_new).flatten()}")
    else:
        print(f"Input: {X_new.flatten()}")
        print(f"Predictions: {predict_gd(X_new, weights, bias).flatten()}")


if __name__ == "__main__":
    main()
