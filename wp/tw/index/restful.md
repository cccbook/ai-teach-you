# RESTful API

## 概述

REST（Representational State Transfer，表現層狀態轉換）是一種 API 設計架構風格，廣泛用於 Web 服務設計。

## 核心原則

1. **客戶端-伺服器架構**：客戶端和伺服器分離
2. **無狀態**：每個請求包含所有必要資訊
3. **可快取**：回應可標記為可快取或不可快取
4. **分層系統**：客戶端不知道中間層的存在
5. **統一介面**：標準化的資源操作方式

## 資源導向

REST 使用 URI 來識別資源：

```
GET    /users          # 取得所有使用者
GET    /users/1        # 取得 ID 為 1 的使用者
POST   /users          # 建立新使用者
PUT    /users/1        # 更新 ID 為 1 的使用者
DELETE /users/1        # 刪除 ID 為 1 的使用者
```

## HTTP 方法對應

| 方法 | 用途 | 語意 |
|------|------|------|
| GET | 取得資源 | 安全、冪等 |
| POST | 建立資源 | 不安全、不冪等 |
| PUT | 更新資源（完整） | 冪等 |
| PATCH | 更新資源（部分） | 不冪等 |
| DELETE | 刪除資源 | 冪等 |

## 狀態碼

### 成功回應

| 狀態碼 | 意義 |
|--------|------|
| 200 | OK |
| 201 | Created |
| 204 | No Content |

### 客戶端錯誤

| 狀態碼 | 意義 |
|--------|------|
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Unprocessable Entity |

### 伺服器錯誤

| 狀態碼 | 意義 |
|--------|------|
| 500 | Internal Server Error |
| 502 | Bad Gateway |
| 503 | Service Unavailable |

## 最佳實踐

1. **使用名詞而非動詞**： `/users` 而非 `/getUsers`
2. **使用複數**： `/users` 而非 `/user`
3. **巢狀資源**：`/users/1/posts/3`
4. **版本控制**：`/v1/users`
5. **分頁**：`/users?page=1&limit=20`
6. **錯誤回應格式**：

```json
{
    "error": {
        "code": "USER_NOT_FOUND",
        "message": "使用者不存在"
    }
}
```

## 參考資源

- [REST API 設計最佳實踐](https://restfulapi.net/)
- [HTTP 狀態碼](https://developer.mozilla.org/zh-TW/docs/Web/HTTP/Status)
