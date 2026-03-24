# 文法定義（使用 EBNF 風格）
# Expr    → Term (( '+' | '-' ) Term)*
# Term    → Factor (( '*' | '/' ) Factor)*
# Factor  → NUMBER | '(' Expr ')'

# 手動 Parser 實現
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def consume(self):
        token = self.current_token()
        self.pos += 1
        return token
    
    def parse(self):
        return self.expr()
    
    def expr(self):
        """Expr → Term (( '+' | '-' ) Term)*"""
        result = self.term()
        while self.current_token() in ['+', '-']:
            op = self.consume()
            right = self.term()
            if op == '+':
                result = ('+', result, right)
            else:
                result = ('-', result, right)
        return result
    
    def term(self):
        """Term → Factor (( '*' | '/' ) Factor)*"""
        result = self.factor()
        while self.current_token() in ['*', '/']:
            op = self.consume()
            right = self.factor()
            if op == '*':
                result = ('*', result, right)
            else:
                result = ('/', result, right)
        return result
    
    def factor(self):
        """Factor → NUMBER | '(' Expr ')'"""
        token = self.current_token()
        if token == '(':
            self.consume()  # '('
            result = self.expr()
            self.consume()  # ')'
            return result
        # 應該是數字
        return ('num', self.consume())

# 測試 Tokenizer 和 Parser
def tokenize(text):
    """簡單的詞法分析"""
    tokens = []
    i = 0
    while i < len(text):
        if text[i].isdigit():
            j = i
            while j < len(text) and text[j].isdigit():
                j += 1
            tokens.append(text[i:j])
            i = j
        elif text[i] in '+-*/()':
            tokens.append(text[i])
            i += 1
        else:
            i += 1  # 跳過空白
    return tokens

# 測試
tokens = tokenize("2 + 3 * 4")
print("Tokens:", tokens)  # ['2', '+', '3', '*', '4']

parser = Parser(tokens)
ast = parser.parse()
print("AST:", ast)  # ('+', ('num', '2'), ('*', ('num', '3'), ('num', '4')))