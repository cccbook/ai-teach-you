"""
下推自動機 (PDA) 實現
"""

from typing import Set, Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class PDAConfig:
    state: str
    remaining: str
    stack: List[str]

class PDA:
    def __init__(self):
        self.states: Set[str] = set()
        self.input_alphabet: Set[str] = set()
        self.stack_alphabet: Set[str] = set()
        self.transitions: Dict[Tuple[str, str, str], Tuple[str, str]] = {}
        self.start_state: str = ""
        self.start_stack_symbol: str = ""
        self.accept_states: Set[str] = set()
    
    def accepts_by_empty_stack(self, input_string: str) -> bool:
        config = PDAConfig(
            state=self.start_state,
            remaining=input_string,
            stack=[self.start_stack_symbol]
        )
        
        while config.remaining is not None:
            a = config.remaining[0] if config.remaining else ''
            X = config.stack[-1] if config.stack else '_'
            
            key = (config.state, a, X)
            if key in self.transitions:
                new_state, gamma = self.transitions[key]
                new_stack = config.stack[:-1]
                if gamma:
                    new_stack.extend(reversed(gamma))
                config = PDAConfig(
                    state=new_state,
                    remaining=config.remaining[1:],
                    stack=new_stack
                )
            else:
                eps_key = (config.state, '', X)
                if eps_key in self.transitions:
                    new_state, gamma = self.transitions[eps_key]
                    new_stack = config.stack[:-1]
                    if gamma:
                        new_stack.extend(reversed(gamma))
                    config = PDAConfig(
                        state=new_state,
                        remaining=config.remaining,
                        stack=new_stack
                    )
                else:
                    break
        
        return len(config.stack) == 0


def create_balanced_parentheses_pda() -> PDA:
    pda = PDA()
    pda.states = {'q0', 'q1'}
    pda.input_alphabet = {'(', ')'}
    pda.stack_alphabet = {'(', 'Z'}
    pda.start_state = 'q0'
    pda.start_stack_symbol = 'Z'
    pda.accept_states = {'q1'}
    
    pda.transitions = {
        ('q0', '(', 'Z'): ('q0', '(Z'),
        ('q0', '(', '('): ('q0', '(('),
        ('q0', ')', '('): ('q0', ''),
        ('q0', '', 'Z'): ('q1', ''),
    }
    
    return pda


def create_a_n_b_n_pda() -> PDA:
    pda = PDA()
    pda.states = {'q0', 'q1', 'q2'}
    pda.input_alphabet = {'a', 'b'}
    pda.stack_alphabet = {'a', 'Z'}
    pda.start_state = 'q0'
    pda.start_stack_symbol = 'Z'
    pda.accept_states = {'q2'}
    
    pda.transitions = {
        ('q0', 'a', 'Z'): ('q0', 'aZ'),
        ('q0', 'a', 'a'): ('q0', 'aa'),
        ('q0', 'b', 'a'): ('q1', ''),
        ('q1', 'b', 'a'): ('q1', ''),
        ('q1', '', 'Z'): ('q2', ''),
    }
    
    return pda


def demo_pda():
    print("=== PDA 演示 ===\n")
    
    pda = create_balanced_parentheses_pda()
    
    print("1. 識別平衡括號：")
    test_cases = ['()', '(())', '()()', '(()', ')(', '((())']
    
    for s in test_cases:
        result = pda.accepts_by_empty_stack(s)
        print(f"  {'✓' if result else '✗'} '{s}'")
    
    print("\n2. 識別 {aⁿbⁿ | n >= 1}：")
    
    pda2 = create_a_n_b_n_pda()
    test_cases = ['ab', 'aabb', 'aaabbb', 'aab', 'ba', 'aabbb']
    
    for s in test_cases:
        result = pda2.accepts_by_empty_stack(s)
        print(f"  {'✓' if result else '✗'} '{s}'")


if __name__ == "__main__":
    demo_pda()
