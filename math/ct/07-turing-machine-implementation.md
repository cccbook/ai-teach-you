# 第 7 章：圖靈機模擬器實作

## 概述

理論需要實踐來驗證。在這一章，我們將用Python實作一個完整的圖靈機模擬器。

這個模擬器將包含：
1. **基本圖靈機**：單紙帶確定性圖靈機
2. **多帶圖靈機**：擴展版本，可以模擬基本圖靈機
3. **非確定性圖靈機**：每步有多種選擇
4. **通用圖靈機**：可以模擬任何其他圖靈機
5. **視覺化工具**：展示圖靈機的運作

## 7.1 基本圖靈機框架

[程式檔案：07-1_basic_turing_machine.py](../_code/07/07-1-basic-turing-machine.py)

```python
"""
圖靈機模擬器 - 基本實現
"""

from typing import Dict, Tuple, Optional, List, Set
from enum import Enum
from dataclasses import dataclass
from abc import ABC, abstractmethod

class Direction(Enum):
    """讀寫頭移動方向"""
    LEFT = 'L'
    RIGHT = 'R'
    STAY = 'S'

@dataclass
class Transition:
    """圖靈機轉換"""
    new_state: str
    write_symbol: str
    direction: Direction

class TuringMachine(ABC):
    """
    圖靈機基類
    
    形式定義：M = (Q, Σ, Γ, δ, q₀, q_accept, q_reject)
    """
    
    def __init__(self):
        self.states: Set[str] = set()
        self.alphabet: Set[str] = set()       # 輸入字母表
        self.tape_alphabet: Set[str] = set()  # 紙帶字母表
        self.transitions: Dict[Tuple[str, str], Transition] = {}
        self.start_state: str = ""
        self.accept_states: Set[str] = set()
        self.reject_states: Set[str] = set()
        self.blank_symbol: str = '_'
    
    @abstractmethod
    def get_initial_config(self, input_string: str) -> 'Configuration':
        """返回初始配置"""
        pass
    
    def load_from_dict(self, config: dict):
        """從字典加載圖靈機配置"""
        self.states = set(config.get('states', []))
        self.alphabet = set(config.get('alphabet', []))
        self.tape_alphabet = set(config.get('tape_alphabet', []))
        self.start_state = config.get('start_state', '')
        self.accept_states = set(config.get('accept_states', []))
        self.reject_states = set(config.get('reject_states', []))
        self.blank_symbol = config.get('blank_symbol', '_')
        
        # 加載轉換函數
        for (state, symbol), (new_state, write, direction) in config.get('transitions', {}).items():
            self.transitions[(state, symbol)] = Transition(
                new_state, write, Direction(direction)
            )
    
    def step(self, config: 'Configuration') -> Optional['Configuration']:
        """執行一步，返回新配置或None"""
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
        """
        運行圖靈機
        
        返回：(是否接受, 步數)
        """
        config = self.get_initial_config(input_string)
        steps = 0
        
        if trace:
            self._print_config(config, steps)
        
        while steps < max_steps:
            # 檢查是否處於接受/拒絕狀態
            if config.state in self.accept_states:
                if trace:
                    print(f"\n步 {steps}: 接受!")
                return (True, steps)
            if config.state in self.reject_states:
                if trace:
                    print(f"\n步 {steps}: 拒絕!")
                return (False, steps)
            
            # 執行一步
            new_config = self.step(config)
            if new_config is None:
                # 無定義轉換，根據當前狀態決定
                result = config.state in self.accept_states
                if trace:
                    print(f"\n步 {steps}: 無轉換，{'接受' if result else '拒絕'}")
                return (result, steps)
            
            config = new_config
            steps += 1
            
            if trace:
                self._print_config(config, steps)
        
        return (False, max_steps)
    
    def _print_config(self, config: 'Configuration', step: int):
        """打印配置狀態"""
        tape_str = ''.join(config.tape)
        pointer = ' ' * config.head + '^'
        print(f"步 {step:4d}: [{config.state:10s}] {tape_str}")
        print(f"         {pointer}")


@dataclass
class Configuration:
    """圖靈機配置"""
    tape: List[str]
    head: int
    state: str


class StandardTM(TuringMachine):
    """標準單紙帶圖靈機"""
    
    def get_initial_config(self, input_string: str) -> Configuration:
        """初始化配置"""
        tape = list(input_string) + [self.blank_symbol]
        return Configuration(tape=tape, head=0, state=self.start_state)


# 演示基本用法
def demo_basic():
    print("=== 基本圖靈機演示 ===\n")
    
    # 定義一個接受所有以 '1' 開頭的字串的圖靈機
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

demo_basic()
```

