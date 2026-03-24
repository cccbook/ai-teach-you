#!/usr/bin/env python3
"""
Chapter 11-1: N-gram Language Model
基礎的統計語言模型
"""

import numpy as np
from collections import defaultdict, Counter
import re

class NGramModel:
    def __init__(self, n=2):
        self.n = n
        self.ngram_counts = defaultdict(Counter)
        self.context_counts = defaultdict(int)
        self.vocabulary = set()
        
    def tokenize(self, text):
        return ['<s>'] * (self.n - 1) + text.lower().split() + ['</s>']
    
    def train(self, corpus):
        sentences = corpus.split('.')
        for sentence in sentences:
            if sentence.strip():
                tokens = self.tokenize(sentence)
                self.vocabulary.update(tokens)
                
                for i in range(len(tokens) - self.n + 1):
                    ngram = tuple(tokens[i:i+self.n])
                    context = ngram[:-1]
                    next_word = ngram[-1]
                    
                    self.ngram_counts[context][next_word] += 1
                    self.context_counts[context] += 1
    
    def predict(self, context):
        context = tuple(context[-(self.n-1):])
        if context not in self.ngram_counts:
            return '<unk>'
        
        candidates = self.ngram_counts[context]
        total = self.context_counts[context]
        
        probs = {word: count/total for word, count in candidates.items()}
        return max(probs, key=probs.get)
    
    def probability(self, word, context):
        context = tuple(context[-(self.n-1):])
        if context not in self.ngram_counts:
            return 1/len(self.vocabulary)
        
        count = self.ngram_counts[context].get(word, 0)
        total = self.context_counts[context]
        return (count + 1) / (total + len(self.vocabulary))

def demo():
    print("=" * 60)
    print("Chapter 11-1: N-gram Language Model")
    print("=" * 60)
    
    print("\n[Concept] N-gram Model:")
    print("  根據前 N-1 個詞預測下一個詞的概率")
    print("  P(w_n | w_1, ..., w_{n-1}) ≈ P(w_n | w_{n-N+1:n-1})")
    
    corpus = """the cat sat on the mat. the dog sat on the log. 
    a cat sat on a mat. the bird flew to the nest.
    i love natural language processing."""
    
    print(f"[Training] corpus length: {len(corpus.split())} words")
    
    bigram = NGramModel(n=2)
    bigram.train(corpus)
    
    print(f"  Vocabulary size: {len(bigram.vocabulary)}")
    print(f"  Unique bigrams: {len(bigram.ngram_counts)}")
    
    print("\n[Prediction]")
    test_contexts = [
        ['<s>', 'the'],
        ['cat', 'sat'],
        ['on', 'the'],
    ]
    
    for ctx in test_contexts:
        next_word = bigram.predict(ctx)
        prob = bigram.probability(next_word, ctx)
        print(f"  Context {ctx}: next = '{next_word}' (p={prob:.4f})")
    
    print("\n[Smoothing]")
    print("  Add-k smoothing: P(w|c) = (count + k) / (total + k*|V|)")
    print("  Good-Turing: 重新分配概率給低頻詞")
    
    print("\n[Backoff]")
    print("  如果 3-gram 未找到，回退到 2-gram")
    print("  Interpolated: 線性組合不同 n-gram")
    
    print("\n[Limitations]")
    print("  • 稀疏性問題")
    print("  • 無法捕捉長距離依賴")
    print("  • 沒有語義理解")
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    print("=" * 60)

if __name__ == "__main__":
    demo()