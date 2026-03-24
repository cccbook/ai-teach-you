#!/usr/bin/env python3
"""
Lisp 符號處理：代數簡化
展示 Lisp 風格的符號處理 - 程式即資料的概念
"""

import re
from typing import Any, List, Union

Symbol = str
SExp = Union[Symbol, List['SExp']]

class LispSymbolic:
    def __init__(self):
        self.rules = []
    
    def add_rule(self, pattern, replacement):
        self.rules.append((pattern, replacement))
    
    def parse(self, s: str) -> SExp:
        s = s.replace('(', ' ( ').replace(')', ' ) ')
        tokens = s.split()
        
        def parse_tokens(tokens: List[str]) -> SExp:
            if not tokens:
                raise ValueError("Unexpected end of input")
            token = tokens.pop(0)
            if token == '(':
                result = []
                while tokens[0] != ')':
                    result.append(parse_tokens(tokens))
                tokens.pop(0)
                return result
            elif token == ')':
                raise ValueError("Unexpected closing parenthesis")
            else:
                try:
                    return int(token)
                except ValueError:
                    try:
                        return float(token)
                    except ValueError:
                        return token
        
        return parse_tokens(tokens)
    
    def simplify(self, expr: SExp) -> SExp:
        if isinstance(expr, (int, float)):
            return expr
        
        if isinstance(expr, Symbol):
            return expr
        
        if not isinstance(expr, list):
            return expr
        
        if len(expr) == 0:
            return expr
        
        op = expr[0]
        
        if op == '+':
            result = 0
            args = []
            for arg in expr[1:]:
                simplified = self.simplify(arg)
                if isinstance(simplified, (int, float)):
                    result += simplified
                else:
                    args.append(simplified)
            if not args and result == 0:
                return 0
            elif not args:
                return result
            elif result == 0:
                return args if len(args) == 1 else ['+'] + args
            else:
                return [result] + args + [0]
        
        if op == '*':
            result = 1
            args = []
            for arg in expr[1:]:
                simplified = self.simplify(arg)
                if isinstance(simplified, (int, float)):
                    result *= simplified
                else:
                    args.append(simplified)
            if result == 0:
                return 0
            elif not args and result == 1:
                return 1
            elif not args:
                return result
            elif result == 1:
                return args if len(args) == 1 else ['*'] + args
            else:
                return [result] + args
        
        if op == '-':
            if len(expr) == 2:
                arg = self.simplify(expr[1])
                if isinstance(arg, (int, float)):
                    return -arg
                return ['-', arg]
            else:
                left = self.simplify(expr[1])
                right = self.simplify(expr[2])
                if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                    return left - right
                return [left, '-', right]
        
        if op == '/':
            left = self.simplify(expr[1])
            right = self.simplify(expr[2])
            if isinstance(left, (int, float)) and isinstance(right, (int, float)) and right != 0:
                return left / right
            return [left, '/', right]
        
        return expr
    
    def to_string(self, expr: SExp) -> str:
        if isinstance(expr, (int, float)):
            return str(expr)
        if isinstance(expr, Symbol):
            return expr
        return '(' + ' '.join(self.to_string(x) for x in expr) + ')'

def lisp_style_example():
    print("=== Lisp 風格符號處理 ===\n")
    
    lisp = LispSymbolic()
    
    tests = [
        "(+ 1 2)",
        "(+ 1 2 3)",
        "(* 2 3)",
        "(* 2 3 0)",
        "(+ (* 2 3) 4)",
        "(- 10 5)",
        "(/ 10 2)",
        "(+ 1 (+ 2 3))",
        "(* (+ 1 2) (+ 3 4))",
    ]
    
    for test in tests:
        parsed = lisp.parse(test)
        simplified = lisp.simplify(parsed)
        result = lisp.to_string(simplified)
        print(f"{test} => {result}")

def algebraic_simplification():
    print("\n=== 代數簡化範例 ===\n")
    
    lisp = LispSymbolic()
    
    tests = [
        ["+", 1, 2],
        ["+", ["+", 1, 2], 3],
        ["*", 2, ["+", 3, 4]],
        ["+", ["*", 0, 5], 10],
        ["*", 1, ["*", 2, 3]],
    ]
    
    for test in tests:
        simplified = lisp.simplify(test)
        result = lisp.to_string(simplified)
        print(f"{test} => {result}")

if __name__ == "__main__":
    lisp_style_example()
    algebraic_simplification()
