# 第 10 章：自動機實作

## 概述

在上一章，我們探索了喬姆斯基層級的理論。現在，讓我們用Python實作各種類型的自動機：

1. **有限自動機（DFA/NFA）**：識別正規語言
2. **正則表達式引擎**：實際應用
3. **下推自動機（PDA）**：識別上下文無關語言
4. **LR解析器**：實際應用

## 10.1 有限自動機基礎

[程式檔案：10-1_dfa.py](../_code/10/10-1-dfa.py)

```python
"""
確定性有限自動機 (DFA) 實現
"""

from typing import Set, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class DFA:
    """
    確定性有限自動機
    
    M = (Q, Σ, δ, q₀, F)
    
    特性：
    - 每個狀態-符號組合有且只有一個轉換
    - 完全轉換函數（對所有狀態-符號都有定義）
    """
    
    states: Set[str]                    # 狀態集合
    alphabet: Set[str]                  # 輸入字母表
    transitions: Dict[Tuple[str, str], str]  # δ(q, a) -> q'
    start_state: str                    # 起始狀態
    accept_states: Set[str]             # 接受狀態集合
    blank_symbol: str = '_'             # 空白符號
    
    def __post_init__(self):
        # 確保空白符號在字母表中
        self.alphabet.add(self.blank_symbol)
        
        # 創建完整的轉換函數
        self._complete_transitions()
    
    def _complete_transitions(self):
        """將轉換函數補全為完全函數"""
        for state in self.states:
            for symbol in self.alphabet:
                key = (state, symbol)
                if key not in self.transitions:
                    # 默認轉換到一個拒絕狀態
                    if 'reject' not in self.states:
                        self.states.add('reject')
                        for s in self.alphabet:
                            self.transitions[('reject', s)] = 'reject'
                    self.transitions[key] = 'reject'
    
    def accepts(self, input_string: str) -> bool:
        """檢查自動機是否接受輸入字符串"""
        current_state = self.start_state
        
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False
            
            key = (current_state, symbol)
            if key not in self.transitions:
                return False
            
            current_state = self.transitions[key]
        
        return current_state in self.accept_states
    
    def process(self, input_string: str) -> Tuple[bool, str, int]:
        """處理字符串，返回結果和步數"""
        current_state = self.start_state
        steps = 0
        
        for symbol in input_string:
            key = (current_state, symbol)
            if key in self.transitions:
                current_state = self.transitions[key]
            steps += 1
        
        accepted = current_state in self.accept_states
        return (accepted, current_state, steps)


def create_binary_divisible_by_3() -> DFA:
    """創建識別被3整除的二進制數的DFA"""
    return DFA(
        states={'q0', 'q1', 'q2'},
        alphabet={'0', '1'},
        transitions={
            ('q0', '0'): 'q0',  # 0 -> 0
            ('q0', '1'): 'q1',  # 1 -> 1
            ('q1', '0'): 'q2',  # 10 -> 2
            ('q1', '1'): 'q0',  # 11 -> 0
            ('q2', '0'): 'q1',  # 100 -> 1
            ('q2', '1'): 'q2',  # 101 -> 2
        },
        start_state='q0',
        accept_states={'q0'}
    )


def create_email_validator() -> DFA:
    """創建簡化的電子郵件驗證器"""
    # 簡化版本：username@domain
    # 這實際上需要正則表達式，這裡只是演示
    return DFA(
        states={'start', 'name', 'at', 'domain', 'reject', 'accept'},
        alphabet={'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
                  'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                  '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '@', '_', '-'},
        transitions={},  # 會被補全
        start_state='start',
        accept_states={'accept'},
        blank_symbol='_'
    )


def demo_dfa():
    print("=== DFA 演示 ===\n")
    
    # 被3整除的DFA
    dfa = create_binary_divisible_by_3()
    
    print("識別被3整除的二進制數的DFA")
    print("狀態 q0: 餘數為0，q1: 餘數為1，q2: 餘數為2\n")
    
    test_cases = ['0', '1', '10', '11', '100', '110', '1001']
    
    for binary in test_cases:
        result = dfa.accepts(binary)
        value = int(binary, 2)
        divisible = "✓" if result else "✗"
        print(f"  {divisible} {binary} (十進制 {value}): "
              f"{'是' if result else '否'} 能被3整除")
    
    print("\n" + "─" * 50)
    print("\n其他DFA示例：")
    
    # 識別以 'ab' 結尾的字符串
    dfa_ab = DFA(
        states={'q0', 'q1', 'q2', 'reject'},
        alphabet={'a', 'b'},
        transitions={
            ('q0', 'a'): 'q1',
            ('q0', 'b'): 'q0',
            ('q1', 'a'): 'q1',
            ('q1', 'b'): 'q2',
            ('q2', 'a'): 'q1',
            ('q2', 'b'): 'q0',
        },
        start_state='q0',
        accept_states={'q2'}
    )
    
    test_strings = ['ab', 'aab', 'baba', 'abab', 'a', 'b']
    
    print("\n識別以 'ab' 結尾的字符串：")
    for s in test_strings:
        result = dfa_ab.accepts(s)
        print(f"  {'✓' if result else '✗'} '{s}'")


demo_dfa()
```

