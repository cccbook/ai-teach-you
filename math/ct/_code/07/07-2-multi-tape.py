"""
多帶圖靈機模擬器
"""

from typing import List, Tuple, Optional, Dict, Set
from dataclasses import dataclass
from enum import Enum

class Direction(Enum):
    LEFT = 'L'
    RIGHT = 'R'
    STAY = 'S'

@dataclass
class MultiTapeConfiguration:
    tapes: List[List[str]]
    heads: List[int]
    state: str

@dataclass
class MultiTapeTransition:
    new_state: str
    writes: List[str]
    directions: List[Direction]

class MultiTapeTM:
    def __init__(self, num_tapes: int):
        self.num_tapes = num_tapes
        self.states: Set[str] = set()
        self.alphabet: Set[str] = set()
        self.tape_alphabet: Set[str] = set()
        self.transitions: Dict[Tuple[str, Tuple], MultiTapeTransition] = {}
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
        
        for key, value in config.get('transitions', {}).items():
            state, symbols = key
            new_state, writes, directions = value
            self.transitions[(state, tuple(symbols))] = MultiTapeTransition(
                new_state, writes, [Direction(d) for d in directions]
            )
    
    def _get_initial_config(self, input_string: str) -> MultiTapeConfiguration:
        tapes = [list(input_string) + [self.blank_symbol]]
        heads = [0]
        
        for _ in range(self.num_tapes - 1):
            tapes.append([self.blank_symbol])
            heads.append(0)
        
        return MultiTapeConfiguration(tapes=tapes, heads=heads, state=self.start_state)
    
    def step(self, config: MultiTapeConfiguration) -> Optional[MultiTapeConfiguration]:
        symbols = tuple(config.tapes[i][config.heads[i]] for i in range(self.num_tapes))
        key = (config.state, symbols)
        
        if key not in self.transitions:
            return None
        
        t = self.transitions[key]
        
        new_tapes = [tape.copy() for tape in config.tapes]
        new_heads = config.heads.copy()
        
        for i in range(self.num_tapes):
            new_tapes[i][new_heads[i]] = t.writes[i]
            
            if t.directions[i] == Direction.LEFT:
                new_heads[i] -= 1
                if new_heads[i] < 0:
                    new_tapes[i].insert(0, self.blank_symbol)
                    new_heads[i] = 0
            elif t.directions[i] == Direction.RIGHT:
                new_heads[i] += 1
                if new_heads[i] >= len(new_tapes[i]):
                    new_tapes[i].append(self.blank_symbol)
        
        return MultiTapeConfiguration(
            tapes=new_tapes,
            heads=new_heads,
            state=t.new_state
        )
    
    def run(self, input_string: str, max_steps: int = 10000) -> Tuple[bool, int]:
        config = self._get_initial_config(input_string)
        steps = 0
        
        while steps < max_steps:
            if config.state in self.accept_states:
                return (True, steps)
            if config.state in self.reject_states:
                return (False, steps)
            
            new_config = self.step(config)
            if new_config is None:
                return (config.state in self.accept_states, steps)
            
            config = new_config
            steps += 1
        
        return (False, max_steps)


def demo_multi_tape():
    print("=== 多帶圖靈機演示 ===\n")
    
    config = {
        'states': ['q0', 'q1', 'q2', 'accept'],
        'alphabet': ['0', '1'],
        'tape_alphabet': ['0', '1', '_', '#'],
        'start_state': 'q0',
        'accept_states': ['accept'],
        'reject_states': [],
        'blank_symbol': '_',
        'transitions': {
            ('q0', ('0', '_')): ('q0', ('0', '0'), ('R', 'R')),
            ('q0', ('1', '_')): ('q0', ('1', '1'), ('R', 'R')),
            ('q0', ('_', '_')): ('q1', ('_', '_'), ('L', 'L')),
            ('q1', ('0', '0')): ('q1', ('0', '0'), ('L', 'L')),
            ('q1', ('1', '1')): ('q1', ('1', '1'), ('L', 'L')),
            ('q1', ('_', '_')): ('accept', ('_', '_'), ('R', 'R')),
        }
    }
    
    tm = MultiTapeTM(num_tapes=2)
    tm.load_from_dict(config)
    
    test_cases = ['1', '101', '111']
    
    for input_str in test_cases:
        accepted, steps = tm.run(input_str)
        print(f"  '{input_str}': {'接受' if accepted else '拒絕'} ({steps} 步)")


if __name__ == "__main__":
    demo_multi_tape()
