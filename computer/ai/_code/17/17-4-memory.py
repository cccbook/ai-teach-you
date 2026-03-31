import numpy as np
from collections import deque

class Memory:
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.buffer = deque(maxlen=capacity)
        
    def add(self, experience):
        self.buffer.append(experience)
        
    def sample(self, batch_size):
        indices = np.random.choice(len(self.buffer), batch_size, replace=False)
        return [self.buffer[i] for i in indices]

class AgentMemory:
    def __init__(self, short_term_capacity=10, long_term_capacity=100):
        self.short_term = deque(maxlen=short_term_capacity)
        self.long_term = Memory(long_term_capacity)
        
    def add_short(self, memory):
        self.short_term.append(memory)
        
    def transfer_to_long(self):
        for m in self.short_term:
            self.long_term.add(m)
        self.short_term.clear()
        
    def retrieve(self, query, k=3):
        return list(self.long_term.buffer)[-k:]

memory = AgentMemory()

memory.add_short({"role": "user", "content": "Hello"})
memory.add_short({"role": "assistant", "content": "Hi!"})
memory.add_short({"role": "user", "content": "What's 2+2?"})
memory.transfer_to_long()

retrieved = memory.retrieve("greeting")

print("=" * 60)
print("Agent Memory Demo")
print("=" * 60)
print(f"Short-term capacity: 10")
print(f"Long-term capacity: 100")
print("\nCurrent memories:")
print(f"  Short-term: {list(memory.short_term)}")
print(f"  Retrieved: {retrieved}")
print("\n✓ Agent memory types:")
print("  - Short-term: Current conversation context")
print("  - Long-term: Persistent knowledge base")
print("  - Transfer: Summary to long-term")
print("  - Retrieval: Relevant context recall")
