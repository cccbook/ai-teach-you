# AI Agent 工具比較

> 來源：第 3 章「AI Agent 基礎」

---

## 主流工具比較表

| 特性 | GitHub Copilot | Claude Code | Cursor |
|------|----------------|-------------|--------|
| 開發商 | Microsoft + OpenAI | Anthropic | Anysphere |
| 基礎模型 | GPT-4 | Claude 3 | GPT-4 + Claude |
| 費用 | $10/月 | $20/月 | $20/月 |
| IDE 整合 | VS Code | 終端機 | 自有 IDE |
| 程式碼補全 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 對話理解 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 重構能力 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 除錯能力 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 文件生成 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## 使用場景推薦

### Copilot 最佳場景

```
// 快速補全重複程式碼
function calculateTotal(items) {
  return items.reduce((sum, item) => {
    return sum + item.price * item.quantity;
  }, 0);
}

// Copilot 會自動建議：
// .toFixed(2) 等格式化
```

### Claude Code 最佳場景

```
使用者：我的 API 效能很差，請幫我分析

Claude：讓我先看一下你的程式碼結構...

[分析後給出詳細建議]
- 資料庫查詢沒有索引
- N+1 查詢問題
- 快取策略建議
```

### Cursor 最佳場景

```
// Cmd+I 打開 Composer
// 輸入：建立一個使用者認證系統

Cursor 會：
1. 建立 auth router
2. 建立 middleware
3. 建立測試檔案
4. 設定環境變數
```

---

## 選擇決策樹

```
需要做什麼？
  │
  ├─ 快速補全程式碼 → Copilot
  │
  ├─ 複雜重構/除錯 → Claude Code
  │
  ├─ 從零開始專案 → Cursor
  │
  └─ 需要視覺化介面 → Cursor
```
