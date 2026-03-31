# 第 1 章：AI 的歷史

## 1.1 人工智慧的起源 (1956年達特茅斯會議)

1956 年的夏天，在美國新罕布夏州的達特茅斯學院，一群科學家聚集在一起，展開了一場為期兩個月的研討會。這次會議被認為是人工智慧（Artificial Intelligence, AI）作為一門學科的誕生時刻。

與會者包括了：
- **John McCarthy**（達特茅斯學院）—— 首先提出「人工智慧」這個術語
- **Marvin Minsky**（哈佛大學）—— 日後成為 AI 領域的先驅
- **Claude Shannon**（貝爾實驗室）—— 資訊理論的創始人
- **Allen Newell** 與 **Herbert A. Simon**（卡內基美隆大學）—— 物理符號系統的提出者

這次會議的目標是：「接下來的兩個月，我們將嘗試讓機器達到以下行為：使用語言、形成抽象概念、解決各種目前只有人類能解決的問題，並且自我改進。」

## 1.2 第一次 AI 熱潮：符號主義與專家系統

### 1.2.1 符號主義 (Symbolism)

符號主義是 AI 最早的研究方向，核心思想是：智慧可以被視為對符號的操作。這些符號代表了世界的概念和關係，而推理過程就是對這些符號進行變換和組合。

符號主義的代表技術包括：
- **邏輯推論**：使用命題邏輯和一階邏輯進行自動推理
- **專家系統**：將人類專家的知識編碼成規則，供電腦使用
- **Lisp 語言**：專為 AI 設計的函數式程式語言

### 1.2.2 ELIZA：第一個聊天機器人 (1966)

1966 年，MIT 的 Joseph Weizenbaum 開發了 ELIZA，這是有史以來第一個聊天機器人。ELIZA 模擬的是一位羅哲斯學派（Rogerian）心理治療師，透過模式匹配和簡單的替換規則，營造出與人對話的假象。

[程式檔案：01-1-eliza.py](../_code/01/01-1-eliza.py)

```python
#!/usr/bin/env python3
"""
ELIZA 聊天機器人 (1966)
最早由 Joseph Weizenbaum 在 MIT 開發的對話程式
"""

import re
import random

class Eliza:
    def __init__(self):
        self.rules = [
            (r'I need (.*)', 
             ["Why do you need %1?", 
              "Would it really help you to get %1?",
              "Are you sure you need %1?"]),
            
            (r'I feel (.*)',
             ["Tell me more about feeling %1.",
              "Do you often feel %1?",
              "What other feelings do you have?"]),
            
            (r'I can\'?t (.*)',
             ["Why can't you %1?",
              "What would it take for you to %1?",
              "Have you tried?"]),
            
            (r'I am (.*)',
             ["How long have you been %1?",
              "Do you believe it is normal to be %1?",
              "What do you think caused you to be %1?"]),
            
            (r'you are (.*)',
             ["What makes you think I am %1?",
              "Does it please you to think I am %1?",
              "Perhaps you would like to be %1."]),
            
            (r'yes',
             ["You seem quite positive.",
              "Are you sure?",
              "What makes you say yes?"]),
            
            (r'no',
             ["Why not?",
              "Are you sure?",
              "What makes you say no?"]),
            
            (r'my (.*) (.*)',
             ["Your %1 %2?",
              "Tell me more about your %1.",
              "How does that make you feel?"]),
            
            (r'(.*) mother(.*)',
             ["Tell me more about your mother.",
              "How did she make you feel?",
              "What is your relationship with your mother?"]),
            
            (r'(.*) father(.*)',
             ["Tell me more about your father.",
              "How did he make you feel?",
              "What is your relationship with your father?"]),
            
            (r'(.*) sorry(.*)',
             ["There's no need to apologize.",
              "Apologies are not necessary.",
              "What feelings do you have when you apologize?"]),
            
            (r'hello(.*)',
             ["Hello. How are you feeling today?",
              "Hi there. What's on your mind?",
              "Hello. What would you like to talk about?"]),
            
            (r'(.*)bye(.*)',
             ["Goodbye. Take care of yourself.",
              "Thank you for talking with me.",
              "Until next time."]),
        ]
        
        self.responses = [
            "Tell me more about that.",
            "How does that make you feel?",
            "Why do you say that?",
            "I see.",
            "That's interesting.",
            "Go on.",
            "Please continue.",
            "What do you think?",
            "How do you feel about that?",
            "Tell me more.",
        ]
    
    def respond(self, user_input):
        user_input = user_input.strip()
        
        if not user_input:
            return "Please tell me more."
        
        for pattern, responses in self.rules:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                response = random.choice(responses)
                if '%1' in response and match.groups():
                    return response % match.groups()
                return response
        
        return random.choice(self.responses)
    
    def chat(self):
        print("ELIZA: Hello. I'm ELIZA. What's on your mind?")
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("ELIZA: Goodbye. Take care.")
                    break
                response = self.respond(user_input)
                print(f"ELIZA: {response}")
            except KeyboardInterrupt:
                print("\nELIZA: Goodbye.")
                break

if __name__ == "__main__":
    eliza = Eliza()
    eliza.chat()
```

