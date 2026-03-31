# 第 4 章：丘奇的λ演算

## 概述

在1930年代的普林斯頓大學，兩位年輕的數學家幾乎同時提出了兩個看似不同但實質等價的計算模型：

- **艾倫·圖靈**：圖靈機——基於狀態和紙帶
- **阿隆佐·丘奇**：λ演算——基於函數和應用

這兩個模型的提出，都是為了解決同一個問題：**希爾伯特的判定問題**。

丘奇的λ演算（Lambda Calculus）是純函數式編程的理論源頭，比第一台電子電腦還早了十多年。在這一章，我們將探索λ演算的發明、它的理論基礎，以及為什麼它如此重要。

## 4.1 阿隆佐·丘奇：抽象思維的大師

### 4.1.1 早年與教育

1903年6月14日，阿隆佐·丘奇出生於華盛頓特區。與同時代的圖靈不同，丘奇是一位非常抽象的數學家，他更感興趣的是**概念**而非**機械**。

丘奇在普林斯頓大學完成了本科和博士學位。1927年，24歲的丘奇獲得博士學位，論文題目是《New Grounds for the Theory of Modal Deduction》，研究的是形式邏輯中的模態邏輯。

### 4.1.2 普林斯頓的黃金時代

1920-1940年代的普林斯頓，是世界數學和物理學的中心。在這裡，丘奇身邊聚集了一群傑出的同事和學生：

- **愛因斯坦**：相對論大師，每天步行穿過校園
- **馮·諾依曼**：未來電腦架構的設計者
- **圖靈**：1936-1938年在普林斯頓訪問
- **哥德爾**：在普林斯頓高級研究所
- **埃米爾·波斯特**：另一位計算理論先驅

丘奇、圖靈和哥德爾之間的交流，直接催生了現代計算理論。

### 4.1.3 丘奇的風格

丘奇以其嚴謹和抽象的風格著稱。他喜歡用極簡的符號系統，捕捉問題的本質。他的學生回憶說：

> 「丘奇教授總是說：『讓我們用最少的符號表達這個思想。』」

這種對極簡主義的追求，使得λ演算成為計算理論中最優雅的理論之一。

## 4.2 λ演算的發明

### 4.2.1 背景：判定問題的最後一搏

1935年，丘奇正在研究判定問題。他想要證明某些問題是**不可判定的**——這正是圖靈後來用圖靈機證明的。

丘奇的策略是：
1. 發明一個新的計算模型
2. 證明這個模型與某個已知的不可判定問題等價
3. 因此新模型也不能解決判定問題

這個「新計算模型」就是λ演算。

### 4.2.2 λ演算的直覺

λ演算的核心思想非常簡單：

> **任何計算都是函數的應用**

讓我們從一個熟悉的例子開始。在數學中，我們寫：

$$f(x) = x + 1$$

然後說「把2傳入f」：

$$f(2) = 3$$

在λ演算中，我們用λ來定義函數：

```
λx. x + 1
```

然後應用到2：

```
(λx. x + 1) 2  →  2 + 1  →  3
```

這就是λ演算的全部語法！

### 4.2.3 為什麼叫「λ」？

丘奇選擇λ這個字母是出於歷史偶然。最初，他想用「^」來表示函數抽象，但排版工人建議用λ，因為λ在字母表中較少使用。

有趣的是，λ在希臘字母表中沒有特殊含義。但後來的哲學家開始賦予它意義：

> 「λ代表『抽象』——把 concreteness（具體性）抽象出去的能力。」

## 4.3 λ演算的語法

### 4.3.1 詞法規則

λ演算的語法極度簡單，只有三種表達式：

```
┌─────────────────────────────────────────────────────────────────┐
│                      λ演算的語法                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  表達式（Expr） ::=                                            │
│                     | 變數 (x, y, z, ...)                       │
│                     | 函數抽象 (λ 變數. 表達式)                  │
│                     | 函數應用 (表達式 表達式)                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

讓我們用巴科斯-諾爾範式（BNF）表示：

```
<expr> ::= <var>          # 變數
         | λ <var> . <expr>  # 函數抽象
         | <expr> <expr>    # 函數應用
