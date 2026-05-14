from datetime import date

from sqlalchemy import delete, func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entries_points import EntriesPoints
from app.models.player import Player
from app.models.tournament import Tournament


class RankingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_rankings(
        self,
        season_id: int,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
        department: str | None = None,
    ) -> tuple[list[dict], int]:
        base_filter = EntriesPoints.season_id == season_id
        player_join = Player.id == EntriesPoints.player_id

        count_query = (
            select(func.count(func.distinct(EntriesPoints.player_id)))
            .join(Player, player_join)
            .where(base_filter)
        )
        if search:
            count_query = count_query.where(Player.full_name.ilike(f"%{search}%"))
        if department:
            count_query = count_query.where(Player.department == department)

        total = (await self.db.execute(count_query)).scalar_one()

        subq = (
            select(
                EntriesPoints.player_id,
                func.sum(EntriesPoints.points_earned).label("total_points"),
                func.count(func.distinct(EntriesPoints.tournament_id)).label("tournament_count"),
            )
            .where(base_filter)
            .group_by(EntriesPoints.player_id)
            .subquery()
        )

        query = (
            select(
                subq.c.player_id,
                Player.full_name,
                Player.department,
                Player.birth_date,
                subq.c.total_points,
                subq.c.tournament_count,
                func.rank().over(order_by=subq.c.total_points.desc()).label("ranking"),
            )
            .join(Player, Player.id == subq.c.player_id)
        )

        if search:
            query = query.where(Player.full_name.ilike(f"%{search}%"))
        if department:
            query = query.where(Player.department == department)

        query = query.order_by(text("ranking")).offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        rows = result.all()

        today = date.today()
        items = []
        for row in rows:
            age = None
            if row.birth_date:
                age = today.year - row.birth_date.year
                if (today.month, today.day) < (row.birth_date.month, row.birth_date.day):
                    age -= 1
            items.append({
                "ranking": row.ranking,
                "player_id": row.player_id,
                "full_name": row.full_name,
                "department": row.department,
                "age": age,
                "total_points": row.total_points,
                "tournament_count": row.tournament_count,
            })

        return items, total

    async def get_player_points(self, player_id: int, season_id: int) -> list[dict]:
        result = await self.db.execute(
            select(
                EntriesPoints,
                Tournament.name.label("tournament_name"),
                Tournament.start_date.label("tournament_date"),
            )
            .join(Tournament, Tournament.id == EntriesPoints.tournament_id)
            .where(
                EntriesPoints.player_id == player_id,
                EntriesPoints.season_id == season_id,
            )
            .order_by(EntriesPoints.created_at.desc())
        )
        rows = result.all()
        items = []
        for row in rows:
            ep = row[0]
            items.append({
                "id": ep.id,
                "tournament_name": row.tournament_name,
                "source_type": ep.source_type,
                "result_type": ep.result_type,
                "points_earned": ep.points_earned,
                "description": ep.description,
                "tournament_date": str(row.tournament_date) if row.tournament_date else None,
                "team_name": None,
                "team_total_points": ep.team_total_points,
                "team_member_count": ep.team_member_count,
            })
        return items

    async def delete_by_tournament(self, tournament_id: int) -> None:
        await self.db.execute(
            delete(EntriesPoints).where(EntriesPoints.tournament_id == tournament_id)
        )
        await self.db.flush()