ELIZA 的核心原理非常簡單：
1. 使用正規表達式匹配使用者的輸入
2. 從匹配的模式中提取關鍵片段
3. 將片段替換到回應模板中

這種「模式匹配 + 替換」的技術雖然原始，但卻能產生令人驚訝的對話效果。雖然 ELIZA 並不理解語言的真正意義，但它展示了電腦可以透過表面的語法規則來模擬對話。

### 1.2.3 規則式系統

規則式系統（Rule-Based System）是早期 AI 的核心技術，其運作方式可以概括為：

```
IF 條件 THEN 結論
```

這類系統的優點是透明、可解釋——我們可以清楚看到為什麼系統做出某個推論。

[程式檔案：01-2-simple-rules.py](../_code/01/01-2-simple-rules.py)

```python
#!/usr/bin/env python3
"""
簡單的規則式系統 - 展示早期專家系統的運作方式
基於 IF-THEN 規則的專家系統架構
"""

class Rule:
    def __init__(self, condition, action):
        self.condition = condition
        self.action = action
    
    def evaluate(self, facts):
        return self.condition(facts)
    
    def execute(self):
        return self.action()

class RuleBasedSystem:
    def __init__(self):
        self.rules = []
        self.facts = set()
    
    def add_rule(self, condition, action):
        rule = Rule(condition, action)
        self.rules.append(rule)
    
    def add_fact(self, fact):
        self.facts.add(fact)
    
    def remove_fact(self, fact):
        if fact in self.facts:
            self.facts.remove(fact)
    
    def forward_chaining(self):
        new_facts = True
        while new_facts:
            new_facts = False
            for rule in self.rules:
                if rule.evaluate(self.facts):
                    result = rule.execute()
                    if result and result not in self.facts:
                        self.add_fact(result)
                        new_facts = True
                        print(f"推論得出: {result}")
        return self.facts

def example_medical_system():
    print("=== 醫療專家系統範例 ===\n")
    
    system = RuleBasedSystem()
    
    system.add_fact("發燒")
    system.add_fact("咳嗽")
    
    system.add_rule(
        lambda f: "發燒" in f and "咳嗽" in f,
        lambda: "肺炎"
    )
    
    system.add_rule(
        lambda f: "肺炎" in f,
        lambda: "建議胸部X光檢查"
    )
    
    system.add_rule(
        lambda f: "發燒" in f,
        lambda: "建議服用退燒藥"
    )
    
    system.add_rule(
        lambda f: "咳嗽" in f,
        lambda: "建議服用止咳藥"
    )
    
    print(f"已知事實: {system.facts}")
    print("\n開始推論:")
    facts = system.forward_chaining()
    print(f"\n最終結論: {facts}")

def example_animal_classifier():
    print("\n=== 動物分類專家系統 ===\n")
    
    system = RuleBasedSystem()
    
    system.add_fact("有羽毛")
    system.add_fact("會飛")
    system.add_fact("會下蛋")
    
    system.add_rule(
        lambda f: "有羽毛" in f,
        lambda: "是鳥類"
    )
    
    system.add_rule(
        lambda f: "是鳥類" in f and "會飛" in f,
        lambda: "可能是燕子"
    )
    
    system.add_rule(
        lambda f: "會下蛋" in f,
        lambda: "是卵生動物"
    )
    
    print(f"已知事實: {system.facts}")
    print("\n開始推論:")
    facts = system.forward_chaining()
    print(f"\n最終結論: {facts}")

if __name__ == "__main__":
    example_medical_system()
    example_animal_classifier()
```

