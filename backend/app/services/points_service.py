from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BusinessConflictError, NotFoundError
from app.models.entries_points import EntriesPoints
from app.repositories.entries_points_repo import EntriesPointsRepository
from app.repositories.event_result_repo import EventResultRepository
from app.repositories.points_rule_repo import PointsRuleRepository
from app.repositories.tournament_repo import TournamentRepository


class PointsService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.tournament_repo = TournamentRepository(db)
        self.event_result_repo = EventResultRepository(db)
        self.points_rule_repo = PointsRuleRepository(db)
        self.entries_repo = EntriesPointsRepository(db)

    async def generate_points(self, tournament_id: int):
        tournament = await self.tournament_repo.get_by_id(tournament_id)
        if not tournament:
            raise NotFoundError(detail="赛事不存在", code="TOURNAMENT_NOT_FOUND")
        if tournament.status not in ("completed", "published"):
            raise BusinessConflictError(
                detail="请先完成赛事结果导入", code="POINTS_TOURNAMENT_NOT_COMPLETED"
            )

        # Delete existing points for re-generation
        already_exists = await self.entries_repo.exists_for_tournament(tournament_id)
        if already_exists:
            from app.repositories.ranking_repo import RankingRepository
            ranking_repo = RankingRepository(self.db)
            await ranking_repo.delete_by_tournament(tournament_id)

        from app.processors.points_generator import PointsGenerator

        generator = PointsGenerator(self.db)
        await generator.generate(tournament)

        tournament.status = "published"
        await self.db.commit()

        return {"tournament_id": tournament_id, "message": "积分生成完成"}
