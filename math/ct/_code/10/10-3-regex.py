"""
正則表達式引擎
Thompson構造法
"""

from typing import Set, Dict, List
from dataclasses import dataclass, field

@dataclass
class State:
    id: int
    label: str = ''
    transitions: Dict[str, Set['State']] = field(default_factory=dict)
    
    def __hash__(self):
        return hash(self.id)

@dataclass
class Fragment:
    start: State
    end: State

class RegexEngine:
    def __init__(self):
        self.state_counter = 0
        self.epsilon = 'ε'
    
    def new_state(self, label: str = '') -> State:
        s = State(self.state_counter, label)
        self.state_counter += 1
        return s
    
    def literal(self, c: str) -> Fragment:
        start = self.new_state()
        end = self.new_state()
        start.transitions[c] = {end}
        return Fragment(start, end)
    
    def concat(self, f1: Fragment, f2: Fragment) -> Fragment:
        f1.end.transitions[self.epsilon] = {f2.start}
        return Fragment(f1.start, f2.end)
    
    def union(self, f1: Fragment, f2: Fragment) -> Fragment:
        start = self.new_state()
        end = self.new_state()
        
        start.transitions[self.epsilon] = {f1.start, f2.start}
        f1.end.transitions[self.epsilon] = {end}
        f2.end.transitions[self.epsilon] = {end}
        
        return Fragment(start, end)
    
    def star(self, f: Fragment) -> Fragment:
        start = self.new_state()
        end = self.new_state()
        
        start.transitions[self.epsilon] = {f.start, end}
        f.end.transitions[self.epsilon] = {f.start, end}
        
        return Fragment(start, end)
    
    def nfa_accepts(self, fragment: Fragment, input_string: str) -> bool:
        current_states = self._epsilon_closure({fragment.start})
        
        for c in input_string:
            next_states = set()
            for state in current_states:
                if c in state.transitions:
                    next_states.update(state.transitions[c])
            current_states = self._epsilon_closure(next_states)
        
        return fragment.end in current_states
    
    def _epsilon_closure(self, states: Set[State]) -> Set[State]:
        closure = set(states)
        stack = list(states)
        
        while stack:
            state = stack.pop()
            if self.epsilon in state.transitions:
                for next_state in state.transitions[self.epsilon]:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
        
        return closure


def demo_regex():
    print("=== 正則表達式引擎演示 ===\n")
    
    engine = RegexEngine()
    
    patterns = [
        ('ab*', ['a', 'ab', 'abb', 'abbb', 'b']),
        ('a|b', ['a', 'b', 'ab', 'c']),
    ]
    
    for pattern, tests in patterns:
        print(f"模式：/{pattern}/\n")
        
        # 簡化的解析
        if pattern == 'ab*':
            nfa = engine.concat(engine.literal('a'), engine.star(engine.literal('b')))
        elif pattern == 'a|b':
            nfa = engine.union(engine.literal('a'), engine.literal('b'))
        else:
            nfa = engine.literal(pattern)
        
        for test in tests:
            result = engine.nfa_accepts(nfa, test)
            print(f"  {'✓' if result else '✗'} '{test}'")
        
        print()


if __name__ == "__main__":
    demo_regex()
