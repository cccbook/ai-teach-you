# 2. 語法理論

## 2.1 正則表達式與有限自動機

### 2.1.1 語言與文法理論基礎

在正式討論正則表達式之前，我們需要理解喬姆斯基語言層級（Chomsky Hierarchy），這是形式語言理論的基石。

**語言的數學定義**

形式語言（Formal Language）是一個抽象的概念：

```
語言 L 是由某個字母表 Σ 上的字串（String）組成的集合：
L ⊆ Σ*

其中 Σ* 表示 Σ 上所有可能的字串集合（包括空字串 ε）
```

**喬姆斯基語言層級**

Noam Chomsky 於 1956 年提出的語言分類体系：

```
┌─────────────────────────────────────────────────────────────────┐
│  層級   │     語言類型        │ 產生規則            │ 辨識模型      │
├─────────────────────────────────────────────────────────────────┤
│  Type 0 │ 任意文法            │ 無限制產生規則       │ 圖靈機       │
├─────────────────────────────────────────────────────────────────┤
│  Type 1 │ 上下文敏感語言      │ αAβ → αγβ         │ 線性界限自動機│
├─────────────────────────────────────────────────────────────────┤
│  Type 2 │ 上下文無關語言     │ A → γ               │ 確定性下推    │
│          │                    │                      │ 自動機        │
├─────────────────────────────────────────────────────────────────┤
│  Type 3 │ 正規語言           │ A → aB 或 A → a    │ 有限自動機    │
└─────────────────────────────────────────────────────────────────┘
```

大多數程式語言的語法屬於 Type 2（上下文無關語言），而正規語言（Type 3）用於描述詞法結構。

### 2.1.2 正規表達式的理論基礎

正則表達式（Regular Expression, Regex）是一種用於描述正規語言的表示法。

**正則表達式的形式定義**

正則表達式 r 描述一個正規語言 L(r)，其語法定義如下：

```
1. ε（空字串）是正則表達式，L(ε) = {ε}
2. 若 a ∈ Σ，則 a 是正則表達式，L(a) = {a}
3. 若 r 和 s 是正則表達式：
   - (r|s) 是正則表達式，L((r|s)) = L(r) ∪ L(s)（聯集）
   - (rs) 是正則表達式，L((rs)) = L(r)L(s)（串接）
   - (r)* 是正則表達式，L((r)*) = L(r)*（Kleene 閉包）
4. 透過上述規則建構的表達式是正則表達式
```

**正則表達式的運算優先順序**

```
最高：(r)*     ← Kleene 閉包
    ：(rs)    ← 串接
最低：(r|s)   ← 聯集
```

**實用的正則表達式擴展**

除了上述基本運算外，現代正則表達式還提供便捷的語法糖：

| 擴展語法 | 意義 | 等價形式 |
|----------|------|----------|
| `r+` | 一或多個 | `rr*` |
| `r?` | 零或一個 | `(r|ε)` |
| `[abc]` | 字元類 | `(a\|b\|c)` |
| `[^abc]` | 排除字元類 | 除了 a,b,c 的字元 |
| `r{n}` | 精確重複 n 次 | - |
| `r{n,m}` | 重複 n 到 m 次 | - |
| `.` | 任意字元 | - |

### 2.1.3 正則表達式的應用

**詞法分析中的應用**

詞法分析器（Lexer）使用正則表達式定義 Token 的模式：

```
IDENTIFIER : [a-zA-Z][a-zA-Z0-9_]*
NUMBER     : [0-9]+
STRING     : "[^"]*"
COMMENT    : //.*
```

**文字處理中的應用**

