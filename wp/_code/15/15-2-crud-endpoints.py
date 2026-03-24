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