### 1.2.4 Prolog 與邏輯程式設計 (1972)

1972 年，法國馬賽大學的 Alain Colmerauer 和 Philippe Roussel 開發了 Prolog（Programming in Logic）語言。Prolog 是邏輯程式設計的代表，它允許程式設計師用一階邏輯的方式表達知識，而不是詳細描述計算步驟。

Prolog 的核心概念是：
- **事實 (Facts)**：描述已知的世界
- **規則 (Rules)**：描述事物之間的邏輯關係
- **查詢 (Queries)**：向系統提問，讓系統自動進行推理

[程式檔案：01-3-prolog-family.py](../_code/01/01-3-prolog-family.py)

```python
#!/usr/bin/env python3
"""
Prolog 家族關係推論 (1972)
展示邏輯式 AI 的基本概念：事實 + 規則 = 推論
"""

class PrologLikeSystem:
    def __init__(self):
        self.facts = set()
        self.rules = []
    
    def add_fact(self, fact):
        self.facts.add(fact)
    
    def add_rule(self, head, body):
        self.rules.append((head, body))
    
    def query(self, goal, depth=0):
        if depth > 10:
            return []
        
        indent = "  " * depth
        
        if goal in self.facts:
            print(f"{indent}事實匹配: {goal}")
            return [goal]
        
        for head, body in self.rules:
            if head == goal:
                print(f"{indent}嘗試規則: {head} <- {body}")
                results = []
                for sub_goal in body:
                    sub_results = self.query(sub_goal, depth + 1)
                    if not sub_results:
                        break
                    results.extend(sub_results)
                else:
                    print(f"{indent}規則匹配成功: {goal}")
                    return [goal]
        
        return []

def family_example():
    print("=== Prolog 風格家族關係推論 ===\n")
    
    kb = PrologLikeSystem()
    
    kb.add_fact("父親(約翰, 瑪麗)")
    kb.add_fact("父親(約翰, 湯姆)")
    kb.add_fact("母親(安娜, 瑪麗)")
    kb.add_fact("母親(安娜, 湯姆)")
    kb.add_fact("父親(湯姆, 班)")
    kb.add_fact("母親(麗莎, 班)")
    
    def parent_rule():
        return ["父親(X, Y)", "母親(X, Y)"]
    
    def grandparent_rule():
        return ["父親(X, Z)", "父親(Z, Y)"]
    
    def grandparent_rule2():
        return ["父親(X, Z)", "母親(Z, Y)"]
    
    kb.add_rule("父母(X, Y)", parent_rule())
    kb.add_rule("祖父母(X, Y)", grandparent_rule())
    kb.add_rule("祖父母(X, Y)", grandparent_rule2())
    kb.add_rule("兄弟姊妹(X, Y)", ["父母(Z, X)", "父母(Z, Y)"])
    
    print("查詢: 誰是瑪麗的父母?")
    results = kb.query("父母(X, 瑪麗)")
    
    print("\n" + "="*50)
    print("\n查詢: 誰是班的祖父母?")
    results = kb.query("祖父母(X, 班)")
    
    print("\n" + "="*50)
    print("\n查詢: 瑪麗和湯姆是兄弟姊妹嗎?")
    results = kb.query("兄弟姊妹(瑪麗, 湯姆)")

def logic_puzzle_example():
    print("\n=== 經典邏輯謎題 ===\n")
    
    kb = PrologLikeSystem()
    
    kb.add_fact("人(蘇格拉底)")
    kb.add_fact("人(柏拉圖)")
    kb.add_fact("人(亞里斯多德)")
    kb.add_fact("凡人(蘇格拉底)")
    
    def mortal_rule():
        return ["人(X)"]
    
    kb.add_rule("會死(X)", mortal_rule())
    
    print("查詢: 蘇格拉底會死嗎?")
    results = kb.query("會死(蘇格拉底)")
    print(f"結果: {'是' if results else '否'}")
    
    print("\n查詢: 柏拉圖會死嗎?")
    results = kb.query("會死(柏拉圖)")
    print(f"結果: {'是' if results else '否'}")

if __name__ == "__main__":
    family_example()
    logic_puzzle_example()
```

### 1.2.5 Lisp 與符號處理

