# 3. 解譯器

## 3.1 解譯器架構

解譯器（Interpreter）直接執行高階語言程式，無需預先編譯為機器碼。讓我們用 Python 實作一個完整的解譯器：

[程式檔案：03-1-interpreter.py](../_code/03/03-1-interpreter.py)
```python
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
```

輸出：
```
>>> let x = 10;
>>> let y = 20;
>>> print(x + y);
30

>>> print(x * 2 - y);
0

>>> let z = (x + y) * 2;
>>> print(z);
60
```

## 3.2 Bytecode 與 VM

位元組碼是介於原始碼和機器碼之間的中間表示。讓我們實作一個簡單的位元組碼 VM：

[程式檔案：03-2-vm.py](../_code/03/03-2-vm.py)
```python
"""
基於堆疊的虛擬機（Stack-based VM）
"""

class VirtualMachine:
    def __init__(self):
        self.stack = []      # 運算堆疊
        self.variables = {}  # 變數表
    
    def run(self, bytecode):
        """執行位元組碼指令"""
        pc = 0  # 程式計數器
        while pc < len(bytecode):
            op = bytecode[pc]
            
            if op == 'LOAD_CONST':  # 載入常數
                self.stack.append(bytecode[pc + 1])
                pc += 2
            
            elif op == 'LOAD_VAR':  # 載入變數
                var_name = bytecode[pc + 1]
                self.stack.append(self.variables.get(var_name, 0))
                pc += 2
            
            elif op == 'STORE_VAR':  # 儲存變數
                var_name = bytecode[pc + 1]
                value = self.stack.pop()
                self.variables[var_name] = value
                pc += 2
            
            elif op == 'ADD':        # 加法
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)
                pc += 1
            
            elif op == 'SUB':        # 減法
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a - b)
                pc += 1
            
            elif op == 'MUL':        # 乘法
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a * b)
                pc += 1
            
            elif op == 'DIV':        # 除法
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a // b)
                pc += 1
            
            elif op == 'PRINT':       # 輸出
                value = self.stack.pop()
                print(value)
                pc += 1
            
            elif op == 'HALT':        # 結束
                break

# 範例：將高階程式編譯為位元組碼
# let a = 10;
// 等同於：
LOAD_CONST, 10
STORE_VAR, 'a'

# print(a + 5);
// 等同於：
LOAD_VAR, 'a'
LOAD_CONST, 5
ADD
PRINT

# 測試 VM
vm = VirtualMachine()
bytecode = [
    'LOAD_CONST', 10,
    'STORE_VAR', 'a',
    'LOAD_CONST', 20,
    'STORE_VAR', 'b',
    'LOAD_VAR', 'a',
    'LOAD_VAR', 'b',
    'ADD',
    'PRINT'
]
vm.run(bytecode)
# 輸出：30
```

## 3.3 垃圾回收（Garbage Collection）

讓我們實作几种垃圾回收演算法：

[程式檔案：03-3-gc.py](../_code/03/03-3-gc.py)
```python
"""
垃圾回收機制實作
"""

# 1. 引用計數（Reference Counting）
class RefCountObject:
    def __init__(self, value):
        self.value = value
        self.ref_count = 0
    
    def __repr__(self):
        return f"Object({self.value}, ref={self.ref_count})"

class RefCountGC:
    def __init__(self):
        self.objects = {}
        self.next_id = 0
    
    def create(self, value):
        obj_id = self.next_id
        self.next_id += 1
        obj = RefCountObject(value)
        self.objects[obj_id] = obj
        return obj_id
    
    def reference(self, obj_id):
        if obj_id in self.objects:
            self.objects[obj_id].ref_count += 1
        return obj_id
    
    def dereference(self, obj_id):
        if obj_id in self.objects:
            obj = self.objects[obj_id]
            obj.ref_count -= 1
            if obj.ref_count == 0:
                del self.objects[obj_id]
                print(f"回收記憶體: {obj}")
    
    def collect(self):
        """手動觸發回收"""
        to_delete = [k for k, v in self.objects.items() if v.ref_count == 0]
        for k in to_delete:
            obj = self.objects[k]
            del self.objects[k]
            print(f"GC 回收: {obj}")

# 測試引用計數
gc = RefCountGC()
a = gc.create("Object A")  # 建立物件
b = gc.create("Object B")
print(f"初始: {gc.objects}")

gc.reference(a)  # a 被 b 引用
gc.reference(b)  # b 被 a 引用（循環引用）
print(f"引用後: {gc.objects}")

# 解除外部引用
gc.dereference(a)  # 外部不再引用 a
gc.dereference(b)  # 外部不再引用 b
print(f"解除引用後: {gc.objects}")

# 注意：循環引用無法被引用計數回收！
# 需要其他 GC 演算法（如 Mark-Sweep）來處理

# 2. 標記-清除（Mark-Sweep）演算法
class MarkSweepGC:
    def __init__(self):
        self.heap = []  # 堆記憶體
        self.roots = set()  # 根集合（全域變數、堆疊）
    
    def allocate(self, size):
        """配置記憶體"""
        obj = {'id': len(self.heap), 'size': size, 'marked': False, 'data': None}
        self.heap.append(obj)
        return obj['id']
    
    def mark(self, obj_id):
        """標記階段：標記所有可達物件"""
        obj = self.heap[obj_id]
        if obj['marked']:
            return
        obj['marked'] = True
        # 這裡需要追蹤物件的指標，簡化版本略過
    
    def sweep(self):
        """清除階段：回收未標記的物件"""
        freed = []
        for obj in self.heap:
            if not obj['marked']:
                freed.append(obj['id'])
                # 實際會呼叫 free() 釋放記憶體
        self.heap = [obj for obj in self.heap if obj['marked']]
        return freed
    
    def collect(self):
        """執行完整 GC"""
        # 1. 標記
        for root in self.roots:
            self.mark(root)
        # 2. 清除
        freed = self.sweep()
        # 3. 取消標記（為下次準備）
        for obj in self.heap:
            obj['marked'] = False
        print(f"GC 完成，回收 {len(freed)} 個物件")

# 3. 複製（Copying）GC
class CopyGC:
    def __init__(self, from_space, to_space):
        self.from_space = from_space  # ['from', 'to']
        self.to_space = to_space
        self.current_space = from_space
    
    def copy(self, obj):
        """將存活物件複製到 To Space"""
        # 簡化版本：直接移動
        new_obj = obj.copy()
        self.to_space.append(new_obj)
        return new_obj
    
    def collect(self):
        """GC 觸發時，交換空間並複製存活物件"""
        old_space = self.current_space
        new_space = self.to_space if self.current_space == self.from_space else self.from_space
        
        new_space.clear()
        for obj in old_space:
            if obj['alive']:  # 假設有方法判斷是否存活
                self.copy(obj)
        
        self.current_space = new_space
        print(f"GC 完成，存活物件數: {len(new_space)}")

# 測試
gc = CopyGC(['from', 'to'])
gc.from_space = [
    {'id': 1, 'alive': True},
    {'id': 2, 'alive': False},
    {'id': 3, 'alive': True},
]
gc.collect()
print(f"To Space: {gc.to_space}")
```