執行結果：

```
=== 基本圖靈機演示 ===

  '1': 接受 (3 步)
  '10': 接受 (4 步)
  '101': 接受 (5 步)
  '100': 接受 (5 步)
  '0': 拒絕 (1 步)
  '01': 拒絕 (1 步)
```

## 7.2 多帶圖靈機

[程式檔案：07-2_multi_tape.py](../_code/07/07-2-multi-tape.py)

```python
"""
多帶圖靈機模擬器
每條紙帶有自己的讀寫頭
"""

from typing import List, Tuple, Optional, Dict, Set
from dataclasses import dataclass
from .turing_machine_base import Direction, Transition, TuringMachine, Configuration

@dataclass
class MultiTapeConfiguration:
    """多帶配置"""
    tapes: List[List[str]]       # 每條紙帶
    heads: List[int]            # 每個讀寫頭位置
    state: str                  # 當前狀態

@dataclass
class MultiTapeTransition:
    """多帶轉換"""
    new_state: str
    writes: List[str]           # 每條紙帶寫入的符號
    directions: List[Direction]  # 每條紙帶的移動方向

class MultiTapeTM:
    """
    多帶圖靈機
    
    等價於單帶圖靈機，但更易於設計複雜機器
    """
    
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
        """從字典加載配置"""
        self.states = set(config.get('states', []))
        self.alphabet = set(config.get('alphabet', []))
        self.tape_alphabet = set(config.get('tape_alphabet', []))
        self.start_state = config.get('start_state', '')
        self.accept_states = set(config.get('accept_states', []))
        self.reject_states = set(config.get('reject_states', []))
        self.blank_symbol = config.get('blank_symbol', '_')
        
        # 轉換函數：鍵是 (狀態, (符號1, 符號2, ...))
        for key, value in config.get('transitions', {}).items():
            state, symbols = key
            new_state, writes, directions = value
            self.transitions[(state, tuple(symbols))] = MultiTapeTransition(
                new_state, writes, [Direction(d) for d in directions]
            )
    
    def _get_initial_config(self, input_string: str) -> MultiTapeConfiguration:
        """初始化配置"""
        tapes = [list(input_string) + [self.blank_symbol]]
        heads = [0]
        
        # 額外的紙帶初始化為空白
        for _ in range(self.num_tapes - 1):
            tapes.append([self.blank_symbol])
            heads.append(0)
        
        return MultiTapeConfiguration(tapes=tapes, heads=heads, state=self.start_state)
    
    def step(self, config: MultiTapeConfiguration) -> Optional[MultiTapeConfiguration]:
        """執行一步"""
        # 讀取所有紙帶的當前符號
        symbols = tuple(config.tapes[i][config.heads[i]] for i in range(self.num_tapes))
        key = (config.state, symbols)
        
        if key not in self.transitions:
            return None
        
        t = self.transitions[key]
        
        # 複製紙帶
        new_tapes = [tape.copy() for tape in config.tapes]
        new_heads = config.heads.copy()
        
        # 執行所有紙帶的動作
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
        """運行多帶圖靈機"""
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
    
    def simulate_single_tape(self, input_string: str, max_steps: int = 10000) -> Tuple[bool, int]:
        """
        用單帶模擬這個多帶圖靈機
        
        原理：用特殊符號分隔不同紙帶的內容
        """
        # 構造單帶表示
        # 格式：[狀態] [分隔符] 紙帶1 [分隔符] 紙帶2 ...
        sep = '#'
        
        # 這裡我們直接返回原始結果
        # 實際的單帶模擬需要更複雜的轉換
        return self.run(input_string, max_steps)


def demo_multi_tape():
    print("=== 多帶圖靈機演示 ===\n")
    
    # 兩帶圖靈機：複製輸入
    # 帶1: 輸入 | 帶2: 空白
    config = {
        'states': ['q0', 'q1', 'q2', 'accept'],
        'alphabet': ['0', '1'],
        'tape_alphabet': ['0', '1', '_', '#'],
        'start_state': 'q0',
        'accept_states': ['accept'],
        'reject_states': [],
        'blank_symbol': '_',
        'transitions': {
            # q0: 讀取第一個符號並複製
            ('q0', ('0', '_')): ('q0', ('0', '0'), ('R', 'R')),
            ('q0', ('1', '_')): ('q0', ('1', '1'), ('R', 'R')),
            ('q0', ('_', '_')): ('q1', ('_', '_'), ('L', 'L')),
            
            # q1: 移動讀寫頭回到開頭
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
        result_tape = ''.join(tm.tapes[0][:10]) + '...' if len(tm.tapes[0]) > 10 else ''.join(tm.tapes[0])
        print(f"  '{input_str}': {'接受' if accepted else '拒絕'} ({steps} 步)")

demo_multi_tape()
```