1958 年，John McCarthy 發明了 Lisp（LISt Processing）語言。Lisp 是最早的高階程式語言之一，其獨特之處在於「程式即資料」的概念——Lisp 程式本身就是由列表（List）組成的資料結構。

Lisp 的特點包括：
- **同像性 (Homoiconicity)**：程式的語法與資料結構相同
- **自動記憶體管理**：垃圾回收機制
- **互動式開發環境**：支援 REPL（Read-Eval-Print Loop）

[程式檔案：01-4-lisp-symbolic.py](../_code/01/01-4-lisp-symbolic.py)

```python
#!/usr/bin/env python3
"""
Lisp 符號處理：代數簡化
展示 Lisp 風格的符號處理 - 程式即資料的概念
"""

import re
from typing import Any, List, Union

Symbol = str
SExp = Union[Symbol, List['SExp']]

class LispSymbolic:
    def __init__(self):
        self.rules = []
    
    def add_rule(self, pattern, replacement):
        self.rules.append((pattern, replacement))
    
    def parse(self, s: str) -> SExp:
        s = s.replace('(', ' ( ').replace(')', ' ) ')
        tokens = s.split()
        
        def parse_tokens(tokens: List[str]) -> SExp:
            if not tokens:
                raise ValueError("Unexpected end of input")
            token = tokens.pop(0)
            if token == '(':
                result = []
                while tokens[0] != ')':
                    result.append(parse_tokens(tokens))
                tokens.pop(0)
                return result
            elif token == ')':
                raise ValueError("Unexpected closing parenthesis")
            else:
                try:
                    return int(token)
                except ValueError:
                    try:
                        return float(token)
                    except ValueError:
                        return token
        
        return parse_tokens(tokens)
    
    def simplify(self, expr: SExp) -> SExp:
        if isinstance(expr, (int, float)):
            return expr
        
        if isinstance(expr, Symbol):
            return expr
        
        if not isinstance(expr, list):
            return expr
        
        if len(expr) == 0:
            return expr
        
        op = expr[0]
        
        if op == '+':
            result = 0
            args = []
            for arg in expr[1:]:
                simplified = self.simplify(arg)
                if isinstance(simplified, (int, float)):
                    result += simplified
                else:
                    args.append(simplified)
            if not args and result == 0:
                return 0
            elif not args:
                return result
            elif result == 0:
                return args if len(args) == 1 else ['+'] + args
            else:
                return [result] + args + [0]
        
        if op == '*':
            result = 1
            args = []
            for arg in expr[1:]:
                simplified = self.simplify(arg)
                if isinstance(simplified, (int, float)):
                    result *= simplified
                else:
                    args.append(simplified)
            if result == 0:
                return 0
            elif not args and result == 1:
                return 1
            elif not args:
                return result
            elif result == 1:
                return args if len(args) == 1 else ['*'] + args
            else:
                return [result] + args
        
        if op == '-':
            if len(expr) == 2:
                arg = self.simplify(expr[1])
                if isinstance(arg, (int, float)):
                    return -arg
                return ['-', arg]
            else:
                left = self.simplify(expr[1])
                right = self.simplify(expr[2])
                if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                    return left - right
                return [left, '-', right]
        
        if op == '/':
            left = self.simplify(expr[1])
            right = self.simplify(expr[2])
            if isinstance(left, (int, float)) and isinstance(right, (int, float)) and right != 0:
                return left / right
            return [left, '/', right]
        
        return expr
    
    def to_string(self, expr: SExp) -> str:
        if isinstance(expr, (int, float)):
            return str(expr)
        if isinstance(expr, Symbol):
            return expr
        return '(' + ' '.join(self.to_string(x) for x in expr) + ')'

def lisp_style_example():
    print("=== Lisp 風格符號處理 ===\n")
    
    lisp = LispSymbolic()
    
    tests = [
        "(+ 1 2)",
        "(+ 1 2 3)",
        "(* 2 3)",
        "(* 2 3 0)",
        "(+ (* 2 3) 4)",
        "(- 10 5)",
        "(/ 10 2)",
        "(+ 1 (+ 2 3))",
        "(* (+ 1 2) (+ 3 4))",
    ]
    
    for test in tests:
        parsed = lisp.parse(test)
        simplified = lisp.simplify(parsed)
        result = lisp.to_string(simplified)
        print(f"{test} => {result}")

def algebraic_simplification():
    print("\n=== 代數簡化範例 ===\n")
    
    lisp = LispSymbolic()
    
    tests = [
        ["+", 1, 2],
        ["+", ["+", 1, 2], 3],
        ["*", 2, ["+", 3, 4]],
        ["+", ["*", 0, 5], 10],
        ["*", 1, ["*", 2, 3]],
    ]
    
    for test in tests:
        simplified = lisp.simplify(test)
        result = lisp.to_string(simplified)
        print(f"{test} => {result}")

if __name__ == "__main__":
    lisp_style_example()
    algebraic_simplification()
```

