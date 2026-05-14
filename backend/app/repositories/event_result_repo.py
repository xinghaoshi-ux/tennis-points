from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entries_points import EntriesPoints
from app.models.event_result import EventResult
from app.models.event_result_player import EventResultPlayer


class EventResultRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_tournament(self, tournament_id: int) -> list[EventResult]:
        result = await self.db.execute(
            select(EventResult).where(EventResult.tournament_id == tournament_id)
        )
        return list(result.scalars().all())

    async def create(self, **kwargs) -> EventResult:
        event_result = EventResult(**kwargs)
        self.db.add(event_result)
        await self.db.flush()
        return event_result

    async def create_player_link(self, event_result_id: int, player_id: int) -> None:
        link = EventResultPlayer(event_result_id=event_result_id, player_id=player_id)
        self.db.add(link)
        await self.db.flush()

    async def get_players_for_result(self, event_result_id: int) -> list[int]:
        result = await self.db.execute(
            select(EventResultPlayer.player_id).where(
                EventResultPlayer.event_result_id == event_result_id
            )
        )
        return [row[0] for row in result.all()]

    async def delete_by_tournament(self, tournament_id: int) -> None:
        results = await self.get_by_tournament(tournament_id)
        result_ids = [r.id for r in results]
        if result_ids:
            await self.db.execute(
                delete(EventResultPlayer).where(
                    EventResultPlayer.event_result_id.in_(result_ids)
                )
            )
        await self.db.execute(
            delete(EventResult).where(EventResult.tournament_id == tournament_id)
        )
        await self.db.flush()
