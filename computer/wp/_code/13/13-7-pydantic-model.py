from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()

class User(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(None, ge=0, le=150)
    is_active: bool = True

@app.post("/users/")
async def create_user(user: User):
    return {"user": user}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
