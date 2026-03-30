# 3. 解譯器

## 3.1 解譯器架構

### 3.1.1 解譯器的基本概念

解譯器（Interpreter）是一種直接執行高階語言程式的系統軟體。與編譯器不同，解譯器不需要預先將程式翻譯為機器碼，而是逐句讀取原始碼並立即執行。

**解譯器 vs 編譯器**

| 特性 | 解譯器 | 編譯器 |
|------|--------|--------|
| 執行方式 | 逐句直接執行 | 先翻譯後執行 |
| 輸出 | 執行結果 | 目的碼檔案 |
| 執行速度 | 較慢（重複翻譯） | 較快 |
| 跨平台性 | 較好 | 需重新編譯 |
| 互動性 | 較好 | 較差 |
| 錯誤報告 | 即時 | 需重新編譯 |

**解譯器的優勢**

1. **快速開發迭代**：不需要編譯-執行迴圈
2. **良好的錯誤報告**：可直接指出錯誤位置
3. **動態特性**：eval()、反射、動態型別
4. **平台無關性**：同一解譯器可在多平台執行

### 3.1.2 解譯器架構模型

現代解譯器的典型架構可分為幾個層次：

```
┌─────────────────────────────────────────────────────────────┐
│                    使用者程式                                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    解譯器引擎                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   詞法分析  │→ │  語法分析   │→ │  AST 執行   │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    執行環境                                 │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐     │
│  │ 符號表  │  │ 堆疊   │  │ 記憶體  │  │ 內建函數│     │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    作業系統 / 硬體                          │
└─────────────────────────────────────────────────────────────┘
```

### 3.1.3 直譯 vs 位元組碼直譯

**純直譯（Pure Interpretation）**

直接執行 AST 或原始的 Token 流：

```
原始碼 → 詞法分析 → 語法分析 → AST → 直譯執行
```

**位元組碼直譯（Bytecode Interpretation）**

先編譯為中間表示（位元組碼），再用 VM 解譯執行：

```
原始碼 → 詞法分析 → 語法分析 → AST → 位元組碼 → VM 直譯執行
```

**兩種方式的比較**

| 特性 | 純直譯 | 位元組碼直譯 |
|------|--------|--------------|
| 執行速度 | 最慢 | 較快 |
| 記憶體效率 | 需保留 AST | 位元組碼更緊湊 |
| 跨平台性 | 最佳 | 需 VM 實作 |
| 實作複雜度 | 簡單 | 中等 |
| JIT 相容性 | 困難 | 容易 |

### 3.1.4 環境與符號表

解譯器需要維護執行環境來追蹤變數、函數和作用域。

**符號表（Symbol Table）**

符號表是儲存所有識別字資訊的資料結構：

| 欄位 | 說明 |
|------|------|
| 名稱 | 識別字的名字 |
| 類型 | 變數型別、函數返回型別 |
| 作用域 | 定義所在的作用域 |
| 位置 | 記憶體位址或堆疊偏移 |
| 屬性 | 常數、參數、區域變數等 |

**作用域管理**

作用域（Scope）決定了識別字的可見性：

```python
x = 10                    # 全域作用域

def outer():
    y = 20                # outer 的作用域
    def inner():
        z = 30            # inner 的作用域
        print(x, y, z)   # 可見 x, y, z
    inner()
    # print(z)           # 錯誤：z 不可見
```

**作用域實現策略**

1. **詞法作用域（Lexical Scope）**：根據原始碼結構靜態決定
2. **動態作用域（Dynamic Scope）**：根據呼叫堆疊動態決定

### 3.1.5 解譯器實作

讓我們實作一個完整的解譯器：