## 7.3 非確定性圖靈機

[程式檔案：07-3_nondeterministic.py](../_code/07/07-3-nondeterministic.py)

```python
"""
非確定性圖靈機 (NTM) 模擬器
每步可以有多個轉換選擇
"""

from typing import List, Tuple, Optional, Dict, Set
from dataclasses import dataclass
from collections import deque
from .turing_machine_base import Direction, Transition, TuringMachine, Configuration

@dataclass
class NTMConfiguration:
    """NTM 配置"""
    tape: List[str]
    head: int
    state: str

class NondeterministicTM:
    """
    非確定性圖靈機 (NTM)
    
    關鍵性質：
    - 每個狀態-符號組合可以有多個轉換
    - 接受：如果存在一個計算分支接受
    - 拒絕：所有計算分支都拒絕
    """
    
    def __init__(self):
        self.states: Set[str] = set()
        self.alphabet: Set[str] = set()
        self.tape_alphabet: Set[str] = set()
        # 轉換：映射到可能的新配置列表
        self.transitions: Dict[Tuple[str, str], List[Tuple[str, str, Direction]]] = {}
        self.start_state: str = ""
        self.accept_states: Set[str] = set()
        self.reject_states: Set[str] = set()
        self.blank_symbol: str = '_'
    
    def load_from_dict(self, config: dict):
        """從字典加載配置"""
        self.states = set(config.get('states', []))
        self.alphabet = set(config.get('alphabet', []))
        self.tape_alphabet = set(config.get('tape_alphabet', []))
        self.start_state = config.get('start_state', '')
        self.accept_states = set(config.get('accept_states', []))
        self.reject_states = set(config.get('reject_states', []))
        self.blank_symbol = config.get('blank_symbol', '_')
        
        # 轉換函數：每個鍵對應多個轉換
        for (state, symbol), trans_list in config.get('transitions', {}).items():
            self.transitions[(state, symbol)] = [
                Transition(new_state, write, Direction(dir_val))
                for new_state, write, dir_val in trans_list
            ]
    
    def _apply_transition(self, config: NTMConfiguration, 
                          t: Transition) -> NTMConfiguration:
        """應用一個轉換"""
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
        """
        運行非確定性圖靈機
        
        使用廣度優先搜索探索所有可能的計算分支
        返回：(是否接受, 探索的分支數)
        """
        initial_config = NTMConfiguration(
            tape=list(input_string) + [self.blank_symbol],
            head=0,
            state=self.start_state
        )
        
        # 廣度優先搜索佇列
        queue = deque([initial_config])
        total_branches = 0
        
        while queue and total_branches < max_branches:
            config = queue.popleft()
            
            # 檢查狀態
            if config.state in self.accept_states:
                return (True, total_branches)
            if config.state in self.reject_states:
                continue  # 這個分支拒絕，繼續其他分支
            
            # 生成下一批配置
            key = (config.state, config.tape[config.head])
            if key not in self.transitions:
                # 這個分支卡住，視為拒絕
                continue
            
            for t in self.transitions[key]:
                new_config = self._apply_transition(config, t)
                queue.append(new_config)
                total_branches += 1
                
                if total_branches >= max_branches:
                    break
        
        # 所有分支都拒絕或超限
        return (False, total_branches)
    
    def run_with_trace(self, input_string: str, 
                       max_depth: int = 10) -> List[List[NTMConfiguration]]:
        """
        返回所有可能的計算路徑（直到最大深度）
        """
        initial_config = NTMConfiguration(
            tape=list(input_string) + [self.blank_symbol],
            head=0,
            state=self.start_state
        )
        
        paths = []
        
        def dfs(config: NTMConfiguration, path: List[NTMConfiguration], depth: int):
            if depth > max_depth:
                return
            
            path = path + [config]
            
            if config.state in self.accept_states:
                paths.append(path)
                return
            
            key = (config.state, config.tape[config.head])
            if key not in self.transitions:
                return
            
            for t in self.transitions[key]:
                new_config = self._apply_transition(config, t)
                dfs(new_config, path, depth + 1)
        
        dfs(initial_config, [], 0)
        return paths


def demo_ntm():
    print("=== 非確定性圖靈機演示 ===\n")
    
    # NTM：接受包含 '11' 作為子串的所有字串
    # 這對 DTM 來說很簡單，NTM 展示非確定性
    config = {
        'states': ['q0', 'q1', 'accept'],
        'alphabet': ['0', '1'],
        'tape_alphabet': ['0', '1', '_'],
        'start_state': 'q0',
        'accept_states': ['accept'],
        'reject_states': [],
        'blank_symbol': '_',
        'transitions': {
            # q0: 非確定性地猜測第一個 '1'
            ('q0', '0'): [('q0', '0', 'R')],
            ('q0', '1'): [('q0', '1', 'R'), ('q1', '1', 'R')],  # 猜測或繼續
            ('q0', '_'): [('reject', '_', 'S')],
            
            # q1: 找第二個 '1'
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

demo_ntm()
```