```python
import re

# 基本模式
pattern = r"[0-9]+"  # 匹配一個或多個數字
text = "年齡是 25 歲，體重 65.5 公斤"

matches = re.findall(pattern, text)
print(matches)  # ['25', '65', '5']

# 電子郵件正則表達式
email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
emails = "聯絡: user@example.com 或 admin@test.org"
print(re.findall(email_pattern, emails))
# ['user@example.com', 'admin@test.org']

# 手機號碼（台灣格式）
phone_pattern = r"09[0-9]{8}"
print(re.match(phone_pattern, "0912345678"))  # <re.Match object>
print(re.match(phone_pattern, "1234567890"))  # None
```

### 2.1.4 有限自動機理論

有限自動機（Finite Automaton）是辨識正規語言的數學模型。

**確定型有限自動機（DFA）**

DFA 是一個五元組 M = (Q, Σ, δ, q₀, F)，其中：

| 符號 | 意義 |
|------|------|
| Q | 有限狀態集合 |
| Σ | 輸入字母表 |
| δ : Q × Σ → Q | 轉換函數 |
| q₀ ∈ Q | 起始狀態 |
| F ⊆ Q | 接受狀態集合 |

**DFA 的形式定義**

δ(q, a) = p 表示：當自動機處於狀態 q，讀入字元 a 時，轉換到狀態 p。

**非確定型有限自動機（NFA）**

NFA 與 DFA 的主要區別：

| 特性 | DFA | NFA |
|------|-----|-----|
| 轉換 | 確定性：每個狀態對每個輸入只有一個轉換 | 非確定性：一個狀態對同一輸入可有多個轉換 |
| ε 轉換 | 不允許 | 允許空字串轉換 |
| 等價性 | - | 任何 NFA 都有等價的 DFA |

**ε-轉換**

ε-轉換允許自動機在不消耗輸入的情況下改變狀態：

```
δ(q, ε) = {p₁, p₂, ...}
```

這在正規表達式到自動機的轉換中特別有用。

### 2.1.5 Thompson 建構法

Thompson 建構法是一種將正則表達式轉換為 NFA 的系統化方法。

**基本模式對應的 NFA**

```
1. ε 對應：
      ┌───┐
  → ─→│ s │─→ (f)
      └───┘

2. 字元 a 對應：
      ┌───┐
  → ─→│ s │─a→│ f │─→ (f)
      └───┘     └───┘

3. 聯集 r|s 對應：
      ┌───┐
  → ─→│ s │───────┐
      └───┘   ε   ▼
              ┌───┐   ┌───┐
              │ r │──→│   │
              └───┘   └───┘
                  ε       ε
              ┌───┐   ┌───┐
              │ s │──→│ f │─→ (f)
              └───┘   └───┘

4. 串接 rs 對應：
      ┌───┐     ┌───┐
  → ─→│ s │─r─→│   │─s─→│ f │─→ (f)
      └───┘     └───┘     └───┘

5. Kleene 閉包 r* 對應：
      ┌───┐
  → ─→│ s │─ε─→┌───┐─ε─→ (f)
      └───┘     │ r │──ε──┘
          ε─────→└───┘
```

### 2.1.6 自動機的最小化

等價的 DFA 可能有多個狀態，我們可以透過狀態最小化得到最簡形式。

**Myhill-Nerode 定理**

狀態區分（State Distinguishability）：

```
兩個狀態 p 和 q 是可區分的，如果存在一字串 w 使得：
- δ*(p, w) ∈ F 但 δ*(q, w) ∉ F，或
- δ*(q, w) ∈ F 但 δ*(p, w) ∉ F
```

**最小化演算法**

1. 初始分組：將狀態分為接受狀態集 F 和非接受狀態集 Q\F
2. 迭代細分：對於每個分組，檢查狀態是否可區分
3. 合併不可區分的狀態

## 2.2 文法（Context-Free Grammar）

### 2.2.1 上下文無關文法的定義

上下文無關文法（Context-Free Grammar, CFG）是描述程式語言語法的主要工具。

**CFG 的形式定義**

CFG G 是一個四元組 G = (V, T, P, S)：

