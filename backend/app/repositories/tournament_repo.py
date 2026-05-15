from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tournament import Tournament


class TournamentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(
        self,
        page: int = 1,
        page_size: int = 20,
        status: str | None = None,
        season_id: int | None = None,
    ) -> tuple[list[Tournament], int]:
        query = select(Tournament)
        count_query = select(func.count(Tournament.id))

        if status:
            query = query.where(Tournament.status == status)
            count_query = count_query.where(Tournament.status == status)
        if season_id:
            query = query.where(Tournament.season_id == season_id)
            count_query = count_query.where(Tournament.season_id == season_id)

        total = (await self.db.execute(count_query)).scalar_one()
        result = await self.db.execute(
            query.order_by(Tournament.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        return list(result.scalars().all()), total

    async def get_by_id(self, tournament_id: int) -> Tournament | None:
        result = await self.db.execute(
            select(Tournament).where(Tournament.id == tournament_id)
        )
        return result.scalar_one_or_none()

    async def create(self, **kwargs) -> Tournament:
        tournament = Tournament(**kwargs)
        self.db.add(tournament)
        await self.db.flush()
        return tournament

    async def update(self, tournament: Tournament, **kwargs) -> Tournament:
        for key, value in kwargs.items():
            if value is not None:
                setattr(tournament, key, value)
        await self.db.flush()
        return tournament

    async def delete(self, tournament: Tournament) -> None:
        await self.db.delete(tournament)
        await self.db.flush()
