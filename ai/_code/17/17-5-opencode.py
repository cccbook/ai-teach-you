import numpy as np

class OpenCodeAgent:
    def __init__(self):
        self.tools = {
            "read": self.read_file,
            "write": self.write_file,
            "edit": self.edit_file,
            "bash": self.run_command,
            "glob": self.search_files,
            "grep": self.search_content,
        }
        
    def read_file(self, args):
        return f"Reading {args.get('filePath', 'file')}..."
    
    def write_file(self, args):
        return f"Writing to {args.get('filePath', 'file')}..."
    
    def edit_file(self, args):
        return f"Editing {args.get('filePath', 'file')}..."
    
    def run_command(self, args):
        return f"Running: {args.get('command', 'cmd')}"
    
    def search_files(self, args):
        return f"Glob: {args.get('pattern', '*')}"
    
    def search_content(self, args):
        return f"Grep: {args.get('pattern', '')}"
    
    def execute(self, action, args):
        if action in self.tools:
            return self.tools[action](args)
        return "Unknown tool"

agent = OpenCodeAgent()

actions = [
    ("read", {"filePath": "main.py"}),
    ("bash", {"command": "python main.py"}),
    ("grep", {"pattern": "def "}),
]

print("=" * 60)
print("OpenCode Agent Demo")
print("=" * 60)
print("\nAvailable tools:")
for tool in agent.tools.keys():
    print(f"  - {tool}")

print("\nTool execution:")
for action, args in actions:
    result = agent.execute(action, args)
    print(f"\n{action}({args}):")
    print(f"  {result}")

print("\n✓ OpenCode agent capabilities:")
print("  - File operations (read/write/edit)")
print("  - Shell command execution")
print("  - Code search and navigation")
print("  - Multi-step task execution")
