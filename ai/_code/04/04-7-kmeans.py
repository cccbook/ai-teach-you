import numpy as np

try:
    from sklearn.cluster import KMeans
    from sklearn.datasets import make_blobs
    from sklearn.metrics import silhouette_score
    USE_SKLEARN = True
except ImportError:
    USE_SKLEARN = False


def euclidean_distance(x1, x2):
    return np.sqrt(np.sum((x1 - x2) ** 2))


class KMeansClustering:
    def __init__(self, n_clusters=3, max_iter=100, random_state=None):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.random_state = random_state
        self.centroids = None

    def fit(self, X):
        np.random.seed(self.random_state)
        indices = np.random.choice(X.shape[0], self.n_clusters, replace=False)
        self.centroids = X[indices]

        for _ in range(self.max_iter):
            labels = np.zeros(X.shape[0])
            for i, x in enumerate(X):
                distances = [euclidean_distance(x, c) for c in self.centroids]
                labels[i] = np.argmin(distances)

            new_centroids = np.zeros((self.n_clusters, X.shape[1]))
            for k in range(self.n_clusters):
                cluster_points = X[labels == k]
                if len(cluster_points) > 0:
                    new_centroids[k] = cluster_points.mean(axis=0)

            if np.allclose(self.centroids, new_centroids):
                break
            self.centroids = new_centroids

        return self

    def predict(self, X):
        labels = np.zeros(X.shape[0])
        for i, x in enumerate(X):
            distances = [euclidean_distance(x, c) for c in self.centroids]
            labels[i] = np.argmin(distances)
        return labels.astype(int)

    def fit_predict(self, X):
        self.fit(X)
        return self.predict(X)


def main():
    np.random.seed(42)
    X, y = make_blobs(n_samples=100, centers=3, n_features=2, random_state=42)

    n_clusters = 3

    if USE_SKLEARN:
        print("Using sklearn KMeans")
        model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = model.fit_predict(X)
    else:
        print("Using pure Python K-Means")
        model = KMeans(n_clusters=n_clusters, random_state=42)
        labels = model.fit_predict(X)

    silhouette = silhouette_score(X, labels)
    print(f"Silhouette Score: {silhouette:.4f}")

    unique, counts = np.unique(labels, return_counts=True)
    print("Cluster distribution:")
    for cluster, count in zip(unique, counts):
        print(f"  Cluster {cluster}: {count} samples")

    print("\nDemo: New points")
    X_new = np.array([[0, 0], [5, 5], [-3, 3]])
    if USE_SKLEARN:
        print(f"Input: {X_new}")
        print(f"Cluster assignments: {model.predict(X_new)}")
    else:
        print(f"Input: {X_new}")
        print(f"Cluster assignments: {model.predict(X_new)}")


if __name__ == "__main__":
    main()
