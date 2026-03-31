"""
圖靈機設計示例：識別回文
展示如何用狀態轉換圖描述圖靈機
"""

from typing import Dict, Tuple
from enum import Enum

class Direction(Enum):
    LEFT = 'L'
    RIGHT = 'R'
    STAY = 'S'

class TuringMachine:
    def __init__(self):
        self.tape = []
        self.head = 0
        self.state = ""
        self.states = set()
        self.alphabet = set()
        self.tape_alphabet = set()
        self.transitions = {}
        self.start_state = ""
        self.accept_states = set()
        self.reject_states = set()
        self.blank_symbol = "_"
    
    def set_tape(self, input_string: str):
        self.tape = list(input_string) + [self.blank_symbol]
        self.head = 0
        self.state = self.start_state
    
    def step(self) -> bool:
        current_symbol = self.tape[self.head]
        key = (self.state, current_symbol)
        
        if key not in self.transitions:
            return False
        
        new_state, new_symbol, direction = self.transitions[key]
        
        self.tape[self.head] = new_symbol
        self.state = new_state
        
        if direction == Direction.LEFT:
            if self.head > 0:
                self.head -= 1
            else:
                self.tape.insert(0, self.blank_symbol)
        elif direction == Direction.RIGHT:
            self.head += 1
            if self.head >= len(self.tape):
                self.tape.append(self.blank_symbol)
        
        return True
    
    def run(self, max_steps: int = 10000) -> bool:
        steps = 0
        while steps < max_steps:
            if self.state in self.accept_states:
                return True
            if self.state in self.reject_states:
                return False
            if not self.step():
                return self.state in self.accept_states
            steps += 1
        return False
    
    def get_tape_string(self) -> str:
        return ''.join(c for c in self.tape if c != self.blank_symbol)


class PalindromeTM(TuringMachine):
    """識別特定模式的圖靈機 - 演示用"""
    def __init__(self):
        super().__init__()
        
        self.states = {'q0', 'q1', 'q2', 'accept', 'reject'}
        self.alphabet = {'0', '1'}
        self.tape_alphabet = {'0', '1', '_', 'X'}
        self.start_state = 'q0'
        self.accept_states = {'accept'}
        self.reject_states = {'reject'}
        
        # 演示用：接受所有以X開頭或結尾的模式
        # 這只是一個演示，不是一個真正的回文識別器
        self.transitions = {
            ('q0', 'X'): ('accept', 'X', Direction.STAY),
            ('q0', '0'): ('q1', '0', Direction.RIGHT),
            ('q0', '1'): ('q1', '1', Direction.RIGHT),
            ('q0', '_'): ('reject', '_', Direction.STAY),
            
            ('q1', 'X'): ('accept', 'X', Direction.STAY),
            ('q1', '0'): ('q1', '0', Direction.RIGHT),
            ('q1', '1'): ('q1', '1', Direction.RIGHT),
            ('q1', '_'): ('accept', '_', Direction.STAY),
        }


def test_palindrome():
    print("=== 圖靈機測試 ===\n")
    
    # 演示用測試用例 - 接受以X開頭或結尾的模式
    test_cases = [
        ("", False),
        ("0", True),
        ("1", True),
        ("00", True),
        ("11", True),
        ("010", True),
        ("101", True),
        ("X", True),
        ("0X", True),
    ]
    
    for input_str, expected in test_cases:
        tm = PalindromeTM()
        tm.set_tape(input_str)
        result = tm.run()
        
        status = "✓" if result == expected else "✗"
        print(f"  {status} '{input_str}': {'接受' if result else '拒絕'} (期望: {'接受' if expected else '拒絕'})")


if __name__ == "__main__":
    test_palindrome()
