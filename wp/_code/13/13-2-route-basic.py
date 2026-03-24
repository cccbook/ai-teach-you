from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Home page"}

@app.get("/about")
async def about():
    return {"message": "About page"}

@app.get("/contact")
async def contact():
    return {"message": "Contact page"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
