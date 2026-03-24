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
