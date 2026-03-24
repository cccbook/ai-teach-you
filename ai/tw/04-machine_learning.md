# 第 4 章：機器學習與 Scikit-Learn 套件

## 4.1 監督式學習與非監督式學習

機器學習是人工智慧的一個分支，專注於讓電腦系統從資料中自動學習和改進。根據學習方式的不同，機器學習可以分為幾大類型：

### 4.1.1 監督式學習 (Supervised Learning)

監督式學習是最常見的機器學習範式。在監督式學習中，訓練資料包含輸入特徵和對應的標籤（輸出）。模型學習建立從輸入到輸出的映射關係。

分類問題的範例：
- 垃圾郵件偵測：輸入是郵件內容，輸出是「垃圾郵件」或「正常郵件」
- 圖像分類：輸入是圖像，輸出是類別標籤

迴歸問題的範例：
- 房價預測：輸入是房屋特徵，輸出是價格
- 溫度預測：輸入是歷史氣象資料，輸出是未來溫度

### 4.1.2 非監督式學習 (Unsupervised Learning)

非監督式學習的訓練資料只有輸入，沒有標籤。模型需要自己發現資料中的結構和規律。

主要任務包括：
- **聚類 (Clustering)**：將相似的樣本分組
- **降維 (Dimensionality Reduction)**：減少特徵數量的同時保留重要資訊
- **異常檢測 (Anomaly Detection)**：識別偏離正常模式的樣本

### 4.1.3 半監督式學習與強化學習

**半監督式學習**介於監督和非監督之間，使用少量標籤資料和大量未標籤資料進行訓練。

**強化學習 (Reinforcement Learning)**則是一種不同的範式：智慧體（agent）透過與環境互動，根據獎懲信號學習最優策略。

## 4.2 線性迴歸與邏輯迴歸

### 4.2.1 線性迴歸 (Linear Regression)

線性迴歸是最基本的監督式學習演算法，用於預測連續值輸出。它的目標是找到一條直線（或平面、超平面），使得預測值與真實值之間的均方誤差最小。

[程式檔案：04-1-linear-regression.py](../_code/04/04-1-linear-regression.py)

```python
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
```

線性迴歸的數學模型為：

```
y = Xw + b
```

其中 X 是輸入矩陣，w 是權重向量，b 是偏置。訓練的目標是最小化均方誤差：

```
L(w, b) = (1/m) * Σ(y_pred - y_true)²
```

### 4.2.2 邏輯迴歸 (Logistic Regression)

邏輯迴歸雖然名字中有「迴歸」，但實際上是一種分類演算法。它使用 Sigmoid 函數將線性輸出轉換為機率值。

[程式檔案：04-2-logistic-regression.py](../_code/04/04-2-logistic-regression.py)

```python
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
```

邏輯迴歸的核心是 Sigmoid 函數：

```
σ(z) = 1 / (1 + e^(-z))
```

它將任意實數映射到 (0, 1) 區間，非常適合表示機率。

## 4.3 決策樹與隨機森林

### 4.3.1 決策樹 (Decision Tree)

決策樹是一種直覺且易於解釋的分類和迴歸方法。它透過一系列的是/否問題來對樣本進行分類，就像一棵倒立的樹。

[程式檔案：04-3-decision-tree.py](../_code/04/04-3-decision-tree.py)

```python
import numpy as np

try:
    from sklearn.tree import DecisionTreeClassifier
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


def main():
    np.random.seed(42)
    X, y = make_classification(n_samples=100, n_features=2, n_informative=2,
                               n_redundant=0, n_clusters_per_class=1, random_state=42)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    if USE_SKLEARN:
        print("Using sklearn DecisionTreeClassifier")
        model = DecisionTreeClassifier(max_depth=5, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        print(f"Tree depth: {model.get_depth()}")
    else:
        print("Using pure Python Decision Tree")
        tree = build_tree(X_train, y_train, max_depth=5)
        y_pred = predict(tree, X_test)

    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {acc:.4f}")

    print("\nDemo: Predicting new values")
    X_new = np.array([[0, 0], [2, 2], [-1, 1]])
    if USE_SKLEARN:
        print(f"Input: {X_new}")
        print(f"Predictions: {model.predict(X_new)}")
    else:
        print(f"Input: {X_new}")
        print(f"Predictions: {predict(tree, X_new)}")


if __name__ == "__main__":
    main()
```

