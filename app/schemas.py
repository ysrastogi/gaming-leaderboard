from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ScoreSubmission(BaseModel):
    user_id: int
    score: int
    game_mode: Optional[str] = "solo"

class ScoreResponse(BaseModel):
    message: str
    user_id: int
    score: int
    total_sessions: int

class LeaderboardEntry(BaseModel):
    user_id: int
    username: str
    total_score: float
    rank: int
    
class PlayerRank(BaseModel):
    user_id: int
    username: str
    rank: int
    total_score: float
    total_sessions: int

class ErrorResponse(BaseModel):
    error: str
    message: str