| 符號 | 意義 |
|------|------|
| V | 變數（非終端符號）集合 |
| T | 終端符號集合（Token） |
| P | 產生規則集合 A → α |
| S ∈ V | 起始符號 |

**產生規則的語法**

```
Expr    → Expr + Term          (1)
Expr    → Expr - Term          (2)
Expr    → Term                 (3)
Term    → Term * Factor        (4)
Term    → Term / Factor        (5)
Term    → Factor               (6)
Factor  → NUMBER               (7)
Factor  → ( Expr )             (8)
```

**衍生（Derivation）**

從起始符號出發，反覆套用產生規則，最終得到只包含終端符號的句子：

```
Expr
⇒ Expr + Term        [套用規則 (1)]
⇒ Term + Term        [套用規則 (3)]
⇒ Factor + Term      [套用規則 (6)]
⇒ NUMBER + Term     [套用規則 (7)]
⇒ NUMBER + Factor    [套用規則 (6)]
⇒ NUMBER + NUMBER    [套用規則 (7)]
```

### 2.2.2 衍生樹（Derivation Tree）

衍生樹是文法的圖形表示，直觀展示句子的語法結構。

**衍生樹的定義**

1. 每個內部節點標記為非終端符號
2. 每個葉節點標記為終端符號或 ε
3. 若節點標記為 A，其子節點由產生規則 A → α 產生

**對於 "3 + 5 * 2" 的衍生樹**

```
        Expr
       /  |  \
     Expr  +  Term
      |       /  |  \
    Term    Term  *  Factor
      |       |         |
   Factor  Factor     NUMBER
      |       |         |
   NUMBER   5         2
      |
      3
```

### 2.2.3 左遞迴與右遞迴

**左遞迴文法**

若文法存在形如 A → Aα 的規則，則 A 是左遞迴的：

```
Expr → Expr + Term    ← 左遞迴
```

左遞迴可能導致遞迴下降 Parser 無限遞迴。

**消除左遞迴**

對於直接左遞迴 A → Aα | β，可以改寫為：

```
A  → β A'
A' → α A' | ε
```

**範例轉換**

原始文法：
```
Expr → Expr + Term | Term
```

轉換後：
```
Expr  → Term Expr'
Expr' → + Term Expr' | ε
```

**右遞迴**

右遞迴使用 A → α A 的形式，通常不會導致 Parser 問題，但可能產生較深的樹。

### 2.2.4 二義性文法

若一個文法對某個句子有多棵不同的衍生樹，則該文法是二義性的（Ambiguous）。

**經典的二義性問題：懸置 else**

```
Stmt  → if Expr then Stmt
       | if Expr then Stmt else Stmt
       | Other

Statement: if E1 then if E2 then S1 else S2
```

這個 Statement 可以有兩種解析：
- `if E1 then (if E2 then S1 else S2)` ← 優先匹配
- `if E1 then (if E2 then S1) else S2`

**消除二義性**

透過引入額外的非終端符號強制優先匹配：

```
Stmt  → MatchedStmt | UnmatchedStmt
MatchedStmt   → if Expr then MatchedStmt else MatchedStmt
UnmatchedStmt → if Expr then Stmt
              | if Expr then MatchedStmt else UnmatchedStmt
```

### 2.2.5 EBNF 語法

擴充巴科斯-諾爾範式（Extended Backus-Naur Form, EBNF）是描述文法的常用符號。

**EBNF 符號**

| 符號 | 意義 |
|------|------|
| `→` 或 `::=` | 定義 |
| `\|` | 或 |
| `[x]` | 零或一個 x |
| `{x}` | 零或多個 x |
| `(x)` | 分組 |
| `'x'` 或 `"x"` | 終端符號 |

**EBNF 範例**

```
Expr    → Term { ('+' | '-') Term }
Term    → Factor { ('*' | '/') Factor }
Factor  → NUMBER | '(' Expr ')'
```

等同於：

