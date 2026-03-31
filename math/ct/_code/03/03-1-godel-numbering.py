"""
哥德爾編號系統
將形式語言中的符號和公式映射為唯一的自然數
"""

from typing import List, Dict
from functools import reduce

class GodelNumbering:
    """哥德爾編號實現"""
    
    def __init__(self):
        self.symbol_to_code: Dict[str, int] = {
            '0': 1,
            'S': 2,
            '+': 3,
            '*': 4,
            '-': 5,
            '=': 6,
            '(': 7,
            ')': 8,
            ',': 9,
            '∧': 10,
            '∨': 11,
            '¬': 12,
            '→': 13,
            '∀': 14,
            '∃': 15,
            'x': 16,
            'y': 17,
            'z': 18,
        }
        
        self.code_to_symbol: Dict[int, str] = {
            v: k for k, v in self.symbol_to_code.items()
        }
        
        self.primes = self._generate_primes(30)
    
    def _generate_primes(self, n: int) -> List[int]:
        sieve = list(range(n + 1))
        for i in range(2, int(n**0.5) + 1):
            if sieve[i]:
                for j in range(i*i, n + 1, i):
                    sieve[j] = 0
        return [p for p in sieve[2:] if p]
    
    def encode_symbol(self, symbol: str) -> int:
        return self.symbol_to_code.get(symbol, 0)
    
    def decode_symbol(self, code: int) -> str:
        return self.code_to_symbol.get(code, '?')
    
    def encode_formula(self, formula: str) -> int:
        codes = [self.encode_symbol(c) for c in formula if c.strip()]
        if not codes:
            return 1
        
        result = 1
        for i, code in enumerate(codes):
            if code > 0:
                result *= self.primes[i] ** code
        return result
    
    def prove_godel_trick(self):
        print("=== 哥德爾編號演示 ===\n")
        
        print("符號到數字的映射：")
        for symbol, code in sorted(self.symbol_to_code.items(), key=lambda x: x[1]):
            print(f"  {symbol} → {code}")
        
        print("\n" + "="*50)
        
        formulas = [
            "0=0",
            "S(0)=0",
            "x=0",
            "∀x(x=0)",
        ]
        
        print("\n公式編碼示例：")
        for formula in formulas:
            godel_num = self.encode_formula(formula)
            print(f"  {formula:20} → {godel_num:,}")
        
        print("\n哥德爾編號的關鍵洞察：")
        print("  • 數字可以代表公式")
        print("  • 公式是符號的序列")
        print("  • 因此，數字可以「代表」數字")
        print("  • 這為自引用打開了大門！")


if __name__ == "__main__":
    gn = GodelNumbering()
    gn.prove_godel_trick()
