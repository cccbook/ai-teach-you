"""
非確定性有限自動機 (NFA) 實現
"""

from typing import Set, Dict, List, Tuple, Optional

class NFA:
    def __init__(self, states: Optional[Set[str]] = None,
                 alphabet: Optional[Set[str]] = None,
                 transitions: Optional[Dict[Tuple[str, str], Set[str]]] = None,
                 start_state: Optional[str] = None,
                 accept_states: Optional[Set[str]] = None,
                 epsilon: str = 'ε'):
        self.states = states or set()
        self.alphabet = alphabet or set()
        self.transitions = transitions or {}
        self.start_state = start_state or ""
        self.accept_states = accept_states or set()
        self.epsilon = epsilon
    
    def epsilon_closure(self, states: Set[str]) -> Set[str]:
        closure = set(states)
        stack = list(states)
        
        while stack:
            state = stack.pop()
            eps_key = (state, self.epsilon)
            if eps_key in self.transitions:
                for next_state in self.transitions[eps_key]:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
        
        return closure
    
    def move(self, states: Set[str], symbol: str) -> Set[str]:
        result = set()
        for state in states:
            key = (state, symbol)
            if key in self.transitions:
                result.update(self.transitions[key])
        return result
    
    def accepts(self, input_string: str) -> bool:
        current_states = self.epsilon_closure({self.start_state})
        
        for symbol in input_string:
            current_states = self.epsilon_closure(
                self.move(current_states, symbol)
            )
            
            if not current_states:
                return False
        
        return bool(current_states & self.accept_states)


def create_nfa_for_ab_plus():
    return NFA(
        states={'q0', 'q1', 'q2'},
        alphabet={'a', 'b', 'ε'},
        transitions={
            ('q0', 'a'): {'q1'},
            ('q1', 'b'): {'q2'},
            ('q2', 'ε'): {'q0'},
        },
        start_state='q0',
        accept_states={'q2'}
    )


def demo_nfa():
    print("=== NFA 演示 ===\n")
    
    nfa = create_nfa_for_ab_plus()
    
    print("識別 (ab)+ 的NFA\n")
    
    test_strings = ['', 'ab', 'aab', 'abab', 'aba', 'bab', 'ababab']
    
    for s in test_strings:
        result = nfa.accepts(s)
        print(f"  {'✓' if result else '✗'} '{s}'")


if __name__ == "__main__":
    demo_nfa()