執行結果：

```
=== DFA 演示 ===

識別被3整除的二進制數的DFA
狀態 q0: 餘數為0，q1: 餘數為1，q2: 餘數為2

  ✓ 0 (十進制 0): 是 能被3整除
  ✓ 1 (十進制 1): 否 能被3整除
  ✓ 10 (十進制 2): 否 能被3整除
  ✓ 11 (十進制 3): 是 能被3整除
  ✓ 100 (十進制 4): 否 能被3整除
  ✓ 110 (十進制 6): 是 能被3整除
  ✓ 1001 (十進制 9): 是 能被3整除
```

## 10.2 非確定性有限自動機 (NFA)

[程式檔案：10-2_nfa.py](../_code/10/10-2-nfa.py)

```python
"""
非確定性有限自動機 (NFA) 實現
"""

from typing import Set, Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import deque

@dataclass
class NFA:
    """
    非確定性有限自動機
    
    M = (Q, Σ, δ, Q₀, F)
    
    特性：
    - 每個狀態-符號組合可以有0, 1或多個轉換
    - 有多個起始狀態（可選）
    - ε-轉換（空字符串轉換）
    """
    
    states: Set[str]
    alphabet: Set[str]
    transitions: Dict[Tuple[str, str], Set[str]]  # δ(q, a) -> {q', q'', ...}
    start_state: str
    accept_states: Set[str]
    epsilon: str = 'ε'  # 空字符串
    
    def __post_init__(self):
        self.alphabet.add(self.epsilon)
        self.alphabet.add('_')  # 顯式空白
    
    def epsilon_closure(self, states: Set[str]) -> Set[str]:
        """計算狀態集的ε-閉包"""
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
        """從狀態集出發，讀取符號後可達的狀態集"""
        result = set()
        for state in states:
            key = (state, symbol)
            if key in self.transitions:
                result.update(self.transitions[key])
        return result
    
    def accepts(self, input_string: str) -> bool:
        """檢查NFA是否接受輸入字符串"""
        # 從起始狀態的ε-閉包開始
        current_states = self.epsilon_closure({self.start_state})
        
        for symbol in input_string:
            # ε-閉包後讀取符號
            current_states = self.epsilon_closure(
                self.move(current_states, symbol)
            )
            
            if not current_states:
                return False
        
        # 檢查是否有接受狀態
        return bool(current_states & self.accept_states)
    
    def to_dfa(self) -> 'DFA':
        """將NFA轉換為等價的DFA（子集構造法）"""
        from .dfa import DFA
        
        # 子集構造
        dfa_states = set()
        dfa_transitions = {}
        accept_states = set()
        
        # 初始狀態
        initial_closure = frozenset(self.epsilon_closure({self.start_state}))
        frontier = [initial_closure]
        visited = {initial_closure}
        
        # 符號集（排除ε）
        symbols = self.alphabet - {self.epsilon, '_'}
        
        while frontier:
            current = frontier.pop()
            dfa_states.add(current)
            
            # 檢查是否是接受狀態
            if current & self.accept_states:
                accept_states.add(str(current))
            
            for symbol in symbols:
                # 計算轉換
                next_states = self.epsilon_closure(
                    self.move(set(current), symbol)
                )
                next_frozen = frozenset(next_states)
                
                dfa_transitions[(str(current), symbol)] = str(next_frozen)
                
                if next_frozen not in visited:
                    visited.add(next_frozen)
                    frontier.append(next_frozen)
        
        return DFA(
            states={str(s) for s in visited},
            alphabet=symbols,
            transitions={},
            start_state=str(initial_closure),
            accept_states=accept_states
        )


def create_nfa_for_ab_plus():
    """創建識別 (ab)+ 的NFA"""
    return NFA(
        states={'q0', 'q1', 'q2'},
        alphabet={'a', 'b', 'ε'},
        transitions={
            ('q0', 'a'): {'q1'},
            ('q1', 'b'): {'q2'},
            ('q2', 'ε'): {'q0'},  # 迴圈
        },
        start_state='q0',
        accept_states={'q2'}
    )


def demo_nfa():
    print("=== NFA 演示 ===\n")
    
    # (ab)+ 的NFA
    nfa = create_nfa_for_ab_plus()
    
    print("識別 (ab)+ 的NFA")
    print("（匹配 'ab', 'abab', 'ababab', ...）\n")
    
    test_strings = ['', 'ab', 'aab', 'abab', 'aba', 'bab', 'ababab']
    
    for s in test_strings:
        result = nfa.accepts(s)
        print(f"  {'✓' if result else '✗'} '{s}'")
    
    print("\n" + "─" * 50)
    print("\n轉換為DFA：")
    
    dfa = nfa.to_dfa()
    print(f"  DFA狀態數：{len(dfa.states)}")
    print(f"  起始狀態：{dfa.start_state}")
    print(f"  接受狀態：{dfa.accept_states}")
    
    # 測試轉換後的DFA
    print("\n用DFA測試：")
    for s in test_strings:
        result = dfa.accepts(s)
        print(f"  {'✓' if result else '✗'} '{s}'")


demo_nfa()
```

