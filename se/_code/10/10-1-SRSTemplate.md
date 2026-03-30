# SRS 完整範本

> 來源：第 10 章「正式需求分析」

---

## 1.  Introduction

### 1.1 Purpose

本文件定義 [產品名稱] 的軟體需求規格。

### 1.2 Scope

描述產品的範圍和目標。

### 1.3 Definitions

| 術語 | 定義 |
|------|------|
| API | 應用程式介面 |
| UI | 使用者介面 |

---

## 2.  Overall Description

### 2.1 Product Perspective

描述產品在系統中的位置。

### 2.2 User Characteristics

| 角色 | 描述 |
|------|------|
| 管理員 | 系統管理 |
| 一般用戶 | 使用功能 |

---

## 3.  Specific Requirements

### 3.1 Functional Requirements

```
REQ-001: 使用者登入
描述：使用者可使用帳號密碼登入系統
```

### 3.2 Non-Functional Requirements

| 需求 | 目標 |
|------|------|
| 效能 | 回應時間 < 200ms |
| 可用性 | 99.9% |

### 3.3 Interface Requirements

| 類型 | 規格 |
|------|------|
| API | RESTful |
| UI | Web + Mobile |
