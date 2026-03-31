from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

users_db = {
    "user1": {"username": "user1", "password": "password123"},
    "user2": {"username": "user2", "password": "password456"}
}

def authenticate_user(username: str, password: str):
    user = users_db.get(username)
    if not user or user["password"] != password:
        return None
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    from 16-2-jwt-token import decode_token
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    token_data = decode_token(token)
    if token_data is None or token_data.username is None:
        raise credentials_exception
    return token_data

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    from 16-2-jwt-token import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}
