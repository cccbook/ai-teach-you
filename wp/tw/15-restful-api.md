# 第 15 章：RESTful API 設計

## 概述

RESTful API 是現代 Web 服務的主流架構風格。本章介紹如何設計高品質的 RESTful API。

## 15.1 REST 基礎概念

REST（Representational State Transfer）是一種 API 設計架構。

[程式檔案：15-1-rest-basics.py](../_code/15/15-1-rest-basics.py)

```python
from fastapi import FastAPI

app = FastAPI()

items_db = {}

@app.get("/items")
async def list_items():
    return {"items": list(items_db.values())}

@app.post("/items")
async def create_item(item_id: int, name: str):
    item = {"id": item_id, "name": name}
    items_db[item_id] = item
    return {"item": item, "status": "created"}

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id not in items_db:
        return {"error": "Not found"}
    return items_db[item_id]

@app.put("/items/{item_id}")
async def update_item(item_id: int, name: str):
    if item_id not in items_db:
        return {"error": "Not found"}
    items_db[item_id]["name"] = name
    return items_db[item_id]

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id in items_db:
        del items_db[item_id]
    return {"status": "deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 15.2 CRUD 端點

完整的 CRUD API 端點設計。

[程式檔案：15-2-crud-endpoints.py](../_code/15/15-2-crud-endpoints.py)

```python
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    price: float

items_db = {}

@app.get("/items", response_model=list[Item])
async def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    items = list(items_db.values())
    return items[skip:skip+limit]

@app.post("/items", response_model=Item, status_code=201)
async def create_item(item: Item):
    if item.id in items_db:
        raise HTTPException(status_code=400, detail="Item exists")
    items_db[item.id] = item
    return item

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Not found")
    return items_db[item_id]

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Not found")
    items_db[item_id] = item
    return item

@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int):
    if item_id in items_db:
        del items_db[item_id]
```

## 15.3 分頁實作

實作分頁功能處理大量資料。

[程式檔案：15-3-pagination.py](../_code/15/15-3-pagination.py)

```python
from fastapi import FastAPI, Query
from typing import Optional

app = FastAPI()

items_db = [{"id": i, "name": f"Item {i}"} for i in range(1, 101)]

