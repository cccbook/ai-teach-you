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
