import numpy as np

def quantize(w, bits=4):
    n = 2 ** bits
    w_min, w_max = w.min(), w.max()
    scale = (w_max - w_min) / n
    quantized = np.round((w - w_min) / scale).astype(int)
    quantized = np.clip(quantized, 0, n - 1)
    return quantized, scale, w_min

def dequantize(quantized, scale, w_min, bits=4):
    n = 2 ** bits
    return (quantized * scale + w_min).astype(np.float32)

class QLoRA:
    def __init__(self, d_model, d_ff, num_layers, rank=4, quant_bits=4):
        self.quant_bits = quant_bits
        self.layers = []
        
        for _ in range(num_layers):
            W = np.random.randn(d_model, d_ff) * 0.1
            q, scale, zero = quantize(W, quant_bits)
            
            A = np.random.randn(rank, d_model) * 0.1
            B = np.random.randn(d_ff, rank) * 0.1
            
            self.layers.append({
                'W_quantized': q,
                'W_scale': scale,
                'W_zero': zero,
                'A': A,
                'B': B
            })
    
    def forward(self, x):
        for layer in self.layers:
            W = dequantize(layer['W_quantized'], layer['W_scale'], layer['W_zero'], self.quant_bits)
            base_out = x @ W
            lora_out = x @ layer['A'].T @ layer['B'].T
            x = base_out + lora_out
        return x
    
    def summary_params(self):
        d_model, d_ff = 512, 2048
        num_layers = len(self.layers)
        
        original = d_model * d_ff * num_layers
        quant_params = original * self.quant_bits // 8
        lora_params = rank * d_model * 2 * num_layers
        rank = self.layers[0]['A'].shape[0]
        
        return quant_params, lora_params, original

d_model = 512
d_ff = 2048
num_layers = 12
rank = 8
quant_bits = 4

qlora = QLoRA(d_model, d_ff, num_layers, rank, quant_bits)
x = np.random.randn(2, d_model)

output = qlora.forward(x)
quant_params, lora_params, original = qlora.summary_params()

print("=" * 60)
print("QLoRA (Quantized LoRA) Demo")
print("=" * 60)
print(f"d_model: {d_model}, d_ff: {d_ff}, num_layers: {num_layers}")
print(f"Rank: {rank}, Quantization bits: {quant_bits}")
print(f"Input shape: {x.shape}")
print(f"Output shape: {output.shape}")
print(f"\nQuantized base weights: {quant_params:,} bytes")
print(f"LoRA adapters: {lora_params:,} params")
print(f"Original weights: {original:,} params")
print("\n✓ QLoRA combines quantization with LoRA for")
print("  even more memory-efficient fine-tuning")
