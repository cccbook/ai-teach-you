# 第 17 章：代理人技術 (Agent)

AI Agent（智慧代理人）是近年來人工智慧領域最重要的發展方向之一。與傳統的對話系統不同，Agent 能夠自主規劃、執行行動、並從反饋中學習。本章將介紹 AI Agent 的核心概念、ReAct 框架、工具使用、記憶機制，以及如何建構自主代理人系統。

## 17.1 AI Agent 概念與架構

AI Agent 是能夠感知環境、做出決策並執行行動的智慧系統。

[程式檔案：17-1-agent-basic.py](../_code/17/17-1-agent-basic.py)

```python
import numpy as np

class SimpleAgent:
    def __init__(self, state_dim, action_dim):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.policy = np.random.randn(state_dim, action_dim) * 0.1
        
    def perceive(self, observation):
        return observation @ self.policy
    
    def decide(self, perception):
        return np.argmax(perception)
    
    def act(self, action):
        return f"Action {action} executed"
    
    def run(self, observation):
        perception = self.perceive(observation)
        action = self.decide(perception)
        result = self.act(action)
        return result

agent = SimpleAgent(state_dim=10, action_dim=4)

observation = np.random.randn(10)
result = agent.run(observation)

print("=" * 60)
print("Basic Agent Demo")
print("=" * 60)
print(f"State dimension: 10")
print(f"Action dimension: 4")
print(f"\nObservation: {observation[:5]}...")
print(f"Result: {result}")
print("\n✓ Simple agent architecture:")
print("  1. Perceive: Process observation")
print("  2. Decide: Choose action based on perception")
print("  3. Act: Execute the chosen action")
```

### 17.1.1 Agent 的核心組成

```
AI Agent 架構：

┌─────────────────────────────────────────────────────────┐
│                    Agent System                         │
│                                                         │
│   ┌───────────┐                                        │
│   │ Perception │ ←── 環境觀測 (Observation)             │
│   └─────┬─────┘                                        │
│         ↓                                              │
│   ┌───────────┐                                        │
│   │ Reasoning │ ←── 規劃、推理、決策                    │
│   └─────┬─────┘                                        │
│         ↓                                              │
│   ┌───────────┐                                        │
│   │   Action  │ ──→ 執行行動                           │
│   └───────────┘                                        │
│         ↓                                              │
│   ┌───────────┐                                        │
│   │  Memory   │ ←── 短期/長期記憶                       │
│   └───────────┘                                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
         ↑                              ↓
         └─────────── 環境 ────────────┘
```

### 17.1.2 Agent vs 傳統 AI

| 特性 | 傳統 AI | AI Agent |
|------|---------|----------|
| 互動方式 | 被動回應 | 主動探索 |
| 規劃能力 | 無 | 有 |
| 工具使用 | 無 | 有 |
| 持久記憶 | 無 | 有 |
| 自主性 | 低 | 高 |

### 17.1.3 Agent 的類型

| 類型 | 說明 | 應用場景 |
|------|------|----------|
| 反射 Agent | 基於當前狀態直接響應 | 簡單機械人 |
| 基於模型的 Agent | 維護環境模型 | 遊戲 AI |
| 目標導向 Agent | 規劃達成特定目標 | 任務自動化 |
| 效用 Agent | 最大化預期效用 | 決策系統 |
| 學習 Agent | 從經驗中學習 | 遊戲、機器人 |

## 17.2 ReAct 推理與行動框架

ReAct (Reasoning + Acting) 是一種結合推理和行動的 AI Agent 框架。

[程式檔案：17-2-react.py](../_code/17/17-2-react.py)

```python
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
```

### 17.2.1 ReAct 的核心思想

ReAct 的核心理念是讓 AI 在執行任務時進行「思考」，而不是直接給出答案：

```
ReAct 循環：

┌─────────┐
│  Thought │ ← 我需要搜索什麼？
└────┬────┘
     ↓
┌─────────┐
│  Action  │ ← 執行搜索
└────┬────┘
     ↓
┌─────────┐
│Observation│ ← 獲得結果
└────┬────┘
     ↓
     ↓ ← 迴圈
```

### 17.2.2 ReAct 的優勢

| 優勢 | 說明 |
|------|------|
| 可解釋性 | 清晰的思考過程 |
| 錯誤修正 | 可追蹤推理錯誤 |
| 靈活性 | 可適應不同任務 |
| 可靠性 | 減少幻覺和錯誤 |

### 17.2.3 ReAct Prompt 模板

