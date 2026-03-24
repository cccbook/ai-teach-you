from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from collections import defaultdict

app = FastAPI()

rate_limit_store = defaultdict(list)

def rate_limit(limit: int = 10, window: int = 60):
    def decorator(func):
        async def wrapper(request: Request, *args, **kwargs):
            client_ip = request.client.host
            now = datetime.now()
            
            rate_limit_store[client_ip] = [
                t for t in rate_limit_store[client_ip]
                if now - t < timedelta(seconds=window)
            ]
            
            if len(rate_limit_store[client_ip]) >= limit:
                raise HTTPException(
                    status_code=429,
                    detail="Too many requests"
                )
            
            rate_limit_store[client_ip].append(now)
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator

@app.get("/items")
@rate_limit(limit=10, window=60)
async def list_items(request: Request):
    return {"items": [], "client": request.client.host}
