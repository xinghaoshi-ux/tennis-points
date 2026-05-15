from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.season import Season


class SeasonRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(self, page: int = 1, page_size: int = 20) -> tuple[list[Season], int]:
        count_result = await self.db.execute(select(func.count(Season.id)))
        total = count_result.scalar_one()

        result = await self.db.execute(
            select(Season)
            .order_by(Season.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        return list(result.scalars().all()), total

    async def get_by_id(self, season_id: int) -> Season | None:
        result = await self.db.execute(select(Season).where(Season.id == season_id))
        return result.scalar_one_or_none()

    async def get_active(self) -> Season | None:
        result = await self.db.execute(select(Season).where(Season.status == "active"))
        return result.scalar_one_or_none()

    async def create(self, **kwargs) -> Season:
        season = Season(**kwargs)
        self.db.add(season)
        await self.db.flush()
        return season

    async def update(self, season: Season, **kwargs) -> Season:
        for key, value in kwargs.items():
            if value is not None:
                setattr(season, key, value)
        await self.db.flush()
        return season

    async def delete(self, season: Season) -> None:
        await self.db.delete(season)
        await self.db.flush()
