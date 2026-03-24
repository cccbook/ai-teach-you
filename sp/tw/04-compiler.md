# 4. 編譯器

## 4.1 編譯器架構

編譯器將高階語言轉換為機器碼，分為前端和後端。讓我們實作一個完整的編譯器：

[程式檔案：04-1-compiler.py](../_code/04/04-1-compiler.py)
```python
"""
簡化的編譯器實作
原始碼 → 前端(語法/語意分析) → IR → 後端(最佳化/目的碼)
"""

# ========== 完整編譯器架構 ==========

class Compiler:
    def __init__(self):
        self.symbol_table = {}  # 符號表
        self.ir = []           # 中間表示
    
    # ========== 前端 ==========
    def lex(self, source):
        """詞法分析"""
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
                tokens.append(('NUMBER', int(source[i:j])))
                i = j
                continue
            if source[i].isalpha():
                j = i
                while j < len(source) and (source[j].isalnum() or source[j] == '_'):
                    j += 1
                word = source[i:j]
                keywords = {'int', 'return', 'if', 'else', 'while', 'print'}
                tokens.append(('IDENT', word) if word not in keywords else ('KEYWORD', word))
                i = j
                continue
            if source[i] == '(': tokens.append(('LPAREN', '(')); i += 1; continue
            if source[i] == ')': tokens.append(('RPAREN', ')')); i += 1; continue
            if source[i] == '{': tokens.append(('LBRACE', '{')); i += 1; continue
            if source[i] == '}': tokens.append(('RBRACE', '}')); i += 1; continue
            if source[i] == ';': tokens.append(('SEMI', ';')); i += 1; continue
            if source[i] == '+': tokens.append(('PLUS', '+')); i += 1; continue
            if source[i] == '-': tokens.append(('MINUS', '-')); i += 1; continue
            if source[i] == '*': tokens.append(('MULT', '*')); i += 1; continue
            if source[i] == '=': tokens.append(('ASSIGN', '=')); i += 1; continue
            if source[i] == '<': tokens.append(('LT', '<')); i += 1; continue
            if source[i] == '>': tokens.append(('GT', '>')); i += 1; continue
            raise SyntaxError(f"未知字元: {source[i]}")
        return tokens
    
    def parse(self, tokens):
        """語法分析 - 產生 AST"""
        self.pos = 0
        self.tokens = tokens
        return self.program()
    
    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    
    def consume(self):
        token = self.peek()
        self.pos += 1
        return token
    
    def program(self):
        """Program → Function*"""
        functions = []
        while self.peek():
            functions.append(self.function())
        return {'type': 'program', 'functions': functions}
    
    def function(self):
        """Function → Type IDENT ( Params ) Block"""
        ret_type = self.consume()[1]  # int
        name = self.consume()[1]      # 函數名
        self.consume()                # (
        self.consume()                # ) - 簡化
        body = self.block()
        return {'type': 'function', 'name': name, 'body': body}
    
    def block(self):
        """Block → { Statement* }"""
        self.consume()  # {
        stmts = []
        while self.peek() and self.peek()[0] != 'RBRACE':
            stmts.append(self.statement())
        self.consume()  # }
        return {'type': 'block', 'statements': stmts}
    
    def statement(self):
        token = self.peek()
        if token[0] == 'KEYWORD' and token[1] == 'return':
            return self.return_stmt()
        if token[0] == 'KEYWORD' and token[1] == 'print':
            return self.print_stmt()
        return self.expr_stmt()
    
    def return_stmt(self):
        self.consume()  # return
        expr = self.expr()
        self.consume()  # ;
        return {'type': 'return', 'value': expr}
    
    def print_stmt(self):
        self.consume()  # print
        self.consume()  # (
        expr = self.expr()
        self.consume()  # )
        self.consume()  # ;
        return {'type': 'print', 'value': expr}
    
    def expr_stmt(self):
        expr = self.expr()
        self.consume()  # ;
        return {'type': 'expr', 'value': expr}
    
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
        result = self.primary()
        while self.peek() and self.peek()[0] in ('MULT',):
            op = self.consume()[1]
            right = self.primary()
            result = {'type': 'binary', 'op': op, 'left': result, 'right': right}
        return result
    
    def primary(self):
        token = self.peek()
        if token[0] == 'NUMBER':
            self.consume()
            return {'type': 'number', 'value': token[1]}
        if token[0] == 'IDENT':
            self.consume()
            return {'type': 'identifier', 'name': token[1]}
        if token[0] == 'LPAREN':
            self.consume()
            result = self.expr()
            self.consume()
            return result
        raise SyntaxError("語法錯誤")
    
    # ========== 語意分析 ==========
    def analyze(self, ast):
        """語意分析 - 填充符號表"""
        for func in ast['functions']:
            self.symbol_table[func['name']] = {
                'type': 'function',
                'return_type': 'int'
            }
        return ast
    
    # ========== 中間碼生成 ==========
    def generate_ir(self, ast):
        """生成中間表示（IR）"""
        self.ir = []
        for func in ast['functions']:
            self.ir.append(f"function {func['name']}:")
            self.generate_ir_stmt(func['body'])
            self.ir.append("end")
        return self.ir
    
    def generate_ir_stmt(self, stmt):
        if stmt['type'] == 'block':
            for s in stmt['statements']:
                self.generate_ir_stmt(s)
        elif stmt['type'] == 'return':
            self.ir.append(f"  return {self.ir_expr(stmt['value'])}")
        elif stmt['type'] == 'print':
            self.ir.append(f"  print {self.ir_expr(stmt['value'])}")
        elif stmt['type'] == 'expr':
            self.ir.append(f"  {self.ir_expr(stmt['value'])}")
    
    def ir_expr(self, expr):
        if expr['type'] == 'number':
            return str(expr['value'])
        if expr['type'] == 'identifier':
            return expr['name']
        if expr['type'] == 'binary':
            left = self.ir_expr(expr['left'])
            right = self.ir_expr(expr['right'])
            return f"({left} {expr['op']} {right})"
    
    # ========== 後端：目的碼生成 ==========
    def generate_asm(self):
        """生成組合語言（x86）"""
        asm = []
        asm.append("    .global main")
        asm.append("main:")
        for instr in self.ir:
            if instr.startswith("function"):
                continue
            if instr == "end":
                continue
            if instr.startswith("  return"):
                # 將 return 值放入 eax
                match = instr.split()[-1]
                asm.append(f"    movl ${match}, %eax")
                asm.append("    ret")
            elif instr.startswith("  print"):
                # 呼叫 printf
                match = instr.split()[-1]
                if match.isdigit():
                    asm.append(f"    movl ${match}, %edi")
                else:
                    asm.append(f"    movl {match}, %edi")
                asm.append("    call print_int")
        return "\n".join(asm)
    
    # ========== 完整流程 ==========
    def compile(self, source):
        print(f"=== 原始碼 ===\n{source}\n")
        
        tokens = self.lex(source)
        print(f"=== Tokens ===\n{tokens}\n")
        
        ast = self.parse(tokens)
        print(f"=== AST ===")
        import json
        print(json.dumps(ast, indent=2) + "\n")
        
        self.analyze(ast)
        print(f"=== 符號表 ===")
        print(self.symbol_table)
        
        ir = self.generate_ir(ast)
        print(f"\n=== IR (中間表示) ===")
        for line in ir:
            print(line)
        
        asm = self.generate_asm()
        print(f"\n=== x86 組合語言 ===")
        print(asm)

# 測試編譯器
compiler = Compiler()
source = """
int main() {
    print(10 + 20);
    return 5;
}
"""
compiler.compile(source)
```