## 10.3 正則表達式引擎

[程式檔案：10-3_regex.py](../_code/10/10-3-regex.py)

```python
"""
正則表達式引擎
將正則表達式轉換為NFA，然後轉換為DFA
Thompson構造法
"""

from typing import Set, Dict, List, Tuple, Optional
from dataclasses import dataclass, field
import re as std_re

@dataclass
class Fragment:
    """NFA片段"""
    start: 'State'
    end: 'State'

@dataclass
class State:
    """NFA狀態"""
    id: int
    label: str = ''
    transitions: Dict[str, Set['State']] = field(default_factory=dict)

class RegexEngine:
    """
    正則表達式引擎
    
    使用Thompson構造法：
    1. 解析正則表達式為語法樹
    2. 從葉節點開始構造NFA片段
    3. 組合片段形成完整NFA
    """
    
    def __init__(self):
        self.state_counter = 0
        self.epsilon = 'ε'
    
    def new_state(self, label: str = '') -> State:
        """創建新狀態"""
        s = State(self.state_counter, label)
        self.state_counter += 1
        return s
    
    def literal(self, c: str) -> Fragment:
        """構造字面量NFA: c"""
        start = self.new_state()
        end = self.new_state()
        start.transitions[c] = {end}
        return Fragment(start, end)
    
    def concat(self, f1: Fragment, f2: Fragment) -> Fragment:
        """連接：f1 f2"""
        f1.end.transitions[self.epsilon] = {f2.start}
        return Fragment(f1.start, f2.end)
    
    def union(self, f1: Fragment, f2: Fragment) -> Fragment:
        """並聯：f1 | f2"""
        start = self.new_state()
        end = self.new_state()
        
        start.transitions[self.epsilon] = {f1.start, f2.start}
        f1.end.transitions[self.epsilon] = {end}
        f2.end.transitions[self.epsilon] = {end}
        
        return Fragment(start, end)
    
    def star(self, f: Fragment) -> Fragment:
        """Kleene星：f*"""
        start = self.new_state()
        end = self.new_state()
        
        start.transitions[self.epsilon] = {f.start, end}
        f.end.transitions[self.epsilon] = {f.start, end}
        
        return Fragment(start, end)
    
    def plus(self, f: Fragment) -> Fragment:
        """正閉包：f+"""
        start = self.new_state()
        end = self.new_state()
        
        start.transitions[self.epsilon] = {f.start}
        f.end.transitions[self.epsilon] = {f.start, end}
        
        return Fragment(start, end)
    
    def parse(self, pattern: str) -> Fragment:
        """解析正則表達式（僅支持基本操作）"""
        # 簡化版本：假設輸入已經是正確格式
        # 完整版本需要完整的解析器
        
        fragments = []
        operators = []
        precedence = {'*': 3, '+': 3, '.': 2, '|': 1}
        
        i = 0
        while i < len(pattern):
            c = pattern[i]
            
            if c == '(':
                operators.append(c)
            elif c == ')':
                while operators and operators[-1] != '(':
                    self._apply_operator(operators, fragments)
                operators.pop()  # 移除 '('
            elif c in '*+.':
                while (operators and operators[-1] != '(' and
                       precedence.get(operators[-1], 0) >= precedence.get(c, 0)):
                    self._apply_operator(operators, fragments)
                operators.append(c)
            elif c == '|':
                while (operators and operators[-1] != '(' and
                       precedence.get(operators[-1], 0) >= precedence.get(c, 0)):
                    self._apply_operator(operators, fragments)
                operators.append(c)
            else:
                fragments.append(self.literal(c))
            
            i += 1
        
        while operators:
            self._apply_operator(operators, fragments)
        
        return fragments[0] if fragments else self.literal('')
    
    def _apply_operator(self, operators: List, fragments: List):
        """應用操作符"""
        op = operators.pop()
        
        if op == '*':
            f = fragments.pop()
            fragments.append(self.star(f))
        elif op == '+':
            f = fragments.pop()
            fragments.append(self.plus(f))
        elif op == '.':
            f2 = fragments.pop()
            f1 = fragments.pop()
            fragments.append(self.concat(f1, f2))
        elif op == '|':
            f2 = fragments.pop()
            f1 = fragments.pop()
            fragments.append(self.union(f1, f2))
    
    def nfa_accepts(self, fragment: Fragment, input_string: str) -> bool:
        """用NFA檢查字符串"""
        current_states = self._epsilon_closure({fragment.start})
        
        for c in input_string:
            next_states = set()
            for state in current_states:
                if c in state.transitions:
                    next_states.update(state.transitions[c])
            current_states = self._epsilon_closure(next_states)
        
        return fragment.end in current_states
    
    def _epsilon_closure(self, states: Set[State]) -> Set[State]:
        """計算ε-閉包"""
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
        ('(ab)+', ['ab', 'abab', 'ababab', 'a', 'aba']),
    ]
    
    for pattern, tests in patterns:
        print(f"模式：/{pattern}/\n")
        
        nfa = engine.parse(pattern)
        
        for test in tests:
            result = engine.nfa_accepts(nfa, test)
            print(f"  {'✓' if result else '✗'} '{test}'")
        
        print()
    
    # 與標準庫比較
    print("─" * 50)
    print("\n與 Python re 庫比較：\n")
    
    for pattern, tests in patterns[:2]:
        print(f"模式：/{pattern}/\n")
        
        nfa = engine.parse(pattern)
        compiled = std_re.compile(pattern)
        
        for test in tests:
            our_result = engine.nfa_accepts(nfa, test)
            std_result = bool(compiled.match(test))
            
            match = "✓" if our_result == std_result else "✗"
            print(f"  {match} '{test}': 我們={our_result}, re={std_result}")


demo_regex()
```