```
Expr    → Term | Expr '+' Term | Expr '-' Term
Term    → Factor | Term '*' Factor | Term '/' Factor
Factor  → NUMBER | '(' Expr ')'
```

## 2.3 Parser 與 Tokenizer

### 2.3.1 詞法分析的理論

詞法分析（Lexical Analysis）是將輸入字元流轉換為 Token 序列的過程。

**Token 的結構**

```python
class Token:
    def __init__(self, type, value, position):
        self.type = type      # Token 類型（IDENT, NUMBER, PLUS...）
        self.value = value    # Token 的值（識別字名、數值等）
        self.position = pos   # 在原始碼中的位置
```

**詞法分析與語法分析的分工**

```
┌──────────────────────────────────────────────────────────────┐
│                      原始碼字元流                             │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                    詞法分析器 (Lexer)                        │
│  - 辨識 Token                                                 │
│  - 去除空白和註解                                             │
│  - 記錄行列號                                                 │
│  - 處理錯誤恢復                                                │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                      Token 流                                │
│  [IDENT x] [ASSIGN =] [NUMBER 42] [PLUS +] [NUMBER 3] ...  │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                    語法分析器 (Parser)                       │
│  - 檢查語法結構                                               │
│  - 產生語法樹                                                 │
│  - 報告語法錯誤                                               │
└──────────────────────────────────────────────────────────────┘
```

### 2.3.2 語法分析的策略

語法分析器（Parser）主要有兩大類策略：自上而下（Top-Down）和自下而上（Bottom-Up）。

**自上而下分析（Top-Down Parsing）**

從起始符號開始，嘗試推導出輸入的 Token 序列。

| 方法 | 特點 |
|------|------|
| 遞迴下降 | 簡單直觀，每個非終端符號一個函數 |
| LL(1) | 向前看一個 Token，構造預測分析表 |

**自下而上分析（Bottom-Up Parsing）**

從輸入的 Token 開始，嘗試歸約為起始符號。

| 方法 | 特點 |
|------|------|
| LR(0) | 不需要向前看 |
| SLR | 簡單 LR，使用 Follow 集合 |
| LALR | Look-Ahead LR，合併同調狀態 |
| LR(1) | 最強大的 LR，狀態數較多 |

### 2.3.3 LL(1) 分析

LL(1) 分析器是遞迴下降分析的系統化形式。

**LL(k) 的含義**

- 第一個 L：從左到右讀取輸入（Left-to-right）
- 第二個 L：最左衍生（Leftmost derivation）
- (k)：向前看 k 個 Token

**First 集合**

First(α) 是可以從 α 推導出的句子的首終端符號集合。

```
計算 First 集合的規則：

1. 若 X 是終端符號，First(X) = {X}
2. 若 X 是非終端符號且有產生規則 X → ε，則 ε ∈ First(X)
3. 若 X 是非終端符號且有產生規則 X → Y₁Y₂...Yₖ
   - 將 First(Y₁) 中的所有非 ε 符號加入 First(X)
   - 若 ε ∈ First(Y₁)，則加入 First(Y₂)...
   - 若對所有 Yᵢ 都有 ε ∈ First(Yᵢ)，則 ε ∈ First(X)
4. 若 α = X₁X₂...Xₙ
   - 加入 First(X₁) 的非 ε 符號
   - 若 ε ∈ First(X₁)，加入 First(X₂) 的非 ε 符號
   - ...
```

**Follow 集合**

Follow(A) 是可能在某些句型中跟在 A 後面的終端符號集合。

```
計算 Follow 集合的規則：

1. 若 S 是起始符號，$ ∈ Follow(S)
2. 若有產生規則 A → αBβ
   - 將 First(β) 中的非 ε 符號加入 Follow(B)
3. 若有產生規則 A → αB 或 A → αBβ 且 ε ∈ First(β)
   - 將 Follow(A) 中的所有符號加入 Follow(B)
```

**預測分析表**

