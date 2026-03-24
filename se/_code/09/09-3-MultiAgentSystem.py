# 多 Agent 協調系統

> 來源：第 9 章「案例：企業 AI 代理」

---

## Agent 協調架構

```python
from typing import Dict, Any, Optional
from pydantic import BaseModel
import asyncio

class Message(BaseModel):
    role: str
    content: str
    metadata: Dict[str, Any] = {}

class AgentOrchestrator:
    """多 Agent 協調器"""
    
    def __init__(self):
        self.intent_router = IntentRouter()
        self.dialog_manager = DialogManager()
        self.llm_agent = LLMAgent()
        self.knowledge_agent = KnowledgeAgent()
        self.handoff_agent = HandoffAgent()
    
    async def process(self, user_message: str, user_id: str) -> str:
        # 1. 取得對話上下文
        context = await self.dialog_manager.get_context(user_id)
        
        # 2. 意圖識別
        intent = await self.intent_router.classify(
            message=user_message,
            context=context
        )
        
        # 3. 根據意圖分派
        if intent.action == "knowledge_query":
            response = await self.knowledge_agent.retrieve(intent)
        elif intent.action == "llm_generate":
            response = await self.llm_agent.generate(
                message=user_message,
                context=context
            )
        elif intent.action == "handoff":
            response = await self.handoff_agent.process(intent)
        else:
            response = await self.knowledge_agent.fallback(intent)
        
        # 4. 儲存對話歷史
        await self.dialog_manager.save(user_id, user_message, response)
        
        return response

class IntentRouter:
    """意圖路由器"""
    
    async def classify(self, message: str, context: Dict) -> Intent:
        # 使用 ML 模型或規則進行意圖分類
        # ...
        pass

class DialogManager:
    """對話管理器"""
    
    async def get_context(self, user_id: str) -> Dict:
        # 取得用戶對話歷史
        pass
    
    async def save(self, user_id: str, message: str, response: str):
        # 儲存對話
        pass

class LLMAgent:
    """LLM Agent"""
    
    async def generate(self, message: str, context: Dict) -> str:
        # 使用 LLM 生成回應
        pass

class KnowledgeAgent:
    """知識庫 Agent"""
    
    async def retrieve(self, intent: Intent) -> str:
        # 從知識庫檢索答案
        pass
    
    async def fallback(self, intent: Intent) -> str:
        # 無法回答時的處理
        pass

class HandoffAgent:
    """轉接 Agent"""
    
    async def process(self, intent: Intent) -> str:
        # 轉接給真人客服
        pass
```

---

## 使用範例

```python
async def main():
    orchestrator = AgentOrchestrator()
    
    response = await orchestrator.process(
        user_message="我想查詢我的帳單",
        user_id="user_123"
    )
    
    print(response)

# 執行
asyncio.run(main())
```
