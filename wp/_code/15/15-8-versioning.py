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

@app.get("/items")
async def list_items_query(version: str = "v1"):
    return {"items": [], "version": version}