```python
"""
簡單解譯器架構
原始碼 → 詞法分析 → 語法分析 → AST → 執行
"""

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

## 3.2 Bytecode 與 VM

### 3.2.1 虛擬機的理論基礎

虛擬機（Virtual Machine, VM）是軟體模擬的計算機，提供指令集和執行環境。

**虛擬機的分類**

| 類型 | 特點 | 代表 |
|------|------|------|
| 系統虛擬機 | 模擬完整硬體，可執行 OS | VMware, VirtualBox, QEMU |
| 程式虛擬機 | 執行單一應用程式 | JVM, .NET CLR, Python VM |

本書主要討論**程式虛擬機**。

**虛擬機的優勢**

1. **跨平台性**：同一 VM 可在多種硬體上執行
2. **安全性**：隔離執行環境，防止惡意程式
3. **可攜性**：一次編譯，到處執行
4. **可驗證性**：位元組碼可在執行前驗證

### 3.2.2 基於堆疊的虛擬機（Stack-based VM）

堆疊式 VM 使用運算元堆疊（Operand Stack）進行運算，是最常見的 VM 設計。

**堆疊式 VM 的特性**

| 特性 | 說明 |
|------|------|
| 隱含運算元位置 | 運算元從堆疊彈出，結果推回堆疊 |
| 指令緊湊 | 指令無需指定暫存器或記憶體位置 |
| 簡單實作 | 堆疊操作易於理解和最佳化 |
| 執行速度 | 需頻繁記憶體訪問（堆疊存取） |

**JVM 是典型的堆疊式 VM**

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

### 3.2.3 基於暫存器的虛擬機（Register-based VM）

暫存器式 VM 使用虛擬暫存器集合儲存運算元。

**暫存器式 VM 的特性**

| 特性 | 說明 |
|------|------|
| 明確運算元位置 | 指令指定來源和目的暫存器 |
| 較少指令 | 減少指令數量 |
| 較快執行 | 減少堆疊存取次數 |
| 實作複雜 | 需管理暫存器分配 |

**Lua VM 是著名的暫存器式 VM**

Lua 5.0 從堆疊式改為暫存器式，效能提升顯著。

```python
# 基於暫存器的 VM 與堆疊式 VM 的比較
print("=== 基於堆疊 VM ===")
# 計算 1 + 2:
stack_bytecode = [
    'iconst', 1,    # 推入 1
    'iconst', 2,    # 推入 2
    'iadd',         # 彈出並相加，結果推回
    'print',        # 輸出
    'halt'
]

print("\n=== 基於暫存器 VM ===")
# 計算 1 + 2:
register_bytecode = [
    'LOADK', 0, 1,     # R0 = 1
    'LOADK', 1, 2,     # R1 = 2
    'ADD', 2, 0, 1,    # R2 = R0 + R1
    'PRINT', 2,        # 輸出 R2
    'HALT'
]
```

### 3.2.4 位元組碼設計原則

設計位元組碼指令集時需考慮：

**指令格式**

| 格式 | 位元組數 | 說明 |
|------|----------|------|
| 零位址 | 1 | 所有運算元隱含（如堆疊 VM） |
| 一位址 | 2 | 一個運算元 |
| 二位址 | 3 | 兩個運算元 |
| 三位址 | 4+ | 三個運算元 |

**指令分類**

| 類別 | 指令範例 |
|------|----------|
| 載入/儲存 | LOAD, STORE, PUSH, POP |
| 算術運算 | ADD, SUB, MUL, DIV |
| 邏輯運算 | AND, OR, NOT, XOR |
| 比較跳轉 | CMP, JMP, JE, JNE |
| 函數呼叫 | CALL, RET, ENTER, LEAVE |
| 物件操作 | NEW, GETFIELD, PUTFIELD |

## 3.3 垃圾回收（Garbage Collection）

### 3.3.1 記憶體管理的基本概念

手動記憶體管理容易出錯，現代程式語言傾向使用自動記憶體管理。

**手動管理的問題**

1. **遺漏釋放**：忘記釋放記憶體 → 記憶體洩漏
2. **重複釋放**：釋放已釋放的記憶體 → 懸垂指標
3. **使用未釋放記憶體**：使用已釋放的記憶體 → 未定義行為

**自動記憶體管理的目標**

1. **自動化**：程式設計師無需關心記憶體釋放
2. **安全性**：杜絕懸垂指標和記憶體洩漏
3. **效率**：最小化 GC 帶來的性能影響

### 3.3.2 引用計數（Reference Counting）

引用計數是最直接的 GC 方法。

**基本原理**

每個物件維護一個引用計數器：
- 建立物件時，計數 = 1
- 有新參照時，計數 +1
- 參照失效時，計數 -1
- 計數 = 0 時，回收記憶體

```python
# 引用計數 GC 實作
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
```

**引用計數的優缺點**

| 優點 | 缺點 |
|------|------|
| 簡單直觀 | 無法處理循環引用 |
| 記憶體即時釋放 | 計數更新開銷大 |
| 增量式、無停顿 | 無法處理分散式場景 |

Python 使用引用計數作為主要記憶體管理，但需配合標記-清除處理循環引用。

### 3.3.3 標記-清除（Mark and Sweep）

標記-清除是一種追蹤式（Tracing）GC 方法。

**演算法步驟**

```
Phase 1: 標記（Mark）
  - 從根集合開始，標記所有可達物件
  
