"""
λ演算解譯器 - 主模組
"""

from .lexer import Lexer
from .parser import Parser
from .reducer import Normalizer
from .ast import LambdaExpr, Var, Abs, App

class LambdaInterpreter:
    def __init__(self):
        self.normalizer = Normalizer(max_steps=10000)
        self._setup_standard_library()
    
    def _setup_standard_library(self):
        self.env = {}
        self.env['I'] = Abs('x', Var('x'))
        self.env['K'] = Abs('x', Abs('y', Var('x')))
        self.env['S'] = Abs('x', Abs('y', Abs('z', App(App(Var('x'), Var('z')), App(Var('y'), Var('z'))))))
        self.env['true'] = Abs('a', Abs('b', Var('a')))
        self.env['false'] = Abs('a', Abs('b', Var('b')))
    
    def eval(self, text: str) -> tuple[str, int, bool]:
        parser = Parser(text)
        ast = parser.parse()
        result, steps, converged = self.normalizer.normalize(ast)
        return str(result), steps, converged
    
    def repl(self):
        print("=== λ演算 REPL ===")
        print("輸入λ表達式求值，:quit 退出\n")
        
        while True:
            try:
                user_input = input("λ> ").strip()
                
                if not user_input:
                    continue
                
                if user_input == ":quit":
                    print("再見！")
                    break
                
                result, steps, converged = self.eval(user_input)
                
                if converged:
                    print(f"  ⇒ {result} (歸約 {steps} 步)")
                else:
                    print(f"  ⚠ 表達式發散（歸約了 {steps} 步）")
            
            except KeyboardInterrupt:
                print("\n使用 :quit 退出")
            except Exception as e:
                print(f"  錯誤: {e}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        interpreter = LambdaInterpreter()
        result, steps, converged = interpreter.eval(text)
        print(f"{result}")
    else:
        interpreter = LambdaInterpreter()
        interpreter.repl()
