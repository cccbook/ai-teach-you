"""
完整流程：原始碼 → Tokenizer → Parser → AST → 直譯執行
"""

# ========== 1. 詞法分析 ==========
def lex(source):
    """將原始碼轉換為 Token 流"""
    tokens = []
    i = 0
    while i < len(source):
        if source[i].isspace():
            i += 1
            continue
        if source[i].isdigit():
            j = i
            while j < len(source) and source[j].isdigit():
                j += 1
            tokens.append(('NUM', int(source[i:j])))
            i = j
            continue
        if source[i] == '+':
            tokens.append(('PLUS', '+'))
            i += 1
            continue
        if source[i] == '-':
            tokens.append(('MINUS', '-'))
            i += 1
            continue
        if source[i] == '*':
            tokens.append(('MULT', '*'))
            i += 1
            continue
        if source[i] == '/':
            tokens.append(('DIV', '/'))
            i += 1
            continue
        if source[i] == '(':
            tokens.append(('LPAREN', '('))
            i += 1
            continue
        if source[i] == ')':
            tokens.append(('RPAREN', ')'))
            i += 1
            continue
        raise SyntaxError(f"無法識別的字元: {source[i]}")
    return tokens

# ========== 2. 語法分析 ==========
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    
    def consume(self):
        token = self.peek()
        self.pos += 1
        return token
    
    def parse(self):
        return self.expr()
    
    def expr(self):
        result = self.term()
        while self.peek() and self.peek()[0] in ('PLUS', 'MINUS'):
            op = self.consume()[1]
            right = self.term()
            result = {'type': 'binary', 'op': op, 'left': result, 'right': right}
        return result
    
    def term(self):
        result = self.factor()
        while self.peek() and self.peek()[0] in ('MULT', 'DIV'):
            op = self.consume()[1]
            right = self.factor()
            result = {'type': 'binary', 'op': op, 'left': result, 'right': right}
        return result
    
    def factor(self):
        token = self.peek()
        if token[0] == 'NUM':
            self.consume()
            return {'type': 'num', 'value': token[1]}
        if token[0] == 'LPAREN':
            self.consume()
            result = self.expr()
            self.consume()  # RPAREN
            return result
        raise SyntaxError("語法錯誤")

# ========== 3. 語意分析與執行 ==========
def evaluate(node):
    """直譯執行 AST"""
    if node['type'] == 'num':
        return node['value']
    
    if node['type'] == 'binary':
        left_val = evaluate(node['left'])
        right_val = evaluate(node['right'])
        op = node['op']
        
        if op == '+': return left_val + right_val
        if op == '-': return left_val - right_val
        if op == '*': return left_val * right_val
        if op == '/': return left_val // right_val
    
    raise ValueError("未知的節點類型")

# ========== 完整流程 ==========
def run(source):
    print(f"原始碼: {source}")
    
    tokens = lex(source)
    print(f"Tokens: {tokens}")
    
    ast = Parser(tokens).parse()
    print(f"AST: {ast}")
    
    result = evaluate(ast)
    print(f"結果: {result}")
    print()

# 測試各種表達式
run("2 + 3")
run("10 - 4 * 2")
run("(10 - 4) * 2")
run("100 / 10 / 2")