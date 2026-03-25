"""
簡單解譯器架構
原始碼 → 詞法分析 → 語法分析 → AST → 執行
"""

# 完整解譯器範例：支援變數、運算、輸出
class Interpreter:
    def __init__(self):
        self.variables = {}  # 變數表
        self.ast = None
    
    # ========== 詞法分析 ==========
    def lex(self, source):
        """將原始碼轉換為 Token"""
        tokens = []
        i = 0
        while i < len(source):
            ch = source[i]
            if ch.isspace():
                i += 1
                continue
            if ch.isdigit():
                j = i
                while j < len(source) and source[j].isdigit():
                    j += 1
                tokens.append(('NUMBER', int(source[i:j])))
                i = j
                continue
            if ch.isalpha() or ch == '_':
                j = i
                while j < len(source) and (source[j].isalnum() or source[j] == '_'):
                    j += 1
                word = source[i:j]
                keywords = {'print', 'let', 'if', 'else', 'while'}
                token_type = 'IDENT' if word not in keywords else word.upper()
                tokens.append((token_type, word))
                i = j
                continue
            if ch == '=':
                tokens.append(('ASSIGN', '='))
                i += 1
                continue
            if ch == '+':
                tokens.append(('PLUS', '+'))
                i += 1
                continue
            if ch == '-':
                tokens.append(('MINUS', '-'))
                i += 1
                continue
            if ch == '*':
                tokens.append(('MULT', '*'))
                i += 1
                continue
            if ch == '/':
                tokens.append(('DIV', '/'))
                i += 1
                continue
            if ch == '(':
                tokens.append(('LPAREN', '('))
                i += 1
                continue
            if ch == ')':
                tokens.append(('RPAREN', ')'))
                i += 1
                continue
            if ch == ';':
                tokens.append(('SEMI', ';'))
                i += 1
                continue
            raise SyntaxError(f"未知字元: {ch}")
        return tokens
    
    # ========== 語法分析 ==========
    def parse(self, tokens):
        """將 Tokens 轉換為 AST"""
        self.pos = 0
        self.tokens = tokens
        
        statements = []
        while self.peek():
            stmt = self.statement()
            statements.append(stmt)
        return {'type': 'program', 'body': statements}
    
    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    
    def consume(self):
        token = self.peek()
        self.pos += 1
        return token
    
    def statement(self):
        token = self.peek()
        if token and token[0] == 'LET':
            return self.var_decl()
        if token and token[0] == 'PRINT':
            return self.print_stmt()
        if token and token[0] == 'IDENT':
            return self.expr_stmt()
        return self.expr()
    
    def var_decl(self):
        self.consume()  # 'let'
        ident = self.consume()[1]
        self.consume()  # '='
        value = self.expr()
        self.consume()  # ';'
        return {'type': 'var_decl', 'name': ident, 'value': value}
    
    def print_stmt(self):
        self.consume()  # 'print'
        self.consume()  # '('
        expr = self.expr()
        self.consume()  # ')'
        self.consume()  # ';'
        return {'type': 'print', 'expr': expr}
    
    def expr_stmt(self):
        expr = self.expr()
        return expr
    
    def expr(self):
        return self.additive()
    
    def additive(self):
        result = self.multiplicative()
        while self.peek() and self.peek()[0] in ('PLUS', 'MINUS'):
            op = self.consume()[1]
            right = self.multiplicative()
            result = {'type': 'binary', 'op': op, 'left': result, 'right': right}
        return result
    
    def multiplicative(self):
        result = self.unary()
        while self.peek() and self.peek()[0] in ('MULT', 'DIV'):
            op = self.consume()[1]
            right = self.unary()
            result = {'type': 'binary', 'op': op, 'left': result, 'right': right}
        return result
    
    def unary(self):
        if self.peek() and self.peek()[0] == 'MINUS':
            self.consume()
            operand = self.unary()
            return {'type': 'unary', 'op': '-', 'operand': operand}
        return self.primary()
    
    def primary(self):
        token = self.peek()
        if token[0] == 'NUMBER':
            self.consume()
            return {'type': 'number', 'value': token[1]}
        if token[0] == 'IDENT':
            self.consume()
            return {'type': 'variable', 'name': token[1]}
        if token[0] == 'LPAREN':
            self.consume()
            result = self.expr()
            self.consume()  # ')'
            return result
        raise SyntaxError(f"語法錯誤: {token}")
    
    # ========== 執行 ==========
    def execute(self, node):
        if node['type'] == 'program':
            for stmt in node['body']:
                self.execute(stmt)
            return
        
        if node['type'] == 'var_decl':
            value = self.execute(node['value'])
            self.variables[node['name']] = value
            return
        
        if node['type'] == 'print':
            value = self.execute(node['expr'])
            print(value)
            return
        
        if node['type'] == 'number':
            return node['value']
        
        if node['type'] == 'variable':
            if node['name'] not in self.variables:
                raise NameError(f"變數未定義: {node['name']}")
            return self.variables[node['name']]
        
        if node['type'] == 'binary':
            left = self.execute(node['left'])
            right = self.execute(node['right'])
            op = node['op']
            if op == '+': return left + right
            if op == '-': return left - right
            if op == '*': return left * right
            if op == '/': return left // right
        
        if node['type'] == 'unary':
            operand = self.execute(node['operand'])
            if node['op'] == '-': return -operand
    
    # ========== 完整流程 ==========
    def run(self, source):
        print(f">>> {source}")
        tokens = self.lex(source)
        ast = self.parse(tokens)
        self.execute(ast)
        print()

# 測試
interp = Interpreter()
interp.run("let x = 10;")
interp.run("let y = 20;")
interp.run("print(x + y);")
interp.run("print(x * 2 - y);")
interp.run("let z = (x + y) * 2;")
interp.run("print(z);")