### 1.2.6 MYCIN：專家系統的代表作 (1976)

MYCIN 是由 Stanford 大學在 1976 年開發的醫療專家系統，用於協助診斷細菌感染和推薦抗生素治療。MYCIN 是第一個真正實用的專家系統，它的設計理念影響了後來無數的專家系統。

MYCIN 的核心特點包括：
- **不確定性推理**：使用可信度因子（Certainty Factor）處理不確定知識
- **知識庫與推理引擎分離**：便於知識的維護和更新
- **推論過程可解釋**：能夠向醫生解釋為什麼做出某個建議

[程式檔案：01-5-expert-system.py](../_code/01/01-5-expert-system.py)

```python
#!/usr/bin/env python3
"""
簡化版 MYCIN 專家系統 (1976)
最早的醫療專家系統之一，用於診斷細菌感染
展示專家系統的核心：知識庫 + 推理引擎
"""

class MYCIN:
    def __init__(self):
        self.rules = []
        self.facts = {}
    
    def add_rule(self, conditions, conclusion, certainty=1.0):
        self.rules.append({
            'conditions': conditions,
            'conclusion': conclusion,
            'certainty': certainty
        })
    
    def add_fact(self, key, value, certainty=1.0):
        self.facts[key] = (value, certainty)
    
    def get_certainty(self, key):
        if key in self.facts:
            return self.facts[key][1]
        return 0.0
    
    def infer(self):
        inferred = True
        while inferred:
            inferred = False
            for rule in self.rules:
                conditions_met = True
                min_certainty = 1.0
                
                for cond_key, cond_value in rule['conditions']:
                    if cond_key not in self.facts:
                        conditions_met = False
                        break
                    fact_value, fact_certainty = self.facts[cond_key]
                    if fact_value != cond_value:
                        conditions_met = False
                        break
                    min_certainty = min(min_certainty, fact_certainty)
                
                if conditions_met:
                    conclusion_key = rule['conclusion']
                    if conclusion_key not in self.facts:
                        new_certainty = rule['certainty'] * min_certainty
                        self.facts[conclusion_key] = (True, new_certainty)
                        inferred = True
                        print(f"推論: {conclusion_key} (可信度: {new_certainty:.2f})")
        
        return self.facts
    
    def diagnose(self, symptoms):
        for symptom, value in symptoms.items():
            self.add_fact(symptom, value)
        
        return self.infer()

def create_infection_diagnoser():
    mycin = MYCIN()
    
    mycin.add_fact("培養部位", "血液")
    mycin.add_fact("發燒", True)
    mycin.add_fact("發冷", True)
    mycin.add_fact("培養結果", "革蘭氏陰性菌")
    
    mycin.add_rule(
        [("發燒", True), ("發冷", True), ("培養結果", "革蘭氏陰性菌")],
        "感染原因"
    )
    
    mycin.add_rule(
        [("感染原因", True), ("培養部位", "血液")],
        "可能是敗血症"
    )
    
    mycin.add_rule(
        [("可能是敗血症", True)],
        "建議抗生素治療"
    )
    
    return mycin

def example_medical():
    print("=== MYCIN 風格醫療專家系統 ===\n")
    
    print("症狀輸入:")
    symptoms = {
        "發燒": True,
        "發冷": True,
        "頭痛": True,
        "頸部僵硬": True,
        "培養結果": "肺炎鏈球菌"
    }
    for k, v in symptoms.items():
        print(f"  {k}: {v}")
    
    print("\n開始診斷...")
    mycin = MYCIN()
    
    mycin.add_rule(
        [("發燒", True), ("頭痛", True), ("頸部僵硬", True)],
        "可能是腦膜炎"
    )
    
    mycin.add_rule(
        [("培養結果", "肺炎鏈球菌")],
        "細菌感染"
    )
    
    mycin.add_rule(
        [("可能是腦膜炎", True), ("細菌感染", True)],
        "細菌性腦膜炎"
    )
    
    mycin.add_rule(
        [("細菌性腦膜炎", True)],
        "建議使用抗生素"
    )
    
    mycin.add_rule(
        [("細菌性腦膜炎", True)],
        "建議使用類固醇"
    )
    
    mycin.diagnose(symptoms)
    
    print("\n" + "="*50)
    print("\n最終診斷結果:")
    for key, (value, certainty) in mycin.facts.items():
        if certainty > 0.3:
            print(f"  {key}: {value} (可信度: {certainty:.2f})")

def example_drug_recommendation():
    print("\n=== 藥物推薦系統 ===\n")
    
    mycin = MYCIN()
    
    mycin.add_fact("體重", 70)
    mycin.add_fact("過敏藥物", "青黴素")
    mycin.add_fact("腎功能", "正常")
    
    mycin.add_rule(
        [("過敏藥物", None)],
        "可以使用青黴素"
    )
    
    mycin.add_rule(
        [("腎功能", "正常")],
        "劑量不需要調整"
    )
    
    mycin.add_rule(
        [("可以使用青黴素", True), ("劑量不需要調整", True)],
        "開立青黴素"
    )
    
    mycin.infer()
    
    print("最終建議:")
    for key, (value, certainty) in mycin.facts.items():
        if certainty > 0.3:
            print(f"  {key}: {value}")

if __name__ == "__main__":
    example_medical()
    example_drug_recommendation()
```

