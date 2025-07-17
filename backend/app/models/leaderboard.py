import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Index, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class GameMode(enum.Enum):
    SOLO = "SOLO"
    TEAM = "TEAM"


class GameSession(Base):
    __tablename__ = "game_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    score = Column(Integer, nullable=False, index=True)
    game_mode = Column(
        Enum(GameMode), nullable=False, default=GameMode.SOLO, index=True
    )
    timestamp = Column(
        DateTime, default=datetime.utcnow, nullable=False, index=True
    )

    user = relationship("User", back_populates="game_sessions")

    __table_args__ = (
        Index("idx_user_score", user_id, score.desc()),
        Index(
            "idx_timestamp_score", timestamp.desc(), score.desc()
        ),
    )


class Leaderboard(Base):
    __tablename__ = "leaderboard"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True, index=True)
    total_score = Column(Float, default=0.0, index=True)
    rank = Column(Integer, nullable=True, index=True)

    user = relationship("User", back_populates="leaderboard_entry")

    # Add index for sorting by score (for leaderboard queries)
    __table_args__ = (
        Index("idx_leaderboard_score", total_score.desc()),
    )
