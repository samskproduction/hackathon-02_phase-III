from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    FRONTEND_URL: Optional[str] = "http://localhost:3000"
    BACKEND_URL: Optional[str] = "http://localhost:8000"
    BETTER_AUTH_SECRET: str
    NEON_DB_URL: str
    COHERE_API_KEY: str
    DEBUG: Optional[bool] = True
    USE_SQLITE_FOR_LOCAL_DEV: Optional[str] = ""

    model_config = {"env_file": ".env"}

settings = Settings()
