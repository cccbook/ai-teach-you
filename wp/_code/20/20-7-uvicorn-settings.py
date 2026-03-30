from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "MyApp"
    debug: bool = False
    database_url: str = "sqlite:///./app.db"
    secret_key: str = "change-me-in-production"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()

# Uvicorn settings
UVICORN_CONFIG = {
    "app": "main:app",
    "host": "0.0.0.0",
    "port": 8000,
    "reload": settings.debug,
    "workers": 4,
    "log_level": "info",
    "access_log": True,
}