## 1.3 AI 寒冬與復甦

### 1.3.1 第一次 AI 寒冬 (1974-1980)

到了 1970 年代中期，AI 領域開始面臨嚴重的挑戰：

1. **計算機能力不足**：當時的電腦運算速度遠遠無法滿足 AI 演算法的需求
2. **知識獲取困難**：專家系統需要大量的領域知識，而知識工程師與專家之間的溝通非常耗時
3. **過度承諾**：AI 研究者當初對 AI 的發展過於樂觀，導致期望落差

1973 年，英國政府委託 James Lighthill 進行了一份關於 AI 研究的評估報告。報告的結論是：「AI 研究在過去二十年來，沒有任何一個領域能夠產生當初承諾的重大突破。」這份報告直接導致英國政府大幅削減對 AI 研究的資助。

### 1.3.2 專家系統的興起與衰落 (1980-1990)

1980 年代，專家系統迎來了短暫的春天。1980 年，DEC 公司部署了 XCON 專家系統來配置電腦訂單，每年為公司節省約 4000 萬美元。這一成功案例激發了企業對專家系統的熱情。

然而，專家系統很快就暴露出了根本性的問題：
- **脆弱性**：專家系統只能在狹窄的領域內運作，無法處理超出知識庫範圍的情況
- **維護成本高**：知識需要不斷更新，但維護專家系統需要專業人員
- **缺乏學習能力**：專家系統無法從經驗中自動學習

到了 1980 年代末期，專家系統的熱潮開始退卻，AI 領域再次陷入低谷。

### 1.3.3 機器學習的興起 (1990-2010)

1990 年代，AI 研究開始從「知識工程」轉向「機器學習」。機器學習的核心理念是：讓電腦從資料中自動學習模式和規律，而不是由人類手動編碼知識。

這一時期的重要進展包括：
- **統計學習理論**：Vladimir Vapnik 提出了支持向量機 (SVM)
- **決策樹學習**：Ross Quinlan 發明了 ID3 和 C4.5 演算法
- **貝葉斯方法**：機率論在 AI 中的應用越來越廣泛
- **神經網路的復興**：雖然仍是邊緣領域，但深度學習的基礎研究仍在繼續

## 1.4 深度學習的興起 (2012年 AlexNet)

### 1.4.1 ImageNet 競賽與深度學習的突破

2012 年是多層次神經網路（深度學習）爆發的元年。在這一年的 ImageNet 大型視覺辨識競賽（ILSVRC）中，Alex Krizhevsky、Ilya Sutskever 和 Geoffrey Hinton 組成的團隊提交了 AlexNet 模型，以壓倒性的優勢赢得了冠軍。