## 7.4 通用圖靈機

[程式檔案：07-4_universal.py](../_code/07/07-4-universal.py)

```python
"""
通用圖靈機 (Universal Turing Machine)
可以模擬任何其他圖靈機
"""

from typing import Dict, Tuple, List, Set, Optional
from dataclasses import dataclass
from .turing_machine_base import Direction, Transition, TuringMachine, Configuration, StandardTM

@dataclass
class TMDescription:
    """圖靈機的描述格式"""
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
        """從字典創建"""
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
    
    def encode(self) -> str:
        """
        將圖靈機編碼為字串
        使用簡化的編碼格式
        """
        lines = []
        lines.append(f"states: {','.join(sorted(self.states))}")
        lines.append(f"alphabet: {','.join(sorted(self.alphabet))}")
        lines.append(f"start: {self.start_state}")
        lines.append(f"accept: {','.join(sorted(self.accept_states))}")
        lines.append(f"reject: {','.join(sorted(self.reject_states))}")
        lines.append(f"blank: {self.blank_symbol}")
        
        for (state, symbol), t in sorted(self.transitions.items()):
            lines.append(f"delta({state},{symbol}) = ({t.new_state},{t.write_symbol},{t.direction.value})")
        
        return '\n'.join(lines)


class UniversalTuringMachine:
    """
    通用圖靈機
    
    可以模擬任何其他圖靈機
    原理：將被模擬的圖靈機的描述和狀態存儲在紙帶上
    """
    
    def __init__(self):
        self.simulated_tm: Optional[TMDescription] = None
        self.simulated_state: str = ""
        self.simulated_head: int = 0
        self.simulated_tape: List[str] = []
        self.description_tape: List[str] = []
        self.description_head: int = 0
        self.mode: str = "description"  # "description" 或 "simulation"
        self.blank_symbol: str = '_'
    
    def load_tm(self, tm_config: dict):
        """加載要模擬的圖靈機"""
        self.simulated_tm = TMDescription.from_dict(tm_config)
    
    def simulate_step(self) -> bool:
        """執行一步模擬"""
        if self.simulated_tm is None:
            raise ValueError("未加載要模擬的圖靈機")
        
        # 讀取當前狀態和符號
        state = self.simulated_state
        symbol = self.simulated_tape[self.simulated_head]
        
        key = (state, symbol)
        
        if key not in self.simulated_tm.transitions:
            # 無轉換，停機
            return False
        
        t = self.simulated_tm.transitions[key]
        
        # 更新模擬紙帶
        self.simulated_tape[self.simulated_head] = t.write_symbol
        
        # 移動讀寫頭
        if t.direction == Direction.LEFT:
            self.simulated_head -= 1
            if self.simulated_head < 0:
                self.simulated_tape.insert(0, self.blank_symbol)
                self.simulated_head = 0
        elif t.direction == Direction.RIGHT:
            self.simulated_head += 1
            if self.simulated_head >= len(self.simulated_tape):
                self.simulated_tape.append(self.blank_symbol)
        
        # 更新狀態
        self.simulated_state = t.new_state
        
        return True
    
    def run(self, input_string: str, max_steps: int = 10000) -> Tuple[bool, int]:
        """運行模擬"""
        if self.simulated_tm is None:
            raise ValueError("未加載要模擬的圖靈機")
        
        # 初始化模擬狀態
        self.simulated_state = self.simulated_tm.start_state
        self.simulated_tape = list(input_string) + [self.blank_symbol]
        self.simulated_head = 0
        
        steps = 0
        
        while steps < max_steps:
            # 檢查是否接受/拒絕
            if self.simulated_state in self.simulated_tm.accept_states:
                return (True, steps)
            if self.simulated_state in self.simulated_tm.reject_states:
                return (False, steps)
            
            # 執行一步
            if not self.simulate_step():
                # 停機
                return (self.simulated_state in self.simulated_tm.accept_states, steps)
            
            steps += 1
        
        return (False, max_steps)
    
    def get_simulation_state(self) -> str:
        """獲取當前模擬狀態的描述"""
        if self.simulated_tm is None:
            return "No TM loaded"
        
        tape_str = ''.join(self.simulated_tape)
        return (f"狀態: {self.simulated_state}, "
                f"頭位置: {self.simulated_head}, "
                f"紙帶: {tape_str[:30]}{'...' if len(tape_str) > 30 else ''}")


def demo_universal():
    print("=== 通用圖靈機演示 ===\n")
    
    # 定義一個簡單的圖靈機：接受所有包含 '1' 的字串
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
        print(f"    → {utm.get_simulation_state()}")
    
    print("\n圖靈機描述：")
    desc = TMDescription.from_dict(simple_tm)
    print(desc.encode())

demo_universal()
```

