import os
import ssl
from contextlib import asynccontextmanager
#import aioredis
from fastapi import FastAPI
from tortoise import Tortoise
from backend.redis import RedisAdapter

@asynccontextmanager
async def lifespan(app: FastAPI):
    await Tortoise.init(
        db_url=f"postgres://{os.getenv("user")}:{os.getenv("password")}@localhost:5432/keiser",
        modules={"models": ["app.models"]}
    )
    
    await Tortoise.generate_schema()

    redis_conn = RedisAdapter()
    app.state.kv_store = redis_conn #app.state basically allows access on a global concept
    
    #app.state.redis = await aioredis.from_url(
    #    "redis://localhost:6739",
    #    decode_responses=True    
    #)

    yield

    await redis_conn.flush()
    await redis_conn.close()
    await Tortoise.close_connections()
    