AlexNet 的關鍵創新：
- **ReLU 激活函數**：大幅加速了訓練過程
- **GPU 加速**：利用 NVIDIA 的 CUDA 進行平行計算
- **Dropout 正則化**：有效防止過擬合
- **更深的神經網路**：8 層網路，遠超過之前的網路深度

AlexNet 的錯誤率為 15.3%，而第二名的錯誤率高達 26.2%。這一差距震驚了整個電腦視覺領域，也正式宣告了深度學習時代的來臨。

### 1.4.2 深度學習的成功因素

深度學習能夠成功的關鍵因素包括：

1. **大量資料**：ImageNet 提供了超過 1400 萬張標註圖片
2. **強大算力**：GPU 的平行計算能力使得訓練大型神經網路成為可能
3. **演算法創新**：ReLU、Batch Normalization、ResNet 等技術相繼出現
4. **開源生態**：TensorFlow、PyTorch 等框架降低了深度學習的門檻

## 1.5 大語言模型時代 (2017年 Transformer, 2022年 ChatGPT)

### 1.5.1 Transformer 架構的革命 (2017)

2017 年，Google 的研究團隊發表了劃時代的論文「Attention Is All You Need」，提出了 Transformer 架構。Transformer 完全基於注意力機制（Attention Mechanism），徹底拋棄了傳統的循環神經網路（RNN）。

Transformer 的核心創新：
- **自注意力機制 (Self-Attention)**：讓模型能夠同時關注序列中的所有位置
- **位置編碼 (Positional Encoding)**：為序列中的每個位置添加獨特的表示
- **平行計算**：大幅加速了訓練過程
- **可擴展性**：可以透過增加層數和參數數量來提升模型能力

### 1.5.2 GPT 系列的演進

Transformer 的提出催生了一系列大型語言模型：

- **GPT (2018)**：OpenAI 發布了第一代 GPT，使用 Transformer 解碼器
- **GPT-2 (2019)**：展示了令人驚艷的文字生成能力，但因擔心被濫用而延遲發布
- **GPT-3 (2020)**：1750 億參數的超大型模型，展示了few-shot 學習能力
- **ChatGPT (2022)**：針對對話場景優化的 GPT-3.5，掀起了生成式 AI 的熱潮
- **GPT-4 (2023)**：多模態能力，支持圖像輸入

### 1.5.3 大語言模型的湧現能力

大語言模型（Large Language Model, LLM）展示了一系列令人驚嘆的「湧現能力」(Emergent Abilities)：

1. **上下文學習 (In-Context Learning)**：透過提供少量範例，模型就能學會執行新任務
2. **思維鏈推論 (Chain-of-Thought)**：模型可以展示逐步推理的過程
3. **程式碼生成**：GPT-4 等模型可以生成高質量的程式碼
4. **多模態理解**：能夠理解和處理文字、圖像、音頻等多種形式的資訊

## 1.6 總結

從 1956 年達特茅斯會議到現在，AI 的發展經歷了多次興衰循環：

| 時期 | 代表技術 | 特點 |
|------|----------|------|
| 1956-1974 | 符號主義、邏輯推論 | 強調知識表示與推理 |
| 1974-1980 | 第一次 AI 寒冬 | 計算能力不足，期望落差 |
| 1980-1990 | 專家系統 | 知識工程，但缺乏學習能力 |
| 1990-2012 | 機器學習 | 統計學習、淺層神經網路 |
| 2012-2017 | 深度學習 | AlexNet、CNN、RNN |
| 2017-現在 | Transformer、大語言模型 | 自注意力、生成式 AI |

每一次寒冬都讓研究者更深刻地理解 AI 的困難所在，而每一次復甦都帶來了新的突破。今天的 AI 已經能夠：
- 辨識圖像中的物體
- 理解自然語言
- 生成高品質的文字、圖像和影片
- 幫助人類編寫程式碼
- 在複雜的遊戲中達到超越人類的水平

然而，我們也必須清醒地認識到：當前的 AI 仍然存在諸多限制，包括：
- 缺乏真正的理解能力
- 無法進行長期規劃
- 容易產生幻覺（生成錯誤但看似合理的資訊）
- 對抗對抗樣本攻擊的脆弱性

理解 AI 的歷史，不僅能幫助我們欣賞當前的成就，更能讓我們思考 AI 未來的發展方向。在接下來的章節中，我們將深入探討支撐現代 AI 的核心技術，從傳統的搜尋演算法到現代的深度學習架構。
