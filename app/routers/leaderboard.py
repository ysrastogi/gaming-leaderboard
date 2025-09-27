from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text, func, desc
from typing import List
from datetime import datetime
from enum import Enum

from app.core.database import get_db
from app.models import User, GameSession, Leaderboard
from app.schemas import ScoreSubmission, ScoreResponse, LeaderboardEntry, PlayerRank, ErrorResponse

router = APIRouter(prefix="/api/leaderboard", tags=["leaderboard"])

class GameMode(Enum):
    SOLO = "SOLO"
    TEAM = "TEAM"

@router.post("/submit", response_model=ScoreResponse)
async def submit_score(
    submission: ScoreSubmission,
    db: Session = Depends(get_db)
):
    """
    Submit a new game score for a user.
    Updates the game_sessions table and refreshes leaderboard data.
    """
    try:
        # Verify user exists
        user = db.query(User).filter(User.id == submission.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {submission.user_id} not found"
            )
        
        # Convert game_mode string to enum value and pass as string
        game_mode_enum = GameMode.SOLO.value if submission.game_mode.lower() == "solo" else GameMode.TEAM.value
        
        # Create new game session
        new_session = GameSession(
            user_id=submission.user_id,
            score=submission.score,
            game_mode=game_mode_enum,  # Pass as string
            timestamp=datetime.utcnow()
        )
        
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        
        # Update or create leaderboard entry
        leaderboard_entry = db.query(Leaderboard).filter(
            Leaderboard.user_id == submission.user_id
        ).first()
        
        # Calculate new total score (average of all scores)
        total_sessions = db.query(func.count(GameSession.id)).filter(
            GameSession.user_id == submission.user_id
        ).scalar()
        
        avg_score = db.query(func.avg(GameSession.score)).filter(
            GameSession.user_id == submission.user_id
        ).scalar()
        
        if leaderboard_entry:
            leaderboard_entry.total_score = float(avg_score)
        else:
            leaderboard_entry = Leaderboard(
                user_id=submission.user_id,
                total_score=float(avg_score)
            )
            db.add(leaderboard_entry)
        
        db.commit()
        
        # Update ranks for all users
        await _update_leaderboard_ranks(db)
        
        return ScoreResponse(
            message="Score submitted successfully",
            user_id=submission.user_id,
            score=submission.score,
            total_sessions=total_sessions
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit score: {str(e)}"
        )

@router.get("/top", response_model=List[LeaderboardEntry])
async def get_top_leaderboard(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get the top players from the leaderboard.
    Returns players sorted by total_score in descending order.
    """
    try:
        # Query top players with their usernames
        top_players = db.query(
            Leaderboard.user_id,
            User.username,
            Leaderboard.total_score,
            Leaderboard.rank
        ).join(
            User, Leaderboard.user_id == User.id
        ).order_by(
            desc(Leaderboard.total_score)
        ).limit(limit).all()
        
        if not top_players:
            return []
        
        return [
            LeaderboardEntry(
                user_id=player.user_id,
                username=player.username,
                total_score=player.total_score,
                rank=player.rank or 0
            )
            for player in top_players
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch leaderboard: {str(e)}"
        )

@router.get("/rank/{user_id}", response_model=PlayerRank)
async def get_player_rank(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific player's rank and stats.
    """
    try:
        # Verify user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        
        # Get player's leaderboard entry
        player_entry = db.query(
            Leaderboard.user_id,
            User.username,
            Leaderboard.total_score,
            Leaderboard.rank
        ).join(
            User, Leaderboard.user_id == User.id
        ).filter(
            Leaderboard.user_id == user_id
        ).first()
        
        if not player_entry:
            # User exists but has no game sessions
            return PlayerRank(
                user_id=user_id,
                username=user.username,
                rank=0,
                total_score=0.0,
                total_sessions=0
            )
        
        # Get total sessions count
        total_sessions = db.query(func.count(GameSession.id)).filter(
            GameSession.user_id == user_id
        ).scalar()
        
        return PlayerRank(
            user_id=player_entry.user_id,
            username=player_entry.username,
            rank=player_entry.rank or 0,
            total_score=player_entry.total_score,
            total_sessions=total_sessions
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch player rank: {str(e)}"
        )

async def _update_leaderboard_ranks(db: Session):
    """
    Helper function to update ranks for all players in the leaderboard.
    """
    try:
        # Use window function to calculate ranks
        if 'sqlite' in str(db.bind.url):
            # SQLite version
            db.execute(text("""
                WITH ranked_players AS (
                    SELECT 
                        user_id,
                        total_score,
                        RANK() OVER (ORDER BY total_score DESC) as new_rank
                    FROM leaderboard
                )
                UPDATE leaderboard 
                SET rank = (
                    SELECT new_rank 
                    FROM ranked_players 
                    WHERE ranked_players.user_id = leaderboard.user_id
                )
            """))
        else:
            # PostgreSQL version
            db.execute(text("""
                UPDATE leaderboard 
                SET rank = ranked_players.new_rank
                FROM (
                    SELECT 
                        user_id,
                        RANK() OVER (ORDER BY total_score DESC) as new_rank
                    FROM leaderboard
                ) ranked_players
                WHERE leaderboard.user_id = ranked_players.user_id
            """))
        
        db.commit()
        
    except Exception as e:
        db.rollback()
        raise e