決策樹的生長過程中，每一步都需要選擇最佳的分隔特徵和閾值。我們使用**基尼不純度 (Gini Impurity)**來衡量資料的純度：

```
Gini = 1 - Σ(p_i)²
```

其中 p_i 是類別 i 所佔的比例。基尼不純度越低，資料越純。

### 4.3.2 隨機森林 (Random Forest)

單棵決策樹容易過擬合，且對資料的微小變化敏感。隨機森林透過集成多棵決策樹來解決這個問題。

[程式檔案：04-4-random-forest.py](../_code/04/04-4-random-forest.py)

```python
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
```

隨機森林的核心思想是「三個臭皮匠，勝過一個諸葛亮」：
1. **自助抽樣 (Bootstrap Sampling)**：每棵樹使用不同的抽樣資料
2. **特徵隨機選擇**：每棵樹在每次分裂時只考慮部分特徵
3. **投票機制**：最終預測由所有樹的投票結果決定

## 4.4 支持向量機 (SVM)

支持向量機是一種強大的分類演算法，特別適合處理高維度資料和非線性分類問題。

[程式檔案：04-5-svm.py](../_code/04/04-5-svm.py)

```python
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
```

SVM 的核心思想是找到一個能夠最大化類別間隔（margin）的超平面。間隔越大，模型的泛化能力通常越好。

## 4.5 K-Nearest Neighbors 與 Clustering

### 4.5.1 K 最近鄰 (KNN)

KNN 是一種簡單但有效的分類和迴歸方法。它的核心思想是「近朱者赤，近墨者黑」——一個樣本的類別由其最近的 K 個鄰居決定。

[程式檔案：04-6-knn.py](../_code/04/04-6-knn.py)

```python
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
```

KNN 的 K 值選擇很重要：
- K 太小：容易過擬合，對噪聲敏感
- K 太大：模型太簡單，可能欠擬合

### 4.5.2 K-Means 聚類

K-Means 是一種經典的非監督式學習演算法，用於將資料分為 K 個簇。

[程式檔案：04-7-kmeans.py](../_code/04/04-7-kmeans.py)

```python
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
```

K-Means 的演算法步驟：
1. 隨機選擇 K 個初始中心點
2. 將每個樣本分配給最近的中心點所屬的簇
3. 重新計算每個簇的中心點
4. 重複步驟 2-3 直到收斂

## 4.6 Scikit-Learn 教學：實作經典機器學習演算法

Scikit-Learn 是 Python 中最流行的機器學習庫之一，它提供了統一的 API 接口，讓使用者可以方便地切換不同的機器學習演算法。

### 4.6.1 Scikit-Learn 的核心 API

Scikit-Learn 的估計器 (Estimator) 遵循統一的 API 設計：

```python
# 1. 選擇模型
model = SomeClassifier()

# 2. 訓練模型
model.fit(X_train, y_train)

# 3. 預測
y_pred = model.predict(X_test)

# 4. 評估
accuracy = accuracy_score(y_test, y_pred)
```

### 4.6.2 資料預處理

真實世界的資料通常需要預處理，包括：
- **缺失值處理**：填補或刪除缺失資料
- **特徵縮放**：標準化或歸一化
- **類別編碼**：將類別變數轉換為數值

### 4.6.3 模型評估

常用的模型評估指標包括：
- **準確率 (Accuracy)**：正確預測的比例
- **精確率 (Precision)**：預測為正類的樣本中，實際為正類的比例
- **召回率 (Recall)**：實際為正類的樣本中，被正確預測為正類的比例
- **F1 分數**：精確率和召回率的調和平均

## 4.7 總結

本章介紹了機器學習的基礎知識和經典演算法：

| 類別 | 演算法 | 應用場景 |
|------|--------|----------|
| 迴歸 | 線性迴歸 | 連續值預測 |
| 分類 | 邏輯迴歸 | 二分類問題 |
| 分類 | 決策樹 | 可解釋的分類 |
| 分類 | 隨機森林 | 集成學習 |
| 分類 | SVM | 高維度分類 |
| 分類 | KNN | 基於距離的分類 |
| 聚類 | K-Means | 無監督分群 |

這些演算法為深度學習奠定了基礎。在接下來的章節中，我們將學習神經網路和深度學習的核心技術。
