# AI 時代的軟體工程：人機協作新模式

> 從敏捷小團隊到正規軍大兵團：AI 與人類如何共同打造軟體系統

---

## 理念

傳統軟體工程書籍分成「瀑布」與「敏捷」兩大陣營，卻忽略了一個關鍵問題：**AI 如何融入？**

本書提出「人機協作」的連續光譜：

```
小團隊 ◀━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━▶ 大團隊
敏捷    │                                      │ 正規軍
        │          AI 時代的新選擇              │
        ▼                                      ▼
   快速迭代                            嚴謹治理
   AI 副駕駛                            多 Agent 協作
   少量文件                            完整規格
```

---

## 目錄

### 第一部分：一人團隊 + 多 Agent 架構

一人團隊 + 多 AI Agent + 外包 = 最敏捷的開發模式。

| 章節 | 主題 | 核心概念 |
|------|------|----------|
| [01-案例：小型敏捷專案](01-CaseAgileEcommerce.md) | 一人團隊電商從零到上線 | 完整案例展示 |
| [02-為何一人團隊](02-why-one-person-team.md) | AI 時代的開發新範式 | 從 Scrum 到 AI-Agent 團隊 |
| [03-AI-Agent-基礎](03-ai-agent-basics.md) | 認識 AI Agent 工具 | Copilot / Claude Code / Cursor |
| [04-單一-Agent-開發](04-single-agent-dev.md) | 一人團隊的開發流程 | Prompt → Code → Test → Deploy |
| [05-多-Agent-協作](05-multi-agent-collab.md) | 多 Agent 分工與協調 | 規劃 Agent + 執行 Agent + 審核 |
| [06-外包策略](06-outsourcing-strategy.md) | Agent 做不到的，用外包 | UI/UX / 雲端架構 / 資安 / 法律 |
| [07-原型迭代](07-prototype-iteration.md) | 快速原型與版本 Sprint | 2 週一個版本持續交付 |
| [08-部署監控](08-deploy-monitor.md) | 自動化上線與監控 | 一鍵部署 + AI 監控 |

### 第二部分：正規軍大兵團（AI 治理）

適合 10 人以上團隊，需要嚴謹流程與治理。

| 章節 | 主題 | 人機協作重點 |
|------|------|-------------|
| [09-案例：企業AI代理](09-case-enterprise-agent.md) | 大型 AI Agent 系統 | 完整案例展示 |
| [10-正式需求分析](10-formal-requirements.md) | 完整 SRS 規格 | AI 協助一致性檢查 |
| [11-使用者研究](11-user-research.md) | 深入理解目標使用者 | AI 分析大量訪談資料 |
| [12-系統架構設計](12-system-architecture.md) | 完整系統架構 | AI 生成 UML，架構師決策 |
| [13-技術選型](13-tech-selection.md) | 科學化技術決策 | AI 評估矩陣，技術委員會把關 |
| [14-程式開發規範](14-coding-standards.md) | 團隊程式碼標準 | AI Lint + 人類訂標準 |
| [15-Code-Review](15-code-review.md) | 程式碼審核 | AI 初審 + 人類複審 |
| [16-完整測試](16-complete-testing.md) | 全面品質確保 | AI 生成測試案例，QA 定義標準 |
| [17-CI-CD-治理](17-cicd-governance.md) | 企業級部署流程 | 多環境部署，AI 監控 |
| [18-監控與維運](18-monitoring-ops.md) | AIOps 運維 | AI AIOps，人工事件處理 |
| [19-安全與合規](19-security-compliance.md) | 資安與法規遵循 | AI 掃描 + 安全審計 |

### 第三部分：AI 工具與實踐

| 章節 | 主題 | 說明 |
|------|------|------|
| [20-提示工程](20-prompt-engineering.md) | 有效的 AI 溝通術 | 設計有效的 Prompt 策略 |
| [21-AI-Agent-實作](21-ai-agent-implementation.md) | 從 Prompt 到 Agent | 構建 AI 代理系統 |
| [22-人機團隊](22-human-ai-team.md) | 新型態角色與職責 | 人機協作下的組織 |
| [23-倫理與治理](23-ethics-governance.md) | AI 決策的歸責 | 誰該為 AI 生成的程式碼負責？ |

---

## 核心框架：人機協作連續光譜

```
小團隊 ◀━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━▶ 大團隊
敏捷    │                                      │ 正規軍
        │          AI 時代的新選擇              │
        ▼                                      ▼
   快速迭代                            嚴謹治理
   AI 副駕駛                            多 Agent 協作
   少量文件                            完整規格
        │                                      │
        ▼                                      ▼
     人工審核                              完整治理
     快速迭代                              規模擴展
```

---

## 程式碼目錄

```
_code/
├── 01/          # 第1章 案例小型敏捷專案
├── 02/          # 第2章 為何一人團隊
├── 03/          # 第3章 AI Agent 基礎
├── 04/          # 第4章 單一 Agent 開發
├── 05/          # 第5章 多 Agent 協作
├── 06/          # 第6章 外包策略
├── 07/          # 第7章 原型迭代
├── 08/          # 第8章 部署監控
├── 09/          # 第9章 案例企業AI代理
├── 10/          # 第10章 正式需求分析
├── 11/          # 第11章 使用者研究
├── 12/          # 第12章 系統架構設計
├── 13/          # 第13章 技術選型
├── 14/          # 第14章 程式開發規範
├── 15/          # 第15章 Code Review
├── 16/          # 第16章 完整測試
├── 17/          # 第17章 CI/CD治理
├── 18/          # 第18章 監控與維運
├── 19/          # 第19章 安全與合規
├── 20/          # 第20章 提示工程
├── 21/          # 第21章 AI Agent 實作
├── 22/          # 第22章 人機團隊
└── 23/          # 第23章 倫理與治理
```

---

## 專有名詞索引

* [瀑布模型](index/瀑布模型.md) - 傳統線性開發流程
* [敏捷開發](index/敏捷開發.md) - 迭代式開發方法
* [CI/CD](index/cicd.md) - 持續整合與持續部署
* [Copilot](index/copilot.md) - AI 程式碼輔助工具
* [Prompt Engineering](index/prompt.md) - AI 提示詞工程
* [Agent](index/agent.md) - AI 代理程式

---

## 參考資源

* [Anthropic Claude](https://anthropic.com/)
* [OpenAI API](https://openai.com/api/)
* [GitHub Copilot](https://github.com/features/copilot)
* [Cursor IDE](https://cursor.sh/)
* [Martin Fowler](https://martinfowler.com/)
* [Software Engineering at Google](https://abseil.io/resources/swe-book)

---

*最後更新：2026-03-24*
