# 4. 編譯器

## 4.1 編譯器架構

### 4.1.1 編譯器的基本概念

編譯器（Compiler）是將高階語言寫成的原始碼翻譯為機器語言或低階語言的系統軟體。

**編譯器的核心任務**

1. **忠實性**：產生的目標程式必須與原始碼語意一致
2. **效率**：目標程式的執行效率應盡可能高
3. **可讀性**：編譯過程中的錯誤訊息應清晰準確

**翻譯 vs 解釋**

```
編譯：原始碼 ──→ 目的碼 ──→ 執行
        [編譯器]     [CPU]

解釋：原始碼 ──→ 直譯執行
        [解譯器]
```

### 4.1.2 編譯器的組織結構

現代編譯器通常採用前端-後端分離的架構：

```
┌─────────────────────────────────────────────────────────────────┐
│                          原始碼                                   │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                        編譯器前端                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │  詞法分析   │→ │  語法分析   │→ │  語意分析   │            │
│  │   (Lexer)   │  │  (Parser)   │  │  (Analyze)  │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
│         │                │                │                      │
│         ▼                ▼                ▼                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    中間表示 (IR)                          │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                        編譯器後端                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   最佳化    │→ │  目的碼     │→ │   連結      │            │
│  │ (Optimize)  │  │  (Codegen) │  │  (Link)    │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                        目的碼 / 執行檔                            │
└─────────────────────────────────────────────────────────────────┘
```

**前端的職責**

- 語言相關：只與特定語言相關
- 產生 IR：將原始碼轉換為與語言無關的中間表示

**後端的職責**

- 硬體相關：只與特定目標架構相關
- 處理 IR：最佳化並產生目標碼

### 4.1.3 編譯器前端的理論

**詞法分析器（Scanner）**

詞法分析器負責將字元流轉換為 Token 序列：

```
"int x = 42;"
          │
          ▼ [詞法分析]
          │
[(INT, "int"), (IDENT, "x"), (ASSIGN, "="), (NUM, 42), (SEMI, ";")]
```

**語法分析器（Parser）**

語法分析器將 Token 序列組織為語法樹：

```
                        宣告
                       /    \
                   類型      賦值
                   "int"   /    \
                         識別字  常數
                          "x"   42
```

**語意分析器**

語意分析負責：
- 類型檢查
- 作用域解析
- 常數折疊
- 雜湊檢查

### 4.1.4 符號表管理

符號表是編譯器維護的核心資料結構，用於儲存識別字的資訊。

**符號表的內容**

| 屬性 | 說明 |
|------|------|
| 名稱 | 識別字的名字 |
| 類型 | int, float, array, function 等 |
| 作用域 | 定義所在的作用域 |
| 記憶體位置 | 堆疊偏移或全域位址 |
| 參數列表 | 函數參數（針對函數） |
| 其他屬性 | const、static 等修飾符 |

**作用域與符號表**

```python
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
```

### 4.1.5 完整編譯器實作

讓我們實作一個簡化的編譯器，展示完整流程：

```python
"""
簡化的編譯器實作
原始碼 → 前端(語法/語意分析) → IR → 後端(最佳化/目的碼)
"""

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
        """語法分析"""
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
        ret_type = self.consume()[1]
        name = self.consume()[1]
        self.consume()  # (
        self.consume()  # ) - 簡化
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
        """語意分析"""
        for func in ast['functions']:
            self.symbol_table[func['name']] = {
                'type': 'function',
                'return_type': 'int'
            }
        return ast
    
    # ========== 中間碼生成 ==========
    def generate_ir(self, ast):
        """生成中間表示"""
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
        """生成組合語言"""
        asm = []
        asm.append("    .global main")
        asm.append("main:")
        for instr in self.ir:
            if instr.startswith("function"):
                continue
            if instr == "end":
                continue
            if instr.startswith("  return"):
                match = instr.split()[-1]
                asm.append(f"    movl ${match}, %eax")
                asm.append("    ret")
            elif instr.startswith("  print"):
                match = instr.split()[-1]
                if match.isdigit():
                    asm.append(f"    movl ${match}, %edi")
                else:
                    asm.append(f"    movl {match}, %edi")
                asm.append("    call print_int")
        return "\n".join(asm)
    
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

## 4.2 語意分析與符號表

### 4.2.1 語意分析的職責

語意分析位於語法分析之後，負責檢查程式在語法正確之外是否具有語意有效性。

**語意分析的任務**

| 任務 | 說明 | 範例 |
|------|------|------|
| 類型檢查 | 確保運算類型相容 | `int x = "hello";` |
| 作用域解析 | 識別字使用前已宣告 | `y = 5;`（y 未宣告）|
| 唯一性檢查 | 同作用域無重複宣告 | `int x, x;` |
| 常數折疊 | 編譯期計算常數表達式 | `int x = 2 * 3;` → `int x = 6;` |
| 雜湊檢查 | 呼叫者與定義匹配 | `foo(a, b)` 但 `foo(x)` |

### 4.2.2 類型系統理論

**靜態 vs 動態類型**

| 特性 | 靜態類型 | 動態類型 |
|------|----------|----------|
| 類型檢查時機 | 編譯時 | 執行時 |
| 執行速度 | 較快 | 較慢 |
| 錯誤時機 | 早期 | 晚期 |
| 範例 | C, C++, Java | Python, JavaScript |

**強類型 vs 弱類型**

| 特性 | 強類型 | 弱類型 |
|------|--------|--------|
| 隱式轉換 | 禁止或嚴格限制 | 允許較多 |
| 類型安全 | 較高 | 較低 |
| 範例 | Java, Haskell | C, JavaScript |

### 4.2.3 符號表的實現

符號表需要支援：
- 插入（Insert）
- 查詢（Lookup）
- 作用域管理

```python
class SymbolTable:
    """符號表實作"""
    
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

