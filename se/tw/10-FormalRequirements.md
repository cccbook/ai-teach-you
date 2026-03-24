# 第 10 章：正式需求分析

> 完整 SRS 規格

---

## 10.1 SRS 文件結構

> 檔案：[10-1-SRSTemplate.md](../_code/10/10-1-SRSTemplate.md)

### 文件大綱

```
1.  Introduction
    1.1 Purpose
    1.2 Scope
    1.3 Definitions

2.  Overall Description
    2.1 Product Perspective
    2.2 User Characteristics
    2.3 Constraints

3.  Specific Requirements
    3.1 Functional Requirements
    3.2 Non-Functional Requirements
    3.3 Interface Requirements
```

---

## 10.2 需求追蹤矩陣

> 檔案：[10-2-RequirementsTraceability.md](../_code/10/10-2-RequirementsTraceability.md)

### 矩陣格式

| ID | 需求描述 | 來源 | 優先 | 狀態 | 測試案例 |
|----|----------|------|------|------|----------|
| REQ-001 | 使用者登入 | Stakeholder | P0 | Done | TC-001 |

---

## 10.3 用例圖

### 用例圖元素

- Actor（參與者）
- Use Case（用例）
- Include/Extend（關係）

---

## 10.4 非功能需求

### NFR 類型

| 類型 | 範例 |
|------|------|
| 效能 | 回應時間 < 200ms |
| 安全性 | 加密儲存 |
| 可用性 | 支援多種裝置 |
| 擴展性 | 支援百萬用戶 |

---

## 10.5 AI 輔助一致性檢查

### Prompt

```
請檢查以下需求文件的一致性：

[貼上需求]

檢查：
1. 需求是否有矛盾
2. 需求是否完整
3. 需求是否可測試
```

---

## 10.6 本章總結

正式需求分析關鍵：

1. **完整文件**：SRS 結構化
2. **追蹤矩陣**：需求可追溯
3. **AI 輔助**：加速一致性檢查

---

## 相關範例檔案

- [10-1-SRSTemplate.md](../_code/10/10-1-SRSTemplate.md)
- [10-2-RequirementsTraceability.md](../_code/10/10-2-RequirementsTraceability.md)
- [10-3-UseCaseDiagram.svg](../_code/10/10-3-UseCaseDiagram.svg)
- [10-4-NFRChecklist.md](../_code/10/10-4-NFRChecklist.md)
