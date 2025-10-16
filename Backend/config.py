import os
from fastapi import FastAPI
from backend.lifespan import lifespan
from typing import Any

app = FastAPI(lifespan=lifespan)

DATABASE_URL: str = "postgres://postgres:postgres@localhost:5432/mydb"
REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
SESSION_COOKIE: str = "sid"
SESSION_TTL_SECONDS: int = 60*60*24*7
CORS_ORIGINS: list[AnyHttpUrl] = ["http://localhost:3000"]
SECRET_KEY: str = "dev-secret"  # use env var in prod