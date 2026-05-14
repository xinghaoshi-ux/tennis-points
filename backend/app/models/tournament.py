from datetime import date, datetime
from typing import Optional

from sqlalchemy import ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Tournament(TimestampMixin, Base):
    __tablename__ = "tournaments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    season_id: Mapped[int] = mapped_column(ForeignKey("seasons.id"))
    name: Mapped[str] = mapped_column(String(200))
    event_category: Mapped[str] = mapped_column(String(50))
    level: Mapped[str] = mapped_column(String(20))
    group_name: Mapped[Optional[str]] = mapped_column(String(50), default=None)
    start_date: Mapped[Optional[date]] = mapped_column(default=None)
    end_date: Mapped[Optional[date]] = mapped_column(default=None)
    location: Mapped[Optional[str]] = mapped_column(String(200), default=None)
    alumni_player_count: Mapped[Optional[int]] = mapped_column(Integer, default=None)
    status: Mapped[str] = mapped_column(String(20), default="draft")

    __table_args__ = (
        Index("ix_tournaments_season_status", "season_id", "status"),
    )
