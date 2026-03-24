import numpy as np

class LoRALayer:
    def __init__(self, d_model, d_ff, rank=4):
        self.d_model = d_model
        self.d_ff = d_ff
        self.rank = rank
        
        self.W = np.random.randn(d_model, d_ff) * 0.1
        self.A = np.random.randn(rank, d_model) * 0.1
        self.B = np.random.randn(d_ff, rank) * 0.1
        
    def forward(self, x):
        base_out = x @ self.W
        lora_out = x @ self.A.T @ self.B.T
        return base_out + lora_out
    
    def get_trainable_params(self):
        return self.A.size + self.B.size
    
    def get_original_params(self):
        return self.W.size

class LoRA:
    def __init__(self, d_model, d_ff, num_layers, rank=4):
        self.layers = [LoRALayer(d_model, d_ff, rank) for _ in range(num_layers)]
        
    def forward(self, x):
        for layer in self.layers:
            x = layer.forward(x)
        return x
    
    def summary_params(self):
        total_trainable = sum(l.get_trainable_params() for l in self.layers)
        total_original = sum(l.get_original_params() for l in self.layers)
        reduction = (1 - total_trainable / total_original) * 100
        return total_trainable, total_original, reduction

d_model = 512
d_ff = 2048
num_layers = 12
rank = 8

lora = LoRA(d_model, d_ff, num_layers, rank)
x = np.random.randn(2, d_model)

output = lora.forward(x)
trainable, original, reduction = lora.summary_params()

print("=" * 60)
print("LoRA (Low-Rank Adaptation) Demo")
print("=" * 60)
print(f"d_model: {d_model}, d_ff: {d_ff}, num_layers: {num_layers}, rank: {rank}")
print(f"Input shape: {x.shape}")
print(f"Output shape: {output.shape}")
print(f"\nTrainable parameters: {trainable:,}")
print(f"Original parameters: {original:,}")
print(f"Parameter reduction: {reduction:.1f}%")
print("\n✓ LoRA adds low-rank matrices to attention/FFN weights")
print("  allowing efficient fine-tuning with minimal parameter changes")
