#!/usr/bin/env python3
"""
Chapter 11-5: GPT API Demo
使用 OpenAI GPT API 進行文本生成
"""

import json
import time

class GPTAPI:
    def __init__(self, api_key=None):
        self.api_key = api_key or "demo-key"
        self.model = "gpt-4"
        self.max_tokens = 100
        
    def chat_completion(self, messages, temperature=0.7, top_p=1.0):
        response = {
            "id": f"chatcmpl-{hash(str(messages)) % 1000000}",
            "model": self.model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "This is a simulated response. In production, use openai.OpenAI() API."
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": sum(len(m["content"].split()) for m in messages),
                "completion_tokens": 20,
                "total_tokens": sum(len(m["content"].split()) for m in messages) + 20
            }
        }
        
        return response
    
    def generate(self, prompt, system_prompt=None):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self.chat_completion(messages)
        return response["choices"][0]["message"]["content"]

def demo():
    print("=" * 60)
    print("Chapter 11-5: GPT API Demo")
    print("=" * 60)
    
    print("\n[Setup] API Configuration")
    gpt = GPTAPI(api_key="sk-...")
    print(f"  Model: {gpt.model}")
    print(f"  Max tokens: {gpt.max_tokens}")
    
    print("\n[Usage] Basic Chat Completion")
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is machine learning?"},
    ]
    
    response = gpt.chat_completion(messages)
    print(f"  Response ID: {response['id']}")
    print(f"  Content: {response['choices'][0]['message']['content']}")
    print(f"  Tokens used: {response['usage']['total_tokens']}")
    
    print("\n[Parameters]")
    print("  • temperature: 控制隨機性 (0=確定性, 2=創意)")
    print("  • top_p: nucleus sampling 閾值")
    print("  • max_tokens: 最大生成 tokens")
    print("  • presence_penalty: 降低重複")
    print("  • frequency_penalty: 降低高頻詞")
    
    print("\n[Advanced Usage]")
    print("  Streaming:")
    print('    response = client.chat.completions.create(')
    print('        model="gpt-4",')
    print('        messages=[{"role": "user", "content": "Hello"}],')
    print('        stream=True')
    print('    )')
    
    print("\n[Code Example]")
    code = '''
from openai import OpenAI

client = OpenAI(api_key="sk-...")
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "你是有用的助手"},
        {"role": "user", "content": "解釋什麼是深度學習"}
    ],
    temperature=0.7,
    max_tokens=500
)

print(response.choices[0].message.content)
'''
    print(code)
    
    print("\n[Models Available]")
    print("  • gpt-4-turbo: 最新 4o 模型")
    print("  • gpt-4: 強大但較慢")
    print("  • gpt-3.5-turbo: 快速，便宜")
    print("  • gpt-3.5-turbo-instruct: 指令調優版本")
    
    print("\n[Pricing]")
    print("  GPT-4: $30-60 / 1M tokens (input/output)")
    print("  GPT-3.5: $0.50-2 / 1M tokens (input/output)")
    
    print("\n[Best Practices]")
    print("  1. 使用 system prompt 定義行為")
    print("  2. 提供具體上下文和範例")
    print("  3. 控制 temperature 平衡確定性與創意")
    print("  4. 使用 Few-shot prompting")
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    print("=" * 60)

if __name__ == "__main__":
    demo()