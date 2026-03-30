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
