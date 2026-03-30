from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    from 16-2-jwt-token import decode_token
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )
    token_data = decode_token(token)
    if token_data is None or token_data.username is None:
        raise credentials_exception
    return {"username": token_data.username}

@app.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {
        "message": "You have access!",
        "user": current_user["username"]
    }

@app.get("/public")
async def public_route():
    return {"message": "This is public"}

@app.get("/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return {"username": current_user["username"]}
