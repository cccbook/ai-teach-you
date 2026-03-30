# OAuth 2.0

## 概述

OAuth 2.0 是一個授權框架，允許第三方應用取得對使用者帳戶的有限存取權限，而無需共享密碼。

## 授權流程

```
+--------+                               +---------------+
|        |--(A)- Authorization Grant ->|   Resource   |
|        |                               |     Owner    |
|        |<-(B)-- Authorization Grant ---|               |
|        |                               +---------------+
|        |
|        |                               +---------------+
|        |--(C)-- Authorization Grant -->| Authorization |
| Client |                               |     Server   |
|        |<-(D)----- Access Token -------|               |
|        |                               +---------------+
|        |
|        |                               +---------------+
|        |--(E)----- Access Token ------>|    Resource  |
|        |                               |     Server   |
|        |<-(F)--- Protected Resource ---|               |
+--------+                               +---------------+
```

## 授權類型

### 授權碼流程（Authorization Code）

最適合有後端的 Web 應用：

```
https://authorization-server.com/authorize?
    response_type=code&
    client_id=your-client-id&
    redirect_uri=https://your-app.com/callback&
    scope=read profile&
    state=random-state-string
```

### 隱式流程（Implicit）

不推薦，已被逐步淘汰。

### 密碼憑證流程（Password Credentials）

僅用於信任的第一方應用：

```python
# FastAPI 範例
from fastapi import Depends, OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # 驗證使用者名稱和密碼
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401)
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
```

### 用戶端憑證流程（Client Credentials）

用於機器對機器通訊：

```python
def get_client_token(client_id, client_secret):
    # 驗證用戶端
    if verify_client(client_id, client_secret):
        return create_client_token(client_id)
```

## Scope 範圍

定義存取的權限範圍：

| Scope | 說明 |
|-------|------|
| `read` | 唯讀存取 |
| `write` | 寫入存取 |
| `profile` | 讀取使用者資料 |
| `email` | 讀取電子郵件 |
| `offline_access` | 取得刷新令牌 |

## 參考資源

- [OAuth 2.0 官方網站](https://oauth.net/2/)
- [RFC 6749](https://tools.ietf.org/html/rfc6749)
