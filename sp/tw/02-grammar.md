# 2. 語法理論

## 2.1 正則表達式與有限自動機

正則表達式描述字串的模式。讓我們用 Python 來實際操作：

[程式檔案：02-1-regex-example.py](../_code/02/02-1-regex-example.py)
```python
import re

# 基本模式
pattern = r"[0-9]+"  # 匹配一個或多個數字
text = "年齡是 25 歲，體重 65.5 公斤"

matches = re.findall(pattern, text)
print(matches)  # ['25', '65', '5']

# 電子郵件正則表達式
email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
emails = "聯絡: user@example.com 或 admin@test.org"
print(re.findall(email_pattern, emails))
# ['user@example.com', 'admin@test.org']

# 手機號碼（台灣格式）
phone_pattern = r"09[0-9]{8}"
print(re.match(phone_pattern, "0912345678"))  # <re.Match object>
print(re.match(phone_pattern, "1234567890"))  # None
```

有限自動機是正則表達式的數學模型。我們可以用程式碼來模擬：

[程式檔案：02-2-dfa.py](../_code/02/02-2-dfa.py)
```python
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
```

## 2.2 文法（Context-Free Grammar）

讓我們用 Python 實作一個簡單的算術表達式文法：

[程式檔案：02-3-parser.py](../_code/02/02-3-parser.py)
```python
# 文法定義（使用 EBNF 風格）
# Expr    → Term (( '+' | '-' ) Term)*
# Term    → Factor (( '*' | '/' ) Factor)*
# Factor  → NUMBER | '(' Expr ')'

# 手動 Parser 實現
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def consume(self):
        token = self.current_token()
        self.pos += 1
        return token
    
    def parse(self):
        return self.expr()
    
    def expr(self):
        """Expr → Term (( '+' | '-' ) Term)*"""
        result = self.term()
        while self.current_token() in ['+', '-']:
            op = self.consume()
            right = self.term()
            if op == '+':
                result = ('+', result, right)
            else:
                result = ('-', result, right)
        return result
    
    def term(self):
        """Term → Factor (( '*' | '/' ) Factor)*"""
        result = self.factor()
        while self.current_token() in ['*', '/']:
            op = self.consume()
            right = self.factor()
            if op == '*':
                result = ('*', result, right)
            else:
                result = ('/', result, right)
        return result
    
    def factor(self):
        """Factor → NUMBER | '(' Expr ')'"""
        token = self.current_token()
        if token == '(':
            self.consume()  # '('
            result = self.expr()
            self.consume()  # ')'
            return result
        # 應該是數字
        return ('num', self.consume())

# 測試 Tokenizer 和 Parser
def tokenize(text):
    """簡單的詞法分析"""
    tokens = []
    i = 0
    while i < len(text):
        if text[i].isdigit():
            j = i
            while j < len(text) and text[j].isdigit():
                j += 1
            tokens.append(text[i:j])
            i = j
        elif text[i] in '+-*/()':
            tokens.append(text[i])
            i += 1
        else:
            i += 1  # 跳過空白
    return tokens

# 測試
tokens = tokenize("2 + 3 * 4")
print("Tokens:", tokens)  # ['2', '+', '3', '*', '4']

parser = Parser(tokens)
ast = parser.parse()
print("AST:", ast)  # ('+', ('num', '2'), ('*', ('num', '3'), ('num', '4')))
```

## 2.3 Parser 與 Tokenizer

Tokenizer（Lexer）將字元流轉換為 Token 序列：

[程式檔案：02-4-tokenizer.py](../_code/02/02-4-tokenizer.py)
```python
import re

class Tokenizer:
    """簡易詞法分析器"""
    
    TOKEN_PATTERNS = [
        ('NUMBER', r'\d+'),
        ('PLUS', r'\+'),
        ('MINUS', r'-'),
        ('MULT', r'\*'),
        ('DIV', r'/'),
        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
        ('EQUAL', r'='),
        ('IDENT', r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ('SKIP', r'[ \t\n]+'),
    ]
    
    def __init__(self, source):
        self.source = source
        self.pos = 0
    
    def tokenize(self):
        tokens = []
        while self.pos < len(self.source):
            matched = False
            for token_type, pattern in self.TOKEN_PATTERNS:
                regex = re.compile(pattern)
                match = regex.match(self.source, self.pos)
                if match:
                    value = match.group(0)
                    if token_type != 'SKIP':
                        tokens.append((token_type, value))
                    self.pos = match.end()
                    matched = True
                    break
            if not matched:
                raise SyntaxError(f"無法識別的字元: {self.source[self.pos]}")
        return tokens

# 測試
source = "x = 42 + y * (10 - 2)"
tokens = Tokenizer(source).tokenize()
for token in tokens:
    print(token)
# 輸出：
# ('IDENT', 'x')
# ('EQUAL', '=')
# ('NUMBER', '42')
# ('PLUS', '+')
# ('IDENT', 'y')
# ('MULT', '*')
# ('LPAREN', '(')
# ('NUMBER', '10')
# ('MINUS', '-')
# ('NUMBER', '2')
# ('RPAREN', ')')
```

