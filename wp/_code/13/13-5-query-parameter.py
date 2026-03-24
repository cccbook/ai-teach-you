from fastapi import FastAPI

app = FastAPI()

@app.get("/search")
async def search(q: str, page: int = 1, limit: int = 10):
    return {
        "query": q,
        "page": page,
        "limit": limit,
        "results": []
    }

@app.get("/items")
async def list_items(category: str = None, sort: str = "asc"):
    return {
        "category": category,
        "sort": sort,
        "items": []
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