Phase 2: 清除（Sweep）
  - 遍歷整個堆，回收未標記的物件
```

**根集合（Root Set）**

根集合包括：
- 全域變數
- 呼叫堆疊上的參照
- 暫存器內容

```python
# 標記-清除 GC 實作
class MarkSweepGC:
    def __init__(self):
        self.heap = []  # 堆記憶體
        self.roots = set()  # 根集合
    
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
        # 遞迴標記可達物件
    
    def sweep(self):
        """清除階段：回收未標記的物件"""
        freed = []
        for obj in self.heap:
            if not obj['marked']:
                freed.append(obj['id'])
        self.heap = [obj for obj in self.heap if obj['marked']]
        return freed
    
    def collect(self):
        """執行完整 GC"""
        # 1. 標記
        for root in self.roots:
            self.mark(root)
        # 2. 清除
        freed = self.sweep()
        # 3. 取消標記
        for obj in self.heap:
            obj['marked'] = False
        print(f"GC 完成，回收 {len(freed)} 個物件")
```

**標記-清除的問題**

| 問題 | 說明 |
|------|------|
| 記憶體碎片化 | 回收後產生不連續空間 |
| STW 暫停 | GC 期間需停止程式執行 |
| 標記耗時 | 需遍歷所有可達物件 |

### 3.3.4 複製（Copying）GC

複製式 GC 將堆記憶體分為兩半，只使用一半。

**原理**

```
┌─────────────────┬─────────────────┐
│    From Space   │    To Space     │
│   (使用中)      │   (空閒)        │
└─────────────────┴─────────────────┘

GC 時：
1. 將 From Space 的存活物件複製到 To Space
2. 交換 From/To Space
```

```python
# 複製 GC 實作
class CopyGC:
    def __init__(self, from_space, to_space):
        self.from_space = from_space
        self.to_space = to_space
        self.current_space = from_space
    
    def copy(self, obj):
        """將存活物件複製到 To Space"""
        new_obj = obj.copy()
        self.to_space.append(new_obj)
        return new_obj
    
    def collect(self):
        """GC 觸發時，交換空間並複製存活物件"""
        old_space = self.current_space
        new_space = self.to_space if self.current_space == self.from_space else self.from_space
        
        new_space.clear()
        for obj in old_space:
            if obj['alive']:
                self.copy(obj)
        
        self.current_space = new_space
        print(f"GC 完成，存活物件數: {len(new_space)}")
```

**複製 GC 的優缺點**

| 優點 | 缺點 |
|------|------|
| 無記憶體碎片 | 只使用一半堆空間 |
| 標記+複製一次完成 | 存活率高時效率低 |
| 無需清除階段 | 需複製所有存活物件 |

### 3.3.5 標記-壓縮（Mark-Compact）

標記-壓縮結合標記-清除和複製的優點。

**三階段演算法**

```
Phase 1: 標記（Mark）
  - 同標記-清除，找出所有存活物件

Phase 2: 計算新位置（Compute Locations）
  - 計算物件壓縮後的新位置

Phase 3: 壓縮（Compact）
  - 將所有存活物件移動到連續區域
