#!/usr/bin/env python3
"""
Chapter 11-4: BERT
Bidirectional Encoder Representations from Transformers
"""

import numpy as np

class BERT:
    def __init__(self, vocab_size=30522, hidden_dim=768, num_layers=12):
        self.vocab_size = vocab_size
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        
        np.random.seed(42)
        
        self.token_embedding = np.random.randn(vocab_size, hidden_dim) * 0.02
        self.position_embedding = np.random.randn(512, hidden_dim) * 0.02
        self.segment_embedding = np.random.randn(2, hidden_dim) * 0.02
        
        self.transformer_layers = [
            {
                'attention': np.random.randn(hidden_dim, hidden_dim) * 0.02,
                'ffn': np.random.randn(hidden_dim, hidden_dim * 4) * 0.02,
                'layer_norm_1': np.ones(hidden_dim),
                'layer_norm_2': np.ones(hidden_dim),
            }
            for _ in range(num_layers)
        ]
        
    def get_embeddings(self, token_ids, segment_ids=None):
        token_emb = self.token_embedding[token_ids]
        position_emb = self.position_embedding[:len(token_ids)]
        
        embeddings = token_emb + position_emb
        if segment_ids is not None:
            seg_emb = self.segment_embedding[segment_ids]
            embeddings += seg_emb
            
        return embeddings
    
    def masked_language_model(self, input_ids, masked_positions):
        embeddings = self.get_embeddings(input_ids)
        
        probs = np.random.rand(len(masked_positions), self.vocab_size)
        predictions = np.argmax(probs, axis=1)
        
        return predictions
    
    def next_sentence_prediction(self, input_ids):
        embeddings = self.get_embeddings(input_ids)
        pooled = np.mean(embeddings, axis=0)
        
        is_next = np.random.rand() > 0.5
        return is_next

def demo():
    print("=" * 60)
    print("Chapter 11-4: BERT")
    print("=" * 60)
    
    print("\n[Concept] BERT:")
    print("  雙向 Transformer 編碼器")
    print("  預訓練任務: MLM + NSP")
    print("  可以 fine-tune 進行各種下游任務")
    
    print("\n[Architecture]")
    print("  Base: 12 layers, 768 hidden, 12 heads")
    print("  Large: 24 layers, 1024 hidden, 16 heads")
    
    bert = BERT(vocab_size=30522, hidden_dim=768, num_layers=12)
    
    print(f"\n[Input Processing]")
    sentence = "the quick brown fox jumps over the lazy dog"
    tokens = sentence.split()
    token_ids = [hash(t) % 30522 for t in tokens]
    print(f"  Sentence: '{sentence}'")
    print(f"  Tokens: {tokens}")
    print(f"  Token IDs: {token_ids[:5]}...")
    
    print("\n[Pre-training Tasks]")
    print("  1. Masked Language Model (MLM):")
    print("     Input: the [MASK] brown fox jumps over the lazy dog")
    print("     Output: 預測被遮罩的詞")
    
    print("  2. Next Sentence Prediction (NSP):")
    print("     Input: A + B (連續兩個句子)")
    print("     Output: Is B the next sentence? [Yes/No]")
    
    masked_positions = [1]
    predictions = bert.masked_language_model(token_ids, masked_positions)
    print(f"\n[MLM Prediction]")
    print(f"  Masked position: {masked_positions}")
    print(f"  Predicted token IDs: {predictions}")
    
    print("\n[Fine-tuning Tasks]")
    print("  • 文本分類 (Classification)")
    print("  • 命名實體識別 (NER)")
    print("  • 問答 (Question Answering)")
    print("  • 句子對分類 (Sentence Pair)")
    
    print("\n[Output]")
    print("  [CLS] token 用於分類")
    print("  所有 token 用於 token-level 任務")
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    print("=" * 60)

if __name__ == "__main__":
    demo()