```python
REACT_TEMPLATE = """
你是一個能夠思考和行動的助手。

任務：{task}

讓我們按照以下步驟進行：

{examples}

現在開始你的任務：
"""

def generate_react_prompt(task, examples):
    steps = []
    for i, (thought, action, obs) in enumerate(examples):
        steps.append(f"Thought {i+1}: {thought}")
        steps.append(f"Action {i+1}: {action}")
        steps.append(f"Observation {i+1}: {obs}")
    
    return REACT_TEMPLATE.format(task=task, examples="\n".join(steps))
```

## 17.3 Tool Use 與 Function Calling

工具使用是 Agent 系統的核心能力，使其能夠與外部世界互動。

[程式檔案：17-3-tool-use.py](../_code/17/17-3-tool-use.py)

```python
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
```

### 17.3.1 工具使用流程

```
工具使用流程：

使用者查詢
    ↓
意圖識別 ──→ 選擇工具
    ↓
參數提取
    ↓
執行工具
    ↓
結果解析
    ↓
回應生成
```

### 17.3.2 常用工具類型

| 工具類型 | 說明 | 範例 |
|----------|------|------|
| 搜索 | 網路搜索 | Google, Bing |
| 計算 | 數學計算 | Calculator, Wolfram |
| 天氣 | 天氣資訊 | OpenWeather |
| 地圖 | 地理位置 | Google Maps |
| 代碼 | 程式執行 | Python, REPL |
| 文件 | 文件處理 | PDF, CSV |

### 17.3.3 Function Calling 實現

```python
# OpenAI Function Calling 格式
FUNCTIONS = [
    {
        "name": "get_weather",
        "description": "獲取指定城市的天氣資訊",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名稱"
                }
            },
            "required": ["city"]
        }
    }
]

def call_function(name, arguments):
    if name == "get_weather":
        city = arguments["city"]
        return get_weather(city)
```

## 17.4 Memory 與長期記憶機制

記憶機制使 Agent 能夠跨會話保持上下文和學習。

[程式檔案：17-4-memory.py](../_code/17/17-4-memory.py)

```python
import numpy as np
from collections import deque

class Memory:
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.buffer = deque(maxlen=capacity)
        
    def add(self, experience):
        self.buffer.append(experience)
        
    def sample(self, batch_size):
        indices = np.random.choice(len(self.buffer), batch_size, replace=False)
        return [self.buffer[i] for i in indices]

class AgentMemory:
    def __init__(self, short_term_capacity=10, long_term_capacity=100):
        self.short_term = deque(maxlen=short_term_capacity)
        self.long_term = Memory(long_term_capacity)
        
    def add_short(self, memory):
        self.short_term.append(memory)
        
    def transfer_to_long(self):
        for m in self.short_term:
            self.long_term.add(m)
        self.short_term.clear()
        
    def retrieve(self, query, k=3):
        return list(self.long_term.buffer)[-k:]

memory = AgentMemory()

memory.add_short({"role": "user", "content": "Hello"})
memory.add_short({"role": "assistant", "content": "Hi!"})
memory.add_short({"role": "user", "content": "What's 2+2?"})
memory.transfer_to_long()

retrieved = memory.retrieve("greeting")

print("=" * 60)
print("Agent Memory Demo")
print("=" * 60)
print(f"Short-term capacity: 10")
print(f"Long-term capacity: 100")
print("\nCurrent memories:")
print(f"  Short-term: {list(memory.short_term)}")
print(f"  Retrieved: {retrieved}")
print("\n✓ Agent memory types:")
print("  - Short-term: Current conversation context")
print("  - Long-term: Persistent knowledge base")
print("  - Transfer: Summary to long-term")
print("  - Retrieval: Relevant context recall")
```

### 17.4.1 記憶層級架構

```
Agent 記憶架構：

┌─────────────────────────────────────────────────────────┐
│                   Working Memory                         │
│   • 當前對話上下文                                       │
│   • 活躍的任務狀態                                       │
│   • 容量：有限                                          │
└─────────────────────────────────────────────────────────┘
                          ↓ 摘要/壓縮
┌─────────────────────────────────────────────────────────┐
│                  Episodic Memory                         │
│   • 過去經驗的結構化存儲                                │
│   • 情境記憶                                             │
│   • 容量：中等                                          │
└─────────────────────────────────────────────────────────┘
                          ↓ 提取/索引
┌─────────────────────────────────────────────────────────┐
│                  Semantic Memory                         │
│   • 結構化知識                                           │
│   • 概念和事實                                           │
│   • 容量：大量                                          │
└─────────────────────────────────────────────────────────┘
```

### 17.4.2 記憶檢索

```python
class MemoryRetrieval:
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
    
    def retrieve_relevant(self, query, memories, top_k=5):
        query_embedding = self.embedding_model.encode(query)
        
        scores = []
        for memory in memories:
            memory_embedding = self.embedding_model.encode(memory["content"])
            score = cosine_similarity(query_embedding, memory_embedding)
            scores.append((memory, score))
        
        scores.sort(key=lambda x: x[1], reverse=True)
        return [m for m, s in scores[:top_k]]
```

