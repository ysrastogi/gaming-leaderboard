from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from . import Base

class GameMode(enum.Enum):
    SOLO = "SOLO"
    TEAM = "TEAM"

class GameSession(Base):
    __tablename__ = 'game_sessions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True, nullable=False)
    score = Column(Integer, nullable=False)
    game_mode = Column(Enum(GameMode), nullable=False, default=GameMode.SOLO)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship to User
    user = relationship("User", back_populates="game_sessions")

class Leaderboard(Base):
    __tablename__ = 'leaderboard'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True, index=True)
    total_score = Column(Float, default=0.0)
    rank = Column(Integer, nullable=True)
    
    # Relationship to User
    user = relationship("User", back_populates="leaderboard_entry")