from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BusinessConflictError, NotFoundError
from app.repositories.season_repo import SeasonRepository
from app.schemas.season import SeasonCreate, SeasonUpdate


class SeasonService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = SeasonRepository(db)

    async def list_seasons(self, page: int = 1, page_size: int = 20):
        return await self.repo.list(page, page_size)

    async def create_season(self, data: SeasonCreate):
        if data.end_date <= data.start_date:
            raise BusinessConflictError(
                detail="结束日期必须晚于开始日期", code="SEASON_DATE_INVALID"
            )
        season = await self.repo.create(
            name=data.name, start_date=data.start_date, end_date=data.end_date
        )
        await self.db.commit()
        return season

    async def update_season(self, season_id: int, data: SeasonUpdate):
        season = await self.repo.get_by_id(season_id)
        if not season:
            raise NotFoundError(detail="赛季不存在", code="SEASON_NOT_FOUND")

        update_data = data.model_dump(exclude_unset=True)
        if "end_date" in update_data or "start_date" in update_data:
            start = update_data.get("start_date", season.start_date)
            end = update_data.get("end_date", season.end_date)
            if end <= start:
                raise BusinessConflictError(
                    detail="结束日期必须晚于开始日期", code="SEASON_DATE_INVALID"
                )

        season = await self.repo.update(season, **update_data)
        await self.db.commit()
        return season

    async def activate_season(self, season_id: int):
        season = await self.repo.get_by_id(season_id)
        if not season:
            raise NotFoundError(detail="赛季不存在", code="SEASON_NOT_FOUND")
        if season.status != "draft":
            raise BusinessConflictError(
                detail="仅 draft 赛季可激活", code="SEASON_STATUS_INVALID"
            )

        current_active = await self.repo.get_active()
        if current_active:
            current_active.status = "closed"

        season.status = "active"
        await self.db.commit()
        return season

    async def close_season(self, season_id: int):
        season = await self.repo.get_by_id(season_id)
        if not season:
            raise NotFoundError(detail="赛季不存在", code="SEASON_NOT_FOUND")
        if season.status != "active":
            raise BusinessConflictError(
                detail="仅 active 赛季可关闭", code="SEASON_STATUS_INVALID"
            )

        season.status = "closed"
        await self.db.commit()
        return season

    async def get_active_season(self):
        return await self.repo.get_active()
