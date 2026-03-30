#!/usr/bin/env python3
"""
Chapter 11-3: GloVe
Global Vectors for Word Representation
結合全局統計與局部上下文
"""

import numpy as np

class GloVe:
    def __init__(self, vocab_size=10000, embedding_dim=100):
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        
        np.random.seed(42)
        self.W = np.random.randn(vocab_size, embedding_dim) * 0.1
        self.W_tilde = np.random.randn(vocab_size, embedding_dim) * 0.1
        self.b = np.random.randn(vocab_size) * 0.1
        self.b_tilde = np.random.randn(vocab_size) * 0.1
        
        self.word_to_idx = {}
        self.co_occurrence = {}
        
    def build_vocab(self, corpus):
        words = corpus.lower().split()
        unique_words = list(set(words))
        
        for idx, word in enumerate(unique_words):
            self.word_to_idx[word] = idx
        
        for i in range(len(words) - 1):
            w1, w2 = words[i], words[i+1]
            if w1 in self.word_to_idx and w2 in self.word_to_idx:
                key = (self.word_to_idx[w1], self.word_to_idx[w2])
                self.co_occurrence[key] = self.co_occurrence.get(key, 0) + 1
    
    def weighting_function(self, x):
        if x < 100:
            return (x / 100) ** 0.75
        return 1.0
    
    def loss(self, i, j, x_ij):
        w_i = self.W[i]
        w_j = self.W_tilde[j]
        b_i = self.b[i]
        b_j = self.b_tilde[j]
        
        pred = np.dot(w_i, w_j) + b_i + b_j
        weight = self.weighting_function(x_ij)
        
        diff = pred - np.log(x_ij + 1e-8)
        return weight * diff * diff
    
    def train(self, epochs=5):
        print("\n[Training] GloVe")
        
        for epoch in range(epochs):
            total_loss = 0
            for (i, j), x_ij in list(self.co_occurrence.items())[:100]:
                l = self.loss(i, j, x_ij)
                total_loss += l
            
            print(f"  Epoch {epoch+1}: loss = {total_loss/100:.4f}")
        
        return self.W

def demo():
    print("=" * 60)
    print("Chapter 11-3: GloVe")
    print("=" * 60)
    
    print("\n[Concept] GloVe:")
    print("  結合全局共現矩陣與神經網路")
    print("  目標: 最小化詞向量與共現次數的差異")
    
    corpus = """the cat sat on the mat. the dog sat on the log.
    a cat ate the fish. a dog chased the cat.
    the fish swam in the water."""
    
    glove = GloVe(vocab_size=100, embedding_dim=50)
    glove.build_vocab(corpus)
    
    print(f"  Vocabulary size: {len(glove.word_to_idx)}")
    print(f"  Co-occurrence pairs: {len(glove.co_occurrence)}")
    
    embeddings = glove.train(epochs=3)
    
    print(f"\n[Architecture]")
    print("  Input: 共現次數 X_ij")
    print("  目標: minimize J = Σ f(X_ij)(w_i^T w_j + b_i + b_j - log(X_ij))²")
    print("  f(x) = (x/x_max)^α if x < x_max else 1")
    
    print("\n[Advantages]")
    print("  ✓ 結合全局統計資訊")
    print("  ✓ 訓練速度快 (非迭代式)")
    print("  ✓ 可解釋性強")
    print("  ✓ 在 analogy 任務表現好")
    
    print("\n[Comparison: Word2Vec vs GloVe]")
    print("  ┌──────────┬─────────────────┬─────────────────┐")
    print("  │  Aspect  │    Word2Vec     │      GloVe     │")
    print("  ├──────────┼─────────────────┼─────────────────┤")
    print("  │ Method   │  Predict-based  │  Count-based   │")
    print("  │ Context  │    Local        │     Global     │")
    print("  │ Speed    │     Fast        │    Faster      │")
    print("  │ Memory   │     Low         │     High       │")
    print("  └──────────┴─────────────────┴─────────────────┘")
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    print("=" * 60)

if __name__ == "__main__":
    demo()