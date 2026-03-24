# 第 13 章：FastAPI 基礎

## 概述

FastAPI 是一個現代、快速的 Python Web 框架，用於建立 API。本章介紹 FastAPI 的基礎知識，包括路由、請求處理和資料驗證。

## 13.1 第一個 FastAPI 應用

讓我們從建立第一個 FastAPI 應用開始。

[程式檔案：13-1-hello.py](../_code/13/13-1-hello.py)

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**執行方式：**
```bash
uvicorn main:app --reload
```

## 13.2 基本路由

使用裝飾器定義路由端點。

[程式檔案：13-2-route-basic.py](../_code/13/13-2-route-basic.py)

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Home page"}

@app.get("/about")
async def about():
    return {"message": "About page"}

@app.get("/contact")
async def contact():
    return {"message": "Contact page"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 13.3 HTTP 方法

FastAPI 支援所有 HTTP 方法。

[程式檔案：13-3-route-methods.py](../_code/13/13-3-route-methods.py)

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def get_data():
    return {"method": "GET"}

@app.post("/")
async def create_data():
    return {"method": "POST"}

@app.put("/")
async def update_data():
    return {"method": "PUT"}

@app.delete("/")
async def delete_data():
    return {"method": "DELETE"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 13.4 路徑參數

使用路徑參數捕捉 URL 中的動態值。

[程式檔案：13-4-path-parameter.py](../_code/13/13-4-path-parameter.py)

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return {"item_id": item_id, "name": f"Item {item_id}"}

@app.get("/users/{user_id}/posts/{post_id}")
async def get_user_post(user_id: int, post_id: int):
    return {
        "user_id": user_id,
        "post_id": post_id,
        "content": "Post content"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 13.5 查詢參數

使用查詢參數處理可選的過濾條件。

[程式檔案：13-5-query-parameter.py](../_code/13/13-5-query-parameter.py)

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/search")
async def search(q: str, page: int = 1, limit: int = 10):
    return {
        "query": q,
        "page": page,
        "limit": limit,
        "results": []
    }

@app.get("/items")
async def list_items(category: str = None, sort: str = "asc"):
    return {
        "category": category,
        "sort": sort,
        "items": []
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 13.6 請求主體

使用 Pydantic 模型處理請求主體。

[程式檔案：13-6-request-body.py](../_code/13/13-6-request-body.py)

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    quantity: int

@app.post("/items/")
async def create_item(item: Item):
    return {"item": item, "status": "created"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 13.7 Pydantic 模型

Pydantic 提供強大的資料驗證和設定管理。

[程式檔案：13-7-pydantic-model.py](../_code/13/13-7-pydantic-model.py)

```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()

class User(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(None, ge=0, le=150)
    is_active: bool = True

@app.post("/users/")
async def create_user(user: User):
    return {"user": user}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 13.8 回應模型

使用 response_model 定義 API 回應格式。

[程式檔案：13-8-response-model.py](../_code/13/13-8-response-model.py)

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    price: float

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    message: str

items_db = [
    {"id": 1, "name": "Item 1", "price": 10.0},
    {"id": 2, "name": "Item 2", "price": 20.0},
]

@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    item = next((i for i in items_db if i["id"] == item_id), None)
    if item:
        return {**item, "message": "Item found"}
    return {"error": "Item not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 13.9 錯誤處理

使用 HTTPException 處理錯誤。

[程式檔案：13-9-error-handler.py](../_code/13/13-9-error-handler.py)

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

items_db = {"1": {"name": "Item 1"}, "2": {"name": "Item 2"}}

@app.get("/items/{item_id}")
async def get_item(item_id: str):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return {"error": "Invalid value"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 13.10 靜態檔案

提供靜態檔案服務。

[程式檔案：13-10-static-files.py](../_code/13/13-10-static-files.py)

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"message": "Check /static for static files"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 重點回顧

| 概念 | 說明 |
|------|------|
| FastAPI | 現代 Python Web 框架 |
| @app.get/post/... | 路由裝飾器 |
| 路徑參數 | URL 中的動態值 |
| 查詢參數 | URL 中的可選參數 |
| Pydantic | 資料驗證和設定 |
| HTTPException | 錯誤處理 |

## 練習題

1. 建立一個使用者 API（CRUD）
2. 實作分頁和搜尋功能
3. 建立產品分類 API
4. 實作自訂錯誤回應格式