```

**優點**

- 消除記憶體碎片
- 完整使用堆空間

**缺點**

- 需要多次堆遍歷
- 壓縮階段耗時

### 3.3.6 分代回收（Generational GC）

分代假設：
- 大多數物件很快就會變成垃圾（早夭）
- 少數物件會存活很久

**分代架構**

```
┌─────────────────────────────────────────────┐
│                  堆記憶體                    │
├──────────────┬──────────────────────────────┤
│   年輕代      │        老年代               │
│  ┌────────┐  │                            │
│  │ Eden   │  │    ┌──────┐ ┌──────┐     │
│  │        │  │    │From  │ │ To   │     │
│  ├────────┤  │    │Survivor│ │Survivor│   │
│  │S0│S1 │  │    └──────┘ └──────┘     │
│  │  │   │  │                            │
│  └────────┘  │                            │
└──────────────┴──────────────────────────────┘
```

**Minor GC vs Major GC**

| GC 類型 | 觸發條件 | 頻率 | 暫停時間 |
|---------|----------|------|----------|
| Minor GC | Eden 滿 | 頻繁 | 短 |
| Major GC | 老年代滿 | 較少 | 長 |

JVM、.NET GC 都是分代回收的典型實作。

### 3.3.7 各語言的 GC 策略

| 語言 | GC 策略 |
|------|---------|
| Python | 引用計數 + 標記-清除（處理循環） |
| Java | 分代 + 標記-清除/複製 |
| C# | 分代 + 標記-壓縮 |
| Go | 並髮標記-清除 |
| JavaScript | 分代 + 增量GC |
| Ruby | 標記-清除 |

## 3.4 例子：Python、JavaScript、Lua、LISP

### 3.4.1 Python 位元組碼

Python 程式會被編譯為 `.pyc` 位元組碼，由 CPython VM 執行。

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

**Python VM 特性**

- 基於堆疊
- 大約 100 個位元組碼指令
- 使用 pyc 檔案快取編譯結果

### 3.4.2 Lua VM

Lua 使用基於暫存器的 VM，5.0 版本從堆疊式改為暫存器式。

```lua
-- Lua 範例
function fib(n)
    if n <= 1 then return n end
    return fib(n - 1) + fib(n - 2)
end

print(fib(10))  -- 輸出 55
```

**Lua 5.3+ 位元組碼結構**

- 40 個 opcode
- 基於暫存器（最多 255 個）
- 緊湊的位元組碼格式

### 3.4.3 JavaScript V8 引擎

V8 是 Chrome 和 Node.js 使用的 JavaScript 引擎，採用 JIT 編譯架構。

**V8 架構**

```
原始碼
   │
   ▼
┌─────────────────────────────────────────────┐
│              Ignition（直譯器）              │
│  - 產生位元組碼                             │
│  - 收集執行資訊                             │
│  - 熱點偵測                                │
└─────────────────────────────────────────────┘
   │
   ▼（熱點程式碼）
┌─────────────────────────────────────────────┐
│         TurboFan（最佳化編譯器）             │
│  - JIT 編譯熱點程式碼                      │
│  - 型別特化                                │
│  - 機器碼生成                              │
└─────────────────────────────────────────────┘
   │
   ▼（效能退化）
┌─────────────────────────────────────────────┐
│         Deoptimization（去最佳化）          │
│  - 假設失敗時回退到 Ignition              │
└─────────────────────────────────────────────┘
```

### 3.4.4 LISP 評価器

LISP 以其簡單而優雅的 eval/apply 循環著稱。

**LISP 評価器原理**

```
eval(expr, env)
  │
  ├─ 數值/字串 → 直接返回
  │
  ├─ 符號 → 在 env 中查找
  │
  └─ 表達式 → 分類處理
      │
      ├─ quote → 返回原始形式
      ├─ if → 條件評価
      ├─ define → 定義變數
      ├─ lambda → 創建函數
      └─ 函數呼叫 → apply(func, args)
                         │
                         ├─ 內建函數 → 直接執行
                         └─ 使用者函數 → 求值函數體
```

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
    ['if', ['=', 'n', 1], 1, ['*', 'n', ['fact', ['-', 'n', 1]]]]]
eval_expr(factorial, env)
print(eval_expr(['fact', 5], env))  # 120
```

這個 LISP 直譯器展示了函數式語言的核心概念：程式即資料、遞迴、高階函數。
