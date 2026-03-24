# 第 7 章：原型迭代

> 快速原型與版本 Sprint

---

## 7.1 快速原型方法論

> 檔案：[07-1-PrototypeMethod.md](../_code/07/07-1-PrototypeMethod.md)

### 原型類型

| 類型 | 精細度 | 用途 | 工具 |
|------|--------|------|------|
| 低保真 | 紙本/線框 | 驗證概念 | Figma |
| 中保真 | 可互動 | 測試流程 | Figma |
| 高保真 | 接近成品 | 最終確認 | Figma/Code |

### AI 輔助原型

```
Prompt：請幫我生成登入頁面的 HTML/CSS
```

---

## 7.2 Sprint 規劃

> 檔案：[07-2-SprintPlanning.md](../_code/07/07-2-SprintPlanning.md)

### 2 週 Sprint 結構

```
Week 1: 開發
- Day 1-2: 新功能開發
- Day 3-4: 整合測試
- Day 5: Bug 修復

Week 2: 準備上線
- Day 6-7: 測試
- Day 8-9: 部署 staging
- Day 10: 發布
```

### Sprint Planning Prompt

```
這是第 X 個 Sprint，請幫我規劃：

產品目標：[目標]
可用時間：2 週
團隊資源：1 人

請產出：
1. Sprint Goal
2. User Stories（優先順序）
3. Task 清單
```

---

## 7.3 MVP 到 PMF

> 檔案：[07-3-MVPToPMF.md](../_code/07/07-3-MVPToPMF.md)

### MVP 定義

| 版本 | 功能 | 目標 |
|------|------|------|
| MVP 1.0 | 核心功能 | 驗證可行性 |
| MVP 1.5 | 優化體驗 | 提高轉換 |
| MVP 2.0 | 擴充功能 | 增加價值 |

### PMF 指標

| 指標 | 目標 |
|------|------|
| 轉換率 | > 3% |
| 留存率 | > 40% |
| NPS | > 30 |
| 用戶增長 | > 10%/月 |

---

## 7.4 使用者回饋循環

> 檔案：[07-4-FeedbackLoop.md](../_code/07/07-4-FeedbackLoop.md)

### 回饋收集方式

| 方式 | 適用階段 | 成本 |
|------|----------|------|
| 訪談 | 早期 | 高 |
| 問卷 | 中期 | 中 |
| 分析工具 | 後期 | 低 |
| 客服對話 | 持續 | 低 |

### 回饋分析 Prompt

```
請分析以下使用者回饋：

[貼上回饋內容]

請產出：
1. 問題分類
2. 優先順序
3. 建議解決方案
```

---

## 7.5 版本規劃

### 版本號碼規則

```
major.minor.patch
  │     │    └─ Bug 修復
  │     └─────── 新功能（向後相容）
  └───────────── 重大變更（不相容）
```

### Changelog 格式

```markdown
## [1.0.0] - 2024-01-01

### 新增
- 使用者登入功能
- 商品列表功能

### 修正
- 首頁載入速度優化

### 移除
- 舊版 API
```

---

## 7.6 本章總結

原型迭代關鍵：

1. **快速產出**：用 AI 加速開發
2. **2 週迭代**：固定節奏
3. **收集回饋**：持續改進
4. **數據驅動**：PMF 指標追蹤

下一章將介紹：部署監控。

---

## 相關範例檔案

- [07-1-PrototypeMethod.md](../_code/07/07-1-PrototypeMethod.md)
- [07-2-SprintPlanning.md](../_code/07/07-2-SprintPlanning.md)
- [07-3-MVPToPMF.md](../_code/07/07-3-MVPToPMF.md)
- [07-4-FeedbackLoop.md](../_code/07/07-4-FeedbackLoop.md)
