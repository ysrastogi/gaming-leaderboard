from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import leaderboard
from app.core.database import engine
from app.models import Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Gaming Leaderboard API",
    description="A high-performance gaming leaderboard API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
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