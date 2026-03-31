"""
通用圖靈機 (Universal Turing Machine)
"""

from typing import Dict, Tuple, List, Set, Optional
from dataclasses import dataclass
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
class TMDescription:
    states: Set[str]
    alphabet: Set[str]
    tape_alphabet: Set[str]
    transitions: Dict[Tuple[str, str], Transition]
    start_state: str
    accept_states: Set[str]
    reject_states: Set[str]
    blank_symbol: str
    
    @staticmethod
    def from_dict(config: dict) -> 'TMDescription':
        transitions = {}
        for (state, symbol), (new_state, write, direction) in config.get('transitions', {}).items():
            transitions[(state, symbol)] = Transition(
                new_state, write, Direction(direction)
            )
        
        return TMDescription(
            states=set(config.get('states', [])),
            alphabet=set(config.get('alphabet', [])),
            tape_alphabet=set(config.get('tape_alphabet', [])),
            transitions=transitions,
            start_state=config.get('start_state', ''),
            accept_states=set(config.get('accept_states', [])),
            reject_states=set(config.get('reject_states', [])),
            blank_symbol=config.get('blank_symbol', '_')
        )


class UniversalTuringMachine:
    def __init__(self):
        self.simulated_tm: Optional[TMDescription] = None
        self.simulated_state: str = ""
        self.simulated_head: int = 0
        self.simulated_tape: List[str] = []
        self.blank_symbol: str = '_'
    
    def load_tm(self, tm_config: dict):
        self.simulated_tm = TMDescription.from_dict(tm_config)
    
    def simulate_step(self) -> bool:
        if self.simulated_tm is None:
            raise ValueError("未加載要模擬的圖靈機")
        
        state = self.simulated_state
        symbol = self.simulated_tape[self.simulated_head]
        
        key = (state, symbol)
        
        if key not in self.simulated_tm.transitions:
            return False
        
        t = self.simulated_tm.transitions[key]
        
        self.simulated_tape[self.simulated_head] = t.write_symbol
        
        if t.direction == Direction.LEFT:
            self.simulated_head -= 1
            if self.simulated_head < 0:
                self.simulated_tape.insert(0, self.blank_symbol)
                self.simulated_head = 0
        elif t.direction == Direction.RIGHT:
            self.simulated_head += 1
            if self.simulated_head >= len(self.simulated_tape):
                self.simulated_tape.append(self.blank_symbol)
        
        self.simulated_state = t.new_state
        
        return True
    
    def run(self, input_string: str, max_steps: int = 10000) -> Tuple[bool, int]:
        if self.simulated_tm is None:
            raise ValueError("未加載要模擬的圖靈機")
        
        self.simulated_state = self.simulated_tm.start_state
        self.simulated_tape = list(input_string) + [self.blank_symbol]
        self.simulated_head = 0
        
        steps = 0
        
        while steps < max_steps:
            if self.simulated_state in self.simulated_tm.accept_states:
                return (True, steps)
            if self.simulated_state in self.simulated_tm.reject_states:
                return (False, steps)
            
            if not self.simulate_step():
                return (self.simulated_state in self.simulated_tm.accept_states, steps)
            
            steps += 1
        
        return (False, max_steps)


def demo_universal():
    print("=== 通用圖靈機演示 ===\n")
    
    simple_tm = {
        'states': ['q0', 'q1', 'accept', 'reject'],
        'alphabet': ['0', '1'],
        'tape_alphabet': ['0', '1', '_'],
        'start_state': 'q0',
        'accept_states': ['accept'],
        'reject_states': ['reject'],
        'blank_symbol': '_',
        'transitions': {
            ('q0', '1'): ('accept', '1', 'S'),
            ('q0', '0'): ('q0', '0', 'R'),
            ('q0', '_'): ('reject', '_', 'S'),
        }
    }
    
    utm = UniversalTuringMachine()
    utm.load_tm(simple_tm)
    
    print("模擬的圖靈機：接受所有包含 '1' 的字串\n")
    
    test_cases = ['1', '10', '101', '0', '00']
    
    for input_str in test_cases:
        accepted, steps = utm.run(input_str)
        print(f"  '{input_str}': {'接受' if accepted else '拒絕'} ({steps} 步)")


if __name__ == "__main__":
    demo_universal()