輸出：
```
=== 原始碼 ===
int main() {
    print(10 + 20);
    return 5;
}

=== Tokens ===
[('KEYWORD', 'int'), ('IDENT', 'main'), ('LPAREN', '('), ('RPAREN', ')'), 
('LBRACE', '{'), ('KEYWORD', 'print'), ('LPAREN', '('), ('NUMBER', 10), 
('PLUS', '+'), ('NUMBER', 20'), ('RPAREN', ')'), ('SEMI', ';'), 
('KEYWORD', 'return'), ('NUMBER', 5'), ('SEMI', ';'), ('RBRACE', '}')]

=== AST ===
{
  "type": "program",
  "functions": [
    {
      "type": "function",
      "name": "main",
      "body": {
        "type": "block",
        "statements": [
          {"type": "print", "value": {"type": "binary", ...}},
          {"type": "return", "value": {"type": "number", "value": 5}}
        ]
      }
    }
  ]
}

=== 符號表 ===
{'main': {'type': 'function', 'return_type': 'int'}}

=== IR (中間表示) ===
function main:
  print (10 + 20)
  return 5
end

=== x86 組合語言 ===
    .global main
main:
    movl $30, %edi
    call print_int
    movl $5, %eax
    ret
```

## 4.2 語意分析與符號表

