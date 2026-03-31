# 第 5 章：多 Agent 協作

> 多 Agent 分工與協調

---

## 5.1 多 Agent 分工模式

> 檔案：[05-1-AgentRoles.md](../_code/05/05-1-AgentRoles.md)

### Agent 角色分類

| Agent 角色 | 功能 | 工具 |
|------------|------|------|
| Planner Agent | 任務規劃、分解 | Claude |
| Executor Agent | 程式碼生成 | Cursor |
| Review Agent | 程式碼審核 | Claude |
| Tester Agent | 測試生成 | Claude |
| Deploy Agent | 部署自動化 | Claude |

### 協作流程

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Planner    │────▶│  Executor    │────▶│   Review     │
│    Agent     │     │    Agent    │     │    Agent     │
└──────────────┘     └──────────────┘     └──────────────┘
       │                     │                    │
       │ 任務分解              │ 程式碼產出          │ 審核結果
       ▼                     ▼                    ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  任務清單     │     │  程式碼檔案   │     │  審核報告    │
└──────────────┘     └──────────────┘     └──────────────┘
```

---

## 5.2 規劃 + 執行 + 審核 Agent

### Planner Agent

```
你是一個任務規劃專家。請將以下任務分解為可執行的步驟：

任務：[描述最終目標]

請輸出：
1. 主要步驟清單
2. 每步的依賴關係
3. 預估難度
```

### Executor Agent

```
請根據以下任務生成程式碼：

任務：[任務描述]
技術棧：[技術選型]

請生成完整可運作的程式碼。
```

### Review Agent

```
請審核以下程式碼：

[貼上程式碼]

請檢查：
1. 安全性
2. 錯誤處理
3. 程式碼品質
4. 效能建議
```

---

## 5.3 Agent 間溝通協議

> 檔案：[05-2-AgentProtocol.md](../_code/05/05-2-AgentProtocol.md)

### 訊息格式

```json
{
  "type": "task",
  "from": "planner",
  "to": "executor",
  "content": {
    "task": "建立使用者 API",
    "requirements": ["REST", "JWT", "SQLite"]
  },
  "context": {
    "project": "my-app",
    "language": "python"
  }
}
```

### 狀態回報

```json
{
  "type": "status",
  "from": "executor",
  "to": "planner",
  "status": "in_progress",
  "progress": "50%",
  "issues": []
}
```

---

## 5.4 人類在多 Agent 中的角色

### Human-in-the-Loop

```
何時需要人類介入：
1. 任務目標確認
2. 關鍵決策點
3. 品質把關
4. 緊急問題處理
```

### 介入時機

| 階段 | 自動化程度 | 人類介入 |
|------|------------|----------|
| 任務規劃 | 80% | 20% 確認 |
| 程式生成 | 90% | 10% 審核 |
| 測試生成 | 80% | 20% 確認 |
| 部署上線 | 70% | 30% 確認 |

---

## 5.5 本章總結

多 Agent 協作模式：

1. **明確分工**：每個 Agent 有特定角色
2. **結構化溝通**：使用 JSON 格式傳遞訊息
3. **人類把關**：關鍵節點需要人類確認
4. **持續迭代**：根據結果調整 Agent 行為

下一章將介紹：外包策略。

---

## 相關範例檔案

- [05-1-AgentRoles.md](../_code/05/05-1-AgentRoles.md)
- [05-2-AgentProtocol.md](../_code/05/05-2-AgentProtocol.md)
- [05-3-HumanInLoop.md](../_code/05/05-3-HumanInLoop.md)
- [05-4-AgentToolsDefinition.json](../_code/05/05-4-AgentToolsDefinition.json)
