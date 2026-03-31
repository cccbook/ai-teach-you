# CORS (Cross-Origin Resource Sharing)

## 概述

CORS 是一種 W3C 規範，允許網頁從一個網域請求另一個網域的資源。瀏覽器出於安全考量實作同源策略，CORS 提供了一種安全的跨域請求方式。

## 同源策略

以下條件都相同時，請求才是同源的：

- 協定（http/https）
- 網域（example.com）
- 連接埠（80/443/3000）

```
https://example.com/page.html
├── https://api.example.com    ✗ 不同網域
├── https://example.com:3000   ✗ 不同連接埠
├── http://example.com         ✗ 不同協定
└── https://example.com/admin ✓ 同源
```

## FastAPI CORS 配置

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 允許的來源
    allow_credentials=True,                     # 允許攜帶憑證
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # 允許的方法
    allow_headers=["*"],                        # 允許的標頭
)

@app.get("/api/data")
async def get_data():
    return {"message": "Hello from API"}
```

## CORS 標頭

### 伺服器回應

| 標頭 | 說明 |
|------|------|
| `Access-Control-Allow-Origin` | 允許的來源 |
| `Access-Control-Allow-Methods` | 允許的 HTTP 方法 |
| `Access-Control-Allow-Headers` | 允許的請求標頭 |
| `Access-Control-Allow-Credentials` | 允許攜帶憑證 |
| `Access-Control-Max-Age` | 預檢請求快取時間 |

### 預檢請求（Preflight）

瀏覽器自動發送的 OPTIONS 請求：

```
OPTIONS /api/data HTTP/1.1
Origin: http://localhost:3000
Access-Control-Request-Method: POST
Access-Control-Request-Headers: Content-Type, Authorization
```

## 常見錯誤

```
Access to fetch at 'http://localhost:8000/api/data' from origin 
'http://localhost:3000' has been blocked by CORS policy: 
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

解決方案：

1. 伺服器端正確配置 CORS
2. 使用代理伺服器
3. 開發環境使用 Vite/Webpack 代理

## 參考資源

- [MDN CORS 文檔](https://developer.mozilla.org/zh-TW/docs/Web/HTTP/CORS)
- [W3C CORS 規範](https://www.w3.org/TR/cors/)
