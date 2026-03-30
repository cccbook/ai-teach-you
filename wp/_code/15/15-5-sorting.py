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
