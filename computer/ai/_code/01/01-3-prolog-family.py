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
