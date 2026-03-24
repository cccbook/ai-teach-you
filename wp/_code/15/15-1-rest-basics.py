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
