"""
確定性有限自動機 (DFA) 實現
"""

from typing import Set, Dict, Tuple, Optional

class DFA:
    def __init__(self, states: Optional[Set[str]] = None, 
                 alphabet: Optional[Set[str]] = None,
                 transitions: Optional[Dict[Tuple[str, str], str]] = None,
                 start_state: Optional[str] = None,
                 accept_states: Optional[Set[str]] = None,
                 blank_symbol: str = '_'):
        self.states = states or set()
        self.alphabet = alphabet or set()
        self.transitions = transitions or {}
        self.start_state = start_state or ""
        self.accept_states = accept_states or set()
        self.blank_symbol = blank_symbol
    
    def load_from_dict(self, config: dict):
        self.states = set(config.get('states', []))
        self.alphabet = set(config.get('alphabet', []))
        self.start_state = config.get('start_state', '')
        self.accept_states = set(config.get('accept_states', []))
        self.blank_symbol = config.get('blank_symbol', '_')
        self.alphabet.add(self.blank_symbol)
        
        for (state, symbol), next_state in config.get('transitions', {}).items():
            self.transitions[(state, symbol)] = next_state
    
    def accepts(self, input_string: str) -> bool:
        current_state = self.start_state
        
        for symbol in input_string:
            key = (current_state, symbol)
            if key not in self.transitions:
                return False
            current_state = self.transitions[key]
        
        return current_state in self.accept_states


def create_binary_divisible_by_3() -> DFA:
    return DFA(
        states={'q0', 'q1', 'q2'},
        alphabet={'0', '1'},
        transitions={
            ('q0', '0'): 'q0',
            ('q0', '1'): 'q1',
            ('q1', '0'): 'q2',
            ('q1', '1'): 'q0',
            ('q2', '0'): 'q1',
            ('q2', '1'): 'q2',
        },
        start_state='q0',
        accept_states={'q0'}
    )


def demo_dfa():
    print("=== DFA 演示 ===\n")
    
    dfa = create_binary_divisible_by_3()
    
    print("識別被3整除的二進制數的DFA\n")
    
    test_cases = ['0', '1', '10', '11', '100', '110', '1001']
    
    for binary in test_cases:
        result = dfa.accepts(binary)
        value = int(binary, 2) if binary else 0
        divisible = "✓" if result else "✗"
        print(f"  {divisible} {binary} (十進制 {value}): "
              f"{'是' if result else '否'} 能被3整除")


if __name__ == "__main__":
    demo_dfa()
