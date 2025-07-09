# backend/app/config.py
from pydantic_settings import BaseSettings

from pydantic import AnyUrl

class Settings(BaseSettings):
    DATABASE_URL: AnyUrl
    JWT_SECRET: str
    FAAS_GATEWAY: AnyUrl
    FAAS_USER: str
    FAAS_PASS: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
