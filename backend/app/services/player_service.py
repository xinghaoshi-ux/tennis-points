from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.entries_points import EntriesPoints
from app.models.event_result_player import EventResultPlayer
from app.repositories.player_repo import PlayerRepository
from app.schemas.player import PlayerCreate, PlayerUpdate


class PlayerService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = PlayerRepository(db)

    async def list_players(
        self, page: int = 1, page_size: int = 20,
        search: str | None = None, department: str | None = None,
    ):
        return await self.repo.list(page, page_size, search, department)

    async def create_player(self, data: PlayerCreate):
        player = await self.repo.create(**data.model_dump())
        await self.db.commit()
        return player

    async def get_player(self, player_id: int):
        player = await self.repo.get_by_id(player_id)
        if not player:
            raise NotFoundError(detail="选手不存在", code="PLAYER_NOT_FOUND")
        return player

    async def update_player(self, player_id: int, data: PlayerUpdate):
        player = await self.repo.get_by_id(player_id)
        if not player:
            raise NotFoundError(detail="选手不存在", code="PLAYER_NOT_FOUND")

        update_data = data.model_dump(exclude_unset=True)
        player = await self.repo.update(player, **update_data)
        await self.db.commit()
        return player

    async def delete_player(self, player_id: int):
        player = await self.repo.get_by_id(player_id)
        if not player:
            raise NotFoundError(detail="选手不存在", code="PLAYER_NOT_FOUND")

        await self.db.execute(
            delete(EntriesPoints).where(EntriesPoints.player_id == player_id)
        )
        await self.db.execute(
            delete(EventResultPlayer).where(EventResultPlayer.player_id == player_id)
        )
        await self.repo.delete(player)
        await self.db.commit()
