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
