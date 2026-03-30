from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from pydantic import BaseModel, SecurityRequirement

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    scopes: list[str] = []

def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    
    from 16-2-jwt-token import decode_token
    token_data = decode_token(token)
    
    if token_data is None or token_data.username is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {"username": token_data.username, "scopes": []}

@app.get("/items/")
async def read_items(current_user: User = Depends(get_current_user)):
    return [{"item": "Item 1"}, {"item": "Item 2"}]

@app.get("/users/me")
async def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user
