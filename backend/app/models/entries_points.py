from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class EntriesPoints(Base):
    __tablename__ = "entries_points"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    tournament_id: Mapped[int] = mapped_column(ForeignKey("tournaments.id"))
    season_id: Mapped[int] = mapped_column(ForeignKey("seasons.id"))
    source_type: Mapped[str] = mapped_column(String(30))
    points_earned: Mapped[int] = mapped_column(Integer)
    result_type: Mapped[Optional[str]] = mapped_column(String(30), default=None)
    description: Mapped[Optional[str]] = mapped_column(String(500), default=None)
    team_id: Mapped[Optional[int]] = mapped_column(ForeignKey("teams.id"), default=None)
    team_total_points: Mapped[Optional[int]] = mapped_column(Integer, default=None)
    team_member_count: Mapped[Optional[int]] = mapped_column(Integer, default=None)
    event_result_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("event_results.id"), default=None
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    __table_args__ = (
        Index("ix_entries_points_season_player", "season_id", "player_id"),
        Index("ix_entries_points_tournament", "tournament_id"),
        Index("ix_entries_points_player_season", "player_id", "season_id"),
    )
