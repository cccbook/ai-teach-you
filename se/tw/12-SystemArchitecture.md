# 第 12 章：系統架構設計

> 完整系統架構

---

## 12.1 系統架構圖

> 檔案：[12-1-SystemArchitecture.svg](../_code/12/12-1-SystemArchitecture.svg)

### 分層架構

- 表現層（Presentation）
- 業務層（Business）
- 資料層（Data）
- 基礎設施層（Infrastructure）

---

## 12.2 類別圖設計

### 主要類別

| 類別 | 職責 |
|------|------|
| User | 使用者資訊 |
| Product | 商品資訊 |
| Order | 訂單資訊 |
| Payment | 支付處理 |

---

## 12.3 元件圖

### 元件劃分

```
前端元件 → API Gateway → 後端服務 → 資料庫
```

---

## 12.4 部署架構

### 雲端部署

```
Load Balancer → Web Servers → App Servers → Database
```

---

## 12.5 ADR 架構決策記錄

> 檔案：[12-5-ADRTemplate.md](../_code/12/12-5-ADRTemplate.md)

---

## 12.6 Git Worktree 協作模式

> 檔案：[12-6-GitWorktreeSetup.md](../_code/12/12-6-GitWorktreeSetup.md)

---

## 12.7 本章總結

系統架構關鍵：

1. **清晰分层**：降低耦合
2. **文件化**：ADR 記錄決策
3. **協作工具**：Git Worktree 提升效率

---

## 相關範例檔案

- [12-1-SystemArchitecture.svg](../_code/12/12-1-SystemArchitecture.svg)
- [12-2-ClassDiagram.svg](../_code/12/12-2-ClassDiagram.svg)
- [12-3-ComponentDiagram.svg](../_code/12/12-3-ComponentDiagram.svg)
- [12-4-DeploymentDiagram.svg](../_code/12/12-4-DeploymentDiagram.svg)
- [12-5-ADRTemplate.md](../_code/12/12-5-ADRTemplate.md)
- [12-6-GitWorktreeSetup.md](../_code/12/12-6-GitWorktreeSetup.md)
