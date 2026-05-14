from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BusinessConflictError
from app.repositories.player_repo import PlayerRepository
from app.repositories.ranking_repo import RankingRepository
from app.repositories.season_repo import SeasonRepository


class RankingService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = RankingRepository(db)
        self.season_repo = SeasonRepository(db)
        self.player_repo = PlayerRepository(db)

    async def get_rankings(
        self, page: int = 1, page_size: int = 20,
        search: str | None = None, department: str | None = None,
    ):
        active = await self.season_repo.get_active()
        if not active:
            return [], 0
        return await self.repo.get_rankings(active.id, page, page_size, search, department)

    async def get_player_points(self, player_id: int):
        from datetime import date

        active = await self.season_repo.get_active()
        if not active:
            raise BusinessConflictError(detail="当前无激活赛季", code="RANKING_NO_ACTIVE_SEASON")

        player = await self.player_repo.get_by_id(player_id)
        if not player:
            from app.core.exceptions import NotFoundError
            raise NotFoundError(detail="选手不存在", code="PLAYER_NOT_FOUND")

        details = await self.repo.get_player_points(player_id, active.id)

        # Calculate summary
        summary = {
            "individual_event": 0,
            "team_share": 0,
            "travel_bonus": 0,
            "representative_team": 0,
            "organizer_bonus": 0,
            "donation_bonus": 0,
        }
        for d in details:
            st = d["source_type"]
            if st in summary:
                summary[st] += d["points_earned"]

        total_points = sum(summary.values())
        tournament_count = len(set(d.get("tournament_name") for d in details))

        age = None
        if player.birth_date:
            today = date.today()
            age = today.year - player.birth_date.year
            if (today.month, today.day) < (player.birth_date.month, player.birth_date.day):
                age -= 1

        # Get ranking
        rankings, _ = await self.repo.get_rankings(active.id, page=1, page_size=1000)
        ranking = 0
        for r in rankings:
            if r["player_id"] == player_id:
                ranking = r["ranking"]
                break

        player_info = {
            "ranking": ranking,
            "player_id": player.id,
            "full_name": player.full_name,
            "department": player.department,
            "age": age,
            "total_points": total_points,
            "tournament_count": tournament_count,
        }

        return {
            "player": player_info,
            "summary": summary,
            "details": details,
        }

    async def refresh(self):
        # MVP: rankings are computed dynamically, refresh is a no-op
        return {"message": "排行榜刷新任务已提交"}