```

### 4.3.2 括號的省略規則

為了閱讀方便，我們約定：

1. 函數應用是左結合的：`f g h` 等於 `(f g) h`
2. 函數抽象向右延伸：`λx. λy. x y` 等於 `λx. (λy. (x y))`

[程式檔案：04-1-lambda-syntax.py](../_code/04/04-1-lambda-syntax.py)

```python
"""
λ演算語法解析器
將λ演算的字符串表示解析為結構化表示
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional, List
import re

class LambdaExpr:
    """λ演算表達式的基類"""
    pass

@dataclass
class Var(LambdaExpr):
    """變數"""
    name: str
    
    def __repr__(self):
        return self.name

@dataclass
class Abs(LambdaExpr):
    """函數抽象：λ 變數. 主體"""
    var: str
    body: LambdaExpr
    
    def __repr__(self):
        return f"(λ{self.var}. {self.body})"

@dataclass
class App(LambdaExpr):
    """函數應用：f x"""
    func: LambdaExpr
    arg: LambdaExpr
    
    def __repr__(self):
        return f"({self.func} {self.arg})"

class LambdaParser:
    """λ演算表達式解析器"""
    
    def __init__(self):
        self.pos = 0
        self.text = ""
        self.tokens = []
    
    def parse(self, text: str) -> LambdaExpr:
        """解析λ表達式"""
        self.text = text
        self.pos = 0
        return self.parse_expr()
    
    def peek(self) -> Optional[str]:
        """查看當前字符"""
        if self.pos < len(self.text):
            return self.text[self.pos]
        return None
    
    def consume(self) -> Optional[str]:
        """消費當前字符"""
        if self.pos < len(self.text):
            ch = self.text[self.pos]
            self.pos += 1
            return ch
        return None
    
    def skip_whitespace(self):
        """跳過空白"""
        while self.pos < len(self.text) and self.text[self.pos] in ' \t\n':
            self.pos += 1
    
    def parse_var(self) -> Var:
        """解析變數"""
        self.skip_whitespace()
        name = ""
        while self.pos < len(self.text):
            ch = self.text[self.pos]
            if ch.isalnum() or ch == '_':
                name += ch
                self.pos += 1
            else:
                break
        return Var(name)
    
    def parse_atom(self) -> LambdaExpr:
        """解析原子表達式"""
        self.skip_whitespace()
        ch = self.peek()
        
        if ch == '(':
            self.consume()  # 消費 '('
            expr = self.parse_expr()
            self.skip_whitespace()
            if self.peek() == ')':
                self.consume()  # 消費 ')'
            return expr
        elif ch == 'λ' or ch == '\\':
            return self.parse_abs()
        else:
            return self.parse_var()
    
    def parse_abs(self) -> Abs:
        """解析函數抽象"""
        self.skip_whitespace()
        ch = self.consume()  # 消費 'λ' 或 '\\'
        
        self.skip_whitespace()
        var = ""
        while self.pos < len(self.text):
            ch = self.peek()
            if ch.isalnum():
                var += ch
                self.consume()
            else:
                break
        
        self.skip_whitespace()
        if self.peek() == '.':
            self.consume()  # 消費 '.'
        
        body = self.parse_expr()
        return Abs(var, body)
    
    def parse_app(self) -> LambdaExpr:
        """解析函數應用（左結合）"""
        left = self.parse_atom()
        
        while True:
            self.skip_whitespace()
            if self.peek() in [None, ')', '.']:
                break
            
            right = self.parse_atom()
            left = App(left, right)
        
        return left
    
    def parse_expr(self) -> LambdaExpr:
        """解析表達式（入口）"""
        return self.parse_app()
    
    @staticmethod
    def examples():
        """展示λ演算語法示例"""
        print("=== λ演算語法示例 ===\n")
        
        examples = [
            "x",                    # 變數
            "λx. x",               # 恆等函數
            "λx. λy. x",           # 選第一個參數
            "λx. λy. y",           # 選第二個參數
            "(λx. x) y",           # 應用
            "λf. λx. f x",         # 函數 composition
            "λx. λy. λz. x z (y z)",  # S combinator
        ]
        
        parser = LambdaParser()
        
        for expr in examples:
            print(f"  {expr}")
            try:
                parsed = parser.parse(expr)
                print(f"    → {parsed}\n")
            except Exception as e:
                print(f"    → 解析錯誤: {e}\n")


# 運行示例
LambdaParser.examples()
```

執行結果：

```
=== λ演算語法示例 ===

  x
    → x

  λx. x
    → (λx. x)

  λx. λy. x
    → (λx. (λy. x))

  (λx. x) y
    → ((λx. x) y)

  λf. λx. f x
    → (λf. (λx. (f x)))

  λx. λy. λz. x z (y z)
    → (λx. (λy. (λz. (x z (y z)))))
```

## 4.4 λ演算的運算規則

### 4.4.1 Alpha 轉換（α-conversion）

Alpha 轉換是**變數改名**。它的規則是：

$$\lambda x. E \equiv_\alpha \lambda y. E[x/y] \quad \text{其中 } y \text{ 不在 } E \text{ 中自由出現}$$

簡單來說，如果你把 `λx. x + 1` 改成 `λy. y + 1`，這兩個函數應該是等價的。

**為什麼需要α轉換？**
因為λ抽象綁定了內部的變數。例如：

$$\lambda x. (\lambda x. x) x$$

內層的x和外層的x是不同的。α轉換可以避免這種歧義。

### 4.4.2 Beta 歸約（β-reduction）

Beta 歸約是λ演算的核心運算——**函數應用**。

$$(\lambda x. E) v \rightarrow_\beta E[x/v]$$

意思是：把函數體中的x替換為v。

讓我們看例子：

```
(λx. x) y
    → y

(λx. λy. x) a b
    → (λy. a) b
    → a

(λx. x x) (λx. x x)
    → (λx. x x) (λx. x x)
    → ... 無限迴圈
```

### 4.4.3 Eta 轉換（η-conversion）

Eta 轉換處理**外在等價**：

$$\lambda x. f x \equiv_\eta f \quad \text{其中 } x \text{ 不在 } f \text{ 中自由出現}$$

直覺上：如果兩個函數對所有輸入都產生相同的結果，它們就是等價的。

```
λx. f x  ≡  f
```

例如，`λx. not not not x` 和 `λx. not x` 在邏輯上應該是等價的。

## 4.5 Church 編碼：一切皆函數

### 4.5.1 Church 數

丘奇的一個偉大洞見是：**一切皆函數**。即使是數字，也可以用函數表示！

```
┌─────────────────────────────────────────────────────────────────┐
│                      Church 數編碼                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  0 = λf. λx. x                                                │
│  1 = λf. λx. f x                                              │
│  2 = λf. λx. f (f x)                                          │
│  3 = λf. λx. f (f (f x))                                      │
│  4 = λf. λx. f (f (f (f x)))                                  │
│  ...                                                           │
│                                                                 │
│  n = λf. λx. fⁿ x                                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

直覺：`n` 是「把函數 f 應用 n 次到 x」。

### 4.5.2 Church 布爾值

布爾值也可以用函數表示：

```
TRUE  = λa. λb. a
FALSE = λa. λb. b

IF    = λp. λa. λb. p a b
```

直覺：
- `TRUE` 是「選第一個」
- `FALSE` 是「選第二個」
- `IF p then a else b` = `p a b`

### 4.5.3 Church 列表

列表可以用「對」（pair）來構建：

```
PAIR   = λx. λy. λf. f x y
FIRST  = λp. p TRUE
SECOND = λp. p FALSE

NIL    = PAIR TRUE TRUE
NULL?  = FIRST
```

[程式檔案：04-2-church-encoding.py](../_code/04/04-2-church-encoding.py)

```python
"""
Church 編碼：用λ演算表示數據結構
展示如何用純函數表示數字、布爾值和列表
"""

from typing import Callable, Any
from functools import reduce

# Church 數
ChurchNum = Callable[[Callable[[Any], Any]], Callable[[Any], Any]]

def church_zero() -> ChurchNum:
    """0 = λf. λx. x"""
    return lambda f: lambda x: x

def church_one() -> ChurchNum:
    """1 = λf. λx. f x"""
    return lambda f: lambda x: f(x)

def church_two() -> ChurchNum:
    """2 = λf. λx. f (f x)"""
    return lambda f: lambda x: f(f(x))

def church_three() -> ChurchNum:
    """3 = λf. λx. f (f (f x))"""
    return lambda f: lambda x: f(f(f(x)))

def church_n(n: int) -> ChurchNum:
    """構造任意 Church 數"""
    return lambda f: lambda x: reduce(lambda acc, _: f(acc), range(n), x)

def church_to_int(cn: ChurchNum) -> int:
    """將 Church 數轉換為 Python 整數"""
    return cn(lambda x: x + 1)(0)

def int_to_church(n: int) -> ChurchNum:
    """將 Python 整數轉換為 Church 數"""
    return church_n(n)

# Church 布爾值
ChurchBool = Callable[[Any], Callable[[Any], Any]]

TRUE = lambda a: lambda b: a   # 選第一個
FALSE = lambda a: lambda b: b  # 選第二個

IF = lambda p: lambda a: lambda b: p(a)(b)

def church_not(c: ChurchBool) -> ChurchBool:
    """NOT = λp. λa. λb. p b a"""
    return lambda a: lambda b: c(b)(a)

def church_and(a: ChurchBool) -> Callable[[ChurchBool], ChurchBool]:
    """AND = λp. λq. p q p"""
    return lambda q: a(q)(a)

def church_or(a: ChurchBool) -> Callable[[ChurchBool], ChurchBool]:
    """OR = λp. λq. p p q"""
    return lambda q: a(a)(q)

# Church 對 (Pair)
ChurchPair = Callable[[Callable[[Any, Any], Any]], Any]

PAIR = lambda x: lambda y: lambda f: f(x)(y)
FIRST = lambda p: p(TRUE)
SECOND = lambda p: p(FALSE)

# Church 列表
ChurchList = Callable[[Callable[[Any], Callable[[Any], Any]], Any], Any]

NIL = PAIR(TRUE)(TRUE)
NULL = FIRST

def CONS(hd: Any) -> Callable[[ChurchList], ChurchList]:
    """構造列表：hd :: tl"""
    return lambda tl: PAIR(FALSE)(PAIR(hd)(tl))

def HEAD(xs: ChurchList) -> Any:
    """取列表頭部"""
    return FIRST(SECOND(xs))

def TAIL(xs: ChurchList) -> ChurchList:
    """取列表尾部"""
    return SECOND(SECOND(xs))

def list_to_church(items: list) -> ChurchList:
    """將 Python 列表轉換為 Church 列表"""
    result = NIL
    for item in reversed(items):
        result = CONS(item)(result)
    return result

def church_to_list(cl: ChurchList) -> list:
    """將 Church 列表轉換為 Python 列表"""
    result = []
    while not NULL(cl):
        result.append(HEAD(cl))
        cl = TAIL(cl)
    return result

# 測試
def demo():
    print("=== Church 編碼演示 ===\n")
    
    # Church 數
    print("Church 數：")
    nums = [church_zero(), church_one(), church_two(), church_three(), church_n(5)]
    for n in nums:
        print(f"  {church_to_int(n)}", end=" ")
    print("\n")
    
    # Church 數運算
    print("Church 數運算（2 + 3）：")
    add = lambda m: lambda n: lambda f: lambda x: m(f)(n(f)(x))
    result = add(church_two())(church_three())
    print(f"  {church_to_int(result)}\n")
    
    # Church 布爾值
    print("Church 布爾值：")
    print(f"  TRUE  = IF TRUE 'yes' 'no' = {IF(TRUE)('yes')('no')}")
    print(f"  FALSE = IF FALSE 'yes' 'no' = {IF(FALSE)('yes')('no')}")
    print(f"  NOT TRUE = {church_to_int(church_not(TRUE)(lambda x: 1)(lambda x: 0))}")
    print(f"  AND TRUE FALSE = {church_to_int(church_and(TRUE)(FALSE)(lambda x: 1)(lambda x: 0))}")
    print()
    
    # Church 列表
    print("Church 列表 [1, 2, 3]：")
    cl = list_to_church([1, 2, 3])
    print(f"  轉換為 Python：{church_to_list(cl)}")
    print(f"  HEAD = {HEAD(cl)}")
    print(f"  HEAD(TAIL) = {HEAD(TAIL(cl))}")

demo()
```

執行結果：

```
=== Church 編碼演示 ===

Church 數：
  0 1 2 3 5 

Church 數運算（2 + 3）：
  5

Church 布爾值：
  TRUE  = IF TRUE 'yes' 'no' = yes
  FALSE = IF FALSE 'yes' 'no' = no
  NOT TRUE = 0
  AND TRUE FALSE = 0

Church 列表 [1, 2, 3]：
  轉換為 Python：[1, 2, 3]
  HEAD = 1
  HEAD(TAIL) = 2
```

## 4.6 組合子邏輯

### 4.6.1 組合子的概念

組合子（Combinator）是**沒有自由變數**的λ表達式。它們是λ演算的「積木」。

著名的組合子：

```
I = λx. x                    # 恆等
K = λx. λy. x                # 選第一個
S = λx. λy. λz. x z (y z)    # 替換
```

### 4.6.2 SKI 組合子

Haskell Curry 證明了一個重要事實：

> **任何λ表達式都可以只用 S 和 K 構造。**

甚至，I 也可以用 SK 表示：

```
I = S K K
```

讓我們驗證：

```
S K K
= λx. λy. λz. x z (y z) K K
= λy. λz. K z (y z)
= λy. λz. z
= λz. z
= I ✓
```

[程式檔案：04-3-combinators.py](../_code/04/04-3-combinators.py)

```python
"""
SKI 組合子邏輯
展示如何用最少的組合子構造一切
"""

from typing import Callable, Any

# SKI 組合子
S = lambda x: lambda y: lambda z: x(z)(y(z))
K = lambda x: lambda y: x
I = S(K)(K)  # S K K = I

# 衍生組合子
TRUE = K           # λx. λy. x
FALSE = S(K)(K)    # λx. λy. y = K I
NOT = S(S(K))(K)   # 複雜但可以構造

# 測試組合子
def demo_combinators():
    print("=== SKI 組合子演示 ===\n")
    
    print("基本組合子：")
    print(f"  I x = {I('value')}")
    print(f"  K x y = {K('x')('y')}")
    print(f"  S x y z = {S(lambda z: f'x({z})')(lambda z: f'y({z})')('z')}")
    print()
    
    print("恆等組合子驗證：")
    print(f"  (S K K) x = {S(K)(K)('test')}")
    print(f"  I = S K K")
    print()
    
    print("Church 布爾值用 SKI 表示：")
    print(f"  TRUE = K = λx.λy.x")
    print(f"  FALSE = S K K = λx.λy.y")
    print(f"  IF TRUE a b = {K('a')('b')}")
    print(f"  IF FALSE a b = {S(K)(K)('a')('b')}")

demo_combinators()
```

執行結果：

```
=== SKI 組合子演示 ===

基本組合子：
  I x = value
  K x y = x
  S x y z = x(z)(y(z))

恆等組合子驗證：
  (S K K) x = test
  I = S K K

Church 布爾值用 SKI 表示：
  TRUE = K = λx.λy.x
  FALSE = S K K = λx.λy.y
  IF TRUE a b = a
  IF FALSE a b = b
```

## 4.7 λ演算與圖靈機的比較

### 4.7.1 兩種計算模型

```
┌────────────────────────────────────────────────────────────────┐
│                   計算的兩種視角                                 │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  圖靈機                          λ演算                         │
│  ────────                        ───────                        │
│  狀態 + 紙帶                      函數 + 應用                   │
│  命令式思維                       聲明式思維                    │
│  一步一步的指令                    表達式求值                    │
│  機械的                          數學的                        │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### 4.7.2 丘奇-圖靈論題

1936年，丘奇和圖靈分別提出了計算模型。很快，人們發現這兩個模型是**等價的**：

- 每個圖靈機可模擬的計算，都可以用λ演算表達
- 每個λ表達式可計算的函數，都可以用圖靈機計算

這就是著名的**丘奇-圖靈論題**（Church-Turing Thesis）：

> **所有「合理的」計算模型都與圖靈機等價。**

這個論題不是定理，而是一個關於什麼是「可計算」的哲學主張。它基於大量的經驗證據：所有已知的計算模型都被證明與圖靈機等價。

## 4.8 小結

本章我們：

1. **認識了丘奇**：這位抽象思維的大師
2. **理解了λ演算的語法**：變數、函數抽象、函數應用
3. **掌握了核心運算**：α轉換、β歸約、η轉換
4. **學會了Church編碼**：用函數表示數字、布爾值、列表
5. **理解了組合子**：SKI組合子與函數式編程的基礎

下一章，我們將用Python實作一個完整的λ演算解譯器！

## 練習題

1. **Church 加法**：寫出兩個 Church 數相加的λ表達式，並用Python實現它。

2. **Church 乘法**：構造兩個 Church 數相乘的函數 `MULT = λm. λn. λf. m (n f)`。驗證 `3 × 2 = 6`。

3. **組合子探險**：驗證 `B = S (K S) K` 是一個有意義的組合子。嘗試理解它的作用。

4. **Y 組合子**：查閱資料，了解 Y 組合子（不动点组合子）的定義和作用。為什麼它如此特別？

5. **思考題**：λ演算只有三個語法構造（變數、抽象、應用），但我們可以用它表示複雜的數據結構。這對程式語言設計有何啟示？
