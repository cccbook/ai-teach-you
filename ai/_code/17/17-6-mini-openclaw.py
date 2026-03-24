import numpy as np

class MiniClaw:
    def __init__(self):
        self.file_tools = ["read", "write", "edit"]
        self.shell_tools = ["bash", "run"]
        self.search_tools = ["glob", "grep"]
        
    def plan(self, task):
        if "write" in task and "file" in task:
            return ["write"]
        elif "search" in task or "find" in task:
            return ["grep", "read"]
        elif "run" in task or "execute" in task:
            return ["bash"]
        return ["read", "bash"]
    
    def execute(self, plan, args):
        results = []
        for action in plan:
            if action == "write":
                results.append(f"Writing file: {args.get('filePath', 'file')}")
            elif action == "read":
                results.append(f"Reading file: {args.get('filePath', 'file')}")
            elif action == "grep":
                results.append(f"Searching: {args.get('pattern', '')}")
            elif action == "bash":
                results.append(f"Running: {args.get('command', '')}")
        return results

claw = MiniClaw()

tasks = [
    "Write hello to test.py",
    "Find all Python files",
    "Run main.py",
]

print("=" * 60)
print("Mini OpenClaw Agent Demo")
print("=" * 60)

for task in tasks:
    plan = claw.plan(task)
    results = claw.execute(plan, {"filePath": "test.py", "command": "python test.py"})
    print(f"\nTask: '{task}'")
    print(f"Plan: {plan}")
    print(f"Results: {results}")

print("\n✓ OpenClaw is an autonomous coding agent that:")
print("  - Plans multi-step tasks")
print("  - Uses file/shell/search tools")
print("  - Executes code and fixes errors")
print("  - Operates in terminal environments")
