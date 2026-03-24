# Agent 通訊協議

> 來源：第 5 章「多 Agent 協作」

---

## 訊息類型

| 類型 | 用途 | 範例 |
|------|------|------|
| task | 分派任務 | Planner → Executor |
| status | 狀態回報 | Executor → Planner |
| result | 結果交付 | Executor → Reviewer |
| approval | 審批確認 | Human → Agent |
| error | 錯誤報告 | Agent → Human |

---

## 訊息格式

### Task 訊息

```json
{
  "type": "task",
  "id": "task-001",
  "from": "planner",
  "to": "executor",
  "timestamp": "2024-01-01T10:00:00Z",
  "content": {
    "task": "建立使用者 REST API",
    "requirements": [
      "FastAPI",
      "JWT 認證",
      "SQLite"
    ],
    "priority": "high",
    "deadline": "2024-01-01T12:00:00Z"
  },
  "context": {
    "project": "my-app",
    "language": "python",
    "framework": "fastapi"
  }
}
```

### Status 訊息

```json
{
  "type": "status",
  "id": "status-001",
  "from": "executor",
  "to": "planner",
  "timestamp": "2024-01-01T11:00:00Z",
  "status": "in_progress",
  "progress": "60%",
  "issues": []
}
```

### Result 訊息

```json
{
  "type": "result",
  "id": "result-001",
  "from": "executor",
  "to": "reviewer",
  "timestamp": "2024-01-01T11:30:00Z",
  "content": {
    "files": [
      "app/routers/user.py",
      "app/schemas/user.py"
    ],
    "tests": [
      "tests/test_user.py"
    ]
  }
}
```
