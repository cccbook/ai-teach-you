from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/hello")
async def hello():
    return {"message": "Hello from FastAPI"}

@app.get("/api/data")
async def get_data():
    return {"items": [{"id": 1, "name": "Item 1"}]}

@app.post("/api/data")
async def create_data(data: dict):
    return {"created": data, "status": "success"}
