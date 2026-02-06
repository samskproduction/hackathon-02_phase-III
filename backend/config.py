from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # JWT Configuration
    better_auth_secret: str
    better_auth_url: str = "http://localhost:3000"

    # Database Configuration
    neon_db_url: str

    # API Configuration
    api_prefix: str = "/api"
    debug: bool = False

    class Config:
        env_file = ".env"


settings = Settings()