from fastapi import FastAPI
from app.routers import tasks
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from redis import Redis
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache import FastAPICache

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = Redis(host="localhost", port=6379, decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    redis.close()

app = FastAPI(lifespan=lifespan)

app.include_router(tasks.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)
