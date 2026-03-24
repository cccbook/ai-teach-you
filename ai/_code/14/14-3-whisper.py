import numpy as np

class WhisperEncoder:
    def __init__(self, n_mels=80, d_model=512):
        self.conv1 = np.random.randn(3* n_mels, d_model) * 0.02
        self.conv2 = np.random.randn(3* n_mels, d_model) * 0.02
        
    def forward(self, mel_spec):
        x = mel_spec.reshape(mel_spec.shape[0], -1)
        x = np.maximum(0, x @ self.conv1)
        x = np.maximum(0, x @ self.conv2)
        return x

class WhisperDecoder:
    def __init__(self, vocab_size, d_model, max_len=448):
        self.embedding = np.random.randn(vocab_size, d_model) * 0.02
        self.pos_embed = np.random.randn(max_len, d_model) * 0.02
        self.lm_head = np.random.randn(d_model, vocab_size) * 0.02
        
    def forward(self, token_ids, encoder_output):
        x = self.embedding[token_ids]
        x = x + self.pos_embed[:x.shape[0]]
        x = x + encoder_output
        return x @ self.lm_head

class Whisper:
    def __init__(self, vocab_size=51865, n_mels=80, d_model=512):
        self.encoder = WhisperEncoder(n_mels, d_model)
        self.decoder = WhisperDecoder(vocab_size, d_model)
        self.vocab_size = vocab_size
        
    def forward(self, mel_spec, token_ids):
        encoder_out = self.encoder.forward(mel_spec)
        logits = self.decoder.forward(token_ids, encoder_out)
        return logits

vocab_size = 51865
n_mels = 80
d_model = 512

whisper = Whisper(vocab_size, n_mels, d_model)

batch_size = 2
mel_spec = np.random.randn(batch_size, n_mels, 3000)
token_ids = np.array([50257, 50359, 41420, 2117])

logits = whisper.forward(mel_spec, token_ids)

print("=" * 60)
print("Whisper (Speech Recognition) Demo")
print("=" * 60)
print(f"Vocab size: {vocab_size:,}")
print(f"Mel spectrogram bins: {n_mels}")
print(f"d_model: {d_model}")
print(f"Input mel shape: {mel_spec.shape}")
print(f"Token IDs: {token_ids}")
print(f"Output logits shape: {logits.shape}")
print("\n✓ Whisper is a speech recognition model that processes")
print("  mel spectrograms to generate text transcriptions")
