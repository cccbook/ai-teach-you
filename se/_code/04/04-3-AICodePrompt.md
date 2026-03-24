# AI 輔助程式開發 Prompt

> 來源：第 4 章「單一 Agent 開發」

---

## 程式開發 Prompt 模板

### 基本模板

```
請用 [技術棧] 建立 [功能描述]：

需求：
1. [具體需求 1]
2. [具體需求 2]

請包含：
- 錯誤處理
- 類型標註
- 基本文件說明
```

### REST API 範例

```
請用 FastAPI + SQLAlchemy 建立一個商品管理 API：

需求：
1. GET /products - 商品列表（分頁）
2. GET /products/{id} - 商品詳情
3. POST /products - 新增商品
4. PUT /products/{id} - 更新商品
5. DELETE /products/{id} - 刪除商品

請包含：
- Pydantic validation
- 錯誤處理（404, 422）
- 類型標註
- docstring
```

### 前端範例

```
請用 React + TypeScript 建立一個登入表單：

需求：
1. 帳號密碼輸入
2. 登入按鈕
3. 錯誤訊息顯示
4. 登入成功轉向

請包含：
- React Hook Form
- TypeScript 類型
- Tailwind CSS 樣式
- 初步驗證
```

---

## 程式碼審核 Prompt

```
請檢查以下程式碼：

[貼上程式碼]

檢查重點：
1. 安全性（SQL Injection, XSS）
2. 錯誤處理
3. 程式碼品質
4. 效能建議
```
