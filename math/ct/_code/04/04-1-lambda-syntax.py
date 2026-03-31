"""
λ演算語法解析器
將λ演算的字符串表示解析為結構化表示
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, List
import re

class LambdaExpr:
    """λ演算表達式的基類"""
    pass

@dataclass
class Var(LambdaExpr):
    name: str
    
    def __repr__(self):
        return self.name

@dataclass
class Abs(LambdaExpr):
    var: str
    body: LambdaExpr
    
    def __repr__(self):
        return f"(λ{self.var}. {self.body})"

@dataclass
class App(LambdaExpr):
    func: LambdaExpr
    arg: LambdaExpr
    
    def __repr__(self):
        return f"({self.func} {self.arg})"

class LambdaParser:
    def __init__(self):
        self.text = ""
        self.pos = 0
    
    def parse(self, text: str) -> LambdaExpr:
        self.text = text
        self.pos = 0
        return self.parse_expr()
    
    def peek(self) -> Optional[str]:
        if self.pos < len(self.text):
            return self.text[self.pos]
        return None
    
    def consume(self) -> Optional[str]:
        if self.pos < len(self.text):
            ch = self.text[self.pos]
            self.pos += 1
            return ch
        return None
    
    def skip_whitespace(self):
        while self.pos < len(self.text) and self.text[self.pos] in ' \t\n':
            self.pos += 1
    
    def parse_var(self) -> Var:
        self.skip_whitespace()
        name = ""
        while self.pos < len(self.text):
            ch = self.text[self.pos]
            if ch.isalnum() or ch == '_':
                name += ch
                self.pos += 1
            else:
                break
        return Var(name)
    
    def parse_atom(self) -> LambdaExpr:
        self.skip_whitespace()
        ch = self.peek()
        
        if ch == '(':
            self.consume()
            expr = self.parse_expr()
            self.skip_whitespace()
            if self.peek() == ')':
                self.consume()
            return expr
        elif ch == 'λ' or ch == '\\':
            return self.parse_abs()
        else:
            return self.parse_var()
    
    def parse_abs(self) -> Abs:
        self.skip_whitespace()
        self.consume()  # 消費 'λ' 或 '\\'
        
        self.skip_whitespace()
        var = ""
        while self.pos < len(self.text):
            ch = self.peek()
            if ch.isalnum():
                var += ch
                self.consume()
            else:
                break
        
        self.skip_whitespace()
        if self.peek() == '.':
            self.consume()
        
        body = self.parse_expr()
        return Abs(var, body)
    
    def parse_app(self) -> LambdaExpr:
        left = self.parse_atom()
        
        while True:
            self.skip_whitespace()
            if self.peek() in [None, ')', '.']:
                break
            right = self.parse_atom()
            left = App(left, right)
        
        return left
    
    def parse_expr(self) -> LambdaExpr:
        return self.parse_app()
    
    @staticmethod
    def examples():
        print("=== λ演算語法示例 ===\n")
        
        examples = [
            "x",
            "λx. x",
            "λx. λy. x",
            "(λx. x) y",
            "λf. λx. f x",
            "λx. λy. λz. x z (y z)",
        ]
        
        parser = LambdaParser()
        
        for expr in examples:
            print(f"  {expr}")
            try:
                parsed = parser.parse(expr)
                print(f"    → {parsed}\n")
            except Exception as e:
                print(f"    → 解析錯誤: {e}\n")


if __name__ == "__main__":
    LambdaParser.examples()
