"""
λ演算解譯器 - 解析器
"""

from __future__ import annotations
from typing import Optional, List
from .lexer import Lexer, Token, TokenType
from .ast import LambdaExpr, Var, Abs, App

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, text: str):
        self.lexer = Lexer(text)
        self.current_token: Optional[Token] = None
        self.tokens: List[Token] = []
        self.pos = 0
        self._tokenize()
    
    def _tokenize(self):
        self.tokens = []
        while True:
            token = self.lexer.get_next_token()
            self.tokens.append(token)
            if token.type == TokenType.EOF:
                break
        self.current_token = self.tokens[0] if self.tokens else None
    
    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = Token(TokenType.EOF, '', 0, 0)
    
    def parse(self) -> LambdaExpr:
        expr = self.expr()
        return expr
    
    def expr(self) -> LambdaExpr:
        saved_pos = self.pos
        try:
            return self.abstraction()
        except ParserError:
            self.pos = saved_pos
            self.current_token = self.tokens[self.pos]
        return self.application()
    
    def abstraction(self) -> LambdaExpr:
        if self.current_token.type == TokenType.LAMBDA:
            self.advance()
        elif self.current_token.type != TokenType.LPAREN:
            raise ParserError("期望 λ 或 (")
        else:
            self.advance()
            if self.current_token.type != TokenType.LAMBDA:
                raise ParserError("期望 λ")
            self.advance()
        
        if self.current_token.type != TokenType.VAR:
            raise ParserError("期望變數名")
        var = self.current_token.value
        self.advance()
        
        if self.current_token.type != TokenType.DOT:
            raise ParserError("期望 .")
        self.advance()
        
        body = self.expr()
        
        if self.current_token.type == TokenType.RPAREN:
            self.advance()
        
        return Abs(var, body)
    
    def application(self) -> LambdaExpr:
        atoms = []
        
        while True:
            atom = self.atom()
            atoms.append(atom)
            
            if (self.current_token.type in [TokenType.LAMBDA, TokenType.EOF, 
                                            TokenType.RPAREN, TokenType.DOT] or
                self.pos + 1 >= len(self.tokens)):
                break
        
        if not atoms:
            raise ParserError("期望表達式")
        
        result = atoms[0]
        for atom in atoms[1:]:
            result = App(result, atom)
        
        return result
    
    def atom(self) -> LambdaExpr:
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
    
    for text in test_cases:
        parser = Parser(text)
        ast = parser.parse()
        print(f"輸入：{text}")
        print(f"AST：  {ast}")
        print()
