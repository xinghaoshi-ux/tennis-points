from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BusinessConflictError, NotFoundError
from app.repositories.event_result_repo import EventResultRepository
from app.repositories.ranking_repo import RankingRepository
from app.repositories.season_repo import SeasonRepository
from app.repositories.tournament_repo import TournamentRepository
from app.schemas.tournament import TournamentCreate, TournamentUpdate


class TournamentService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = TournamentRepository(db)
        self.season_repo = SeasonRepository(db)
        self.ranking_repo = RankingRepository(db)

    async def list_tournaments(
        self, page: int = 1, page_size: int = 20,
        status: str | None = None, season_id: int | None = None,
    ):
        return await self.repo.list(page, page_size, status, season_id)

    async def create_tournament(self, data: TournamentCreate):
        active_season = await self.season_repo.get_active()
        if not active_season:
            raise BusinessConflictError(
                detail="无激活赛季，无法创建赛事", code="TOURNAMENT_NO_ACTIVE_SEASON"
            )

        tournament = await self.repo.create(
            season_id=active_season.id, **data.model_dump()
        )
        await self.db.commit()
        return tournament

    async def get_tournament(self, tournament_id: int):
        tournament = await self.repo.get_by_id(tournament_id)
        if not tournament:
            raise NotFoundError(detail="赛事不存在", code="TOURNAMENT_NOT_FOUND")
        return tournament

    async def update_tournament(self, tournament_id: int, data: TournamentUpdate):
        tournament = await self.repo.get_by_id(tournament_id)
        if not tournament:
            raise NotFoundError(detail="赛事不存在", code="TOURNAMENT_NOT_FOUND")
        if tournament.status != "draft":
            raise BusinessConflictError(
                detail="仅 draft 赛事可编辑", code="TOURNAMENT_STATUS_INVALID"
            )

        update_data = data.model_dump(exclude_unset=True)
        tournament = await self.repo.update(tournament, **update_data)
        await self.db.commit()
        return tournament

    async def revoke_publish(self, tournament_id: int):
        tournament = await self.repo.get_by_id(tournament_id)
        if not tournament:
            raise NotFoundError(detail="赛事不存在", code="TOURNAMENT_NOT_FOUND")
        if tournament.status != "published":
            raise BusinessConflictError(
                detail="仅 published 赛事可撤回", code="TOURNAMENT_STATUS_INVALID"
            )

        await self.ranking_repo.delete_by_tournament(tournament_id)
        tournament.status = "completed"
        await self.db.commit()
        return tournament

    async def delete_tournament(self, tournament_id: int):
        tournament = await self.repo.get_by_id(tournament_id)
        if not tournament:
            raise NotFoundError(detail="赛事不存在", code="TOURNAMENT_NOT_FOUND")

        await self.ranking_repo.delete_by_tournament(tournament_id)
        event_result_repo = EventResultRepository(self.db)
        await event_result_repo.delete_by_tournament(tournament_id)

        from sqlalchemy import delete
        from app.models.upload import Upload
        await self.db.execute(delete(Upload).where(Upload.tournament_id == tournament_id))

        await self.repo.delete(tournament)
        await self.db.commit()
