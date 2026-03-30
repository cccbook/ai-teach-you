# 程式碼範例清單

> AI 時代的軟體工程：人機協作新模式

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

## 內容架構

### 第一部分：一人團隊 + 多 Agent 架構

一人團隊 + 多 AI Agent + 外包 = 最敏捷的開發模式。

| 範疇 | 章節 | 主題 | 核心概念 |
|------|------|------|----------|
| 案例 | 01 | 案例小型敏捷專案 | 一人團隊電商從零到上線 |
| 起動 | 02 | 為何一人團隊 | AI 時代的開發新範式 |
| 基礎 | 03 | AI Agent 基礎 | Copilot / Claude Code / Cursor |
| 開發 | 04 | 單一 Agent 開發 | Prompt → Code → Test → Deploy |
| 協作 | 05 | 多 Agent 協作 | 規劃 + 執行 + 審核 Agent |
| 外包 | 06 | 外包策略 | Agent 做不到的，用外包 |
| 迭代 | 07 | 原型迭代 | 2 週一個版本持續交付 |
| 部署 | 08 | 部署監控 | 一鍵部署 + AI 監控 |

### 第二部分：正規軍大兵團（AI 治理）

適合 10 人以上團隊，需要嚴謹流程與治理。

| 範疇 | 章節 | 主題 | 人機協作重點 |
|------|------|------|-------------|
| 案例 | 09 | 案例企業AI代理 | 大型 AI Agent 系統 |
| 規劃 | 10 | 正式需求分析 | 完整 SRS，AI 協助一致性檢查 |
| 規劃 | 11 | 使用者研究 | AI 分析大量訪談資料 |
| 設計 | 12 | 系統架構設計 | AI 生成 UML，架構師決策 |
| 設計 | 13 | 技術選型 | AI 評估矩陣，技術委員會把關 |
| 開發 | 14 | 程式開發規範 | AI Lint + 人類訂標準 |
| 開發 | 15 | Code Review | AI 初審 + 人類複審 |
| 開發 | 16 | 完整測試 | AI 生成測試案例，QA 定義標準 |
| 部署 | 17 | CI/CD 治理 | 多環境部署，AI 監控 |
| 維運 | 18 | 監控與維運 | AI AIOps，人工事件處理 |
| 維運 | 19 | 安全與合規 | AI 掃描 + 安全審計 |

### 第三部分：AI 工具與實踐

| 章節 | 主題 | 說明 |
|------|------|------|
| 20 | 提示工程 | 有效的 AI 溝通術 |
| 21 | AI Agent 實作 | 從 Prompt 到 Agent |
| 22 | 人機團隊 | 新型態角色與職責 |
| 23 | 倫理與治理 | AI 決策的歸責 |

---

## 程式碼清單

### 第一部分：一人團隊 + 多 Agent 架構

#### 第 1 章：案例 - 小型敏捷專案（電商）
- `01-1-OneManTeam.md` - 團隊運作方式
- `01-2-TechStack.md` - 技術決策
- `01-3-DevLog.md` - 開發記錄
- `01-4-DeployConfig.md` - 部署配置
- `01-5-Monitoring.md` - 監控設定

#### 第 2 章：為何一人團隊
- `02-1-一人團隊宣言.md` - 一人團隊的核心價值
- `02-2-ai能力邊界.md` - AI 能做與不能做的
- `02-3-團隊選擇決策表.md` - 何時選一人 vs 團隊

#### 第 3 章：AI Agent 基礎
- `03-1-cursor設定.json` - Cursor IDE 最佳化設定
- `03-2-claude-config.md` - Claude Code 專案設定
- `03-3-agent工具比較.md` - Copilot vs Claude vs Cursor
- `03-4-環境建置清單.md` - 開發環境檢查清單

#### 第 4 章：單一 Agent 開發
- `04-1-dev-workflow.md` - 一人團隊開發流程
- `04-2-prompt-to-deploy.md` - Prompt → Code → Test → Deploy 範例
- `04-3-ai需求分析-prompt.md` - AI 輔助需求分析
- `04-4-ai程式開發-prompt.md` - AI 輔助程式開發
- `04-5-ai測試生成-prompt.md` - AI 輔助測試生成
- `04-6-docker-quickstart.yml` - 快速開發容器

#### 第 5 章：多 Agent 協作
- `05-1-agent分工模式.md` - 多 Agent 分工策略
- `05-2-planner-executor.md` - 規劃 + 執行 Agent 範例
- `05-3-review-agent.md` - 審核 Agent 範例
- `05-4-agent通訊協議.md` - Agent 間溝通格式
- `05-5-human-in-loop.md` - 人類介入時機

#### 第 6 章：外包策略
- `06-1外包決策矩陣.md` - 什麼該外包 vs 自己做
- `06-2-uiux外包指南.md` - UI/UX 設計外包要點
- `06-3雲端顧問選擇.md` - 雲端架構顧問選擇
- `06-4資安外包清單.md` - 資安與滲透測試外包
- `06-5外包合約模板.md` - 外包合約要點

#### 第 7 章：原型迭代
- `07-1-sprint範本.md` - 2 週 Sprint 規劃範本
- `07-2-mvp定義.md` - MVP 功能定義
- `07-3-使用者回饋表.md` - 回饋收集模板
- `07-4-版本發布記錄.md` - Changelog 範本