若文法是 LL(1) 的，可以構造預測分析表：

| 非終端 \ 終端 | id | + | * | ( | ) | $ |
|--------------|-----|---|---|---|---|---|
| E | T E' | error | error | T E' | error | error |
| E' | error | + T E' | error | error | ε | ε |
| T | F T' | error | error | F T' | error | error |
| T' | error | ε | * F T' | error | ε | ε |
| F | id | error | error | ( E ) | error | error |

### 2.3.4 LR 分析

LR 分析是最強大的表驅動分析方法。

**LR 分析器架構**

```
                    ┌──────────────────┐
    Token ────────→│                  │
                    │    LR 分析器     │──────→ 接受/錯誤
                    │                  │
    ┌───────────┐   │                  │
    │  分析表    │──→│                  │
    │  (Action/ │   │                  │
    │   Goto)    │   │                  │
    └───────────┘   └──────────────────┘
                           │
                           ▼
                    ┌──────────────────┐
                    │      堆疊        │
                    │ [狀態, 符號, ...]│
                    └──────────────────┘
```

**LR 分析動作**

| 動作 | 意義 |
|------|------|
| shift | 移入下一個 Token 並推入對應狀態 |
| reduce | 根據產生規則歸約，彈出右部並推入左部 |
| accept | 分析成功完成 |
| error | 發現語法錯誤 |

## 2.4 語法分析技術

### 2.4.1 遞迴下降 Parser

遞迴下降 Parser 是最直觀的 Parser 實作方式。

**特點：**

- 每個非終端符號對應一個函數
- 函數體反映該非終端符號的文法規則
- 容易理解和實作
- 若文法是左遞迴的，需要先消除左遞迴

```python
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
    
    def E(self):
        result = self.T()
        return self.E_prime(result)
    
    def E_prime(self, left):
        token = self.current()
        if token and token[0] in ['PLUS', 'MINUS']:
            op = self.consume()[1]
            right = self.T()
            new_left = (op, left, right)
            return self.E_prime(new_left)
        return left
    
    def T(self):
        result = self.F()
        return self.T_prime(result)
    
    def T_prime(self, left):
        token = self.current()
        if token and token[0] in ['MULT', 'DIV']:
            op = self.consume()[1]
            right = self.F()
            new_left = (op, left, right)
            return self.T_prime(new_left)
        return left
    
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
```

### 2.4.2 語法分析器的產生工具

現代編譯器開發通常使用自動產生的 Parser。

**Lex/Yacc 工具家族**

| 工具 | 語言 | 說明 |
|------|------|------|
| Lex + Yacc | C | 傳統的詞法/語法分析器產生器 |
| Flex + Bison | C | Lex/Yacc 的 GNU 版本 |
| PLY | Python | Python 實現的 Lex/Yacc |
| ANTLR | Java/C#/Python | 功能強大的產生器 |

**PLY 範例**

```python
# 安裝: pip install ply
from ply import yacc

# 詞法分析
tokens = ['NUMBER', 'PLUS', 'MINUS', 'MULT', 'DIV', 'LPAREN', 'RPAREN']

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_MULT    = r'\*'
t_DIV     = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_NUMBER  = r'\d+'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print(f"詞法錯誤: {t.value[0]}")
    t.lexer.skip(1)

lexer = yacc.lex()

# 語法分析
def p_expr(p):
    '''expr : expr PLUS expr
            | expr MINUS expr'''
    p[0] = ('+', p[1], p[3]) if p[2] == '+' else ('-', p[1], p[3])

def p_expr_term(p):
    'expr : term'
    p[0] = p[1]

def p_term(p):
    '''term : term MULT term
            | term DIV term'''
    p[0] = ('*', p[1], p[3]) if p[2] == '*' else ('/', p[1], p[3])

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_number(p):
    'factor : NUMBER'
    p[0] = ('num', p[1])

def p_factor_expr(p):
    'factor : LPAREN expr RPAREN'
    p[0] = p[2]

def p_error(p):
    print("語法錯誤!")

parser = yacc.yacc()

# 測試
result = parser.parse("2 + 3 * 4")
print(result)  # ('+', ('num', 2), ('*', ('num', 3), ('num', 4)))
```

