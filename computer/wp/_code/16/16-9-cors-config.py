from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://myfrontend.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

@app.get("/")
async def root():
    return {"message": "CORS enabled"}

@app.get("/api/data")
async def get_data():
    return {"data": "Protected data"}

@app.post("/api/submit")
async def submit_data(data: dict):
    return {"received": data}
