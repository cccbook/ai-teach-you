"""
λ演算解譯器 - 抽象語法樹
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Set

@dataclass
class LambdaExpr:
    pass

@dataclass
class Var(LambdaExpr):
    name: str
    
    def free_vars(self) -> Set[str]:
        return {self.name}
    
    def bound_vars(self) -> Set[str]:
        return set()
    
    def substitute(self, var: str, replacement: LambdaExpr) -> LambdaExpr:
        if self.name == var:
            return replacement
        return Var(self.name)
    
    def __str__(self) -> str:
        return self.name

@dataclass
class Abs(LambdaExpr):
    var: str
    body: LambdaExpr
    
    def free_vars(self) -> Set[str]:
        return self.body.free_vars() - {self.var}
    
    def bound_vars(self) -> Set[str]:
        return {self.var} | self.body.bound_vars()
    
    def substitute(self, var: str, replacement: LambdaExpr) -> LambdaExpr:
        if var == self.var:
            return self
        else:
            if self.var in replacement.free_vars():
                new_var = self._fresh_var(self.var, replacement.free_vars())
                new_body = self.body.substitute(self.var, Var(new_var))
                return Abs(new_var, new_body.substitute(var, replacement))
            else:
                return Abs(self.var, self.body.substitute(var, replacement))
    
    @staticmethod
    def _fresh_var(base: str, avoid: Set[str]) -> str:
        if base not in avoid:
            return base
        suffix = 0
        while f"{base}{suffix}" in avoid:
            suffix += 1
        return f"{base}{suffix}"
    
    def __str__(self) -> str:
        return f"λ{self.var}. {self.body}"

@dataclass
class App(LambdaExpr):
    func: LambdaExpr
    arg: LambdaExpr
    
    def free_vars(self) -> Set[str]:
        return self.func.free_vars() | self.arg.free_vars()
    
    def bound_vars(self) -> Set[str]:
        return self.func.bound_vars() | self.arg.bound_vars()
    
    def substitute(self, var: str, replacement: LambdaExpr) -> LambdaExpr:
        return App(
            self.func.substitute(var, replacement),
            self.arg.substitute(var, replacement)
        )
    
    def __str__(self) -> str:
        func_str = str(self.func)
        if isinstance(self.func, App):
            func_str = f"({func_str})"
        return f"{func_str} {self.arg}"


if __name__ == "__main__":
    print("=== λ演算 AST 測試 ===\n")
    
    identity = Abs("x", Var("x"))
    print(f"恆等函數：{identity}")
    print(f"  自由變數：{identity.free_vars()}")
    print(f"  約束變數：{identity.bound_vars()}")
    
    app = App(identity, Var("y"))
    print(f"\n應用 (λx. x) y：{app}")
    print(f"  自由變數：{app.free_vars()}")
    
    const = Abs("x", Abs("y", Var("x")))
    print(f"\n常函數：{const}")
    print(f"  自由變數：{const.free_vars()}")
    
    result = app.substitute("y", Var("z"))
    print(f"\n替換 (λx. x) y 中的 y → z：{result}")