## 3.4 例子：Python、JavaScript、Lua、LISP

### Python 位元組碼

[程式檔案：03-4-bytecode.py](../_code/03/03-4-bytecode.py)
```python
import dis

def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

# 查看 Python 的位元組碼
dis.dis(factorial)
```

輸出：
```
  2           0 LOAD_FAST                0 (n)
              2 LOAD_CONST               1 (1)
              4 COMPARE_OP               0 (<=)
              6 POP_JUMP_IF_FALSE       12

  3           8 LOAD_CONST               1 (1)
             10 RETURN_VALUE

  4          12 LOAD_FAST                0 (n)
             14 LOAD_GLOBAL              0 (factorial)
             16 LOAD_FAST                0 (n)
             18 LOAD_CONST               1 (1)
             20 BINARY_SUBTRACT
             22 CALL_FUNCTION            1
             24 BINARY_MULTIPLY
             26 RETURN_VALUE
```

### Lua VM

[程式檔案：03-5-fib.lua](../_code/03/03-5-fib.lua)
```lua
-- Lua 範例
function fib(n)
    if n <= 1 then return n end
    return fib(n - 1) + fib(n - 2)
end

print(fib(10))  -- 輸出 55
```

Lua 使用基於暫存器的 VM，效率比基於堆疊的 VM 更高。

### JavaScript V8 引擎

V8 是 Chrome 和 Node.js 使用的 JavaScript 引擎，採用 JIT 編譯：
- Ignition：直譯器，產生位元組碼
- TurboFan：最佳化編譯器，將熱點程式碼編譯為機器碼

### LISP 評価器

[程式檔案：03-6-lisp.py](../_code/03/03-6-lisp.py)
```python
"""簡化的 LISP 直譯器"""

def eval_expr(expr, env):
    if isinstance(expr, str):  # 符號
        return env.get(expr, expr)
    if isinstance(expr, (int, float)):  # 數字
        return expr
    
    # 表達式 (op args...)
    op = expr[0]
    args = expr[1:]
    
    if op == 'quote':
        return args[0]
    
    if op == 'if':
        condition = eval_expr(args[0], env)
        if condition:
            return eval_expr(args[1], env)
        return eval_expr(args[2], env) if len(args) > 2 else None
    
    if op == 'define':
        env[args[0]] = eval_expr(args[1], env)
        return None
    
    if op == 'lambda':
        return {'type': 'function', 'params': args[0], 'body': args[1], 'env': env.copy()}
    
    # 函數呼叫
    func = eval_expr(op, env)
    if isinstance(func, dict) and func['type'] == 'function':
        new_env = func['env'].copy()
        for param, arg in zip(func['params'], args):
            new_env[param] = eval_expr(arg, env)
        return eval_expr(func['body'], new_env)
    
    # 內建函數
    evaled_args = [eval_expr(arg, env) for arg in args]
    if op == '+': return sum(evaled_args)
    if op == '-': return evaled_args[0] - sum(evaled_args[1:])
    if op == '*': return eval_expr(args[0], env) * eval_expr(args[1], env)
    if op == '=': return evaled_args[0] == evaled_args[1]
    if op == 'car': return evaled_args[0][0]
    if op == 'cdr': return evaled_args[0][1:]
    if op == 'cons': return [evaled_args[0]] + evaled_args[1]

# 測試
env = {}
print(eval_expr(['+', 2, 3], env))  # 5
print(eval_expr(['if', ['=', 1, 1], 'yes', 'no'], env))  # yes
print(eval_expr(['define', 'x', 10], env))
print(eval_expr('x', env))  # 10

# 遞迴範例：階乘
factorial = ['define', 'fact', ['lambda', ['n'],
    ['if', ['=', 'n', 1], 1, ['*', 'n', ['fact', ['-', 'n', 1]]]]]]
eval_expr(factorial, env)
print(eval_expr(['fact', 5], env))  # 120
```

這個 LISP 直譯器展示了函數式語言的核心概念：程式即資料、遞迴、高階函數。