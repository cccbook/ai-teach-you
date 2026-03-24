# JWT (JSON Web Token)

## 概述

JWT 是一種用於在各方之間安全傳輸資訊的開放標準。常用於使用者認證和授權。

## 結構

JWT 由三部分組成，用 `.` 分隔：

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

| 部分 | 說明 |
|------|------|
| Header | 標頭，指定演算法和類型 |
| Payload | 內容，包含宣告和資料 |
| Signature | 簽名，用於驗證真實性 |

## Header

```json
{
    "alg": "HS256",
    "typ": "JWT"
}
```

## Payload

```json
{
    "sub": "1234567890",
    "name": "王小明",
    "role": "admin",
    "iat": 1516239022,
    "exp": 1516242622
}
```

## Python 實作

```python
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def create_token(data):
    expire = datetime.utcnow() + timedelta(hours=24)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None

token = create_token({"sub": "user123", "name": "王小明"})
payload = decode_token(token)
print(payload)
```

## JavaScript 實作

```javascript
import jwt from 'jsonwebtoken';

const SECRET_KEY = "your-secret-key";

function createToken(data) {
    return jwt.sign(data, SECRET_KEY, { expiresIn: '24h' });
}

function decodeToken(token) {
    try {
        return jwt.verify(token, SECRET_KEY);
    } catch (err) {
        return null;
    }
}

const token = createToken({ sub: 'user123', name: '王小明' });
const payload = decodeToken(token);
console.log(payload);
```

## 參考資源

- [JWT 官方網站](https://jwt.io/)
- [RFC 7519](https://tools.ietf.org/html/rfc7519)
