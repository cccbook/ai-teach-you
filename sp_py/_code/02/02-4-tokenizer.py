import re

class Tokenizer:
    """簡易詞法分析器"""
    
    TOKEN_PATTERNS = [
        ('NUMBER', r'\d+'),
        ('PLUS', r'\+'),
        ('MINUS', r'-'),
        ('MULT', r'\*'),
        ('DIV', r'/'),
        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
        ('EQUAL', r'='),
        ('IDENT', r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ('SKIP', r'[ \t\n]+'),
    ]
    
    def __init__(self, source):
        self.source = source
        self.pos = 0
    
    def tokenize(self):
        tokens = []
        while self.pos < len(self.source):
            matched = False
            for token_type, pattern in self.TOKEN_PATTERNS:
                regex = re.compile(pattern)
                match = regex.match(self.source, self.pos)
                if match:
                    value = match.group(0)
                    if token_type != 'SKIP':
                        tokens.append((token_type, value))
                    self.pos = match.end()
                    matched = True
                    break
            if not matched:
                raise SyntaxError(f"無法識別的字元: {self.source[self.pos]}")
        return tokens

# 測試
source = "x = 42 + y * (10 - 2)"
tokens = Tokenizer(source).tokenize()
for token in tokens:
    print(token)
# 輸出：
# ('IDENT', 'x')
# ('EQUAL', '=')
# ('NUMBER', '42')
# ('PLUS', '+')
# ('IDENT', 'y')
# ('MULT', '*')
# ('LPAREN', '(')
# ('NUMBER', '10')
# ('MINUS', '-')
# ('NUMBER', '2')
# ('RPAREN', ')')