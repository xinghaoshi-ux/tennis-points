from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class EventResult(Base):
    __tablename__ = "event_results"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tournament_id: Mapped[int] = mapped_column(ForeignKey("tournaments.id"))
    result_type: Mapped[str] = mapped_column(String(30))
    team_id: Mapped[Optional[int]] = mapped_column(ForeignKey("teams.id"), default=None)
    team_total_points: Mapped[Optional[int]] = mapped_column(Integer, default=None)
    team_member_count: Mapped[Optional[int]] = mapped_column(Integer, default=None)
    is_cross_province: Mapped[bool] = mapped_column(Boolean, default=False)
    is_cross_border: Mapped[bool] = mapped_column(Boolean, default=False)
    upload_id: Mapped[Optional[int]] = mapped_column(ForeignKey("uploads.id"), default=None)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    __table_args__ = (
        Index("ix_event_results_tournament_id", "tournament_id"),
    )
