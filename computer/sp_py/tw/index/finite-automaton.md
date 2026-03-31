# 有限狀態自動機 (Finite Automaton)

## 概述

有限狀態自動機（Finite Automaton，FA）是計算理論中的基本概念，用於模擬具有有限數量狀態的系統。它分為確定性有限自動機（DFA）和非確定性有限自動機（NFA），是正規表達式的理論基礎。

## 歷史

- **1956**：Mealy 和 Moore 發明有限狀態機
- **1959**：Rabin 和 Scott 發表 NFA 到 DFA 轉換
- **現在**：广泛用於正規表達式、 lex、電路設計

## DFA 與 NFA

### 1. DFA（確定性有限自動機）

DFA 每個狀態對每個輸入只有唯一轉換：

```python
class DFA:
    def __init__(self, states, alphabet, transition, start, accept):
        self.states = states           # 狀態集合
        self.alphabet = alphabet       # 輸入字母表
        self.transition = transition   # 轉換函數
        self.start = start             # 起始狀態
        self.accept = accept           # 接受狀態集合
    
    def accepts(self, input_string):
        state = self.start
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False
            state = self.transition.get((state, symbol))
            if state is None:
                return False
        return state in self.accept

# 範例：匹配以 'ab' 結尾的字串
dfa = DFA(
    states={'q0', 'q1', 'q2'},
    alphabet={'a', 'b'},
    transition={
        ('q0', 'a'): 'q1',
        ('q0', 'b'): 'q0',
        ('q1', 'a'): 'q1',
        ('q1', 'b'): 'q2',
        ('q2', 'a'): 'q1',
        ('q2', 'b'): 'q0',
    },
    start='q0',
    accept={'q2'}
)

print(dfa.accepts("ab"))    # True
print(dfa.accepts("aab"))   # True
print(dfa.accepts("aabb"))  # True
print(dfa.accepts("ba"))    # False
```

### 2. NFA（非確定性有限自動機）

NFA 一個狀態對同一輸入可有多個轉換：

```python
class NFA:
    def __init__(self, states, alphabet, transition, start, accept):
        self.states = states
        self.alphabet = alphabet
        self.transition = transition
        self.start = start
        self.accept = accept
    
    def epsilon_closure(self, states):
        """計算 epsilon 閉包（空字元轉換）"""
        closure = set(states)
        stack = list(states)
        
        while stack:
            state = stack.pop()
            for next_state in self.transition.get((state, ''), []):
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        return closure
    
    def move(self, states, symbol):
        """計算從某狀態集合接受符號後可達的狀態"""
        result = set()
        for state in states:
            result.update(self.transition.get((state, symbol), []))
        return result
    
    def accepts(self, input_string):
        current_states = self.epsilon_closure({self.start})
        
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False
            current_states = self.epsilon_closure(
                self.move(current_states, symbol)
            )
        
        return bool(current_states & self.accept)

# 範例：匹配 ab*（a 後面多個 b）
nfa = NFA(
    states={'q0', 'q1', 'q2'},
    alphabet={'a', 'b'},
    transition={
        ('q0', 'a'): {'q1'},
        ('q1', 'b'): {'q1', 'q2'},
    },
    start='q0',
    accept={'q2'}
)

print(nfa.accepts("ab"))    # True
print(nfa.accepts("abb"))   # True
print(nfa.accepts("abbb"))  # True
print(nfa.accepts("a"))     # False
```

### 3. NFA 到 DFA 轉換（子集建構）

```python
def nfa_to_dfa(nfa):
    """將 NFA 轉換為 DFA"""
    dfa_transition = {}
    start_closure = nfa.epsilon_closure({nfa.start})
    start_state = frozenset(start_closure)
    
    queue = [start_state]
    dfa_states = {start_state}
    
    while queue:
        current = queue.pop(0)
        dfa_transition[current] = {}
        
        for symbol in nfa.alphabet:
            new_closure = nfa.epsilon_closure(
                nfa.move(current, symbol)
            )
            
            if new_closure:
                new_state = frozenset(new_closure)
                dfa_transition[current][symbol] = new_state
                
                if new_state not in dfa_states:
                    dfa_states.add(new_state)
                    queue.append(new_state)
    
    accept_states = {
        s for s in dfa_states
        if s & nfa.accept
    }
    
    return DFA(
        states=dfa_states,
        alphabet=nfa.alphabet,
        transition=dfa_transition,
        start=start_state,
        accept=accept_states
    )
```

## 正規表達式到 NFA（Thompson 建構）

```python
def regex_to_nfa(regex):
    """將正規表達式轉換為 NFA"""
    # 簡化版本，實際實現複雜
    pass

# Thompson 建構法規則：
# 1. 基本符號：建立簡單的 NFA
# 2. 連接：串接兩個 NFA
# 3. 或（|）：建立分支 NFA
# 4. 星號（*）：建立迴圈 NFA
```

## 自動機圖示

```
     a       b
→ q0 ──→ q1 ──→ q2 (接受)
```

```
     a           b
→ q0 ──→ (q1) ──→ q2 ──→ (q3)
         ↑_____________|
            b（迴圈）
```

## 為什麼學習有限狀態自動機？

1. **理論基礎**：理解正規語言
2. **正規表達式**：理解 regex 運作原理
3. **詞法分析**： lexer 實現基礎
4. **電路設計**：硬體狀態機

## 參考資源

- "Introduction to Automata Theory"
- "Compilers: Principles, Techniques, and Tools"
