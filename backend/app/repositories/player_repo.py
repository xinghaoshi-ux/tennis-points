from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.player import Player


class PlayerRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(
        self,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
        department: str | None = None,
    ) -> tuple[list[Player], int]:
        query = select(Player)
        count_query = select(func.count(Player.id))

        if search:
            query = query.where(Player.full_name.ilike(f"%{search}%"))
            count_query = count_query.where(Player.full_name.ilike(f"%{search}%"))
        if department:
            query = query.where(Player.department == department)
            count_query = count_query.where(Player.department == department)

        total = (await self.db.execute(count_query)).scalar_one()
        result = await self.db.execute(
            query.order_by(Player.id.desc()).offset((page - 1) * page_size).limit(page_size)
        )
        return list(result.scalars().all()), total

    async def get_by_id(self, player_id: int) -> Player | None:
        result = await self.db.execute(select(Player).where(Player.id == player_id))
        return result.scalar_one_or_none()

    async def get_by_name(self, full_name: str) -> Player | None:
        result = await self.db.execute(select(Player).where(Player.full_name == full_name))
        return result.scalar_one_or_none()

    async def get_departments(self) -> list[str]:
        result = await self.db.execute(
            select(Player.department)
            .where(Player.department.isnot(None))
            .distinct()
            .order_by(Player.department)
        )
        return [row[0] for row in result.all()]

    async def create(self, **kwargs) -> Player:
        player = Player(**kwargs)
        self.db.add(player)
        await self.db.flush()
        return player

    async def update(self, player: Player, **kwargs) -> Player:
        for key, value in kwargs.items():
            if value is not None:
                setattr(player, key, value)
        await self.db.flush()
        return player

    async def delete(self, player: Player) -> None:
        await self.db.delete(player)
        await self.db.flush()