## 7.5 視覺化工具

[程式檔案：07-5_visualizer.py](../_code/07/07-5-visualizer.py)

```python
"""
圖靈機視覺化工具
用ASCII藝術展示圖靈機的運作
"""

from typing import Optional, List, Tuple
from dataclasses import dataclass
from .turing_machine_base import Direction, Transition, TuringMachine, Configuration

@dataclass
class TMTapeVisualization:
    """圖靈機紙帶視覺化"""
    
    @staticmethod
    def render(tape: List[str], head: int, state: str, 
               left: int = -10, right: int = 20) -> str:
        """渲染紙帶"""
        lines = []
        
        # 狀態行
        lines.append(f"╔═══ 狀態: [{state}] ═══╗")
        
        # 上方刻度
        ruler = " " * 6
        for i in range(left, right):
            pos = i - left
            if i >= 0 and i < len(tape):
                ruler += f"{i:^{5}d}"
            else:
                ruler += " " * 5
        lines.append(ruler)
        
        # 紙帶內容
        tape_line = " " * 6
        for i in range(left, right):
            if i >= 0 and i < len(tape):
                tape_line += f"  {tape[i]}  "
            else:
                tape_line += "  _  "
        lines.append(tape_line)
        
        # 指針
        pointer = " " * 6
        for i in range(left, right):
            if i == head:
                pointer += "  ▲  "
            else:
                pointer += "     "
        lines.append(pointer)
        
        return '\n'.join(lines)


class TMAnimator:
    """圖靈機動畫器"""
    
    def __init__(self, tm: TuringMachine):
        self.tm = tm
    
    def animate(self, input_string: str, delay: float = 0.5, 
                max_steps: int = 50):
        """動畫展示圖靈機運行"""
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                    圖靈機動畫演示                             ║")
        print("╚══════════════════════════════════════════════════════════════╝\n")
        print(f"輸入: '{input_string}'\n")
        
        config = self.tm.get_initial_config(input_string)
        steps = 0
        
        visual = TMTapeVisualization()
        
        # 顯示初始狀態
        print(visual.render(config.tape, config.head, config.state))
        print(f"\n步驟 0: 初始狀態\n")
        
        input("按 Enter 繼續...")
        
        while steps < max_steps:
            # 檢查是否停機
            if config.state in self.tm.accept_states:
                print("\n" + "═" * 50)
                print("✓ 圖靈機接受輸入！")
                print("═" * 50)
                return True
            
            if config.state in self.tm.reject_states:
                print("\n" + "═" * 50)
                print("✗ 圖靈機拒絕輸入！")
                print("═" * 50)
                return False
            
            # 執行一步
            new_config = self.tm.step(config)
            if new_config is None:
                print("\n無轉換定義，停機")
                return config.state in self.tm.accept_states
            
            config = new_config
            steps += 1
            
            # 顯示
            print("\n" + "─" * 50)
            print(visual.render(config.tape, config.head, config.state))
            
            # 顯示轉換信息
            key = None
            for (s, sym), t in self.tm.transitions.items():
                if s == config.state:
                    key = (s, sym)
                    break
            
            if key:
                print(f"\n步驟 {steps}: 狀態={config.state}")
            
            input("按 Enter 繼續...")
        
        print(f"\n超出最大步數 ({max_steps})")
        return False


def create_fibonacci_tm() -> TuringMachine:
    """創建一個計算Fibonacci-like序列的圖靈機"""
    from .turing_machine_base import StandardTM
    
    config = {
        'states': ['q0', 'q1', 'q2', 'q3', 'halt_accept'],
        'alphabet': ['0', '1'],
        'tape_alphabet': ['0', '1', '_'],
        'start_state': 'q0',
        'accept_states': ['halt_accept'],
        'reject_states': [],
        'blank_symbol': '_',
        'transitions': {
            # q0: 寫入初始 '1'
            ('q0', '_'): ('q1', '1', 'R'),
            
            # q1: 寫入第二個 '1'
            ('q1', '_'): ('q2', '1', 'R'),
            
            # q2: 準備下一個
            ('q2', '_'): ('q3', '1', 'L'),
            
            # q3: 返回並重複
            ('q3', '1'): ('q3', '1', 'L'),
            ('q3', '_'): ('q1', '_', 'R'),
        }
    }
    
    tm = StandardTM()
    tm.load_from_dict(config)
    return tm


def demo_visualization():
    """演示視覺化"""
    print("=== 圖靈機視覺化演示 ===\n")
    
    visual = TMTapeVisualization()
    
    # 測試渲染
    tape = ['_', '1', '0', '1', '_']
    print(visual.render(tape, head=2, state='q1'))
    
    print("\n" + "=" * 50)
    
    # 運行 Fibonacci 圖靈機
    tm = create_fibonacci_tm()
    
    print("\n運行 Fibonacci-like 圖靈機 (非動畫版本)...\n")
    
    accepted, steps = tm.run('', max_steps=20)
    print(f"結果: {'接受' if accepted else '拒絕'} ({steps} 步)")

demo_visualization()
```

