"""
Naive Bayes Classifier Implementation
Uses Bayes theorem with independence assumption
"""

from collections import defaultdict
import math


class NaiveBayesClassifier:
    def __init__(self, alpha=1.0):
        self.alpha = alpha  # Laplace smoothing
        self.class_probs = {}
        self.feature_probs = defaultdict(dict)
        self.classes = []
    
    def fit(self, X, y):
        """Train the classifier on feature matrix X and labels y"""
        self.classes = list(set(y))
        n_samples = len(y)
        
        for cls in self.classes:
            self.class_probs[cls] = (y.count(cls) + self.alpha) / (n_samples + self.alpha * len(self.classes))
        
        n_features = len(X[0])
        for cls in self.classes:
            class_samples = [X[i] for i in range(len(y)) if y[i] == cls]
            for feature_idx in range(n_features):
                feature_values = [sample[feature_idx] for sample in class_samples]
                value_counts = defaultdict(int)
                for val in feature_values:
                    value_counts[val] += 1
                
                unique_values = len(set(feature_values))
                self.feature_probs[(cls, feature_idx)] = {
                    val: (count + self.alpha) / (len(class_samples) + self.alpha * unique_values)
                    for val, count in value_counts.items()
                }
    
    def predict_single(self, sample):
        """Predict class for a single sample"""
        best_class = None
        best_prob = -1
        
        for cls in self.classes:
            prob = math.log(self.class_probs[cls])
            for feature_idx, value in enumerate(sample):
                probs = self.feature_probs.get((cls, feature_idx), {})
                prob += math.log(probs.get(value, self.alpha))
            
            if prob > best_prob or best_class is None:
                best_prob = prob
                best_class = cls
        
        return best_class
    
    def predict(self, X):
        """Predict classes for multiple samples"""
        return [self.predict_single(sample) for sample in X]


if __name__ == "__main__":
    # Weather dataset: [Outlook, Temperature, Humidity, Windy, Play]
    training_data = [
        ['sunny', 'hot', 'high', 'weak', 'no'],
        ['sunny', 'hot', 'high', 'strong', 'no'],
        ['overcast', 'hot', 'high', 'weak', 'yes'],
        ['rainy', 'mild', 'high', 'weak', 'yes'],
        ['rainy', 'cool', 'normal', 'weak', 'yes'],
        ['rainy', 'cool', 'normal', 'strong', 'no'],
        ['overcast', 'cool', 'normal', 'strong', 'yes'],
        ['sunny', 'mild', 'high', 'weak', 'no'],
        ['sunny', 'cool', 'normal', 'weak', 'yes'],
        ['rainy', 'mild', 'normal', 'weak', 'yes'],
        ['sunny', 'mild', 'normal', 'strong', 'yes'],
        ['overcast', 'mild', 'high', 'strong', 'yes'],
        ['overcast', 'hot', 'normal', 'weak', 'yes'],
        ['rainy', 'mild', 'high', 'strong', 'no'],
    ]
    
    X = [row[:-1] for row in training_data]
    y = [row[-1] for row in training_data]
    
    print("=== Naive Bayes Classifier ===")
    print("Features: Outlook, Temperature, Humidity, Windy")
    print("Target: Play (yes/no)\n")
    print("Training samples:", len(training_data))
    
    clf = NaiveBayesClassifier()
    clf.fit(X, y)
    
    test_samples = [
        ['sunny', 'cool', 'high', 'weak'],
        ['rainy', 'hot', 'normal', 'strong'],
        ['overcast', 'mild', 'normal', 'weak'],
    ]
    
    predictions = clf.predict(test_samples)
    
    print("\nPredictions:")
    for sample, pred in zip(test_samples, predictions):
        print(f"  {sample} -> Play: {pred}")
    
    print(f"\nClass priors: {clf.class_probs}")