@app.get("/items")
async def list_items(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    start = (page - 1) * page_size
    end = start + page_size
    
    return {
        "items": items_db[start:end],
        "total": len(items_db),
        "page": page,
        "page_size": page_size,
        "total_pages": (len(items_db) + page_size - 1) // page_size
    }

@app.get("/items/cursor")
async def cursor_pagination(
    cursor: Optional[int] = None,
    limit: int = Query(10, ge=1, le=100)
):
    start = 0
    if cursor:
        start = next((i for i, item in enumerate(items_db) if item["id"] == cursor), 0) + 1
    
    return {
        "items": items_db[start:start+limit],
        "next_cursor": items_db[start+limit]["id"] if start+limit < len(items_db) else None
    }
```

## 15.4 篩選功能

實作多條件篩選。

[程式檔案：15-4-filtering.py](../_code/15/15-4-filtering.py)

```python
from fastapi import FastAPI, Query
from typing import Optional, List

app = FastAPI()

items_db = [
    {"id": 1, "name": "Apple", "category": "fruit", "price": 1.0},
    {"id": 2, "name": "Banana", "category": "fruit", "price": 0.5},
    {"id": 3, "name": "Carrot", "category": "vegetable", "price": 0.8},
]

@app.get("/items")
async def filter_items(
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    search: Optional[str] = None,
    tags: Optional[List[str]] = Query(None)
):
    results = items_db.copy()
    
    if category:
        results = [i for i in results if i["category"] == category]
    
    if min_price is not None:
        results = [i for i in results if i["price"] >= min_price]
    
    if max_price is not None:
        results = [i for i in results if i["price"] <= max_price]
    
    if search:
        results = [i for i in results if search.lower() in i["name"].lower()]
    
    return {"items": results, "count": len(results)}
```

## 15.5 排序功能

實作多欄位排序。

[程式檔案：15-5-sorting.py](../_code/15/15-5-sorting.py)

```python
from fastapi import FastAPI, Query
from typing import Optional

app = FastAPI()

items_db = [
    {"id": i, "name": f"Item {i}", "price": i * 10.0}
    for i in range(1, 21)
]

@app.get("/items")
async def sort_items(
    sort_by: str = Query("id", regex="^(id|name|price)$"),
    order: str = Query("asc", regex="^(asc|desc)$")
):
    reverse = order == "desc"
    sorted_items = sorted(items_db, key=lambda x: x[sort_by], reverse=reverse)
    
    return {"items": sorted_items}

@app.get("/items/multisort")
async def multi_sort(
    primary: str = Query("price"),
    secondary: str = Query("name")
):
    sorted_items = sorted(items_db, key=lambda x: (x[primary], x[secondary]))
    return {"items": sorted_items}
```

## 15.6 資料驗證

使用 Pydantic 進行嚴格的資料驗證。

[程式檔案：15-6-validation.py](../_code/15/15-6-validation.py)

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator

app = FastAPI()

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., regex=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    age: int = Field(None, ge=0, le=150)
    
    @validator("name")
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int = None

users_db = {}
user_id_counter = 1

@app.post("/users/", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate):
    global user_id_counter
    
    if any(u.email == user.email for u in users_db.values()):
        raise HTTPException(status_code=400, detail="Email already exists")
    
    user_id = user_id_counter
    user_id_counter += 1
    
    user_data = user.model_dump()
    user_data["id"] = user_id
    users_db[user_id] = user_data
    
    return user_data
```

## 15.7 錯誤回應格式

統一錯誤回應格式。

[程式檔案：15-7-error-responses.py](../_code/15/15-7-error-responses.py)

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi import APIRouter

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str

items_db_v1 = []
items_db_v2 = [{"id": 1, "name": "Item 1", "description": "Description v2"}]

router_v1 = APIRouter(prefix="/v1")
router_v2 = APIRouter(prefix="/v2")

@router_v1.get("/items")
async def list_items_v1():
    return {"items": items_db_v1, "version": "v1"}

@router_v2.get("/items")
async def list_items_v2():
    return {"items": items_db_v2, "version": "v2"}

app.include_router(router_v1)
app.include_router(router_v2)
```

## 15.8 API 版本控制

管理 API 的不同版本。

[程式檔案：15-8-versioning.py](../_code/15/15-8-versioning.py)

```python
from fastapi import FastAPI, Header
from typing import Optional

app = FastAPI()

API_VERSIONS = ["v1", "v2"]

@app.get("/api/v1/items")
async def list_items_v1():
    return {"version": "v1", "items": []}

@app.get("/api/v2/items")
async def list_items_v2():
    return {"version": "v2", "items": []}

@app.get("/items")
async def list_items(
    x_api_version: str = Header("v1", regex="^(v1|v2)$")
):
    return {
        "items": [],
        "version": x_api_version,
        "deprecated": x_api_version == "v1"
    }
```

## 15.9 速率限制

防止 API 被濫用。

[程式檔案：15-9-rate-limiting.py](../_code/15/15-9-rate-limiting.py)

```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from collections import defaultdict

app = FastAPI()

rate_limit_store = defaultdict(list)

def rate_limit(limit: int = 10, window: int = 60):
    def decorator(func):
        async def wrapper(request: Request, *args, **kwargs):
            client_ip = request.client.host
            now = datetime.now()
            
            rate_limit_store[client_ip] = [
                t for t in rate_limit_store[client_ip]
                if now - t < timedelta(seconds=window)
            ]
            
            if len(rate_limit_store[client_ip]) >= limit:
                raise HTTPException(
                    status_code=429,
                    detail="Too many requests"
                )
            
            rate_limit_store[client_ip].append(now)
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator

@app.get("/items")
@rate_limit(limit=10, window=60)
async def list_items(request: Request):
    return {"items": [], "client": request.client.host}
```

## 15.10 快取機制

減少重複的資料庫查詢。

[程式檔案：15-10-caching.py](../_code/15/15-10-caching.py)

```python
from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
from functools import lru_cache

app = FastAPI()

cache = {}
CACHE_TTL = timedelta(minutes=5)

def get_cache(key: str):
    if key in cache:
        data, timestamp = cache[key]
        if datetime.now() - timestamp < CACHE_TTL:
            return data
        del cache[key]
    return None

def set_cache(key: str, value):
    cache[key] = (value, datetime.now())

@lru_cache(maxsize=100)
def expensive_computation(n: int):
    return n ** 2

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    cache_key = f"item_{item_id}"
    cached = get_cache(cache_key)
    
    if cached:
        return {"item": cached, "cached": True}
    
    item = {"id": item_id, "name": f"Item {item_id}"}
    set_cache(cache_key, item)
    
    return {"item": item, "cached": False}

@app.on_event("startup")
async def clear_cache():
    cache.clear()
```

## 重點回顧

| 概念 | 說明 |
|------|------|
| REST | API 設計架構 |
| CRUD | Create, Read, Update, Delete |
| 分頁 | Offset 和 Cursor 分頁 |
| 篩選 | 多條件過濾 |
| 排序 | 多欄位排序 |
| 版本控制 | API 版本管理 |
| 速率限制 | 防止濫用 |
| 快取 | 減少查詢 |

## 練習題

1. 實作一個電子商城的商品 API
2. 建立評論系統的 API
3. 實作 JWT 認證的 API
4. 建立一個檔案上傳 API