## 2.5 語法樹與抽象語法樹

### 2.5.1 完整語法樹 vs 抽象語法樹

**完整語法樹（Parse Tree）**

完整語法樹忠實反映文法結構，每個文法規則都對應一個節點。

```
         E
       / | \
      E  +  T
     /|\     |
    T * F   F
    | | |   |
    F 3 2   1
    |
    1
```

**抽象語法樹（Abstract Syntax Tree, AST）**

AST 只保留語意上重要的資訊，省略輔助性的文法節點。

```
      *
     / \
    +   4
   / \
  2   3
```

**比較**

| 特性 | 完整語法樹 | 抽象語法樹 |
|------|------------|------------|
| 節點類型 | 包含所有非終端和終端 | 只包含有語意意義的節點 |
| 結構 | 忠實反映文法 | 簡化、專注語意 |
| 大小 | 較大 | 較小 |
| 用途 | 教學、分析 | 實際編譯 |

### 2.5.2 AST 的表示方式

**元組表示**

```python
# 二元運算
('+', ('num', 2), ('*', ('num', 3), ('num', 4))

# 條件陳述
('if', ('>', ('var', 'x'), ('num', 0)), 
    ('block', ...),  # then 部分
    ('block', ...))  # else 部分
```

**類別表示**

```python
class ASTNode:
    def __init__(self, node_type, value=None):
        self.type = node_type
        self.value = value
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)
    
    def __repr__(self):
        if self.value:
            return f"({self.type}: {self.value})"
        return f"({self.type})"

class BinaryOp(ASTNode):
    def __init__(self, operator, left, right):
        super().__init__("binary_op", operator)
        self.add_child(left)
        self.add_child(right)

class Number(ASTNode):
    def __init__(self, value):
        super().__init__("number", value)
```

### 2.5.3 語法樹的遍歷

**深度優先遍歷（DFS）**

```python
def traverse(node):
    """前序遍歷"""
    if node is None:
        return
    
    print(f"訪問: {node}")  # 前序：先處理當前節點
    for child in node.children:
        traverse(child)      # 中序：處理子節點
    print(f"離開: {node}")  # 後序：離開節點前處理
```

**語法導向翻譯**

語法樹的遍歷常用於語法導向翻譯（Syntax-Directed Translation）：

```
屬性文法 (Attribute Grammar)：
- 每個文法符號有屬性
- 屬性由產生規則的語義規則定義
- 綜合屬性：從子節點計算
- 繼承屬性：從父節點或兄弟節點計算
```

## 實作：完整的小型語言編譯器

讓我們實作一個完整的小型語言編譯器流程，展示理論的實際應用：

```python
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
```

執行結果：
```
原始碼: 2 + 3
Tokens: [('NUM', 2), ('PLUS', '+'), ('NUM', 3)]
AST: {'type': 'binary', 'op': '+', 'left': {'type': 'num', 'value': 2}, 'right': {'type': 'num', 'value': 3}}
結果: 5

原始碼: 10 - 4 * 2
Tokens: [('NUM', 10), ('MINUS', '-'), ('NUM', 4), ('MULT', '*'), ('NUM', 2)]
AST: {'type': 'binary', 'op': '-', 'left': {'type': 'num', 'value': 10}, 'right': {'type': 'binary', 'op': '*', ...}}
結果: 2

原始碼: (10 - 4) * 2
結果: 12

原始碼: 100 / 10 / 2
結果: 5
```

這個簡單的解譯器展示了從原始碼到執行結果的完整流程：詞法分析 → 語法分析 → 建立 AST → 直譯執行。
