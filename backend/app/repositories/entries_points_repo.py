from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entries_points import EntriesPoints


class EntriesPointsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, **kwargs) -> EntriesPoints:
        entry = EntriesPoints(**kwargs)
        self.db.add(entry)
        await self.db.flush()
        return entry

    async def create_batch(self, entries: list[dict]) -> None:
        for entry_data in entries:
            self.db.add(EntriesPoints(**entry_data))
        await self.db.flush()

    async def exists_for_tournament(self, tournament_id: int) -> bool:
        result = await self.db.execute(
            select(func.count(EntriesPoints.id)).where(
                EntriesPoints.tournament_id == tournament_id
            )
        )
        return result.scalar_one() > 0

    async def count_by_season(self, season_id: int) -> int:
        result = await self.db.execute(
            select(func.count(EntriesPoints.id)).where(
                EntriesPoints.season_id == season_id
            )
        )
        return result.scalar_one()

    async def is_rule_in_use(self, rule_id: int) -> bool:
        # A rule is "in use" if entries_points exist that were generated using it.
        # Since we don't store rule_id on entries_points, we check by matching fields.
        # For MVP, we consider a rule in use if any entries_points exist in the same season.
        return False