## 4.3 中間碼生成

### 4.3.1 中間表示（IR）的類型

IR 是編譯器內部的程式表示，介於原始碼和目的碼之間。

**IR 的特性**

1. **與語言無關**：適用於多種原始語言
2. **與硬體無關**：適用於多種目標架構
3. **易於最佳化**：便於進行各種轉換

**常見的 IR 形式**

| 形式 | 說明 | 範例 |
|------|------|------|
| 三地址碼（TAC） | 每條指令最多三個運算元 | `t1 = a + b` |
| 靜態單一形式（SSA） | 每個變數只被賦值一次 | `t1 = a + b` |
| 控制流程圖（CFG） | 基本區塊 + 跳轉邊 | 圖結構 |

### 4.3.2 三地址碼（TAC）

三地址碼是最廣泛使用的 IR 形式。

**TAC 的特點**

- 每條指令最多包含：一個運算和三個運算元
- 形式：`x = y op z` 或 `x = op y`
- 臨時變數用於儲存中間結果

**TAC 範例**

原始碼：
```c
a = b + c * d;
```

TAC：
```
t1 = c * d
a = b + t1
```

### 4.3.3 控制流程圖（CFG）

CFG 將程式劃分為基本區塊，並記錄跳轉關係。

**基本區塊（Basic Block）**

基本區塊是滿足以下條件的最大連續指令序列：
1. 指令按序執行，無跳轉進入（除入口外）
2. 無跳轉離開（除末尾外）

**CFG 的構建**

```
入口 → B1 → B2 → B3 → 出口
            ↓
            B4 → B5
```

## 4.4 目的碼生成

### 4.4.1 目的碼生成的考量

目的碼生成將 IR 轉換為特定硬體的機器碼或組合語言。

**生成的考量因素**

| 因素 | 說明 |
|------|------|
| 指令選擇 | 選擇合適的目標指令 |
| 暫存器配置 | 有效利用有限暫存器 |
| 指令排程 | 最小化延遲 |
| 呼叫約定 | 遵守 ABI 規範 |

### 4.4.2 x86-64 呼叫約定

x86-64 System V ABI 的呼叫約定：

**參數傳遞順序**

```
%rdi, %rsi, %rdx, %rcx, %r8, %r9
```

**返回值**

```
整數/指標：%rax
浮點數：%xmm0
```

**被呼叫者保存**

```
%rbx, %rbp, %r12, %r13, %r14, %r15
```

### 4.4.3 目的碼範例

組合語言範例：
```asm
    .global _main
_main:
    # 參數傳遞
    movq $10, %rdi      # 第一個參數
    call _factorial
    
    # 列印結果
    movq %rax, %rsi
    leaq format(%rip), %rdi
    movq $0, %rax
    syscall
    
    ret

factorial:
    cmpq $1, %rdi
    jle .Lbase
    
    pushq %rbp
    movq %rsp, %rbp
    
    decq %rdi
    call factorial
    
    popq %rbp
    ret

.Lbase:
    movq $1, %rax
    ret

format:
    .asciz "%d\n"
```

## 4.5 連結器與載入器

### 4.5.1 連結器的角色

連結器（Linker）將多個目的檔合併為單一執行檔。

**連結的類型**

| 類型 | 說明 |
|------|------|
| 靜態連結 | 編譯時完成所有符號解析 |
| 動態連結 | 執行時動態載入共享庫 |

**連結的步驟**

1. **符號解析**：將符號引用與定義匹配
2. **重定位**：調整位址參照
3. **段合併**：合併相同類型的段

### 4.5.2 連結器實作概念

```python
class Linker:
    def __init__(self):
        self.object_files = []
        self.symbols = {}
    
    def add_object(self, obj):
        """加入目的檔"""
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
        return {'type': 'executable', 'sections': []}
```

### 4.5.3 載入器

載入器（Loader）負責將執行檔載入記憶體並開始執行。

**載入過程**

1. 讀取執行檔頭部
2. 映射段到記憶體
3. 設定程式計數器
4. 跳轉到入口點

```python
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
```