## 17.5 OpenCode、Claude Code、Codex 等程式工具

程式碼相關的 Agent 是目前最成功的應用場景之一。

[程式檔案：17-5-opencode.py](../_code/17/17-5-opencode.py)

```python
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
```

### 17.5.1 OpenCode 工具系統

| 工具 | 功能 | 使用場景 |
|------|------|----------|
| read | 讀取文件內容 | 查看代碼 |
| write | 創建新文件 | 生成代碼 |
| edit | 修改文件 | 修補代碼 |
| bash | 執行命令 | 運行測試 |
| glob | 搜索文件 | 查找文件 |
| grep | 搜索內容 | 定位代碼 |

### 17.5.2 Claude Code 的架構

Claude Code 是 Anthropic 推出的程式碼 Agent：

```
Claude Code 架構：

┌─────────────────────────────────────────────────────────┐
│                 Claude (LLM)                            │
│   • 理解任務                                            │
│   • 生成行動計劃                                        │
│   • 推理和決策                                          │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                   Tool System                           │
│   • Bash: 執行命令                                      │
│   • Read/Edit: 文件操作                                │
│   • Glob/Grep: 搜索                                     │
│   • WebSearch: 網路搜索                                 │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                  Sandbox Environment                   │
│   • 文件系統                                            │
│   • 進程隔離                                            │
│   • 安全控制                                            │
└─────────────────────────────────────────────────────────┘
```

## 17.6 實作：建構 AI 助手

讓我們實現一個簡化的 AI 助手來展示 Agent 的核心功能。

[程式檔案：17-6-mini-openclaw.py](../_code/17/17-6-mini-openclaw.py)

```python
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
```

### 17.6.1 任務規劃器

```python
class TaskPlanner:
    def __init__(self):
        self.task_templates = {
            "write_code": ["read", "write", "bash"],
            "fix_bug": ["grep", "read", "edit", "bash"],
            "add_feature": ["read", "grep", "edit", "test"],
            "refactor": ["read", "analyze", "edit", "test"]
        }
    
    def plan(self, task_description):
        task_lower = task_description.lower()
        
        if "write" in task_lower and "new" in task_lower:
            return self.task_templates["write_code"]
        elif "fix" in task_lower or "bug" in task_lower:
            return self.task_templates["fix_bug"]
        elif "add" in task_lower and "feature" in task_lower:
            return self.task_templates["add_feature"]
        elif "refactor" in task_lower:
            return self.task_templates["refactor"]
        
        return ["read", "bash"]
```

### 17.6.2 自我修正迴圈

```python
class SelfCorrection:
    def __init__(self, max_attempts=3):
        self.max_attempts = max_attempts
    
    def execute_with_retry(self, agent, task):
        for attempt in range(self.max_attempts):
            result = agent.execute(task)
            
            if self.validate_result(result):
                return result
            
            # 根據錯誤反饋調整
            error = self.analyze_error(result)
            task = self.modify_task(task, error)
        
        return {"status": "failed", "attempts": self.max_attempts}
    
    def validate_result(self, result):
        # 檢查結果是否正確
        return result.get("success", False)
```

### 17.6.3 Agent 系統架構總覽

```
完整 Agent 系統架構：

┌─────────────────────────────────────────────────────────────┐
│                      User Interface                          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      Task Manager                           │
│   • 任務解析                                                │
│   • 目標分解                                                │
│   • 執行計劃                                                │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Reasoning Engine                         │
│   • ReAct 推理                                             │
│   • Chain-of-Thought                                        │
│   • 自我反思                                                │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                     Tool Executor                           │
│   • 工具調用                                                │
│   • 結果解析                                                │
│   • 錯誤處理                                                │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      Memory System                          │
│   • 短期記憶                                                │
│   • 長期記憶                                                │
│   • 經驗總結                                                │
└─────────────────────────────────────────────────────────────┘
```

## 17.7 總結

本章介紹了 AI Agent 的核心概念和技術：

| 組件 | 說明 |
|------|------|
| 感知 | 處理環境輸入 |
| 推理 | 思考和規劃 |
| 行動 | 執行工具和任務 |
| 記憶 | 保持上下文和經驗 |

| 框架 | 特點 |
|------|------|
| ReAct | 推理+行動的循環 |
| Tool Use | 外部工具整合 |
| Memory | 多層級記憶系統 |

AI Agent 代表了人工智慧從「回答問題」到「解決問題」的進化。隨著工具使用能力、推理能力和記憶機制的不斷完善，Agent 系統正在成為人工智慧應用的新範式。
