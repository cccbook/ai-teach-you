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
