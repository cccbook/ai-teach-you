import numpy as np

class PromptEngineer:
    def __init__(self):
        self.templates = {
            "zero_shot": "Task: {task}\nInput: {input}\nOutput:",
            "few_shot": "Task: {task}\nExamples:\n{examples}\nInput: {input}\nOutput:",
            "cot": "Task: {task}\nInput: {input}\nLet's think step by step.\nOutput:",
            "style": "Task: {task}\nStyle: {style}\nInput: {input}\nOutput:",
        }
        
    def format_prompt(self, template, **kwargs):
        return self.templates[template].format(**kwargs)
    
    def zero_shot(self, task, input_text):
        return self.format_prompt("zero_shot", task=task, input=input_text)
    
    def few_shot(self, task, examples, input_text):
        ex_str = "\n".join([f"Input: {e['input']} -> Output: {e['output']}" for e in examples])
        return self.format_prompt("few_shot", task=task, examples=ex_str, input=input_text)
    
    def chain_of_thought(self, task, input_text):
        return self.format_prompt("cot", task=task, input=input_text)

pe = PromptEngineer()

zero_shot_prompt = pe.zero_shot("Sentiment analysis", "I love this product!")
few_shot_prompt = pe.few_shot(
    "Translation",
    [{"input": "hello", "output": "hola"}, {"input": "goodbye", "output": "adios"}],
    "thank you"
)
cot_prompt = pe.chain_of_thought("Math problem", "What is 23 * 17?")

print("=" * 60)
print("Prompt Engineering Demo")
print("=" * 60)

print("\n[Zero-Shot Prompting]")
print(zero_shot_prompt)

print("\n[Few-Shot Prompting]")
print(few_shot_prompt)

print("\n[Chain-of-Thought Prompting]")
print(cot_prompt)

print("\n✓ Prompt engineering techniques:")
print("  - Zero-shot: Direct task description")
print("  - Few-shot: Include examples")
print("  - Chain-of-thought: Encourage reasoning")
print("  - Style control: Specify output format/tone")
