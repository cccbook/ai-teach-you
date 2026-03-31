from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app_v1 = FastAPI()
app_v2 = FastAPI()

class Item(BaseModel):
    id: int
    name: str

items_db_v1 = []
items_db_v2 = [{"id": 1, "name": "Item 1", "description": "Description v2"}]

@router_v1.get("/v1/items")
async def list_items_v1():
    return {"items": items_db_v1}

@router_v2.get("/v2/items")
async def list_items_v2():
    return {"items": items_db_v2, "version": "v2"}

from fastapi import APIRouter

router_v1 = APIRouter(prefix="/v1")
router_v2 = APIRouter(prefix="/v2")

@router_v1.get("/items")
async def list_items_v1():
    return {"items": items_db_v1, "version": "v1"}

@router_v2.get("/items")
async def list_items_v2():
    return {"items": items_db_v2, "version": "v2"}

app = FastAPI()
app.include_router(router_v1)
app.include_router(router_v2)