## 2.4 語法分析技術

### LL 分析法 - 遞迴下降 Parser

[程式檔案：02-5-llparser.py](../_code/02/02-5-llparser.py)
```python
class LLParser:
    """LL(1) 遞迴下降 Parser - 解析簡單的算術表達式"""
    
    # 文法:
    # E  → T E'
    # E' → + T E' | - T E' | ε
    # T  → F T'
    # T' → * F T' | / F T' | ε
    # F  → ( E ) | number
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    
    def consume(self, expected_type=None):
        token = self.current()
        if expected_type and token[0] != expected_type:
            raise SyntaxError(f"期望 {expected_type}，得到 {token[0]}")
        self.pos += 1
        return token
    
    def parse(self):
        return self.E()
    
    # E → T E'
    def E(self):
        result = self.T()
        return self.E_prime(result)
    
    # E' → + T E' | - T E' | ε
    def E_prime(self, left):
        token = self.current()
        if token and token[0] in ['PLUS', 'MINUS']:
            op = self.consume()[1]
            right = self.T()
            new_left = (op, left, right)
            return self.E_prime(new_left)
        return left
    
    # T → F T'
    def T(self):
        result = self.F()
        return self.T_prime(result)
    
    # T' → * F T' | / F T' | ε
    def T_prime(self, left):
        token = self.current()
        if token and token[0] in ['MULT', 'DIV']:
            op = self.consume()[1]
            right = self.F()
            new_left = (op, left, right)
            return self.T_prime(new_left)
        return left
    
    # F → ( E ) | number
    def F(self):
        token = self.current()
        if token and token[0] == 'LPAREN':
            self.consume()
            result = self.E()
            self.consume('RPAREN')
            return result
        elif token and token[0] == 'NUMBER':
            return ('num', self.consume()[1])
        else:
            raise SyntaxError(f"語法錯誤: {token}")

# 測試
tokens = [
    ('NUMBER', '2'), ('PLUS', '+'), ('NUMBER', '3'),
    ('MULT', '*'), ('NUMBER', '4')
]
parser = LLParser(tokens)
ast = parser.parse()
print(ast)  # ('+', ('num', '2'), ('*', ('num', '3'), ('num', '4')))
```

### LR 分析法 - 使用 Yacc/Bison 風格的語法

雖然 Python 中沒有原生的 Yacc，但我們可以用 PLY 庫來實現：

[程式檔案：02-6-ply-parser.py](../_code/02/02-6-ply-parser.py)
```python
# 安裝: pip install ply
# 檔案: calc.py

from ply import yacc

# 詞法分析
tokens = ['NUMBER', 'PLUS', 'MINUS', 'MULT', 'DIV', 'LPAREN', 'RPAREN']

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_MULT    = r'\*'
t_DIV     = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_NUMBER  = r'\d+'

def t_ignore(t):
    r' +'
    pass

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print(f"詞法錯誤: {t.value[0]}")
    t.lexer.skip(1)

lexer = yacc.lex()

# 語法分析
def p_expr(p):
    '''expr : expr PLUS expr
            | expr MINUS expr'''
    p[0] = ('+', p[1], p[3]) if p[2] == '+' else ('-', p[1], p[3])

def p_expr_term(p):
    'expr : term'
    p[0] = p[1]

def p_term(p):
    '''term : term MULT term
            | term DIV term'''
    p[0] = ('*', p[1], p[3]) if p[2] == '*' else ('/', p[1], p[3])

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_number(p):
    'factor : NUMBER'
    p[0] = ('num', p[1])

def p_factor_expr(p):
    'factor : LPAREN expr RPAREN'
    p[0] = p[2]

def p_error(p):
    print("語法錯誤!")

parser = yacc.yacc()

# 測試
result = parser.parse("2 + 3 * 4")
print(result)
```

## 2.5 語法樹與抽象語法樹

[程式檔案：02-7-ast.py](../_code/02/02-7-ast.py)
```python
# 語法樹與抽象語法樹的比較

# 完整語法樹（Parse Tree）- 忠實反映文法結構
#          *
#         / \
#        +   4
#       / \
#      2   3

# 抽象語法樹（AST）- 只保留必要資訊
#      *
#     / \
#    +   4
#   / \
#  2   3

class ASTNode:
    def __init__(self, node_type, value=None):
        self.type = node_type
        self.value = value
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)
    
    def __repr__(self):
        if self.value:
            return f"({self.type}: {self.value})"
        return f"({self.type})"

# 將 Parser 輸出的元組轉換為 AST
def build_ast(parse_tree):
    """將簡化的 parse tree 轉換為 AST"""
    if not isinstance(parse_tree, tuple):
        return ASTNode('number', parse_tree)
    
    op, left, right = parse_tree
    node = ASTNode('binary_op', op)
    node.add_child(build_ast(left))
    node.add_child(build_ast(right))
    return node

def print_ast(node, indent=0):
    print("  " * indent + str(node))
    for child in node.children:
        print_ast(child, indent + 1)

# 測試
parse_tree = ('+', ('num', '2'), ('*', ('num', '3'), ('num', '4')))
ast = build_ast(parse_tree)
print_ast(ast)
# 輸出：
# (+)
#   (num: 2)
#   (*)
#     (num: 3)
#     (num: 4)
```

