# 第 3 章：AI Agent 基礎

> 認識 AI Agent 工具

---

## 3.1 主流 AI Agent 工具介紹

> 檔案：[03-1-AgentToolsComparison.md](../_code/03/03-1-AgentToolsComparison.md)

### Copilot

GitHub Copilot 是最早的 AI 程式碼輔助工具：

- **定位**：程式碼自動完成
- **特色**：根據上下文預測下一行程式碼
- **費用**：$10/月
- **適合**：快速輸入、重複程式碼

### Claude Code

Anthropic 推出的 Claude Code 更強調推理能力：

- **定位**：AI 開發夥伴
- **特色**：強大的理解能力，可進行複雜對話
- **費用**：$20/月（Pro）
- **適合**：重構、除錯、架構建議

### Cursor

結合 IDE 與 AI 的新一代工具：

- **定位**：AI-first IDE
- **特色**：完整 IDE 功能 + AI 深度整合
- **費用**：$20/月（Pro）
- **適合**：需要完整 IDE 的開發

---

## 3.2 工具選擇建議

| 使用場景 | 推薦工具 | 理由 |
|----------|----------|------|
| 快速補全程式碼 | Copilot | 輕量、快速 |
| 複雜重構 | Claude Code | 推理能力強 |
| 從零開始專案 | Cursor | IDE 整合好 |
| 除錯分析 | Claude Code | 上下文理解強 |
| 文件生成 | Claude Code | 生成品質高 |

---

## 3.3 Agent 運作原理

### 基礎架構

```
使用者 Prompt
     │
     ▼
┌─────────────┐
│   理解意圖   │ ← 大語言模型
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   規劃行動   │ ← ReAct/Chain-of-Thought
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   執行工具   │ ← Tools/Function Calling
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   生成回應   │
└─────────────┘
```

### 關鍵能力

1. **上下文理解**：理解專案結構、程式碼風格
2. **工具調用**：可執行命令、搜尋檔案
3. **記憶保持**：跨對話保持狀態
4. **迭代改進**：根據回饋修正輸出

---

## 3.4 環境建置

> 檔案：[03-2-EnvSetup.md](../_code/03/03-2-EnvSetup.md)

### Cursor 環境建置

```bash
# 1. 下載 Cursor
# https://cursor.sh/

# 2. 安裝後開啟資料夾

# 3. 登入帳號

# 4. 設定 Model（Settings → Model）
#    - Default: GPT-4
#    - Sonnet: 免費額度

# 5. 設定快捷鍵
#    - Cmd+K: 輸入 Prompt
#    - Cmd+L: 開啟 Chat
#    - Cmd+I: 開啟 Composer
```

### Claude Code 環境建置

```bash
# 1. 安裝
npm install -g @anthropic-ai/claude-code

# 2. 登入
claude auth

# 3. 初始化專案
claude init

# 4. 使用
claude "幫我建立一個 REST API"
```

---

## 3.5 本章總結

選擇 AI Agent 工具時：

1. **Copilot**：適合輕量補全
2. **Claude Code**：適合複雜推理
3. **Cursor**：適合完整開發體驗

下一章將介紹：如何使用單一 Agent 進行開發。

---

## 相關範例檔案

- [03-1-AgentToolsComparison.md](../_code/03/03-1-AgentToolsComparison.md)
- [03-2-EnvSetup.md](../_code/03/03-2-EnvSetup.md)
- [03-3-CursorSettings.json](../_code/03/03-3-CursorSettings.json)
- [03-4-ClaudeConfig.md](../_code/03/03-4-ClaudeConfig.md)
