# HTTP (HyperText Transfer Protocol)

## 概述

HTTP 是應用層協定，用於網頁瀏覽器與伺服器之間的通訊。HTTP 基於請求-回應模式，是 RESTful API、網頁服務的基礎。目前廣泛使用 HTTP/1.1 和 HTTP/2，HTTP/3 也在推廣中。

## 歷史

- **1991**：HTTP 0.9（僅 GET）
- **1996**：HTTP/1.0
- **1999**：HTTP/1.1（標準化）
- **2015**：HTTP/2
- **2022**：HTTP/3

## HTTP 請求

### 1. 請求格式

```
GET /index.html HTTP/1.1\r\n
Host: www.example.com\r\n
User-Agent: Mozilla/5.0\r\n
Accept: text/html\r\n
\r\n
```

### 2. 方法

```http
GET     /api/users     # 取得資源
POST    /api/users     # 建立資源
PUT     /api/users/1   # 更新資源
DELETE  /api/users/1   # 刪除資源
PATCH   /api/users/1   # 部分更新
HEAD    /index.html   # 只取得Header
OPTIONS /api/users    # 查詢支援的方法
```

### 3. Python HTTP 客戶端

```python
import http.client

conn = http.client.HTTPConnection("www.example.com")

conn.request("GET", "/index.html")

response = conn.getresponse()
print(response.status)
print(response.read().decode())

conn.close()
```

### 4. Python requests 庫

```python
import requests

# GET
response = requests.get("https://api.example.com/data")
print(response.json())

# POST
data = {"name": "John", "age": 30}
response = requests.post("https://api.example.com/users", json=data)

# 帶 Header
headers = {"Authorization": "Bearer token"}
response = requests.get("https://api.example.com/secure", headers=headers)
```

### 5. HTTP 回應

```
HTTP/1.1 200 OK\r\n
Content-Type: text/html\r\n
Content-Length: 1234\r\n
\r\n
<html>...</html>
```

### 6. 狀態碼

```http
1xx: 資訊
  100 Continue
  101 Switching Protocols

2xx: 成功
  200 OK
  201 Created
  204 No Content

3xx: 重新導向
  301 Moved Permanently
  302 Found
  304 Not Modified

4xx: 客戶端錯誤
  400 Bad Request
  401 Unauthorized
  403 Forbidden
  404 Not Found

5xx: 伺服器錯誤
  500 Internal Server Error
  503 Service Unavailable
```

### 7. Header

```http
# 請求 Header
Host: example.com
User-Agent: Mozilla/5.0
Accept: application/json
Authorization: Bearer token

# 回應 Header
Content-Type: application/json
Content-Length: 123
Cache-Control: max-age=3600
Set-Cookie: session=abc123
```

## HTTP/2 特性

```python
# HTTP/2 多路複用
# 同一連接並行多個請求

# 伺服器推送
# 伺服器主動推送資源

# 標頭壓縮
# HPACK 壓縮

# 二進制框架
# 二進制傳輸
```

## 為什麼學習 HTTP？

1. **網頁開發**：基礎知識
2. **API 設計**：RESTful
3. **安全**：HTTPS
4. **效能**：HTTP/2, HTTP/3

## 參考資源

- RFC 7231
- MDN HTTP
- "HTTP: The Definitive Guide"