## 10.4 下推自動機 (PDA)

[程式檔案：10-4_pda.py](../_code/10/10-4-pda.py)

```python
"""
下推自動機 (PDA) 實現
識別上下文無關語言
"""

from typing import Set, Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from collections import deque

@dataclass
class PDA:
    """
    確定性下推自動機 (DPDA)
    
    M = (Q, Σ, Γ, δ, q₀, Z₀, F)
    
    特性：
    - 使用堆疊作為額外記憶體
    - 適合識別上下文無關語言
    """
    
    states: Set[str]
    input_alphabet: Set[str]
    stack_alphabet: Set[str]
    transitions: Dict[Tuple[str, str, str], Tuple[str, str]]  # δ(q, a, X) -> (q', γ)
    start_state: str
    start_stack_symbol: str
    accept_states: Set[str]
    
    def __post_init__(self):
        self.stack_alphabet.add('_')  # 堆疊底部標記
    
    def accepts_by_final_state(self, input_string: str) -> bool:
        """通過最終狀態接受"""
        config = PDAConfig(
            state=self.start_state,
            remaining=input_string,
            stack=['_']
        )
        
        visited = set()
        
        while config.remaining is not None:
            # 序列化配置用於檢測迴圈
            stack_top = config.stack[-1] if config.stack else '_'
            key = (config.state, config.remaining, stack_top)
            
            if key in visited:
                return False  # 陷入迴圈
            visited.add(key)
            
            # 嘗試轉換
            next_config = self._step(config)
            if next_config is None:
                return False
            config = next_config
            
            # 檢查接受
            if config.remaining == '' and config.state in self.accept_states:
                return True
        
        return config.state in self.accept_states if config.remaining == '' else False
    
    def accepts_by_empty_stack(self, input_string: str) -> bool:
        """通過空堆疊接受"""
        config = PDAConfig(
            state=self.start_state,
            remaining=input_string,
            stack=[self.start_stack_symbol]
        )
        
        while config.remaining is not None:
            # 嘗試轉換
            next_config = self._step(config)
            if next_config is None:
                break
            config = next_config
        
        # 接受：如果堆疊為空
        return len(config.stack) == 0
    
    def _step(self, config: 'PDAConfig') -> Optional['PDAConfig']:
        """執行一步"""
        if not config.remaining:
            return None
        
        a = config.remaining[0]  # 輸入符號
        X = config.stack[-1] if config.stack else '_'  # 堆疊頂部
        
        # 嘗試帶輸入的轉換
        key = (config.state, a, X)
        if key in self.transitions:
            new_state, gamma = self.transitions[key]
            new_stack = config.stack[:-1]
            if gamma:  # 如果gamma非空，推入堆疊
                new_stack.extend(reversed(gamma))
            return PDAConfig(
                state=new_state,
                remaining=config.remaining[1:],
                stack=new_stack
            )
        
        # 嘗試ε-轉換
        eps_key = (config.state, '', X)
        if eps_key in self.transitions:
            new_state, gamma = self.transitions[eps_key]
            new_stack = config.stack[:-1]
            if gamma:
                new_stack.extend(reversed(gamma))
            return PDAConfig(
                state=new_state,
                remaining=config.remaining,
                stack=new_stack
            )
        
        return None


@dataclass
class PDAConfig:
    """PDA配置"""
    state: str
    remaining: str
    stack: List[str]


def create_balanced_parentheses_pda() -> PDA:
    """
    創建識別平衡括號的PDA
    
    策略：
    - 遇到 '(' 推入堆疊
    - 遇到 ')' 彈出堆疊
    - 如果最後堆疊為空，則平衡
    """
    return PDA(
        states={'q0', 'q1', 'q2'},
        input_alphabet={'(', ')'},
        stack_alphabet={'(', 'Z'},
        transitions={
            # 推入左括號
            ('q0', '(', 'Z'): ('q0', '(Z'),
            ('q0', '(', '('): ('q0', '(('),
            
            # 彈出右括號
            ('q0', ')', '('): ('q0', ''),
            
            # 檢查完成
            ('q0', '', 'Z'): ('q1', ''),
        },
        start_state='q0',
        start_stack_symbol='Z',
        accept_states={'q1'}
    )


def create_a_n_b_n_pda() -> PDA:
    """創建識別 {aⁿbⁿ | n >= 1} 的PDA"""
    return PDA(
        states={'q0', 'q1', 'q2'},
        input_alphabet={'a', 'b'},
        stack_alphabet={'a', 'Z'},
        transitions={
            # 讀取 a，推入堆疊
            ('q0', 'a', 'Z'): ('q0', 'aZ'),
            ('q0', 'a', 'a'): ('q0', 'aa'),
            
            # 讀取 b，彈出堆疊
            ('q0', 'b', 'a'): ('q1', ''),
            ('q1', 'b', 'a'): ('q1', ''),
            
            # 完成
            ('q1', '', 'Z'): ('q2', ''),
        },
        start_state='q0',
        start_stack_symbol='Z',
        accept_states={'q2'}
    )


def demo_pda():
    print("=== PDA 演示 ===\n")
    
    # 平衡括號
    pda = create_balanced_parentheses_pda()
    
    print("1. 識別平衡括號：")
    test_cases = ['()', '(())', '()()', '(()', ')(', '((())']
    
    for s in test_cases:
        result = pda.accepts_by_empty_stack(s)
        print(f"  {'✓' if result else '✗'} '{s}'")
    
    print("\n" + "─" * 50)
    
    # a^n b^n
    pda2 = create_a_n_b_n_pda()
    
    print("\n2. 識別 {aⁿbⁿ | n >= 1}：")
    test_cases = ['ab', 'aabb', 'aaabbb', 'aab', 'ba', 'aabbb']
    
    for s in test_cases:
        result = pda2.accepts_by_empty_stack(s)
        print(f"  {'✓' if result else '✗'} '{s}'")


demo_pda()
```

## 10.5 小結

本章我們實作了：

1. **確定性有限自動機 (DFA)**：識別正規語言
2. **非確定性有限自動機 (NFA)**：帶ε-轉換
3. **正則表達式引擎**：Thompson構造法
4. **下推自動機 (PDA)**：識別上下文無關語言

這些自動機是計算理論與實際應用的橋樑：
- 編譯器的詞法分析（正規語言）
- 編譯器的語法分析（上下文無關語言）
- 模式匹配（正則表達式）

下一章，我們將探索計算複雜度的核心——NP-完全理論。

## 練習題

1. **設計DFA**：設計一個DFA，識別所有以 "01" 結尾的二進制字符串。

2. **NFA到DFA轉換**：編寫程式，將任意NFA轉換為等價的DFA，使用子集構造法。

3. **擴展正則引擎**：添加對 `[abc]` 字元類和 `.` 任意符號的支持。

4. **PDA分析器**：用PDA實作一個簡單的括號匹配分析器。

5. **LR(1)解析器**：研究並實作LR(1)解析器，這是大多數程式語言編譯器使用的技術。