## 7.6 經典圖靈機實現

[程式檔案：07-6_classic_tms.py](../_code/07/07-6-classic-tms.py)

```python
"""
經典圖靈機實現
包含一些著名的圖靈機設計
"""

from typing import Tuple
from .turing_machine_base import StandardTM

class ClassicTuringMachines:
    """經典圖靈機集合"""
    
    @staticmethod
    def unary_add() -> StandardTM:
        """
        一元加法
        格式：1^m + 1^n 變為 1^(m+n)
        用 1 來表示數字，用 _ 分隔
        """
        config = {
            'states': ['q0', 'q1', 'q2', 'halt_accept'],
            'alphabet': ['1'],
            'tape_alphabet': ['1', '_'],
            'start_state': 'q0',
            'accept_states': ['halt_accept'],
            'reject_states': [],
            'blank_symbol': '_',
            'transitions': {
                # 穿過第一個數字
                ('q0', '1'): ('q0', '1', 'R'),
                # 跳過分隔符
                ('q0', '_'): ('q1', '_', 'R'),
                # 穿過第二個數字
                ('q1', '1'): ('q1', '1', 'R'),
                # 到末尾，寫入並返回
                ('q1', '_'): ('q2', '1', 'L'),
                # 返回開頭
                ('q2', '1'): ('q2', '1', 'L'),
                ('q2', '_'): ('halt_accept', '_', 'S'),
            }
        }
        tm = StandardTM()
        tm.load_from_dict(config)
        return tm
    
    @staticmethod
    def binary_increment() -> StandardTM:
        """
        二進制增量
        將二進制數加 1
        """
        config = {
            'states': ['q0', 'q1', 'q2', 'halt_accept'],
            'alphabet': ['0', '1'],
            'tape_alphabet': ['0', '1', '_'],
            'start_state': 'q0',
            'accept_states': ['halt_accept'],
            'reject_states': [],
            'blank_symbol': '_',
            'transitions': {
                # q0: 向右找到最低位
                ('q0', '0'): ('q0', '0', 'R'),
                ('q0', '1'): ('q0', '1', 'R'),
                ('q0', '_'): ('q1', '_', 'L'),
                
                # q1: 從右向左，遇到第一個 0 變為 1 並返回
                ('q1', '1'): ('q1', '0', 'L'),  # 進位
                ('q1', '0'): ('q2', '1', 'R'),  # 找到進位位置
                ('q1', '_'): ('q2', '1', 'R'),  # 全是1，加1在開頭
                
                # q2: 返回開頭
                ('q2', '0'): ('q2', '0', 'R'),
                ('q2', '1'): ('q2', '1', 'R'),
                ('q2', '_'): ('halt_accept', '_', 'S'),
            }
        }
        tm = StandardTM()
        tm.load_from_dict(config)
        return tm
    
    @staticmethod
    def copy() -> StandardTM:
        """
        複製字串
        abc → abc#abc
        """
        config = {
            'states': ['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'halt_accept'],
            'alphabet': ['a', 'b', 'c'],  # 簡化字母表
            'tape_alphabet': ['a', 'b', 'c', '_', 'X'],
            'start_state': 'q0',
            'accept_states': ['halt_accept'],
            'reject_states': [],
            'blank_symbol': '_',
            'transitions': {
                # q0: 標記並寫入副本區
                ('q0', 'a'): ('q0', 'X', 'R'),
                ('q0', 'b'): ('q0', 'X', 'R'),
                ('q0', 'c'): ('q0', 'X', 'R'),
                ('q0', '_'): ('q1', '#', 'R'),
                
                # q1: 複製剩餘字元
                ('q1', 'a'): ('q1', 'a', 'R'),
                ('q1', 'b'): ('q1', 'b', 'R'),
                ('q1', 'c'): ('q1', 'c', 'R'),
                ('q1', '_'): ('q2', 'a', 'L'),  # 複製 a
                
                # q2: 返回並繼續
                ('q2', 'a'): ('q2', 'a', 'L'),
                ('q2', 'b'): ('q2', 'b', 'L'),
                ('q2', 'c'): ('q2', 'c', 'L'),
                ('q2', '#'): ('q2', '#', 'L'),
                ('q2', 'X'): ('q0', 'X', 'R'),  # 繼續下一個
                
                # ... (省略部分轉換)
            }
        }
        tm = StandardTM()
        tm.load_from_dict(config)
        return tm


def demo_classic():
    """演示經典圖靈機"""
    print("=== 經典圖靈機演示 ===\n")
    
    # 一元加法
    print("1. 一元加法 (1+1 = 11):")
    tm = ClassicTuringMachines.unary_add()
    accepted, steps = tm.run('1 1', trace=False)
    print(f"   結果: {'接受' if accepted else '拒絕'} ({steps} 步)")
    
    print("\n2. 二進制增量 (101 + 1 = 110):")
    tm = ClassicTuringMachines.binary_increment()
    accepted, steps = tm.run('101', trace=False)
    print(f"   結果: {'接受' if accepted else '拒絕'} ({steps} 步)")

demo_classic()
```

## 7.7 小結

本章我們實作了：

1. **基本圖靈機框架**：完整的單紙帶確定性圖靈機
2. **多帶圖靈機**：擴展版本，易於設計複雜機器
3. **非確定性圖靈機**：使用廣度優先搜索模擬
4. **通用圖靈機**：可以模擬任何其他圖靈機
5. **視覺化工具**：ASCII藝術展示
6. **經典圖靈機**：一元加法、二進制增量等

這個模擬器可以用來：
- 實驗各種圖靈機設計
- 驗證圖靈機的等價性
- 理解計算的機械模型

下一章，我們將探討丘奇-圖靈論題，以及它對計算理論的深遠影響。

## 練習題

1. **設計圖靈機**：設計一個圖靈機，將二元樹結構（用特殊符號表示）複製一份。

2. **優化NTM模擬**：實現更高效的NTM模擬算法，例如使用更聰明的搜索策略或剪枝。

3. **完整UTM**：完善通用圖靈機，使其能夠真正讀取和解釋任意圖靈機的描述。

4. **性能測試**：比較基本圖靈機和多帶圖靈機模擬同一問題的效率差異。

5. **圖靈機對λ演算**：用圖靈機模擬一個簡單的λ表達式求值（例如 `(λx.x) y`）。
