"""
λ演算解譯器 - 詞法分析器
"""

from __future__ import annotations
from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional, List

class TokenType(Enum):
    LAMBDA = auto()
    DOT = auto()
    LPAREN = auto()
    RPAREN = auto()
    VAR = auto()
    EOF = auto()

@dataclass
class Token:
    type: TokenType
    value: str
    line: int = 0
    column: int = 0

class LexerError(Exception):
    pass

class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = self.text[0] if text else None
    
    def advance(self):
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
    
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char in ' \t\n\r':
            self.advance()
    
    def read_identifier(self) -> str:
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return result
    
    def get_next_token(self) -> Token:
        while self.current_char is not None:
            if self.current_char in ' \t\n\r':
                self.skip_whitespace()
                continue
            
            if self.current_char == 'λ' or self.current_char == '\\':
                token = Token(TokenType.LAMBDA, self.current_char, self.line, self.column)
                self.advance()
                return token
            
            if self.current_char == '.':
                token = Token(TokenType.DOT, '.', self.line, self.column)
                self.advance()
                return token
            
            if self.current_char == '(':
                token = Token(TokenType.LPAREN, '(', self.line, self.column)
                self.advance()
                return token
            
            if self.current_char == ')':
                token = Token(TokenType.RPAREN, ')', self.line, self.column)
                self.advance()
                return token
            
            if self.current_char.isalpha() or self.current_char == '_':
                var_name = self.read_identifier()
                return Token(TokenType.VAR, var_name, self.line, self.column - len(var_name))
            
            raise LexerError(f"未預期的字符: {self.current_char!r}")
        
        return Token(TokenType.EOF, '', self.line, self.column)
    
    def tokenize(self) -> List[Token]:
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens


if __name__ == "__main__":
    print("=== λ演算詞法分析器測試 ===\n")
    
    test_inputs = [
        "λx. x",
        "λx. λy. x y",
        "(λx. x) y",
        "λf. λx. f (f x)",
    ]
    
    for text in test_inputs:
        lexer = Lexer(text)
        tokens = lexer.tokenize()
        print(f"輸入：{text}")
        print(f"Token：{[(t.type.name, t.value) for t in tokens]}")
        print()
