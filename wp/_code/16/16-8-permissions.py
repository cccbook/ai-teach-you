from enum import Enum
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class User(BaseModel):
    username: str
    role: Role

users_db = {
    "admin": {"username": "admin", "role": Role.ADMIN},
    "user1": {"username": "user1", "role": Role.USER},
    "guest1": {"username": "guest1", "role": Role.GUEST}
}

def get_current_user(token: str = Depends(oauth2_scheme)):
    from 16-2-jwt-token import decode_token
    token_data = decode_token(token)
    if not token_data or not token_data.username:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return users_db.get(token_data.username)

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

@app.get("/admin")
async def admin_only(user: User = Depends(require_admin)):
    return {"message": "Welcome, admin!", "user": user.username}

@app.get("/user")
async def user_route(user: User = Depends(get_current_user)):
    return {"message": "Welcome!", "user": user.username}
