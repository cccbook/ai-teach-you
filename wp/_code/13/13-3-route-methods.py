from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def get_data():
    return {"method": "GET"}

@app.post("/")
async def create_data():
    return {"method": "POST"}

@app.put("/")
async def update_data():
    return {"method": "PUT"}

@app.delete("/")
async def delete_data():
    return {"method": "DELETE"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