## 實作：完整的小型語言編譯器

讓我們實作一個完整的小型語言編譯器流程：

[程式檔案：02-8-compiler.py](../_code/02/02-8-compiler.py)
```python
"""
完整流程：原始碼 → Tokenizer → Parser → AST → 直譯執行
"""

# ========== 1. 詞法分析 ==========
def lex(source):
    """將原始碼轉換為 Token 流"""
    tokens = []
    i = 0
    while i < len(source):
        if source[i].isspace():
            i += 1
            continue
        if source[i].isdigit():
            j = i
            while j < len(source) and source[j].isdigit():
                j += 1
            tokens.append(('NUM', int(source[i:j])))
            i = j
            continue
        if source[i] == '+':
            tokens.append(('PLUS', '+'))
            i += 1
            continue
        if source[i] == '-':
            tokens.append(('MINUS', '-'))
            i += 1
            continue
        if source[i] == '*':
            tokens.append(('MULT', '*'))
            i += 1
            continue
        if source[i] == '/':
            tokens.append(('DIV', '/'))
            i += 1
            continue
        if source[i] == '(':
            tokens.append(('LPAREN', '('))
            i += 1
            continue
        if source[i] == ')':
            tokens.append(('RPAREN', ')'))
            i += 1
            continue
        raise SyntaxError(f"無法識別的字元: {source[i]}")
    return tokens

# ========== 2. 語法分析 ==========
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    
    def consume(self):
        token = self.peek()
        self.pos += 1
        return token
    
    def parse(self):
        return self.expr()
    
    def expr(self):
        result = self.term()
        while self.peek() and self.peek()[0] in ('PLUS', 'MINUS'):
            op = self.consume()[1]
            right = self.term()
            result = {'type': 'binary', 'op': op, 'left': result, 'right': right}
        return result
    
    def term(self):
        result = self.factor()
        while self.peek() and self.peek()[0] in ('MULT', 'DIV'):
            op = self.consume()[1]
            right = self.factor()
            result = {'type': 'binary', 'op': op, 'left': result, 'right': right}
        return result
    
    def factor(self):
        token = self.peek()
        if token[0] == 'NUM':
            self.consume()
            return {'type': 'num', 'value': token[1]}
        if token[0] == 'LPAREN':
            self.consume()
            result = self.expr()
            self.consume()  # RPAREN
            return result
        raise SyntaxError("語法錯誤")

# ========== 3. 語意分析與執行 ==========
def evaluate(node):
    """直譯執行 AST"""
    if node['type'] == 'num':
        return node['value']
    
    if node['type'] == 'binary':
        left_val = evaluate(node['left'])
        right_val = evaluate(node['right'])
        op = node['op']
        
        if op == '+': return left_val + right_val
        if op == '-': return left_val - right_val
        if op == '*': return left_val * right_val
        if op == '/': return left_val // right_val
    
    raise ValueError("未知的節點類型")

# ========== 完整流程 ==========
def run(source):
    print(f"原始碼: {source}")
    
    tokens = lex(source)
    print(f"Tokens: {tokens}")
    
    ast = Parser(tokens).parse()
    print(f"AST: {ast}")
    
    result = evaluate(ast)
    print(f"結果: {result}")
    print()

# 測試各種表達式
run("2 + 3")
run("10 - 4 * 2")
run("(10 - 4) * 2")
run("100 / 10 / 2")
```

執行結果：
```
原始碼: 2 + 3
Tokens: [('NUM', 2), ('PLUS', '+'), ('NUM', 3)]
AST: {'type': 'binary', 'op': '+', 'left': {'type': 'num', 'value': 2}, 'right': {'type': 'num', 'value': 3}}
結果: 5

原始碼: 10 - 4 * 2
Tokens: [('NUM', 10), ('MINUS', '-'), ('NUM', 4), ('MULT', '*'), ('NUM', 2)]
AST: {'type': 'binary', 'op': '-', 'left': {'type': 'num', 'value': 10}, 'right': {'type': 'binary', 'op': '*', ...}}
結果: 2

原始碼: (10 - 4) * 2
結果: 12

原始碼: 100 / 10 / 2
結果: 5
```

這個簡單的解譯器展示了從原始碼到執行結果的完整流程：詞法分析 → 語法分析 → 建立 AST → 直譯執行。
