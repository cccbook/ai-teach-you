import numpy as np

try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
    USE_SKLEARN = True
except ImportError:
    USE_SKLEARN = False


class DecisionTreeNode:
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value
        self.is_leaf = value is not None


def gini_impurity(labels):
    if len(labels) == 0:
        return 0
    counts = np.bincount(labels)
    probs = counts / len(labels)
    return 1 - np.sum(probs ** 2)


def best_split(X, y):
    best_gini = float('inf')
    best_feature, best_threshold = None, None

    for feature in range(X.shape[1]):
        thresholds = np.unique(X[:, feature])
        for threshold in (thresholds[1:] + thresholds[:-1]) / 2:
            left = y[X[:, feature] <= threshold]
            right = y[X[:, feature] > threshold]
            if len(left) == 0 or len(right) == 0:
                continue
            gini = (len(left) * gini_impurity(left) + len(right) * gini_impurity(right)) / len(y)
            if gini < best_gini:
                best_gini = gini
                best_feature = feature
                best_threshold = threshold

    return best_feature, best_threshold


def build_tree(X, y, depth=0, max_depth=5):
    if len(np.unique(y)) == 1 or depth >= max_depth:
        return DecisionTreeNode(value=np.bincount(y).argmax())

    feature, threshold = best_split(X, y)
    if feature is None:
        return DecisionTreeNode(value=np.bincount(y).argmax())

    left_idx = X[:, feature] <= threshold
    right_idx = X[:, feature] > threshold

    left = build_tree(X[left_idx], y[left_idx], depth + 1, max_depth)
    right = build_tree(X[right_idx], y[right_idx], depth + 1, max_depth)

    return DecisionTreeNode(feature, threshold, left, right)


def predict_tree(node, x):
    if node.is_leaf:
        return node.value
    if x[node.feature] <= node.threshold:
        return predict_tree(node.left, x)
    return predict_tree(node.right, x)


def predict(tree, X):
    return np.array([predict_tree(tree, x) for x in X])


class RandomForest:
    def __init__(self, n_estimators=10, max_depth=5, random_state=None):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.random_state = random_state
        self.trees = []

    def fit(self, X, y):
        np.random.seed(self.random_state)
        n_samples = X.shape[0]
        for _ in range(self.n_estimators):
            indices = np.random.choice(n_samples, n_samples, replace=True)
            X_boot = X[indices]
            y_boot = y[indices]
            tree = build_tree(X_boot, y_boot, max_depth=self.max_depth)
            self.trees.append(tree)
        return self

    def predict(self, X):
        preds = np.array([predict(tree, X) for tree in self.trees])
        result = np.apply_along_axis(lambda x: np.bincount(x).argmax(), axis=0, arr=preds)
        return result


def main():
    np.random.seed(42)
    X, y = make_classification(n_samples=100, n_features=2, n_informative=2,
                               n_redundant=0, n_clusters_per_class=1, random_state=42)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    if USE_SKLEARN:
        print("Using sklearn RandomForestClassifier")
        model = RandomForestClassifier(n_estimators=10, max_depth=5, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
    else:
        print("Using pure Python Random Forest")
        model = RandomForest(n_estimators=10, max_depth=5, random_state=42)
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
