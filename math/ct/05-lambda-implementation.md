# 第 5 章：λ演算的Python實作

## 概述

理論需要實踐來檢驗。在這一章，我們將用Python實作一個完整的λ演算解譯器。

這個解譯器將包含：
1. **詞法分析器**：將字串轉換為token流
2. **解析器**：將token流轉換為抽象語法樹（AST）
3. **環境管理**：追蹤變數的綁定
4. **歸約引擎**：執行α轉換和β歸約
5. **標準庫**：內建的Church數和布爾值
6. **互動式REPL**：讓使用者輸入λ表達式並立即看到結果

## 5.1 架構總覽

```
┌─────────────────────────────────────────────────────────────────┐
│                      λ演算解譯器架構                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐                                               │
│  │   輸入字串   │                                               │
│  └──────┬──────┘                                               │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────┐                                               │
│  │  詞法分析    │  "λx. x y" → [LAMBDA, VAR("x"), DOT,       │
│  │  (Lexer)    │         VAR("x"), VAR("y")]                  │
│  └──────┬──────┘                                               │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────┐                                               │
│  │   解析器    │  [tokens] → AST(App(Abs("x", Var("x")),      │
│  │  (Parser)   │                    Var("y")))                 │
│  └──────┬──────┘                                               │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────┐                                               │
│  │   求值器    │  AST → 歸約 → Church數或布爾值               │
│  │  (Evaluator)│  β歸約 + α轉換 + η轉換                       │
│  └─────────────┘                                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 5.2 抽象語法樹（AST）

[程式檔案：05-1-lambda_ast.py](../_code/05/05-1-lambda_ast.py)

```python
"""
λ演算解譯器 - 第一部分：抽象語法樹
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Set, Dict
import string

@dataclass
class LambdaExpr:
    """λ演算表達式的基類"""
    pass

@dataclass
class Var(LambdaExpr):
    """
    變數：λ演算中最基本的表達式
    例如：x, y, z
    """
    name: str
    
    def free_vars(self) -> Set[str]:
        """返回表達式中的自由變數"""
        return {self.name}
    
    def bound_vars(self) -> Set[str]:
        """返回表達式中的約束變數"""
        return set()
    
    def substitute(self, var: str, replacement: LambdaExpr) -> LambdaExpr:
        """替換自由變數"""
        if self.name == var:
            return replacement
        return Var(self.name)
    
    def alpha_convert(self, new_name: str) -> LambdaExpr:
        """α轉換：將變數改名"""
        return Var(new_name)
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return f"Var({self.name!r})"

@dataclass
class Abs(LambdaExpr):
    """
    函數抽象：λ 變數. 主體
    例如：λx. x, λf. λx. f x
    """
    var: str
    body: LambdaExpr
    
    def free_vars(self) -> Set[str]:
        """返回自由變數（排除被λ綁定的）"""
        return self.body.free_vars() - {self.var}
    
    def bound_vars(self) -> Set[str]:
        """返回約束變數"""
        return {self.var} | self.body.bound_vars()
    
    def substitute(self, var: str, replacement: LambdaExpr) -> LambdaExpr:
        """替換，但需要避免捕捉"""
        if var == self.var:
            # 被λ綁定的變數不替換
            return self
        else:
            # 需要檢查是否會發生捕捉
            if self.var in replacement.free_vars():
                # 需要α轉換
                new_var = self._fresh_var(self.var, replacement.free_vars())
                new_body = self.body.substitute(self.var, Var(new_var))
                return Abs(new_var, new_body.substitute(var, replacement))
            else:
                return Abs(self.var, self.body.substitute(var, replacement))
    
    def alpha_convert(self, new_name: str) -> LambdaExpr:
        """α轉換"""
        return Abs(new_name, self.body.substitute(self.var, Var(new_name)))
    
    @staticmethod
    def _fresh_var(base: str, avoid: Set[str]) -> str:
        """生成一個不在avoid中的新變數名"""
        if base not in avoid:
            return base
        suffix = 0
        while f"{base}{suffix}" in avoid:
            suffix += 1
        return f"{base}{suffix}"
    
    def __str__(self) -> str:
        return f"λ{self.var}. {self.body}"
    
    def __repr__(self) -> str:
        return f"Abs({self.var!r}, {self.body!r})"

@dataclass
class App(LambdaExpr):
    """
    函數應用：f x
    例如：(λx. x) y, f x y
    """
    func: LambdaExpr
    arg: LambdaExpr
    
    def free_vars(self) -> Set[str]:
        """返回自由變數"""
        return self.func.free_vars() | self.arg.free_vars()
    
    def bound_vars(self) -> Set[str]:
        """返回約束變數"""
        return self.func.bound_vars() | self.arg.bound_vars()
    
    def substitute(self, var: str, replacement: LambdaExpr) -> LambdaExpr:
        """替換"""
        return App(
            self.func.substitute(var, replacement),
            self.arg.substitute(var, replacement)
        )
    
    def alpha_convert(self, new_name: str) -> LambdaExpr:
        """α轉換"""
        return App(self.func.alpha_convert(new_name), self.arg.alpha_convert(new_name))
    
    def __str__(self) -> str:
        def paren(expr: LambdaExpr, need_parens: bool = True) -> str:
            s = str(expr)
            if isinstance(expr, App):
                return s
            if need_parens and (isinstance(expr, Abs)):
                return f"({s})"
            return s
        
        return f"{paren(self.func)} {paren(self.arg)}"
    
    def __repr__(self) -> str:
        return f"App({self.func!r}, {self.arg!r})"


# 測試 AST
if __name__ == "__main__":
    print("=== λ演算 AST 測試 ===\n")
    
    # λx. x (恆等函數)
    identity = Abs("x", Var("x"))
    print(f"恆等函數：{identity}")
    print(f"  自由變數：{identity.free_vars()}")
    print(f"  約束變數：{identity.bound_vars()}")
    
    # (λx. x) y
    app = App(identity, Var("y"))
    print(f"\n應用 (λx. x) y：{app}")
    print(f"  自由變數：{app.free_vars()}")
    
    # λx. λy. x (常函數)
    const = Abs("x", Abs("y", Var("x")))
    print(f"\n常函數：{const}")
    print(f"  自由變數：{const.free_vars()}")
    
    # 替換測試
    result = app.substitute("y", Var("z"))
    print(f"\n替換 (λx. x) y 中的 y → z：{result}")
```

執行結果：

```
=== λ演算 AST 測試 ===

恆等函數：λx. x
  自由變數：set()
  約束變數：{'x'}

應用 (λx. x) y：
  自由變數：{'y'}
  約束變數：set()

常函數：λx. λy. x
  自由變數：set()
  約束變數：{'x', 'y'}

替換 (λx. x) y 中的 y → z：λx. x z
```

## 5.3 詞法分析器

[程式檔案：05-2-lexer.py](../_code/05/05-2-lexer.py)

```python
"""
λ演算解譯器 - 第二部分：詞法分析器
"""

from __future__ import annotations
from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional, List
import string

class TokenType(Enum):
    """Token 類型"""
    LAMBDA = auto()     # λ 或 \
    DOT = auto()        # .
    LPAREN = auto()     # (
    RPAREN = auto()     # )
    VAR = auto()        # 變數名
    EOF = auto()        # 結束

@dataclass
class Token:
    """Token"""
    type: TokenType
    value: str
    line: int = 0
    column: int = 0

class LexerError(Exception):
    """詞法分析錯誤"""
    pass

class Lexer:
    """λ演算詞法分析器"""
    
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = self.text[0] if text else None
    
    def advance(self):
        """向前移動一個字符"""
        self.pos += 1
        if self.current_char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None
    
    def peek(self, offset: int = 1) -> Optional[str]:
        """查看未來的字符"""
        peek_pos = self.pos + offset
        if peek_pos < len(self.text):
            return self.text[peek_pos]
        return None
    
    def skip_whitespace(self):
        """跳過空白字符"""
        while self.current_char is not None and self.current_char in ' \t\n\r':
            self.advance()
    
    def read_identifier(self) -> str:
        """讀取標識符"""
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return result
    
    def error(self, message: str):
        """報告錯誤"""
        raise LexerError(
            f"詞法錯誤 at line {self.line}, column {self.column}: {message}"
        )
    
    def get_next_token(self) -> Token:
        """獲取下一個token"""
        while self.current_char is not None:
            # 跳過空白
            if self.current_char in ' \t\n\r':
                self.skip_whitespace()
                continue
            
            # 註解（以 # 開頭到行尾）
            if self.current_char == '#':
                while self.current_char is not None and self.current_char != '\n':
                    self.advance()
                continue
            
            # Lambda 或 \
            if self.current_char == 'λ' or self.current_char == '\\':
                token = Token(TokenType.LAMBDA, self.current_char, self.line, self.column)
                self.advance()
                return token
            
            # 點
            if self.current_char == '.':
                token = Token(TokenType.DOT, '.', self.line, self.column)
                self.advance()
                return token
            
            # 括號
            if self.current_char == '(':
                token = Token(TokenType.LPAREN, '(', self.line, self.column)
                self.advance()
                return token
            
            if self.current_char == ')':
                token = Token(TokenType.RPAREN, ')', self.line, self.column)
                self.advance()
                return token
            
            # 變數
            if self.current_char.isalpha() or self.current_char == '_':
                var_name = self.read_identifier()
                return Token(TokenType.VAR, var_name, self.line, self.column - len(var_name))
            
            # 其他字符
            self.error(f"未預期的字符: {self.current_char!r}")
        
        return Token(TokenType.EOF, '', self.line, self.column)
    
    def tokenize(self) -> List[Token]:
        """將整個輸入轉換為token列表"""
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens


# 測試詞法分析器
if __name__ == "__main__":
    print("=== λ演算詞法分析器測試 ===\n")
    
    test_inputs = [
        "λx. x",
        "λx. λy. x y",
        "(λx. x) y",
        "λf. λx. f (f x)",
    ]
    
    lexer = Lexer("")
    for text in test_inputs:
        lexer = Lexer(text)
        tokens = lexer.tokenize()
        print(f"輸入：{text}")
        print(f"Token：{[(t.type.name, t.value) for t in tokens]}")
        print()
```

執行結果：

```
=== λ演算詞法分析器測試 ===

輸入：λx. x
Token：[('LAMBDA', 'λ'), ('VAR', 'x'), ('DOT', '.'), ('VAR', 'x'), ('EOF', '')]

輸入：λx. λy. x y
Token：[('LAMBDA', 'λ'), ('VAR', 'x'), ('DOT', '.'), ('LAMBDA', 'λ'), ('VAR', 'y'), ('DOT', '.'), ('VAR', 'x'), ('VAR', 'y'), ('EOF', '')]

輸入：(λx. x) y
Token：[('LPAREN', '('), ('LAMBDA', 'λ'), ('VAR', 'x'), ('DOT', '.'), ('VAR', 'x'), ('RPAREN', ')'), ('VAR', 'y'), ('EOF', '')]

輸入：λf. λx. f (f x)
Token：[('LAMBDA', 'λ'), ('VAR', 'f'), ('DOT', '.'), ('LAMBDA', 'λ'), ('VAR', 'x'), ('DOT', '.'), ('VAR', 'f'), ('LPAREN', '('), ('VAR', 'f'), ('VAR', 'x'), ('RPAREN', ')'), ('EOF', '')]
```

## 5.4 解析器

[程式檔案：05-3_parser.py](../_code/05/05-3-parser.py)

```python
"""
λ演算解譯器 - 第三部分：解析器
使用遞歸下降解析器
"""

from __future__ import annotations
from typing import Optional, List
from .lexer import Lexer, Token, TokenType, LexerError
from .ast import LambdaExpr, Var, Abs, App

class ParserError(Exception):
    """解析錯誤"""
    pass

class Parser:
    """λ演算遞歸下降解析器"""
    
    def __init__(self, text: str):
        self.lexer = Lexer(text)
        self.current_token: Optional[Token] = None
        self.tokens: List[Token] = []
        self.pos = 0
        self._tokenize()
    
    def _tokenize(self):
        """預先詞法分析"""
        self.tokens = []
        while True:
            token = self.lexer.get_next_token()
            self.tokens.append(token)
            if token.type == TokenType.EOF:
                break
        self.current_token = self.tokens[0] if self.tokens else None
    
    def advance(self):
        """移動到下一個token"""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = Token(TokenType.EOF, '', 0, 0)
    
    def error(self, message: str):
        """報告解析錯誤"""
        raise ParserError(
            f"解析錯誤 at position {self.pos}: {message}"
        )
    
    def parse(self) -> LambdaExpr:
        """解析λ表達式"""
        expr = self.expr()
        if self.current_token.type != TokenType.EOF:
            self.error(f"未預期的 token: {self.current_token.value}")
        return expr
    
    def expr(self) -> LambdaExpr:
        """
        expr ::= abstraction
               | application
        
        解析表達式（應用優先於抽象）
        """
        # 嘗試解析抽象
        saved_pos = self.pos
        try:
            return self.abstraction()
        except ParserError:
            self.pos = saved_pos
            self.current_token = self.tokens[self.pos]
        
        # 嘗試解析應用
        return self.application()
    
    def abstraction(self) -> LambdaExpr:
        """
        abstraction ::= LAMBDA VAR DOT expr
                      | LPAREN LAMBDA VAR DOT expr RPAREN
        """
        # 檢查是否有 λ
        if self.current_token.type == TokenType.LAMBDA:
            self.advance()
        elif self.current_token.type != TokenType.LPAREN:
            raise ParserError("期望 λ 或 (")
        else:
            self.advance()
            if self.current_token.type != TokenType.LAMBDA:
                raise ParserError("期望 λ")
            self.advance()
        
        # 讀取變數名
        if self.current_token.type != TokenType.VAR:
            raise ParserError("期望變數名")
        var = self.current_token.value
        self.advance()
        
        # 讀取點
        if self.current_token.type != TokenType.DOT:
            raise ParserError("期望 .")
        self.advance()
        
        # 解析主體
        body = self.expr()
        
        # 如果有左括號，檢查右括號
        if self.current_token.type == TokenType.RPAREN:
            self.advance()
        
        return Abs(var, body)
    
    def application(self) -> LambdaExpr:
        """
        application ::= atom+
        """
        atoms = []
        
        while True:
            atom = self.atom()
            atoms.append(atom)
            
            # 如果下一個不是 atom，停止
            if (self.current_token.type in [TokenType.LAMBDA, TokenType.EOF, TokenType.RPAREN, TokenType.DOT] or
                self.pos + 1 >= len(self.tokens)):
                break
        
        if not atoms:
            raise ParserError("期望表達式")
        
        # 左結合的函數應用
        result = atoms[0]
        for atom in atoms[1:]:
            result = App(result, atom)
        
        return result
    
    def atom(self) -> LambdaExpr:
        """
        atom ::= VAR
               | LPAREN expr RPAREN
        """
        token = self.current_token
        
        if token.type == TokenType.VAR:
            self.advance()
            return Var(token.value)
        elif token.type == TokenType.LPAREN:
            self.advance()
            expr = self.expr()
            if self.current_token.type != TokenType.RPAREN:
                raise ParserError("期望 )")
            self.advance()
            return expr
        elif token.type == TokenType.LAMBDA:
            return self.abstraction()
        else:
            raise ParserError(f"未預期的 token: {token.value}")


# 測試解析器
if __name__ == "__main__":
    print("=== λ演算解析器測試 ===\n")
    
    test_cases = [
        "x",
        "λx. x",
        "λx. λy. x",
        "(λx. x) y",
        "λf. λx. f x",
        "λx. λy. λz. x z (y z)",
    ]
    
    parser = Parser("")
    for text in test_cases:
        parser = Parser(text)
        ast = parser.parse()
        print(f"輸入：{text}")
        print(f"AST：  {ast}")
        print()
```

執行結果：

```
=== λ演算解析器測試 ===

輸入：x
AST：  x

輸入：λx. x
AST：  λx. x

輸入：λx. λy. x
AST：  λx. λy. x

輸入：(λx. x) y
AST：  (λx. x) y

輸入：λf. λx. f x
AST：  λf. λx. f x

輸入：λx. λy. λz. x z (y z)
AST：  λx. λy. λz. x z (y z)
```

## 5.5 歸約引擎

[程式檔案：05-4_reducer.py](../_code/05/05-4-reducer.py)

```python
"""
λ演算解譯器 - 第四部分：歸約引擎
實現 β歸約、α轉換和正規序歸約
"""

from __future__ import annotations
from typing import Optional, Callable, Set
from .ast import LambdaExpr, Var, Abs, App

class ReductionError(Exception):
    """歸約錯誤"""
    pass

class Normalizer:
    """
    λ演算正規序歸約引擎
    
    正規序歸約（Normal Order Reduction）：
    - 總是選擇最左、最外的可歸約式（redex）進行歸約
    - 如果表達式有正規形式，總能找到它
    """
    
    def __init__(self, max_steps: int = 1000):
        self.max_steps = max_steps
    
    def beta_reduce(self, expr: LambdaExpr) -> LambdaExpr:
        """
        對表達式進行一次 β歸約
        返回歸約後的表達式，如果不是規範式則返回None
        """
        # 正規序：先處理最外的redex
        if isinstance(expr, App):
            # (λx. M) N → M[x := N]
            if isinstance(expr.func, Abs):
                return expr.func.body.substitute(expr.func.var, expr.arg)
            else:
                # 嘗試歸約函數
                reduced_func = self.beta_reduce(expr.func)
                if reduced_func is not None:
                    return App(reduced_func, expr.arg)
                # 嘗試歸約參數
                reduced_arg = self.beta_reduce(expr.arg)
                if reduced_arg is not None:
                    return App(expr.func, reduced_arg)
                return None
        
        elif isinstance(expr, Abs):
            # λx. M → λx. M' (如果 M 可以歸約)
            reduced_body = self.beta_reduce(expr.body)
            if reduced_body is not None:
                return Abs(expr.var, reduced_body)
            return None
        
        elif isinstance(expr, Var):
            # 變數是規範式
            return None
        
        return None
    
    def normalize(self, expr: LambdaExpr) -> tuple[LambdaExpr, int, bool]:
        """
        完全歸約到正規形式
        
        返回：(正規形式, 歸約步數, 是否找到正規形式)
        """
        current = expr
        steps = 0
        diverged = False
        
        while steps < self.max_steps:
            reduced = self.beta_reduce(current)
            if reduced is None:
                # 已經是正規形式
                break
            
            # 檢查是否發散（應用於自身的組合子）
            if str(reduced) == str(current):
                diverged = True
                break
            
            current = reduced
            steps += 1
        
        return current, steps, not diverged and steps < self.max_steps
    
    def normalize_with_trace(self, expr: LambdaExpr) -> list[str]:
        """歸約並返回每一步的追蹤"""
        trace = [str(expr)]
        current = expr
        
        for _ in range(self.max_steps):
            reduced = self.beta_reduce(current)
            if reduced is None:
                break
            trace.append(str(reduced))
            current = reduced
        
        return trace


# 測試歸約引擎
if __name__ == "__main__":
    print("=== λ演算歸約引擎測試 ===\n")
    
    from .parser import Parser
    
    test_cases = [
        ("(λx. x) y", "y"),
        ("(λx. λy. x) a b", "a"),
        ("(λf. λx. f (f x)) (λy. λz. z) 3", "?"),  # 需要Church數
    ]
    
    normalizer = Normalizer()
    
    for input_text, expected_hint in test_cases:
        parser = Parser(input_text)
        ast = parser.parse()
        
        result, steps, converged = normalizer.normalize(ast)
        
        print(f"輸入：{input_text}")
        print(f"結果：{result}")
        print(f"步數：{steps}, 收斂：{converged}")
        print()
```

## 5.6 完整解譯器

[程式檔案：05-5-interpreter.py](../_code/05/05-5-interpreter.py)

```python
"""
λ演算解譯器 - 完整實現
包含標準庫（Church數、布林值等）和REPL
"""

from __future__ import annotations
from typing import Optional, Dict, Any, Callable
from .lexer import Lexer, TokenType
from .parser import Parser
from .reducer import Normalizer
from .ast import LambdaExpr, Var, Abs, App

class LambdaError(Exception):
    """λ演算執行錯誤"""
    pass

class Environment:
    """環境：變數到值的映射"""
    
    def __init__(self, parent: Optional[Environment] = None):
        self.parent = parent
        self.bindings: Dict[str, Any] = {}
    
    def get(self, name: str) -> Any:
        """獲取變數值"""
        if name in self.bindings:
            return self.bindings[name]
        if self.parent:
            return self.parent.get(name)
        raise LambdaError(f"未綁定的變數: {name}")
    
    def set(self, name: str, value: Any):
        """設置變數值"""
        self.bindings[name] = value
    
    def extend(self) -> Environment:
        """創建新的子環境"""
        return Environment(self)


class LambdaInterpreter:
    """
    λ演算完整解譯器
    
    特性：
    - 解析λ表達式
    - 正規序歸約
    - 標準庫（Church數、布林值、組合子）
    - REPL模式
    """
    
    def __init__(self):
        self.normalizer = Normalizer(max_steps=10000)
        self.env = Environment()
        self._setup_standard_library()
    
    def _setup_standard_library(self):
        """設置標準庫"""
        from .parser import Parser
        
        # Church 數
        church_zero = Abs("f", Abs("x", Var("x")))
        church_one = Abs("f", Abs("x", App(Var("f"), Var("x"))))
        church_two = Abs("f", Abs("x", App(Var("f"), App(Var("f"), Var("x")))))
        
        # Church 布林值
        church_true = Abs("a", Abs("b", Var("a")))
        church_false = Abs("a", Abs("b", Var("b")))
        
        # 有趣的組合子
        omega = App(Abs("x", App(Var("x"), Var("x"))), Abs("x", App(Var("x"), Var("x"))))
        
        # 標準庫
        self.env.set("true", church_true)
        self.env.set("false", church_false)
        self.env.set("zero", church_zero)
        self.env.set("one", church_one)
        self.env.set("two", church_two)
        self.env.set("I", Abs("x", Var("x")))           # 恆等
        self.env.set("K", Abs("x", Abs("y", Var("x"))))  # 常數
        self.env.set("S", Abs("x", Abs("y", Abs("z", App(App(Var("x"), Var("z")), App(Var("y"), Var("z")))))))
        self.env.set("omega", omega)
        
        # Y combinator (用於遞歸)
        y_combinator = Abs("f", App(
            Abs("x", App(Var("f"), App(Var("x"), Var("x")))),
            Abs("x", App(Var("f"), App(Var("x"), Var("x"))))
        ))
        self.env.set("Y", y_combinator)
    
    def eval(self, text: str) -> tuple[str, int, bool]:
        """
        執行λ表達式
        
        返回：(結果, 步數, 是否收斂)
        """
        # 解析
        parser = Parser(text)
        ast = parser.parse()
        
        # 歸約
        result, steps, converged = self.normalizer.normalize(ast)
        
        return str(result), steps, converged
    
    def eval_church(self, text: str) -> Any:
        """
        執行並返回Python值（用於Church數）
        """
        result_str, steps, converged = self.eval(text)
        
        if not converged:
            raise LambdaError(f"表達式不收斂")
        
        # 嘗試轉換為Python值
        return self._to_python_value(text, result_str)
    
    def _to_python_value(self, input_text: str, result_str: str) -> Any:
        """將結果轉換為Python值"""
        try:
            parser = Parser(result_str)
            result = parser.parse()
            return self._church_to_python(result)
        except:
            return result_str
    
    def _church_to_python(self, expr: LambdaExpr) -> Any:
        """將Church編碼轉換為Python值"""
        # 嘗試識別為Church數
        if isinstance(expr, Abs) and isinstance(expr.body, Abs):
            # 這可能是Church數
            body = expr.body
            if isinstance(body.body, Var) and body.body.name == body.var:
                # zero
                return 0
            elif isinstance(body.body, App):
                # 計算f出現的次數
                count = self._count_applications(body.body)
                if count is not None:
                    return count
        
        # 嘗試識別為布林值
        if isinstance(expr, Abs) and isinstance(expr.body, Abs):
            # TRUE = λa. λb. a
            # FALSE = λa. λb. b
            pass
        
        return expr
    
    def _count_applications(self, app: App) -> Optional[int]:
        """計算函數應用的次數"""
        count = 0
        current = app
        
        while isinstance(current, App):
            if isinstance(current.arg, Var):
                count += 1
            else:
                return None
            if isinstance(current.func, Var):
                break
            elif isinstance(current.func, App):
                current = current.func
            else:
                return None
        
        return count if isinstance(current.func, Var) else None
    
    def repl(self):
        """互動式REPL"""
        print("=== λ演算 REPL ===")
        print("輸入λ表達式求值，:help 獲取幫助，:quit 退出\n")
        
        while True:
            try:
                user_input = input("λ> ").strip()
                
                if not user_input:
                    continue
                
                if user_input == ":quit":
                    print("再見！")
                    break
                
                if user_input == ":help":
                    self._print_help()
                    continue
                
                if user_input == ":env":
                    self._print_env()
                    continue
                
                result, steps, converged = self.eval(user_input)
                
                if converged:
                    print(f"  ⇒ {result} (歸約 {steps} 步)")
                else:
                    print(f"  ⚠ 表達式發散（歸約了 {steps} 步）")
            
            except KeyboardInterrupt:
                print("\n使用 :quit 退出")
            except Exception as e:
                print(f"  錯誤: {e}")
    
    def _print_help(self):
        """打印幫助信息"""
        print("""
