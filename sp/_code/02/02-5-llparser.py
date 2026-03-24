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