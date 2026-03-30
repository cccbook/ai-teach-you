# FastAPI

## 概述

FastAPI 是一個現代、快速的 Python Web 框架，用於建立 RESTful API。它基於 Starlette 框架，使用 Pydantic 進行資料驗證。

## 特點

- **高性能**：與 Node.js 和 Go 相當
- **開發速度快**：自動 API 文件
- **類型安全**：完整的 Type hints 支援
- **自動驗證**：Pydantic 模型自動驗證

## 基本範例

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    description: str = None

items_db = {}

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}

@app.post("/items/")
async def create_item(item: Item):
    items_db[item.name] = item
    return item

@app.get("/items/{item_name}")
async def get_item(item_name: str):
    if item_name in items_db:
        return items_db[item_name]
    return {"error": "Item not found"}
```

## 路由裝飾器

```python
@app.get("/items")           # 取得資源
@app.post("/items")          # 建立資源
@app.put("/items/{id}")      # 更新資源
@app.delete("/items/{id}")   # 刪除資源
@app.patch("/items/{id}")    # 部分更新
```

## Pydantic 模型

```python
from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(None, ge=0, le=150)
    is_active: bool = True
```

## 依賴注入

```python
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/")
async def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()
```

## 認證

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # 驗證 token
    user = verify_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return user
```

## 參考資源

- [FastAPI 官方文檔](https://fastapi.tiangolo.com/)
- [Pydantic 文檔](https://docs.pydantic.dev/)
