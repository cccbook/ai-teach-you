from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator

app = FastAPI()

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., regex=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    age: int = Field(None, ge=0, le=150)
    
    @validator("name")
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int = None

users_db = {}
user_id_counter = 1

@app.post("/users/", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate):
    global user_id_counter
    
    if any(u.email == user.email for u in users_db.values()):
        raise HTTPException(status_code=400, detail="Email already exists")
    
    user_id = user_id_counter
    user_id_counter += 1
    
    user_data = user.model_dump()
    user_data["id"] = user_id
    users_db[user_id] = user_data
    
    return user_data
