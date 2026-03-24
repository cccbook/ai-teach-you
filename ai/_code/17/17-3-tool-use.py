import numpy as np

class Tool:
    def __init__(self, name, func):
        self.name = name
        self.func = func
        
    def run(self, args):
        return self.func(args)

class ToolUseAgent:
    def __init__(self):
        self.tools = {}
        self.history = []
        
    def register_tool(self, name, func):
        self.tools[name] = Tool(name, func)
        
    def select_tool(self, query):
        if "search" in query.lower():
            return "search"
        elif "calculate" in query.lower():
            return "calculator"
        elif "weather" in query.lower():
            return "weather"
        return None
    
    def execute(self, query):
        tool_name = self.select_tool(query)
        if tool_name and tool_name in self.tools:
            result = self.tools[tool_name].run({"query": query})
            self.history.append({"tool": tool_name, "result": result})
            return result
        return "No suitable tool found"

def search_tool(args):
    return f"Search results for: {args['query']}"

def calc_tool(args):
    return "Calculation result: 42"

def weather_tool(args):
    return "Weather: Sunny, 72°F"

agent = ToolUseAgent()
agent.register_tool("search", search_tool)
agent.register_tool("calculator", calc_tool)
agent.register_tool("weather", weather_tool)

queries = [
    "Search for Python tutorials",
    "Calculate 5*8",
    "What's the weather today?"
]

print("=" * 60)
print("Tool Use Agent Demo")
print("=" * 60)
print("\nQuery -> Tool Selection:")
for q in queries:
    result = agent.execute(q)
    print(f"\nQuery: '{q}'")
    print(f"Result: {result}")

print("\n✓ Tool use enables agents to:")
print("  - Call external APIs and functions")
print("  - Access real-time information")
print("  - Perform computations")
print("  - Extend capabilities beyond base model")
