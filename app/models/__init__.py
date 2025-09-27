from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import all models to ensure they're registered with the Base
from .users import User
from .leaderboard import GameSession, Leaderboard

__all__ = ["Base", "User", "GameSession", "Leaderboard"]