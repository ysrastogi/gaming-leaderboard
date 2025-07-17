from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import Redis

from app.routers import leaderboard
from app.core.database import engine
from app.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Gaming Leaderboard API",
    description="A high-performance gaming leaderboard API",
    version="1.0.0"
)

@app.on_event("startup")
async def startup():
    redis = Redis(host="localhost", port=6379)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache:")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(leaderboard.router)

@app.get("/")
async def root():
    return {"message": "Gaming Leaderboard API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}