#### 第 8 章：部署監控
- `08-1-vercel一鍵部署.md` - Vercel 部署指南
- `08-2-Railway部署.md` - Railway 部署指南
- `08-3-prometheus-light.yml` - 輕量監控
- `08-4-error-tracking.md` - 錯誤追蹤設定

---

### 第二部分：正規軍大兵團

#### 第 9 章：案例 -- 企業 AI 代理
- `09-1-企業需求-full.md` - 完整企業需求
- `09-2-架構-enterprise.svg` - 企業級架構
- `09-3-agent系統.py` - 多 Agent 協調系統
- `09-4-security-full.md` - 完整安全方案
- `09-5-compliance.md` - 合規方案

#### 第 10 章：正式需求分析
- `10-1-srs-完整範本.md` - Software Requirements Specification
- `10-2-需求追蹤矩陣.md` - Requirements Traceability Matrix
- `10-3-用例圖-full.svg` - Full Use Case Diagram
- `10-4-非功能需求清單.md` - NFR Checklist
- `10-5-ai一致性檢查-prompt.md` - AI 輔助需求一致性檢查

#### 第 11 章：使用者研究
- `11-1-人物誌模板.md` - Full Persona Template
- `11-2-同理心地圖.svg` - Empathy Map
- `11-3-使用者旅程圖-full.svg` - Detailed Journey Map
- `11-4-ai訪談分析-prompt.md` - 大量訪談資料分析

#### 第 12 章：系統架構設計
- `12-1-系統架構圖-full.svg` - 完整系統架構圖
- `12-2-類別圖.svg` - Class Diagram
- `12-3-元件圖.svg` - Component Diagram
- `12-4-部署圖.svg` - Deployment Diagram
- `12-5-adr模板.md` - Architecture Decision Record
- `12-6-git-worktree設定.md` - Git Worktree 協作設定

#### 第 13 章：技術選型
- `13-1-技術評估矩陣-full.md` - 完整技術評估
- `13-2-poc規範.md` - PoC 執行規範
- `13-3-技術決策記錄.md` - Technology Decision Record

#### 第 14 章：程式開發規範
- `14-1-coding-standards.md` - 程式碼規範手冊
- `14-2-lint-config.json` - ESLint + Prettier + TypeScript
- `14-3-git-workflow.md` - 分支策略（大型團隊）
- `14-4-commit-convention.md` - Commit 規範

#### 第 15 章：Code Review
- `15-1-review-checklist-full.md` - 完整 Review 清單
- `15-2-ai-review-prompt.md` - AI 輔助 Code Review
- `15-3-pr-template-full.md` - 詳細 PR 模板

#### 第 16 章：完整測試
- `16-1-test-plan-full.md` - 完整測試計畫
- `16-2-test-case-template.md` - 測試案例模板
- `16-3-test-pyramid.svg` - 測試金字塔
- `16-4-security-checklist.md` - 安全測試清單

#### 第 17 章：CI/CD 治理
- `17-1-github-actions-full.yml` - 完整 CI/CD Pipeline
- `17-2-environment-configs/` - 多環境設定
- `17-3-部署策略.md` - Blue-Green/CANARY
- `17-4-rollback-procedure.md` - 回滾程序

#### 第 18 章：監控與維運
- `18-1-prometheus-full.yml` - 完整監控設定
- `18-2-grafana-dashboard.json` - 企業級儀表板
- `18-3-alerting-rules.yml` - 告警規則
- `18-4-incident-response.md` - 事件回應流程

#### 第 19 章：安全與合規
- `19-1-security-policy.md` - 資安政策
- `19-2-owasp-checklist.md` - OWASP 檢查清單
- `19-3-pentest-report-template.md` - 滲透測試報告
- `19-4-compliance-checklist.md` - 合規檢查清單

---

### 第三部分：AI 工具與實踐

#### 第 20 章：提示工程
- `20-1-context-prompt.md` - 上下文設定 Prompt
- `20-2-code-gen-prompt.md` - 程式碼生成 Prompt
- `20-3-debug-prompt.md` - 錯誤除錯 Prompt
- `20-4-refactor-prompt.md` - 重構 Prompt
- `20-5-doc-prompt.md` - 文件生成 Prompt

#### 第 21 章：AI Agent 實作
- `21-1-agent架構圖.svg` - Agent 系統架構
- `21-2-agent程式碼.py` - 簡易 Agent 實作
- `21-3-tools定義.json` - Tools 定義範例
- `21-4-memory管理.md` - Context/Memory 管理
- `21-5-eval-metrics.md` - 評估指標

#### 第 22 章：人機團隊
- `22-1-角色矩陣.md` - 人類與 AI 角色定義
- `22-2-技能清單.md` - AI 時代所需技能
- `22-3-培訓計畫.md` - AI 工具培訓

#### 第 23 章：倫理與治理
- `23-1-ai使用政策.md` - AI 使用政策
- `23-2-責任矩陣.md` - 責任歸屬
- `23-3-隱私評估.md` - 隱私影響評估
- `23-4-程式碼授權.md` - AI 生成程式碼授權

---

## 檔案類型統計

| 類型 | 數量 |
|------|------|
| Markdown (.md) | ~50 |
| YAML (.yml, .yaml) | ~10 |
| JSON (.json) | ~8 |
| Python (.py) | ~5 |
| Shell (.sh) | ~3 |
| SVG 圖表 | ~8 |
| Config (.conf, .ini) | ~5 |

**總計：約 90 個範例檔案**
