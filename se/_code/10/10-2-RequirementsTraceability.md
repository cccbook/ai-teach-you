# 需求追蹤矩陣

> 來源：第 10 章「正式需求分析」

---

## 矩陣格式

| ID | 需求描述 | 來源 | 優先 | 狀態 | 測試案例 |
|----|----------|------|------|------|----------|
| REQ-001 | 使用者登入功能 | PM | P0 | Done | TC-001 |
| REQ-002 | 商品列表顯示 | PM | P0 | Done | TC-002 |
| REQ-003 | 購物車功能 | Stakeholder | P0 | In Progress | TC-003 |
| REQ-004 | 訂單管理 | PM | P1 | Pending | TC-004 |
| REQ-005 | 庫存管理 | Stakeholder | P1 | Pending | TC-005 |

---

## 追蹤規則

1. 每個需求有唯一 ID
2. 優先順序：P0 > P1 > P2
3. 狀態：Pending → In Progress → Done
4. 每個需求關聯測試案例
