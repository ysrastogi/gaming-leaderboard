from datetime import datetime
from enum import Enum
from functools import lru_cache
from typing import List

from app.core.database import get_db
from app.models import GameSession, Leaderboard, User
from app.schemas import (
    ErrorResponse,
    LeaderboardEntry,
    PlayerRank,
    ScoreResponse,
    ScoreSubmission,
)
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import Redis
from sqlalchemy import desc, func, text
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/leaderboard", tags=["leaderboard"])

class GameMode(Enum):
    SOLO = "SOLO"
    TEAM = "TEAM"


@router.post("/submit", response_model=ScoreResponse)
async def submit_score(
    submission: ScoreSubmission,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    try:
        user_and_leaderboard = (
            db.query(User, Leaderboard)
            .outerjoin(Leaderboard, User.id == Leaderboard.user_id)
            .filter(User.id == submission.user_id)
            .first()
        )

        if not user_and_leaderboard or not user_and_leaderboard[0]:
            raise HTTPException(
                status_code=404, detail=f"User with ID {submission.user_id} not found"
            )

        with db.begin_nested():

            game_mode_str = "SOLO" if submission.game_mode.lower() == "solo" else "TEAM"
            db.execute(
                text(
                    """
                    INSERT INTO game_sessions (user_id, score, game_mode, timestamp)
                    VALUES (:user_id, :score, :game_mode, :timestamp)
                    """
                ),
                {
                    "user_id": submission.user_id,
                    "score": submission.score,
                    "game_mode": game_mode_str,
                    "timestamp": datetime.utcnow(),
                },
            )

            # Calculate stats
            stats = db.execute(
                text(
                    """
            SELECT COUNT(*) as total_sessions, AVG(score) as avg_score
            FROM game_sessions
            WHERE user_id = :user_id
            """
                ),
                {"user_id": submission.user_id},
            ).first()
            total_sessions = stats[0]
            avg_score = stats[1]

            db.execute(
                text(
                    """
            INSERT INTO leaderboard (user_id, total_score)
            VALUES (:user_id, :avg_score)
            ON CONFLICT(user_id) DO UPDATE SET total_score = :avg_score
            """
                ),
                {"user_id": submission.user_id, "avg_score": avg_score},
            )

            db.execute(
                text(
                    """
                UPDATE leaderboard
                SET rank = (
                    SELECT COUNT(*) + 1
                    FROM leaderboard AS l2
                    WHERE l2.total_score > leaderboard.total_score
                )
                WHERE user_id = :user_id
                """
                ),
                {"user_id": submission.user_id},
            )

        db.commit()

        background_tasks.add_task(_update_single_player_rank, db, submission.user_id)

        return ScoreResponse(
            message="Score submitted successfully",
            user_id=submission.user_id,
            score=submission.score,
            total_sessions=total_sessions,
        )

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to submit score: {str(e)}")


@router.get("/top", response_model=List[LeaderboardEntry])
@cache(expire=60)
async def get_top_leaderboard(limit: int = 10, db: Session = Depends(get_db)):
    """
    Get the top players from the leaderboard.
    Returns players sorted by total_score in descending order.
    """
    try:
        top_players = (
            db.query(
                Leaderboard.user_id,
                User.username,
                Leaderboard.total_score,
                Leaderboard.rank,
            )
            .join(User, Leaderboard.user_id == User.id)
            .order_by(desc(Leaderboard.total_score))
            .limit(limit)
            .all()
        )

        if not top_players:
            return []

        return [
            LeaderboardEntry(
                user_id=player.user_id,
                username=player.username,
                total_score=player.total_score,
                rank=player.rank or 0,
            )
            for player in top_players
        ]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch leaderboard: {str(e)}",
        )


@router.get("/rank/{user_id}", response_model=PlayerRank)
async def get_player_rank(user_id: int, db: Session = Depends(get_db)):
    """
    Get a specific player's rank and stats.
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found",
            )

        player_entry = (
            db.query(
                Leaderboard.user_id,
                User.username,
                Leaderboard.total_score,
                Leaderboard.rank,
            )
            .join(User, Leaderboard.user_id == User.id)
            .filter(Leaderboard.user_id == user_id)
            .first()
        )

        if not player_entry:
            return PlayerRank(
                user_id=user_id,
                username=user.username,
                rank=0,
                total_score=0.0,
                total_sessions=0,
            )

        total_sessions = (
            db.query(func.count(GameSession.id))
            .filter(GameSession.user_id == user_id)
            .scalar()
        )

        return PlayerRank(
            user_id=player_entry.user_id,
            username=player_entry.username,
            rank=player_entry.rank or 0,
            total_score=player_entry.total_score,
            total_sessions=total_sessions,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch player rank: {str(e)}",
        )

@router.post("/create/", response_model=List[int])
def create_test_users(count: int = 1000000, db: Session = Depends(get_db)):
    try:
        current_time = datetime.now()
        new_user_ids = []

        # Find the last created player index (so we don’t overwrite usernames)
        last_user = db.query(User).order_by(User.id.desc()).first()
        start_index = last_user.id + 1 if last_user else 1

        for i in range(start_index, start_index + count):
            username = f"player_{i}"
            
            user = User(
                username=username,
                join_date=current_time
            )
            db.add(user)
            db.flush()  # get user.id before commit
            new_user_ids.append(user.id)

            # Commit every 100 users to avoid large transactions
            if i % 10000 == 0:
                db.commit()
                print(f"Created {i} users")
        
        db.commit()

        print(f"Successfully created {len(new_user_ids)} new users.")
        return new_user_ids
    
    except Exception as e:
        db.rollback()
        print(f"Error creating users: {str(e)}")
        return []


async def _update_leaderboard_ranks(db: Session):
    """
    Helper function to update ranks for all players in the leaderboard.
    """
    try:
        if "sqlite" in str(db.bind.url):
            db.execute(
                text(
                    """
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
            """
                )
            )
        else:
            db.execute(
                text(
                    """
                UPDATE leaderboard 
                SET rank = ranked_players.new_rank
                FROM (
                    SELECT 
                        user_id,
                        RANK() OVER (ORDER BY total_score DESC) as new_rank
                    FROM leaderboard
                ) ranked_players
                WHERE leaderboard.user_id = ranked_players.user_id
            """
                )
            )

        db.commit()

    except Exception as e:
        db.rollback()
        raise e


def _update_single_player_rank(db: Session, user_id: int):
    """
    Update rank for a single player without recalculating all ranks.
    Much more efficient than updating all ranks.
    """
    try:

        player_score = (
            db.query(Leaderboard.total_score)
            .filter(Leaderboard.user_id == user_id)
            .scalar()
        )

        if player_score is None:
            return

        higher_scores = (
            db.query(func.count())
            .filter(Leaderboard.total_score > player_score)
            .scalar()
        )

        db.query(Leaderboard).filter(Leaderboard.user_id == user_id).update(
            {"rank": higher_scores + 1}
        )

        db.commit()

    except Exception as e:
        db.rollback()
        raise e
    

