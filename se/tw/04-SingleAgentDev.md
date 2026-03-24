# 第 4 章：單一 Agent 開發

> 一人團隊的開發流程

---

## 4.1 一人團隊開發流程

> 檔案：[04-1-DevWorkflow.md](../_code/04/04-1-DevWorkflow.md)

### 標準開發流程

```
┌─────────────────────────────────────────────────────────┐
│                    開發流程                              │
├─────────────────────────────────────────────────────────┤
│  需求 → AI 生成 → 審核 → 測試 → 部署                    │
│    │                                              │    │
│    └──────────────── 迭代 ◀────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

### 每日開發循環

1. **晨間規劃**（15 分鐘）
   - 確認今日目標
   - 向 AI 描述任務

2. **開發時間**（3-4 小時）
   - AI 生成程式碼
   - 人工審核

3. **測試時間**（1 小時）
   - AI 生成測試
   - 執行驗證

4. **部署時間**（30 分鐘）
   - 部署到測試環境
   - 驗證功能

---

## 4.2 Prompt → Code → Test → Deploy

### Step 1: Prompt（需求描述）

```
請幫我建立一個使用者認證系統：
- 使用 FastAPI + JWT
- 包含註冊、登入、權驗證
- 密碼需要雜湊儲存
- 使用 SQLite 資料庫
```

### Step 2: Code（AI 生成）

AI 會生成：
- `models/user.py` - 資料模型
- `schemas/user.py` - Pydantic schema
- `routers/auth.py` - API 路由
- `auth/jwt.py` - JWT 工具

### Step 3: Test（測試生成）

```
請為上述程式碼生成單元測試：
- 測試使用者註冊
- 測試登入成功/失敗
- 測試 JWT 權杖驗證
```

### Step 4: Deploy（部署）

```bash
# 部署到 Railway
railway deploy
```

---

## 4.3 AI 輔助需求分析

> 檔案：[04-2-AIRequirementsPrompt.md](../_code/04/04-2-AIRequirementsPrompt.md)

### 需求分析 Prompt

```
我要建立一個 [產品類型]，
目標用戶是 [描述目標用戶]，
核心功能是 [列出功能]，
請幫我：
1. 細化需求
2. 產出使用者故事
3. 列出 MVP 功能優先順序
```

---

## 4.4 AI 輔助程式開發

> 檔案：[04-3-AICodePrompt.md](../_code/04/04-3-AICodePrompt.md)

### 程式開發 Prompt

```
請用 [技術棧] 建立 [功能描述]：

需求：
1. [具體需求 1]
2. [具體需求 2]

請包含：
- 錯誤處理
- 類型標註
- 基本文件說明
```

---

## 4.5 AI 輔助測試

> 檔案：[04-4-AITestPrompt.md](../_code/04/04-4-AITestPrompt.md)

### 測試生成 Prompt

```
請為以下程式碼生成 pytest 測試：

[貼上程式碼]

請包含：
- 正常情況測試
- 邊界情況測試
- 錯誤情況測試
```

---

## 4.6 部署自動化

### 一鍵部署 Prompt

```
請幫我建立部署腳本：
- 使用 Docker
- 部署到 Railway
- 包含環境變數設定
```

---

## 4.7 本章總結

一人團隊的開發流程：

1. **清晰描述需求** → AI 才能準確生成
2. **嚴格審核程式碼** → 品質把關在人
3. **自動化測試** → AI 生成 + 執行
4. **簡化部署** → 一鍵部署工具

下一章將介紹：多 Agent 協作模式。

---

## 相關範例檔案

- [04-1-DevWorkflow.md](../_code/04/04-1-DevWorkflow.md)
- [04-2-AIRequirementsPrompt.md](../_code/04/04-2-AIRequirementsPrompt.md)
- [04-3-AICodePrompt.md](../_code/04/04-3-AICodePrompt.md)
- [04-4-AITestPrompt.md](../_code/04/04-4-AITestPrompt.md)
- [04-5-DockerQuickstart.yml](../_code/04/04-5-DockerQuickstart.yml)
