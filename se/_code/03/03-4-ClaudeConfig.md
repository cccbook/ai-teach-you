# Claude Code 專案設定

> 來源：第 3 章「AI Agent 基礎」

---

## 安裝 Claude Code

```bash
# 使用 npm 安裝
npm install -g @anthropic-ai/claude-code

# 或使用 homebrew
brew install anthropic/claude-code/claude
```

---

## 專案初始化

```bash
# 進入專案目錄
cd my-project

# 初始化 Claude Code
claude init

# 回答問題設定專案
? What is this project? > My web app
? What would you like to do? > Code, debug, and test
```

---

## 常用指令

| 指令 | 功能 |
|------|------|
| claude | 進入對話模式 |
| claude "prompt" | 單次執行 |
| claude --help | 說明 |

---

## 最佳實踐

### 1. 提供上下文

```
// 不好
幫我寫一個 API

// 好
幫我建立一個使用者 REST API，使用 FastAPI，
需要包含 CRUD 操作，連接到 SQLite 資料庫。
```

### 2. 指定程式碼風格

```
使用：
- Python type hints
- docstring 格式文件
- 錯誤處理要完善
```

### 3. 逐步確認

```
先給我大綱 → 確認後再實作 → 最後審核
```
