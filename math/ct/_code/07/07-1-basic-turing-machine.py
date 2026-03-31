"""
圖靈機模擬器 - 基本實現
"""

from typing import Dict, Tuple, Optional, List, Set
from enum import Enum
from dataclasses import dataclass
from abc import ABC, abstractmethod

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
class Configuration:
    tape: List[str]
    head: int
    state: str

class TuringMachine(ABC):
    def __init__(self):
        self.states: Set[str] = set()
        self.alphabet: Set[str] = set()
        self.tape_alphabet: Set[str] = set()
        self.transitions: Dict[Tuple[str, str], Transition] = {}
        self.start_state: str = ""
        self.accept_states: Set[str] = set()
        self.reject_states: Set[str] = set()
        self.blank_symbol: str = '_'
    
    @abstractmethod
    def get_initial_config(self, input_string: str) -> Configuration:
        pass
    
    def load_from_dict(self, config: dict):
        self.states = set(config.get('states', []))
        self.alphabet = set(config.get('alphabet', []))
        self.tape_alphabet = set(config.get('tape_alphabet', []))
        self.start_state = config.get('start_state', '')
        self.accept_states = set(config.get('accept_states', []))
        self.reject_states = set(config.get('reject_states', []))
        self.blank_symbol = config.get('blank_symbol', '_')
        
        for (state, symbol), (new_state, write, direction) in config.get('transitions', {}).items():
            self.transitions[(state, symbol)] = Transition(
                new_state, write, Direction(direction)
            )
    
    def step(self, config: Configuration) -> Optional[Configuration]:
        key = (config.state, config.tape[config.head])
        
        if key not in self.transitions:
            return None
        
        t = self.transitions[key]
        
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
        
        return Configuration(
            tape=new_tape,
            head=new_head,
            state=t.new_state
        )
    
    def run(self, input_string: str, max_steps: int = 10000, 
            trace: bool = False) -> Tuple[bool, int]:
        config = self.get_initial_config(input_string)
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


class StandardTM(TuringMachine):
    def get_initial_config(self, input_string: str) -> Configuration:
        tape = list(input_string) + [self.blank_symbol]
        return Configuration(tape=tape, head=0, state=self.start_state)


def demo_basic():
    print("=== 基本圖靈機演示 ===\n")
    
    config = {
        'states': ['q0', 'q1', 'accept', 'reject'],
        'alphabet': ['0', '1'],
        'tape_alphabet': ['0', '1', '_'],
        'start_state': 'q0',
        'accept_states': ['accept'],
        'reject_states': ['reject'],
        'blank_symbol': '_',
        'transitions': {
            ('q0', '1'): ('q1', '1', 'R'),
            ('q0', '0'): ('reject', '0', 'S'),
            ('q0', '_'): ('reject', '_', 'S'),
            ('q1', '0'): ('q1', '0', 'R'),
            ('q1', '1'): ('q1', '1', 'R'),
            ('q1', '_'): ('accept', '_', 'S'),
        }
    }
    
    tm = StandardTM()
    tm.load_from_dict(config)
    
    test_cases = ['1', '10', '101', '100', '0', '01']
    
    for input_str in test_cases:
        accepted, steps = tm.run(input_str)
        print(f"  '{input_str}': {'接受' if accepted else '拒絕'} ({steps} 步)")


if __name__ == "__main__":
    demo_basic()
