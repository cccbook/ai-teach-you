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
