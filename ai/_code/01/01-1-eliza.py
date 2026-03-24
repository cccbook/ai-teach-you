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
