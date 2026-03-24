import numpy as np

class ReActAgent:
    def __init__(self):
        self.thoughts = []
        self.actions = []
        self.observations = []
        
    def think(self, context):
        thought = f"Analyzing: {context[:30]}..."
        self.thoughts.append(thought)
        return thought
    
    def act(self, thought):
        action = f"search({context_from_thought(thought)})"
        self.actions.append(action)
        return action
    
    def observe(self, action, result):
        obs = f"Result of {action}: {result}"
        self.observations.append(obs)
        return obs
    
    def run(self, query, max_steps=3):
        context = query
        for step in range(max_steps):
            thought = self.think(context)
            action = self.act(thought)
            result = "relevant info found"
            obs = self.observe(action, result)
            context = obs
            
            if "answer" in obs.lower():
                break
                
        return self.observations

def context_from_thought(thought):
    return "query"

agent = ReActAgent()
result = agent.run("What is the capital of France?")

print("=" * 60)
print("ReAct (Reasoning + Acting) Agent Demo")
print("=" * 60)
print("\nThought-Action-Observation trace:")
for i, (t, a, o) in enumerate(zip(agent.thoughts, agent.actions, agent.observations)):
    print(f"\nStep {i+1}:")
    print(f"  Thought: {t}")
    print(f"  Action: {a}")
    print(f"  Observation: {o[:50]}...")

print("\n✓ ReAct combines reasoning (thought) with acting (action)")
print("  and observing results in an interleaved manner")
