import numpy as np

try:
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
    USE_SKLEARN = True
except ImportError:
    USE_SKLEARN = False


def euclidean_distance(x1, x2):
    return np.sqrt(np.sum((x1 - x2) ** 2))


class KNN:
    def __init__(self, k=3):
        self.k = k
        self.X_train = None
        self.y_train = None

    def fit(self, X, y):
        self.X_train = X
        self.y_train = y

    def predict(self, X):
        predictions = []
        for x in X:
            distances = [euclidean_distance(x, x_train) for x_train in self.X_train]
            k_indices = np.argsort(distances)[:self.k]
            k_labels = self.y_train[k_indices]
            counts = np.bincount(k_labels)
            predictions.append(np.argmax(counts))
        return np.array(predictions)


def main():
    np.random.seed(42)
    X, y = make_classification(n_samples=100, n_features=2, n_informative=2,
                               n_redundant=0, n_clusters_per_class=1, random_state=42)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    k = 5

    if USE_SKLEARN:
        print("Using sklearn KNeighborsClassifier")
        model = KNeighborsClassifier(n_neighbors=k)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
    else:
        print("Using pure Python KNN")
        model = KNN(k=k)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {acc:.4f}")

    print("\nDemo: Predicting new values")
    X_new = np.array([[0, 0], [2, 2], [-1, 1]])
    if USE_SKLEARN:
        print(f"Input: {X_new}")
        print(f"Predictions: {model.predict(X_new)}")
    else:
        print(f"Input: {X_new}")
        print(f"Predictions: {model.predict(X_new)}")


if __name__ == "__main__":
    main()
