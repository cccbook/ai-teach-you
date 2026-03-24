import numpy as np

try:
    from sklearn.svm import SVC
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
    from sklearn.preprocessing import StandardScaler
    USE_SKLEARN = True
except ImportError:
    USE_SKLEARN = False


def kernel_linear(x1, x2):
    return np.dot(x1, x2)


def kernel_rbf(x1, x2, gamma=0.1):
    return np.exp(-gamma * np.sum((x1 - x2) ** 2))


class SVM:
    def __init__(self, kernel='linear', C=1.0, gamma=0.1, epochs=1000):
        self.kernel = kernel
        self.C = C
        self.gamma = gamma
        self.epochs = epochs
        self.alphas = None
        self.b = 0
        self.X_train = None
        self.y_train = None

    def _compute_kernel(self, x1, x2):
        if self.kernel == 'linear':
            return kernel_linear(x1, x2)
        return kernel_rbf(x1, x2, self.gamma)

    def fit(self, X, y):
        self.X_train = X
        self.y_train = y
        n_samples, n_features = X.shape
        self.alphas = np.zeros(n_samples)
        self.b = 0

        for _ in range(self.epochs):
            for i in range(n_samples):
                j = np.random.randint(0, n_samples)
                while j == i:
                    j = np.random.randint(0, n_samples)

                ei = sum(self.alphas[j] * self.y_train[j] * self._compute_kernel(X[i], X[j])) + self.b - self.y_train[i]
                ej = sum(self.alphas[j] * self.y_train[j] * self._compute_kernel(X[i], X[j])) + self.b - self.y_train[j]

                if (self.y_train[i] != self.y_train[j] and abs(self.alphas[i] - self.alphas[j]) > 0) or \
                   (self.y_train[i] == self.y_train[j] and abs(self.alphas[i] + self.alphas[j]) > self.C):
                    continue

                alpha_i_old = self.alphas[i]
                alpha_j_old = self.alphas[j]

                L = max(0, self.alphas[j] - self.alphas[i]) if self.y_train[i] == self.y_train[j] else max(0, self.alphas[j] + self.alphas[i] - self.C)
                H = min(self.C, self.C + self.alphas[j] - self.alphas[i]) if self.y_train[i] == self.y_train[j] else min(self.C, self.alphas[j] + self.alphas[i])

                if L >= H:
                    continue

                eta = 2 * self._compute_kernel(X[i], X[j]) - self._compute_kernel(X[i], X[i]) - self._compute_kernel(X[j], X[j])
                if eta >= 0:
                    continue

                self.alphas[j] -= (self.y_train[j] * (ei - ej)) / eta
                self.alphas[j] = np.clip(self.alphas[j], L, H)

                self.alphas[i] += self.y_train[i] * self.y_train[j] * (alpha_j_old - self.alphas[j])

                b1 = self.b - ei - self.y_train[i] * (self.alphas[i] - alpha_i_old) * self._compute_kernel(X[i], X[i]) - \
                     self.y_train[j] * (self.alphas[j] - alpha_j_old) * self._compute_kernel(X[i], X[j])
                b2 = self.b - ej - self.y_train[i] * (self.alphas[i] - alpha_i_old) * self._compute_kernel(X[i], X[j]) - \
                     self.y_train[j] * (self.alphas[j] - alpha_j_old) * self._compute_kernel(X[j], X[j])

                if 0 < self.alphas[i] < self.C:
                    self.b = b1
                elif 0 < self.alphas[j] < self.C:
                    self.b = b2
                else:
                    self.b = (b1 + b2) / 2

    def predict(self, X):
        result = np.zeros(X.shape[0])
        for i in range(X.shape[0]):
            result[i] = sum(self.alphas[j] * self.y_train[j] * self._compute_kernel(X[i], self.X_train[j]) for j in range(len(self.alphas))) + self.b
        return np.sign(result)


def main():
    np.random.seed(42)
    X, y = make_classification(n_samples=100, n_features=2, n_informative=2,
                               n_redundant=0, n_clusters_per_class=1, random_state=42)
    y = np.where(y == 0, -1, 1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    if USE_SKLEARN:
        print("Using sklearn SVC")
        model = SVC(kernel='linear', C=1.0, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
    else:
        print("Using pure Python SVM")
        model = SVM(kernel='linear', C=1.0, epochs=100)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {acc:.4f}")

    print("\nDemo: Predicting new values")
    X_new = np.array([[0, 0], [2, 2], [-1, 1]])
    X_new = scaler.transform(X_new)
    if USE_SKLEARN:
        print(f"Input: {X_new}")
        print(f"Predictions: {model.predict(X_new)}")
    else:
        print(f"Input: {X_new}")
        print(f"Predictions: {model.predict(X_new)}")


if __name__ == "__main__":
    main()
