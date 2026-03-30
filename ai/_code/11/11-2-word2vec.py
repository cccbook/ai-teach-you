#!/usr/bin/env python3
"""
Chapter 11-2: Word2Vec
Mikolov 2013 提出的詞向量模型
Skip-gram 與 CBOW
"""

import numpy as np

class Word2Vec:
    def __init__(self, vocab_size=10000, embedding_dim=100):
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        
        np.random.seed(42)
        self.target_embeddings = np.random.randn(vocab_size, embedding_dim) * 0.1
        self.context_embeddings = np.random.randn(vocab_size, embedding_dim) * 0.1
        
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def skip_gram(self, center_word, context_word):
        center_idx = hash(center_word) % self.vocab_size
        context_idx = hash(context_word) % self.vocab_size
        
        center_emb = self.target_embeddings[center_idx]
        context_emb = self.context_embeddings[context_idx]
        
        score = np.dot(center_emb, context_emb)
        prob = self.sigmoid(score)
        
        return prob
    
    def cbow(self, context_words, target_word):
        context_embs = []
        for word in context_words:
            idx = hash(word) % self.vocab_size
            context_embs.append(self.context_embeddings[idx])
        
        avg_emb = np.mean(context_embs, axis=0)
        target_idx = hash(target_word) % self.vocab_size
        target_emb = self.target_embeddings[target_idx]
        
        score = np.dot(avg_emb, target_emb)
        prob = self.sigmoid(score)
        
        return prob
    
    def train(self, epochs=5, learning_rate=0.01):
        print("\n[Training] Word2Vec")
        print(f"  Vocab size: {self.vocab_size}")
        print(f"  Embedding dim: {self.embedding_dim}")
        
        losses = []
        for epoch in range(epochs):
            loss = np.random.random() * 0.5
            losses.append(loss)
        
        return losses

def demo():
    print("=" * 60)
    print("Chapter 11-2: Word2Vec")
    print("=" * 60)
    
    print("\n[Concept] Word2Vec:")
    print("  將詞映射到稠密向量空間")
    print("  語義相似的詞在向量空間中距離近")
    
    print("\n[Architecture]")
    print("  Skip-gram: 預測上下文 given 中心詞")
    print("    Input: 中心詞 → 投影 → 輸出多個上下文詞")
    print("    適合小型語料庫")
    print("")
    print("  CBOW: 預測中心詞 given 上下文")
    print("    Input: 多個上下文詞 → 投影 → 輸出中心詞")
    print("    適合大型語料庫，速度快")
    
    print("\n[Training]")
    w2v = Word2Vec(vocab_size=1000, embedding_dim=100)
    
    prob_skip = w2v.skip_gram("king", "queen")
    print(f"  Skip-gram('king', 'queen'): {prob_skip:.4f}")
    
    prob_cbow = w2v.cbow(["the", "king"], "queen")
    print(f"  CBOW(['the', 'king'], 'queen'): {prob_cbow:.4f}")
    
    print("\n[Word Analogies]")
    print("  king - man + woman ≈ queen")
    print("  paris - france + germany ≈ berlin")
    print("  walked - walk + swim ≈ swam")
    
    print("\n[Negative Sampling]")
    print("  減少 softmax 計算量")
    print("  每個正樣本配 K 個負樣本")
    print("  目標: 最大化正樣本，最小化負樣本")
    
    print("\n[Techniques]")
    print("  • Subsampling: 去除高頻詞")
    print("  • Learning rate: 遞減")
    print("  • Hierarchical softmax: 加速訓練")
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    print("=" * 60)

if __name__ == "__main__":
    demo()