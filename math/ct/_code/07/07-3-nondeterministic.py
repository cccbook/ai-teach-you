"""
非確定性圖靈機 (NTM) 模擬器
"""

from typing import List, Tuple, Optional, Dict, Set
from dataclasses import dataclass
from collections import deque
from enum import Enum

class Direction(Enum):
    LEFT = 'L'
    RIGHT = 'R'
    STAY = 'S'

@dataclass
class Transition:
    new_state: str
    write_symbol: str
    direction: Direction

@dataclass
class NTMConfiguration:
    tape: List[str]
    head: int
    state: str

class NondeterministicTM:
    def __init__(self):
        self.states: Set[str] = set()
        self.alphabet: Set[str] = set()
        self.tape_alphabet: Set[str] = set()
        self.transitions: Dict[Tuple[str, str], List[Tuple[str, str, Direction]]] = {}
        self.start_state: str = ""
        self.accept_states: Set[str] = set()
        self.reject_states: Set[str] = set()
        self.blank_symbol: str = '_'
    
    def load_from_dict(self, config: dict):
        self.states = set(config.get('states', []))
        self.alphabet = set(config.get('alphabet', []))
        self.tape_alphabet = set(config.get('tape_alphabet', []))
        self.start_state = config.get('start_state', '')
        self.accept_states = set(config.get('accept_states', []))
        self.reject_states = set(config.get('reject_states', []))
        self.blank_symbol = config.get('blank_symbol', '_')
        
        for (state, symbol), trans_list in config.get('transitions', {}).items():
            self.transitions[(state, symbol)] = [
                Transition(new_state, write, Direction(dir_val))
                for new_state, write, dir_val in trans_list
            ]
    
    def _apply_transition(self, config: NTMConfiguration, 
                          t: Transition) -> NTMConfiguration:
        new_tape = config.tape.copy()
        new_tape[config.head] = t.write_symbol
        
        new_head = config.head
        if t.direction == Direction.LEFT:
            new_head -= 1
            if new_head < 0:
                new_tape.insert(0, self.blank_symbol)
                new_head = 0
        elif t.direction == Direction.RIGHT:
            new_head += 1
            if new_head >= len(new_tape):
                new_tape.append(self.blank_symbol)
        
        return NTMConfiguration(
            tape=new_tape,
            head=new_head,
            state=t.new_state
        )
    
    def run(self, input_string: str, max_steps: int = 10000, 
            max_branches: int = 10000) -> Tuple[bool, int]:
        initial_config = NTMConfiguration(
            tape=list(input_string) + [self.blank_symbol],
            head=0,
            state=self.start_state
        )
        
        queue = deque([initial_config])
        total_branches = 0
        
        while queue and total_branches < max_branches:
            config = queue.popleft()
            
            if config.state in self.accept_states:
                return (True, total_branches)
            if config.state in self.reject_states:
                continue
            
            key = (config.state, config.tape[config.head])
            if key not in self.transitions:
                continue
            
            for t in self.transitions[key]:
                new_config = self._apply_transition(config, t)
                queue.append(new_config)
                total_branches += 1
                
                if total_branches >= max_branches:
                    break
        
        return (False, total_branches)


def demo_ntm():
    print("=== 非確定性圖靈機演示 ===\n")
    
    config = {
        'states': ['q0', 'q1', 'accept'],
        'alphabet': ['0', '1'],
        'tape_alphabet': ['0', '1', '_'],
        'start_state': 'q0',
        'accept_states': ['accept'],
        'reject_states': [],
        'blank_symbol': '_',
        'transitions': {
            ('q0', '0'): [('q0', '0', 'R')],
            ('q0', '1'): [('q0', '1', 'R'), ('q1', '1', 'R')],
            ('q0', '_'): [('reject', '_', 'S')],
            ('q1', '1'): [('accept', '1', 'S')],
            ('q1', '0'): [('q1', '0', 'R')],
            ('q1', '_'): [('reject', '_', 'S')],
        }
    }
    
    ntm = NondeterministicTM()
    ntm.load_from_dict(config)
    
    test_cases = ['1', '11', '101', '110', '010', '1001']
    
    for input_str in test_cases:
        accepted, branches = ntm.run(input_str, max_branches=1000)
        print(f"  '{input_str}': {'接受' if accepted else '拒絕'} (探索 {branches} 個分支)")


if __name__ == "__main__":
    demo_ntm()
