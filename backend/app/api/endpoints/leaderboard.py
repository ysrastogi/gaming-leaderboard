from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from backend.app.models.leaderboard import Score
from backend.app.services.leaderboard_service import LeaderboardService

router = APIRouter()
leaderboard_service = LeaderboardService()

class SubmitScoreRequest(BaseModel):
    user_id: str
    score: int

class PlayerRankResponse(BaseModel):
    user_id: str
    rank: int

@router.post("/api/leaderboard/submit")
async def submit_score(request: SubmitScoreRequest):
    try:
        await leaderboard_service.submit_score(request.user_id, request.score)
        return {"message": "Score submitted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/api/leaderboard/top", response_model=List[Score])
async def get_leaderboard():
    try:
        top_players = await leaderboard_service.get_top_players()
        return top_players
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/leaderboard/rank/{user_id}", response_model=PlayerRankResponse)
async def get_player_rank(user_id: str):
    try:
        rank = await leaderboard_service.get_player_rank(user_id)
        return PlayerRankResponse(user_id=user_id, rank=rank)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))