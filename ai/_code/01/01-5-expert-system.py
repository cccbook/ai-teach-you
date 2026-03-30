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
