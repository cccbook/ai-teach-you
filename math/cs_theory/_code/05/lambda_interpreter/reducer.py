"""
λ演算解譯器 - 歸約引擎
"""

from __future__ import annotations
from typing import Optional
from .ast import LambdaExpr, Var, Abs, App

class Normalizer:
    def __init__(self, max_steps: int = 1000):
        self.max_steps = max_steps
    
    def beta_reduce(self, expr: LambdaExpr) -> Optional[LambdaExpr]:
        if isinstance(expr, App):
            if isinstance(expr.func, Abs):
                return expr.func.body.substitute(expr.func.var, expr.arg)
            else:
                reduced_func = self.beta_reduce(expr.func)
                if reduced_func is not None:
                    return App(reduced_func, expr.arg)
                reduced_arg = self.beta_reduce(expr.arg)
                if reduced_arg is not None:
                    return App(expr.func, reduced_arg)
                return None
        
        elif isinstance(expr, Abs):
            reduced_body = self.beta_reduce(expr.body)
            if reduced_body is not None:
                return Abs(expr.var, reduced_body)
            return None
        
        elif isinstance(expr, Var):
            return None
        
        return None
    
    def normalize(self, expr: LambdaExpr) -> tuple[LambdaExpr, int, bool]:
        current = expr
        steps = 0
        diverged = False
        
        while steps < self.max_steps:
            reduced = self.beta_reduce(current)
            if reduced is None:
                break
            
            if str(reduced) == str(current):
                diverged = True
                break
            
            current = reduced
            steps += 1
        
        return current, steps, not diverged and steps < self.max_steps


if __name__ == "__main__":
    from lambda_interpreter.parser import Parser
    
    print("=== λ演算歸約引擎測試 ===\n")
    
    test_cases = [
        ("(λx. x) y", "y"),
        ("(λx. λy. x) a b", "a"),
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
