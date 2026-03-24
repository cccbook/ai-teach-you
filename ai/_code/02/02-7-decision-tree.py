"""
Simple Decision Tree Implementation
Uses information gain (entropy) to select splitting features
"""

from collections import Counter
import math


def entropy(labels):
    """Calculate entropy of a label distribution"""
    total = len(labels)
    if total == 0:
        return 0
    counts = Counter(labels)
    probs = [count / total for count in counts.values()]
    return -sum(p * math.log2(p) for p in probs if p > 0)


def information_gain(data, feature_idx, threshold):
    """Calculate information gain from splitting on a feature"""
    labels = [row[-1] for row in data]
    parent_entropy = entropy(labels)
    
    left_data = [row for row in data if row[feature_idx] <= threshold]
    right_data = [row for row in data if row[feature_idx] > threshold]
    
    if not left_data or not right_data:
        return 0
    
    left_labels = [row[-1] for row in left_data]
    right_labels = [row[-1] for row in right_data]
    
    left_weight = len(left_data) / len(data)
    right_weight = len(right_data) / len(data)
    
    child_entropy = (left_weight * entropy(left_labels) + 
                     right_weight * entropy(right_labels))
    
    return parent_entropy - child_entropy


def build_tree(data, depth=0, max_depth=3):
    """Build decision tree recursively"""
    labels = [row[-1] for row in data]
    
    if len(set(labels)) == 1:
        return labels[0]
    
    if len(data[0]) == 1 or depth >= max_depth:
        return Counter(labels).most_common(1)[0][0]
    
    best_gain = -1
    best_split = None
    
    for feature_idx in range(len(data[0]) - 1):
        values = [row[feature_idx] for row in data]
        thresholds = set(values)
        for threshold in thresholds:
            gain = information_gain(data, feature_idx, threshold)
            if gain > best_gain:
                best_gain = gain
                best_split = (feature_idx, threshold)
    
    if best_gain <= 0:
        return Counter(labels).most_common(1)[0][0]
    
    feature_idx, threshold = best_split
    left = [row for row in data if row[feature_idx] <= threshold]
    right = [row for row in data if row[feature_idx] > threshold]
    
    return {
        'feature': feature_idx,
        'threshold': threshold,
        'left': build_tree(left, depth + 1, max_depth),
        'right': build_tree(right, depth + 1, max_depth)
    }


def predict(tree, sample):
    """Predict class label for a sample"""
    if isinstance(tree, dict):
        if sample[tree['feature']] <= tree['threshold']:
            return predict(tree['left'], sample)
        else:
            return predict(tree['right'], sample)
    return tree


if __name__ == "__main__":
    # Data: [humidity, temperature, play]
    # humidity <= 80: normal, > 80: high
    # temperature: numeric
    # play: 1=yes, 0=no
    training_data = [
        [70, 25, 1],
        [85, 30, 0],
        [75, 20, 1],
        [90, 28, 0],
        [65, 22, 1],
        [80, 32, 0],
        [60, 18, 1],
        [95, 35, 0],
    ]
    
    print("=== Simple Decision Tree ===")
    print("Features: Humidity, Temperature")
    print("Target: Play (1=Yes, 0=No)\n")
    print("Training data:")
    for row in training_data:
        print(f"  Humidity: {row[0]}, Temp: {row[1]}, Play: {row[2]}")
    
    tree = build_tree(training_data, max_depth=3)
    print(f"\nDecision Tree: {tree}")
    
    test_samples = [
        [70, 26],  # normal humidity, moderate temp
        [88, 30],  # high humidity
    ]
    
    print("\nPredictions:")
    for sample in test_samples:
        prediction = predict(tree, sample)
        print(f"  Humidity: {sample[0]}, Temp: {sample[1]} -> Play: {prediction}")