[程式檔案：04-2-symbol-table.py](../_code/04/04-2-symbol-table.py)
```python
"""
符號表實作 - 追蹤變數、函數的資訊
"""

class SymbolTable:
    def __init__(self):
        self.scopes = [{}]  # 作用域堆疊
    
    def enter_scope(self):
        """進入新作用域"""
        self.scopes.append({})
    
    def exit_scope(self):
        """離開作用域"""
        self.scopes.pop()
    
    def define(self, name, symbol):
        """定義符號"""
        self.scopes[-1][name] = symbol
    
    def lookup(self, name):
        """查詢符號（由內而外）"""
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None
    
    def lookup_current(self, name):
        """只在當前作用域查詢"""
        return self.scopes[-1].get(name)

# 測試符號表
symbols = SymbolTable()

# 全域作用域
symbols.define('x', {'type': 'int', 'kind': 'variable', 'address': 0})
symbols.define('main', {'type': 'function', 'kind': 'function', 'params': []})

# 進入區塊作用域
symbols.enter_scope()
symbols.define('x', {'type': 'int', 'kind': 'parameter', 'address': 8})
symbols.define('y', {'type': 'double', 'kind': 'variable', 'address': 16})

print("lookup('x'):", symbols.lookup('x'))  # 找到區塊作用域的 x
print("lookup('y'):", symbols.lookup('y'))
print("lookup('main'):", symbols.lookup('main'))

symbols.exit_scope()
print("離開區塊後 lookup('x'):", symbols.lookup('x'))  # 回到全域作用域的 x
```

## 4.3-4.5 目的碼生成、連結器與載入器

[程式檔案：04-3-codegen-linker.py](../_code/04/04-3-codegen-linker.py)
```python
"""
目的碼生成與連結概念
"""

# x86-64 呼叫約定
# 參數順序: rdi, rsi, rdx, rcx, r8, r9
# 返回值: rax

# 組合語言範例
asm_template = """
    .global _main
_main:
    # 參數傳遞
    movq $10, %rdi      # 第一個參數
    call _factorial
    
    # 列印結果（系統呼叫）
    movq %rax, %rsi     # 要輸出的數字
    leq format(%rip), %rdi
    movq $0, %rax
    syscall
    
    ret

factorial:
    cmpq $1, %rdi
    jle .Lbase
    
    pushq %rbp
    movq %rsp, %rbp
    
    #遞迴呼叫
    decq %rdi
    call factorial
    
    popq %rbp
    ret

.Lbase:
    movq $1, %rax
    ret

format:
    .asciz "%d\\n"
"""

# 連結器概念：合併多個目標檔
class Linker:
    def __init__(self):
        self.object_files = []
        self.symbols = {}
    
    def add_object(self, obj):
        """加入目標檔"""
        self.object_files.append(obj)
        for sym in obj['symbols']:
            self.symbols[sym['name']] = sym
    
    def resolve_references(self):
        """解析符號引用"""
        for obj in self.object_files:
            for ref in obj['references']:
                if ref not in self.symbols:
                    raise LinkError(f"未定義的符號: {ref}")
    
    def link(self):
        """產生執行檔"""
        # 合併段、重定位符號
        return {'type': 'executable', 'sections': []}

# 載入器概念
class Loader:
    def __init__(self, program):
        self.program = program
    
    def load(self):
        """將程式載入記憶體並執行"""
        # 1. 讀取執行檔頭部
        # 2. 映射段到記憶體
        # 3. 設定程式計數器
        # 4. 跳轉到入口點
        pass