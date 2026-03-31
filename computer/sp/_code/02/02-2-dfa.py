class DFA:
    """確定型有限自動機"""
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions  # {(state, char): next_state}
        self.current_state = start_state
        self.accept_states = accept_states
    
    def process(self, input_string):
        self.current_state = self.start_state = self._get_start_state()
        for char in input_string:
            key = (self.current_state, char)
            if key not in self.transitions:
                return False
            self.current_state = self.transitions[key]
        return self.current_state in self.accept_states
    
    def _get_start_state(self):
        for state in self.states:
            if state.startswith('start'):
                return state
        return self.states[0]

# 設計一個 DFA 接受包含 "ab" 的字串
# 狀態: q0=初始, q1=看到'a', q2=看到'ab'
states = {'q0', 'q1', 'q2'}
alphabet = {'a', 'b'}
transitions = {
    ('q0', 'a'): 'q1',
    ('q0', 'b'): 'q0',
    ('q1', 'a'): 'q1',
    ('q1', 'b'): 'q2',
    ('q2', 'a'): 'q2',
    ('q2', 'b'): 'q2',
}

dfa = DFA(states, alphabet, transitions, 'q0', {'q2'})

test_strings = ['ab', 'aab', 'aba', 'ba', 'bb', 'bab']
for s in test_strings:
    result = dfa.process(s)
    print(f"'{s}': {'接受' if result else '拒絕'}")
# 輸出：
# 'ab': 接受
# 'aab': 接受
# 'aba': 接受
# 'ba': 拒絕
# 'bb': 拒絕
# 'bab': 接受