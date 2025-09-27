from sqlalchemy.orm import Session
from app.models.leaderboard import GameSession
from app.schemas.leaderboard import ScoreSubmission, PlayerRank
from typing import List

class LeaderboardService:
    def __init__(self, db: Session):
        self.db = db

    def submit_score(self, score_submission: ScoreSubmission):
        game_session = GameSession(user_id=score_submission.user_id, score=score_submission.score)
        self.db.add(game_session)
        self.db.commit()
        self.db.refresh(game_session)
        return game_session

    def get_top_leaderboard(self, limit: int = 10) -> List[PlayerRank]:
        top_players = (
            self.db.query(GameSession.user_id, func.sum(GameSession.score).label('total_score'))
            .group_by(GameSession.user_id)
            .order_by(desc('total_score'))
            .limit(limit)
            .all()
        )
        return [PlayerRank(user_id=user_id, total_score=total_score) for user_id, total_score in top_players]

    def get_player_rank(self, user_id: str) -> int:
        player_score = (
            self.db.query(func.sum(GameSession.score))
            .filter(GameSession.user_id == user_id)
            .scalar()
        )
        if player_score is None:
            return None

        rank = (
            self.db.query(func.count(GameSession.user_id))
            .filter(func.sum(GameSession.score) > player_score)
            .scalar()
        )
        return rank + 1 if rank is not None else 1