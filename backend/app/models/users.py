from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from . import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    join_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    game_sessions = relationship("GameSession", back_populates="user")
    leaderboard_entry = relationship("Leaderboard", back_populates="user", uselist=False)