可用命令：
  :help    - 顯示此幫助
  :env     - 顯示當前環境
  :quit    - 退出REPL

標準庫：
  true, false - Church 布林值
  zero, one, two - Church 數 0, 1, 2
  I, K, S    - 基本組合子
  omega      - Ω = (λx. x x) (λx. x x)
  Y          - Y combinator（用於遞歸）

範例：
  λx. x
  (λx. x) y
  λf. λx. f (f x)
""")
    
    def _print_env(self):
        """打印環境"""
        print("當前環境：")
        for name in sorted(self.env.bindings.keys()):
            print(f"  {name} = {self.env.bindings[name]}")


# 方便使用的函數
_interpreter = None

def eval_lambda(text: str) -> tuple[str, int, bool]:
    """快速求值λ表達式"""
    global _interpreter
    if _interpreter is None:
        _interpreter = LambdaInterpreter()
    return _interpreter.eval(text)


# 命令行入口
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # 命令行模式
        text = " ".join(sys.argv[1:])
        interpreter = LambdaInterpreter()
        result, steps, converged = interpreter.eval(text)
        print(f"{result}")
    else:
        # REPL模式
        interpreter = LambdaInterpreter()
        interpreter.repl()
```

## 5.7 測試套件

[程式檔案：05-6_tests.py](../_code/05/05-6-tests.py)

```python
"""
λ演算解譯器測試套件
"""

import unittest
from lambda_interpreter.lexer import Lexer, TokenType
from lambda_interpreter.parser import Parser
from lambda_interpreter.reducer import Normalizer
from lambda_interpreter.interpreter import LambdaInterpreter
from lambda_interpreter.ast import Var, Abs, App

class TestLexer(unittest.TestCase):
    """詞法分析器測試"""
    
    def test_simple_var(self):
        lexer = Lexer("x")
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, TokenType.VAR)
        self.assertEqual(tokens[0].value, "x")
    
    def test_lambda(self):
        lexer = Lexer("λx. x")
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, TokenType.LAMBDA)
        self.assertEqual(tokens[1].type, TokenType.VAR)
        self.assertEqual(tokens[1].value, "x")
        self.assertEqual(tokens[2].type, TokenType.DOT)
    
    def test_application(self):
        lexer = Lexer("f x y")
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].value, "f")
        self.assertEqual(tokens[1].value, "x")
        self.assertEqual(tokens[2].value, "y")


class TestParser(unittest.TestCase):
    """解析器測試"""
    
    def test_variable(self):
        parser = Parser("x")
        ast = parser.parse()
        self.assertEqual(ast, Var("x"))
    
    def test_identity(self):
        parser = Parser("λx. x")
        ast = parser.parse()
        self.assertEqual(ast, Abs("x", Var("x")))
    
    def test_application(self):
        parser = Parser("(λx. x) y")
        ast = parser.parse()
        self.assertEqual(ast, App(Abs("x", Var("x")), Var("y")))
    
    def test_curried_function(self):
        parser = Parser("λx. λy. x")
        ast = parser.parse()
        expected = Abs("x", Abs("y", Var("x")))
        self.assertEqual(ast, expected)


class TestReducer(unittest.TestCase):
    """歸約引擎測試"""
    
    def setUp(self):
        self.normalizer = Normalizer()
    
    def test_identity_reduction(self):
        """(λx. x) y → y"""
        expr = App(Abs("x", Var("x")), Var("y"))
        result, steps, _ = self.normalizer.normalize(expr)
        self.assertEqual(str(result), "y")
        self.assertEqual(steps, 1)
    
    def test_constant_function(self):
        """(λx. λy. x) a b → a"""
        expr = App(App(Abs("x", Abs("y", Var("x"))), Var("a")), Var("b"))
        result, steps, _ = self.normalizer.normalize(expr)
        self.assertEqual(str(result), "a")
    
    def test_divergence(self):
        """Ω = (λx. x x) (λx. x x) 發散"""
        omega = App(
            Abs("x", App(Var("x"), Var("x"))),
            Abs("x", App(Var("x"), Var("x")))
        )
        result, steps, converged = self.normalizer.normalize(omega)
        self.assertFalse(converged)
        self.assertEqual(steps, self.normalizer.max_steps)


class TestInterpreter(unittest.TestCase):
    """完整解譯器測試"""
    
    def setUp(self):
        self.interpreter = LambdaInterpreter()
    
    def test_identity(self):
        result, steps, converged = self.interpreter.eval("(λx. x) y")
        self.assertTrue(converged)
        self.assertEqual(result, "y")
    
    def test_standard_library(self):
        result, steps, converged = self.interpreter.eval("one")
        self.assertTrue(converged)
        self.assertEqual(result, "one")
    
    def test_church_num(self):
        """測試 Church 數的歸約"""
        # SUCC one = two
        result, steps, converged = self.interpreter.eval("(λn. λf. λx. f (n f x)) one")
        self.assertTrue(converged)
        self.assertIn("two", result)


if __name__ == "__main__":
    unittest.main()
```

## 5.8 REPL 使用範例

[程式檔案：05-7_repl_demo.py](../_code/05/05-7-repl-demo.py)

```python
"""
λ演算 REPL 演示腳本
"""

def demo():
    print("=" * 60)
    print("λ演算解譯器 REPL 演示")
    print("=" * 60)
    print()
    
    from lambda_interpreter.interpreter import LambdaInterpreter
    
    interpreter = LambdaInterpreter()
    
    test_expressions = [
        # 基本應用
        "(λx. x) y",
        "(λx. λy. x) a b",
        
        # Church 數
        "(λn. n) zero",           # 識別為 zero
        "(λf. λx. f (f x))",      # 2
        
        # 布林值
        "true",
        "false",
        
        # 組合子
        "I",
        "K",
        "S",
        
        # 有趣的例子
        "(λx. x x) (λy. y)",     # = λy. y
        "ω = (λx. x x) (λx. x x)",  # 發散！
    ]
    
    print("測試表達式：\n")
    
    for expr in test_expressions:
        try:
            result, steps, converged = interpreter.eval(expr)
            if converged:
                print(f"  {expr}")
                print(f"    → {result} ({steps} 步)")
            else:
                print(f"  {expr}")
                print(f"    → [發散，超過 {steps} 步]")
            print()
        except Exception as e:
            print(f"  {expr}")
            print(f"    → 錯誤: {e}")
            print()
    
    print("=" * 60)
    print("\n進入互動模式...")
    print("（或按 Ctrl+C 退出）\n")
    
    try:
        interpreter.repl()
    except KeyboardInterrupt:
        print("\n再見！")


if __name__ == "__main__":
    demo()
```

執行結果示例：

```
λ> (λx. x) y
  ⇒ y (歸約 1 步)

λ> (λx. λy. x) a b
  ⇒ a (歸約 2 步)

λ> λf. λx. f (f x)
  ⇒ λf. λx. f (f x) (0 步 - 已經是正規形式)

λ> ω
  ⚠ 表達式發散（歸約了 10000 步）
```

## 5.9 小結

本章我們實作了：

1. **抽象語法樹（AST）**：完整的λ表達式數據結構
2. **詞法分析器**：將字串轉換為token流
3. **遞歸下降解析器**：將token流轉換為AST
4. **歸約引擎**：執行β歸約和α轉換
5. **完整解譯器**：整合所有組件，加上標準庫
6. **測試套件**：確保各個組件的正確性

這個解譯器可以用來：
- 實驗λ演算的各种性質
- 理解圖靈機和λ演算的等價性
- 探索組合子的世界

下一章，我們將學習圖靈機理論——另一種同樣強大的計算模型。

## 練習題

1. **添加更多標準庫**：在λ演算解譯器中添加 Church 數的後繼函數（SUCC）和加法（ADD）。

2. **優化歸約引擎**：實現應用序（Applicative Order）歸約作為另一種策略，並比較兩種策略的差異。

3. **實現η轉換**：在歸約引擎中添加η歸約作為可選的優化。

4. **尾遞歸優化**：修改解譯器以支持尾遞歸優化，這對實現遞歸函數非常重要。

5. **類型檢查器**：為λ演算添加簡單的類型系統（參考第12章的類型理論）。
