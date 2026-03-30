# 第 16 章：認證與授權

## 概述

安全性是 API 開發的重要環節。本章介紹 JWT 認證、密碼雜湊、OAuth2 等認證機制。

## 16.1 密碼雜湊

安全儲存使用者密碼。

[程式檔案：16-1-password-hash.py](../_code/16/16-1-password-hash.py)

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

if __name__ == "__main__":
    hashed = hash_password("mysecretpassword")
    print(f"Hashed: {hashed}")
    print(f"Verify: {verify_password('mysecretpassword', hashed)}")
    print(f"Wrong: {verify_password('wrongpassword', hashed)}")
```

## 16.2 JWT Token 生成

JWT 用於安全的身份驗證。

[程式檔案：16-2-jwt-token.py](../_code/16/16-2-jwt-token.py)

```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from pydantic import BaseModel

SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class TokenData(BaseModel):
    username: str | None = None

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenData(username=payload.get("sub"))
    except JWTError:
        return None

if __name__ == "__main__":
    token = create_access_token({"sub": "user123"})
    print(f"Token: {token}")
    data = decode_token(token)
    print(f"Decoded: {data}")
```

## 16.3 OAuth2 基礎

OAuth2 是授權的開放標準。

[程式檔案：16-3-oauth2-basic.py](../_code/16/16-3-oauth2-basic.py)

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

users_db = {
    "user1": {"username": "user1", "password": "password123"},
    "user2": {"username": "user2", "password": "password456"}
}

def authenticate_user(username: str, password: str):
    user = users_db.get(username)
    if not user or user["password"] != password:
        return None
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    from 16-2-jwt-token import decode_token
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    token_data = decode_token(token)
    if token_data is None or token_data.username is None:
        raise credentials_exception
    return token_data

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    from 16-2-jwt-token import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}
```

## 16.4 登入端點

實作完整的登入功能。

[程式檔案：16-4-login-endpoint.py](../_code/16/16-4-login-endpoint.py)

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str

users_db = {
    "alice": {"username": "alice", "password": "alice123"},
    "bob": {"username": "bob", "password": "bob123"}
}

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    from 16-2-jwt-token import create_access_token
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}
```

## 16.5 受保護路由

使用 JWT 保護 API 端點。

[程式檔案：16-5-protected-route.py](../_code/16/16-5-protected-route.py)

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    from 16-2-jwt-token import decode_token
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )
    token_data = decode_token(token)
    if token_data is None or token_data.username is None:
        raise credentials_exception
    return {"username": token_data.username}

@app.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {
        "message": "You have access!",
        "user": current_user["username"]
    }

@app.get("/public")
async def public_route():
    return {"message": "This is public"}

@app.get("/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return {"username": current_user["username"]}
```

## 16.6 依賴注入認證

使用 FastAPI 依賴注入系統進行認證。

[程式檔案：16-6-dependencies.py](../_code/16/16-6-dependencies.py)

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from pydantic import BaseModel, SecurityRequirement

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    scopes: list[str] = []

def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    
    from 16-2-jwt-token import decode_token
    token_data = decode_token(token)
    
    if token_data is None or token_data.username is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {"username": token_data.username, "scopes": []}

@app.get("/items/")
async def read_items(current_user: User = Depends(get_current_user)):
    return [{"item": "Item 1"}, {"item": "Item 2"}]

@app.get("/users/me")
async def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user
```

## 16.7 Refresh Token

實作 Token 刷新機制。

[程式檔案：16-7-refresh-token.py](../_code/16/16-7-refresh-token.py)

```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from pydantic import BaseModel

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str, expected_type: str = "access"):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != expected_type:
            return None
        return payload
    except JWTError:
        return None

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

if __name__ == "__main__":
    access = create_access_token({"sub": "user123"})
    refresh = create_refresh_token({"sub": "user123"})
    print(f"Access: {access}")
    print(f"Refresh: {refresh}")
```

## 16.8 權限管理

實作基於角色的存取控制（RBAC）。

[程式檔案：16-8-permissions.py](../_code/16/16-8-permissions.py)

```python
from enum import Enum
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class User(BaseModel):
    username: str
    role: Role

users_db = {
    "admin": {"username": "admin", "role": Role.ADMIN},
    "user1": {"username": "user1", "role": Role.USER},
    "guest1": {"username": "guest1", "role": Role.GUEST}
}

def get_current_user(token: str = Depends(oauth2_scheme)):
    from 16-2-jwt-token import decode_token
    token_data = decode_token(token)
    if not token_data or not token_data.username:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return users_db.get(token_data.username)

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

@app.get("/admin")
async def admin_only(user: User = Depends(require_admin)):
    return {"message": "Welcome, admin!", "user": user.username}

@app.get("/user")
async def user_route(user: User = Depends(get_current_user)):
    return {"message": "Welcome!", "user": user.username}
```

## 16.9 CORS 配置

配置跨來源資源共享。

[程式檔案：16-9-cors-config.py](../_code/16/16-9-cors-config.py)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://myfrontend.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

@app.get("/")
async def root():
    return {"message": "CORS enabled"}

@app.get("/api/data")
async def get_data():
    return {"data": "Protected data"}

@app.post("/api/submit")
async def submit_data(data: dict):
    return {"received": data, "status": "success"}
```

## 16.10 安全最佳實踐

開發安全 API 的重要原則。

[程式檔案：16-10-security-tips.py](../_code/16/16-10-security-tips.py)

```python
import secrets
from hashlib import scrypt

def hash_password_secure(password: str) -> str:
    salt = secrets.token_hex(16)
    hashed = scrypt(password.encode(), salt=salt.encode(), n=16384, r=8, p=1)
    return f"{salt}${hashed.hex()}"

def verify_password_secure(password: str, stored_hash: str) -> bool:
    salt, hash_hex = stored_hash.split("$")
    expected = scrypt(password.encode(), salt=salt.encode(), n=16384, r=8, p=1).hex()
    return secrets.compare_digest(hash_hex, expected)

TIPS = [
    "Use HTTPS in production",
    "Store secrets in environment variables",
    "Implement rate limiting",
    "Validate all input on server side",
    "Use parameterized queries to prevent SQL injection",
    "Implement CSRF protection",
    "Use secure session management",
    "Keep dependencies updated",
    "Implement proper logging",
    "Use security headers (CSP, HSTS, etc.)"
]

if __name__ == "__main__":
    for tip in TIPS:
        print(f"- {tip}")
```

## 重點回顧

| 概念 | 說明 |
|------|------|
| 密碼雜湊 | 安全儲存密碼（bcrypt） |
| JWT | JSON Web Token |
| OAuth2 | 授權框架 |
| 認證 | 驗證使用者身份 |
| 授權 | 控制存取權限 |
| RBAC | 基於角色的存取控制 |
| CORS | 跨來源資源共享 |

## 練習題

1. 實作完整的註冊和登入功能
2. 建立 JWT 認證的中介軟體
3. 實作多角色權限系統
4. 建立安全的密碼重置功能
